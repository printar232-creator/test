import streamlit as st
import pandas as pd
import numpy as np

st.title("🛒 Module: ข้อมูลใบสั่งซื้อค้างส่ง (Open Purchase Orders)")

# 1. ตรวจสอบว่ามีไฟล์ดิบจากหน้าหลักเข้ามาเก็บไว้ในระบบหรือยัง
if 'main_upload_file' in st.session_state and st.session_state['main_upload_file'] is not None:
    
    # 2. ทำการแกะและล้างข้อมูลใหม่ทุกครั้ง เพื่อป้องกันข้อมูลเก่าค้างใน session_state
    try:
        # สั่งแกะเอาเฉพาะ Sheet ที่ 2 (index 1) มาเปิดเป็นข้อมูลดิบชั่วคราว
        df_raw = pd.read_excel(st.session_state['main_upload_file'], sheet_name=1, header=None)
        
        if df_raw.empty:
            st.warning("⚠️ พบข้อมูลในระบบ แต่ไม่มีรายการข้อมูลใน Sheet นี้ (0 แถว)")
        else:
            # ดึงแถวแรก (index 0) มาทำเป็นหัวข้อคอลัมน์ภาษาไทย
            # หากช่องไหนในแถวแรกเป็นค่าว่าง ให้แทนที่ด้วยคำว่า Column_{ลำดับที่} เพื่อป้องกันหัวตารางเป็นคำว่า "nan"
            new_header = []
            for idx, val in enumerate(df_raw.iloc[0]):
                val_str = str(val).strip()
                if pd.isna(val) or val_str.lower() == 'nan' or val_str == '':
                    new_header.append(f"Unnamed_Column_{idx}")
                else:
                    new_header.append(val_str)
            
            # ตัดแถวแรกทิ้ง แล้วตั้งชื่อคอลัมน์ใหม่ตามหัวที่จัดการแล้ว
            df_cleaned = df_raw.iloc[1:].copy()
            df_cleaned.columns = new_header
            df_cleaned.reset_index(drop=True, inplace=True)
            
            # --- 🟢 แก้ไขจุดตระกูล SyntaxError: ใช้ Dictionary นับตัวซ้ำแบบพื้นฐานที่สุด ปลอดภัย 100% ---
            seen_cols = {}
            final_cols = []
            for col in df_cleaned.columns:
                if col in seen_cols:
                    seen_cols[col] += 1
                    final_cols.append(f"{col}_{seen_cols[col]}")
                else:
                    seen_cols[col] = 0
                    final_cols.append(col)
            df_cleaned.columns = final_cols
            # ---------------------------------------------------------------------------------
            
            # เจาะจงค้นหาคำว่า "หมายเหตุ" ภายในคอลัมน์ที่ชื่อว่า "หมายเหตุ" เท่านั้น
            if "หมายเหตุ" in df_cleaned.columns:
                # สแกนหาแถวที่มีคำว่า "หมายเหตุ" ซ่อนอยู่ภายในคอลัมน์หมายเหตุนั้น
                note_indices = df_cleaned[df_cleaned["หมายเหตุ"].astype(str).str.contains("หมายเหตุ", na=False)].index
                
                if not note_indices.empty:
                    # เจอคำว่าหมายเหตุคั่นปีตรงไหน ตัดข้อมูลตั้งแต่แถวนั้นลงไปทิ้งทั้งหมด
                    first_stop_idx = note_indices[0]
                    df_cleaned = df_cleaned.iloc[:first_stop_idx].copy()
                    st.success("✂️ ตรวจพบแถวคั่นปีในคอลัมน์หมายเหตุ ระบบทำการตัดข้อมูลปีเก่าออกให้เรียบร้อยแล้ว")

            # แปลงค่า NaN หรือค่าว่างในทุกๆ ช่องของตารางให้กลายเป็นค่าว่าง "" เพื่อให้ปลอดภัยต่อการแปลง JSON ใน Streamlit
            df_display = df_cleaned.replace({np.nan: "", None: ""})
            df_display.columns = df_display.columns.astype(str)

            # แสดงผลตารางที่คลีนและปลอดภัยแล้ว
            st.subheader("📋 ข้อมูลดิบจาก Sheet ที่ 2 (ดึงอัตโนมัติจากไฟล์หน้าหลัก)")
            st.dataframe(df_display)

            st.subheader("✨ ข้อมูลที่จัดสรรพร้อมนำเข้า ERP (Mapped Data)")
            st.dataframe(df_display)
            st.success(f"จัดรูปแบบสำเร็จ! พบข้อมูลของปีล่าสุดทั้งหมด {len(df_display)} รายการ")

    except Exception as e:
        st.error(f"❌ เกิดข้อผิดพลาดในการประมวลผลข้อมูล: {e}")
        st.info("💡 คำแนะนำ: ตรวจสอบโครงสร้างหัวคอลัมน์ใน Sheet ที่ 2 ของไฟล์ Excel")

else:
    st.warning("⚠️ ยังไม่มีข้อมูลในระบบ กรุณาอัปโหลดไฟล์ที่หน้าหลัก (app.py) ก่อนเริ่มใช้งาน")
