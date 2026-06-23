import streamlit as st
import pandas as pd

st.title("📦 Module: ข้อมูลสินค้าและวัตถุดิบ (Item Master)")

if 'df_item' in st.session_state and not st.session_state['df_item'].empty:
    df = st.session_state['df_item'].copy()
    
    st.subheader("📋 ข้อมูลดิบที่ดึงมาจาก Session State")
    st.dataframe(df, use_container_width=True)

    # ==========================================
    # 🧼 STEP 1: ล้างข้อมูลขยะ (Data Cleaning)
    # ==========================================
    # 1. ค้นหาแถวที่เป็นหัวตารางเดิม (เช่น คำว่า "รหัส" หรือ "รายการ") แล้วตัดทิ้งไป
    # สมมติว่ามองหาในทุกคอลัมน์ ถ้าแถวไหนมีคำว่า "รหัส" หรือเป็นค่าว่างทั้งหมด ให้ลบออก
    df = df.dropna(how='all') # ลบแถวที่เป็นช่องว่างทั้งหมดออกก่อน (Row 0 ที่เป็น None)
    
    # กำหนดให้แน่ใจว่าทำงานกับข้อมูลสตริงเพื่อฟิลเตอร์หัวตารางเก่าออก
    if len(df) > 0:
        # ลบแถวที่มีคำว่า "รหัส" หรือ "รายการ" ที่ติดมาในเนื้อข้อมูลออก (Row 1 ในรูปภาพ)
        df = df[~df.astype(str).apply(lambda x: x.str.contains('รหัส|รายการ')).any(axis=1)]

    # ==========================================
    # 🎯 STEP 2: แมปปิ้งข้อมูลเข้า ERP ด้วยชื่อคอลัมน์ (ยืดหยุ่นกว่า)
    # ==========================================
    st.subheader("✨ ข้อมูลที่จัดสรรพร้อมนำเข้า ERP (Mapped Data)")
    
    mapped_df = pd.DataFrame(index=range(len(df)))
    
    # ฟังก์ชันช่วยค้นหาคอลัมน์จากชื่อภาษาไทย (ป้องกันเรื่องตำแหน่งคอลัมน์เคลื่อน)
    def find_column_by_name(df, keywords):
        for col in df.columns:
            # ตรวจสอบทั้งชื่อคอลัมน์ และ ข้อมูลในแถวแรกๆ (เผื่อไม่ได้ตั้งชื่อหัวตาราง)
            col_str = str(col)
            if any(kw in col_str for kw in keywords):
                return df[col].values
            
            # เผื่อว่าหัวตารางภาษาไทยไปอยู่ในแถวแรกๆ ของข้อมูลดิบ
            sample_values = df[col].head(3).astype(str).tolist()
            if any(any(kw in val for kw in keywords) for val in sample_values):
                return df[col].values
        return None

    # ดึงข้อมูล "รหัส"
    code_data = find_column_by_name(df, ['รหัส', 'Code', 'code'])
    mapped_df['Item_Code'] = code_data if code_data is not None else "N/A"
    
    # ด
