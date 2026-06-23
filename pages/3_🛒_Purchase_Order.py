import streamlit as st
import pandas as pd

st.title("🛒 Module: ข้อมูลใบสั่งซื้อค้างส่ง (Open Purchase Orders)")

# 1. ตรวจสอบว่ามีไฟล์ดิบจากหน้าหลักเข้ามาเก็บไว้ในระบบหรือยัง
if 'main_upload_file' in st.session_state and st.session_state['main_upload_file'] is not None:
    
    # 2. ถ้ามีไฟล์ดิบ และหน้านี้ยังไม่เคยดึง Sheet 2 ให้ทำการดึงและเก็บไว้แยกต่างหาก
    if 'df_po_sheet2' not in st.session_state:
        try:
            # สั่งแกะเอาเฉพาะ Sheet ที่ 2 (index 1) มาเก็บไว้ใช้เฉพาะหน้านี้
            st.session_state['df_po_sheet2'] = pd.read_excel(st.session_state['main_upload_file'], sheet_name=1, header=None)
        except Exception as e:
            st.error(f"❌ ไม่สามารถดึงข้อมูล Sheet ที่ 2 ได้: {e}")
            st.info("💡 คำแนะนำ: ตรวจสอบว่าไฟล์ Excel ที่อัปโหลดมีอย่างน้อย 2 Sheet หรือไม่")

# 3. ส่วนการแสดงผล
if 'df_po_sheet2' in st.session_state:
    df_raw = st.session_state['df_po_sheet2']
    
    if df_raw.empty:
        st.warning("⚠️ พบข้อมูลในระบบ แต่ไม่มีรายการข้อมูลใน Sheet นี้ (0 แถว)")
    else:
        # ดึงแถวแรก (index 0) มาทำเป็นหัวข้อคอลัมน์ภาษาไทย
        new_header = df_raw.iloc[0].astype(str).tolist()
        
        # ตัดแถวแรกทิ้ง แล้วตั้งชื่อคอลัมน์ใหม่ตามหัวภาษาไทย
        df_cleaned = df_raw.iloc[1:].copy()
        df_cleaned.columns = new_header
        df_cleaned.reset_index(drop=True, inplace=True)
        
        # --- 🟢 ส่วนที่แก้ไข: จัดการปัญหาชื่อคอลัมน์ซ้ำกัน (Fix Duplicate Column Names) ---
        s = pd.Series(df_cleaned.columns)
        # ถ้าระบบพบชื่อซ้ำ จะรันตัวเลขห้อยท้ายให้เองอัตโนมัติ เช่น คอลัมน์ว่าง 'nan' จะกลายเป็น 'nan', 'nan.1', 'nan.2'
        df_cleaned.columns = s.where(~s.duplicated(), s + '.' + s.groupby(s).cumcount().astype(str))
        # ---------------------------------------------------------------------------------
        
        # เจาะจงค้นหาคำว่า "หมายเหตุ" ภายในคอลัมน์ "หมายเหตุ"
        if "หมายเหตุ" in df_cleaned.columns:
            # สแกนหาแถวที่มีคำว่า "หมายเหตุ" ซ่อนอยู่ในคอลัมน์หมายเหตุ
            note_indices = df_cleaned[df_cleaned["หมายเหตุ"].astype(str).str.contains("หมายเหตุ", na=False)].index
            
            if not note_indices.empty:
                # เจอคำว่าหมายเหตุคั่นปีตรงไหน ตัดข้อมูลตั้งแต่แถวนั้นลงไปทิ้งทั้งหมด
                first_stop_idx = note_indices[0]
                df_cleaned = df_cleaned.iloc[:first_stop_idx].copy()
                st.success(f"✂️ ตรวจพบแถวคั่นปีในคอลัมน์หมายเหตุ ระบบทำการตัดข้อมูลปีเก่าออกให้เรียบร้อยแล้ว")

        st.subheader("📋 ข้อมูลดิบจาก Sheet ที่ 2 (ดึงอัตโนมัติจากไฟล์หน้าหลัก)")
        st.dataframe(df_cleaned)

        st.subheader("✨ ข้อมูลที่จัดสรรพร้อมนำเข้า ERP (Mapped Data)")
        st.dataframe(df_cleaned)
        
        st.success(f"จัดรูปแบบสำเร็จ! พบข้อมูลของปีล่าสุดทั้งหมด {len(df_cleaned)} รายการ")
else:
    st.warning("⚠️ ยังไม่มีข้อมูลในระบบ กรุณาอัปโหลดไฟล์ที่หน้าหลัก (app.py) ก่อนเริ่มใช้งาน")
