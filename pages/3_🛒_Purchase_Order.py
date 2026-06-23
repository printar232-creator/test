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
                if pd.isna(val) or str(val).strip().lower() == 'nan' or str(val).strip() == '':
                    new_header.append(f"Unnamed_Column_{idx}")
                else:
                    new_header.append(str(val).strip())
            
            # ตัดแถวแรกทิ้ง แล้วตั้งชื่อคอลัมน์ใหม่ตามหัวที่จัดการแล้ว
            df_cleaned = df_raw.iloc[1:].copy()
            df_cleaned.columns = new_header
            df_cleaned.reset_index(drop=True, inplace=True)
            
            # --- จัดการปัญหาชื่อคอลัมน์ซ้ำกัน เพื่อป้องกันการชนกันของคอลัมน์ ---
            cols = list(df_cleaned.columns)
            counts = {}
            for i, col in enumerate(cols):
                if cols.count(col) > 1:
                    counts[col] = counts.get(col, 0) + 1
                    if counts[col] > 1:
                        cols[i] = f"{col}_{counts[col] - 1}"
            df_cleaned.columns = cols
            
            # --- เจาะจงค้นหาคำว่า "หมายเหตุ" ภายในคอลัมน์ที่ชื่อว่า "หมายเหตุ" เท่านั้น ---
            if "หมายเหตุ" in df_cleaned.columns:
                # สแกนหาแถวที่มีคำว่า "หมายเหตุ" ซ่อนอยู่ภายในคอลัมน์หมายเหตุนั้น
                note_indices = df_cleaned[df_cleaned["หมายเหตุ"].astype(str).str.contains("หมายเหตุ", na=False)].index
                
                if not note_indices.empty:
                    # เจอคำว่าหมายเหตุคั่นปีตรงไหน ตัดข้อมูลตั้งแต่แถวนั้นลงไปทิ้งทั้งหมด
                    first_stop_idx = note_indices[0]
                    df_cleaned = df_cleaned.iloc[:first_stop_idx].copy()
                    st.success(f"✂️ ตรวจพบแถวคั่นปีในคอลัมน์หมายเหตุ ระบบทำการตัดข้อมูลปีเก่าออกให้เรียบร้อยแล้ว")

            # --- 🟢 ส่วนที่แก้ไขหลักเพื่อแก้ปัญหา JSON Invalid Token NaN ---
            # แปลงค่า NaN หรือค่าว่างในทุกๆ ช่องของตารางให้กลายเป็นค่าว่าง "" หรือข้อความที่ระบุได้ เพื่อให้ปลอดภัยต่อ JSON
            df_display = df_cleaned.replace({np.nan: "", None: ""})
            # บ
