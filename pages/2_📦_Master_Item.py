import streamlit as st
import pandas as pd

st.title("📦 Module: ข้อมูลสินค้าและวัตถุดิบ (Item Master)")

uploaded_file = st.file_uploader("อัปโหลดไฟล์ Item Master ข้อมูลดิบ", type=['csv', 'xlsx'], key="item")

if uploaded_file:
    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)
    st.subheader("📋 ข้อมูลดิบที่อัปโหลดเข้าสู่ระบบ")
    st.dataframe(df)

    st.subheader("✨ ข้อมูลที่จัดสรรพร้อมนำเข้า ERP (Mapped Data)")
    mapped_df = pd.DataFrame()
    mapped_df['Item_Code'] = df.iloc[:, 0] if len(df.columns) > 0 else "N/A"
    mapped_df['Item_Description'] = df.iloc[:, 1] if len(df.columns) > 1 else "N/A"
    mapped_df['Base_UOM'] = df.iloc[:, 2] if len(df.columns) > 2 else "Pcs" # ตัวอย่าง Default Unit
    
    st.dataframe(mapped_df)
    st.success(f"ตรวจสอบเสร็จสิ้น: พบสินค้าทั้งหมด {len(mapped_df)} รายการ")
