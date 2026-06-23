import streamlit as st
import pandas as pd

st.title("🛒 Module: ข้อมูลใบสั่งซื้อค้างส่ง (Open Purchase Orders)")

# 1. ตรวจสอบว่ามีไฟล์ดิบจากหน้าหลักเข้ามาเก็บไว้ในระบบหรือยัง
if 'main_upload_file' in st.session_state and st.session_state['main_upload_file'] is not None:
    
    # 2. ทำการแกะและล้างข้อมูลใหม่ทุกครั้ง เพื่อป้องกันข้อมูลเก่าค้างใน session_state
    try:
        # สั่งแกะเอาเฉพาะ Sheet ที่ 2 (index 1) มาเปิดเป็น ข้อมูลดิบชั่วคราว
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
            
            # --- 🟢 ส่วนที่แก้ไขหลัก: ล้างปัญหาชื่อคอลัมน์ซ้ำกันให้ขาดก่อนส่งให้ Streamlit ---
            cols = pd.Series(df_cleaned.columns)
            for duplicate in cols[cols.duplicated()].unique():
                cols[cols == duplicate] = [f"{duplicate}_{i}" if i != 0 else duplicate for i in range(len(cols[cols == duplicate]))]
            df_cleaned.columns = cols
            # ---------------------------------------------------------------------------------
            
            # เจาะจงค้นหาคำว่า "หมายเหตุ" ภายในคอลัมน์ "หมายเหตุ" (หรือคอลัมน์ที่ขึ้นต้นด้วย หมายเหตุ)
            # หาชื่อคอลัมน์จริงที่สัมพันธ์กับคำว่าหมายเหตุ
            note_col = [c for c in df_cleaned.columns if "หมายเหตุ" in c]
            
            if note_col:
                # สแกนหาแถวที่มีคำว่า "หมายเหตุ" ซ่อนอยู่ภายในคอลัมน์หมายเหตุนั้น
                target_col = note_col[0]
                note_indices = df_cleaned[df_cleaned[target_col].astype(str).str.contains("หมายเหตุ", na=False)].index
                
                if not note_indices.empty:
                    # เจอคำว่าหมายเหตุคั่นปีตรงไหน ตัดข้อมูลตั้งแต่แถวนั้นลงไปทิ้งทั้งหมด
                    first_stop_idx = note_indices[0]
                    df_
