import streamlit as st
import pandas as pd

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
            new_header = df_raw.iloc[0].astype(str).tolist()
            
            # ตัดแถวแรกทิ้ง แล้วตั้งชื่อคอลัมน์ใหม่ตามหัวภาษาไทย
            df_cleaned = df_raw.iloc[1:].copy()
            df_cleaned.columns = new_header
            df_cleaned.reset_index(drop=True, inplace=True)
            
            # --- 🟢 แก้ไขจุดที่ทำให้เกิด SyntaxError: เปลี่ยนวิธีรันลำดับชื่อคอลัมน์ที่ซ้ำให้ปลอดภัย ---
            cols = list(df_cleaned.columns)
            counts = {}
            for i, col in enumerate(cols):
                if cols.count(col) > 1:
                    counts[col] = counts.get(col, 0) + 1
                    if counts[col] > 1:
                        cols[i] = f"{col}_{counts[col] - 1}"
            df_cleaned.columns = cols
            # ---------------------------------------------------------------------------------
            
            # เจาะจงค้นหาคำว่า "หมายเหตุ" ภายในคอลัมน์ที่ชื่อว่า "หมายเหตุ" เท่านั้น
            if "หมายเหตุ" in df_cleaned.columns:
                # สแกนหาแถวที่มีคำว่า "หมายเหตุ" ซ่อนอยู่ภายในคอลัมน์หมายเหตุนั้น
                note_indices = df_cleaned[df_cleaned["หมายเหตุ"].astype(str).str.contains("หมายเหตุ", na=False)].index
                
                if not note_indices.empty:
                    # เจอคำว่าหมายเหตุคั่นปีตรงไหน ตัดข้อมูลตั้งแต่แถวนั้นลงไปทิ้งทั้งหมด
                    first_stop_idx = note_indices[0]
                    df_cleaned = df_cleaned.iloc[:first_stop_idx].copy()
                    st.success(f"✂️ ตรวจพบแถวคั่นปีในคอลัมน์หมายเหตุ ระบบทำการตัดข้อมูลปีเก่าออกให้เรียบร้อยแล้ว")

            # แสดงผลตารางที่คลีนเรียบร้อยแล้ว
            st.subheader("📋 ข้อมูลดิบจาก Sheet ที่ 2 (ดึงอัตโนมัติจากไฟล์หน้าหลัก)")
            st.dataframe(df_cleaned)

            st.subheader("✨ ข้อมูลที่จัดสรรพร้อมนำเข้า ERP (Mapped Data)")
            st.dataframe(df_cleaned)
            st.success(f"จัดรูปแบบสำเร็จ! พบข้อมูลของปีล่าสุดทั้งหมด {len(df_cleaned)} รายการ")

    except Exception as e:
        st.error(f"❌ เกิดข้อผิดพลาดในการประมวลผลข้อมูล: {e}")
        st.info("💡 คำแนะนำ: ตรวจสอบโครงสร้างหัวคอลัมน์ใน Sheet ที่ 2 ของไฟล์ Excel")

else:
    st.warning("⚠️ ยังไม่มีข้อมูลในระบบ หรือระบบหาไฟล์จากหน้าหลักไม่เจอ กรุณาอัปโหลดไฟล์ที่หน้าหลัก (app.py) ก่อนเริ่มใช้งาน")
