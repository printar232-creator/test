import streamlit as st
import pandas as pd

st.title("📦 Module: ข้อมูลสินค้าและวัตถุดิบ (Item Master)")

if 'df_item' in st.session_state:
    df = st.session_state['df_item']
    
    st.subheader("📋 ข้อมูลดิบที่ดึงมาจาก Session State")
    st.dataframe(df)

    st.subheader("✨ ข้อมูลที่จัดสรรพร้อมนำเข้า ERP (Mapped Data)")
    mapped_df = pd.DataFrame()
    mapped_df['Item_Code'] = df.iloc[:, 0] if len(df.columns) > 0 else "N/A"
    mapped_df['Item_Description'] = df.iloc[:, 1] if len(df.columns) > 1 else "N/A"
    mapped_df['Base_UOM'] = df.iloc[:, 2] if len(df.columns) > 2 else "Pcs"
    
    st.dataframe(mapped_df)
    st.success(f"ตรวจสอบเสร็จสิ้น: พบสินค้าทั้งหมด {len(mapped_df)} รายการ")
else:
    st.warning("⚠️ ยังไม่มีข้อมูลในระบบ กรุณากลับไปอัปโหลดไฟล์ที่หน้าหลัก (app.py) ก่อนเริ่มใช้งาน")
