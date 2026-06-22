import streamlit as st
import pandas as pd

st.title("🏢 Module: ข้อมูลคู่ค้า (Vendor Master Data)")

# 1. เพิ่ม 'xls' ในช่อง type
uploaded_file = st.file_uploader("อัปโหลดไฟล์ Vendor ข้อมูลดิบ", type=['csv', 'xlsx', 'xls'], key="vendor")

if uploaded_file:
    # 2. ปรับ Logic การอ่านไฟล์รองรับทั้ง xlsx, xls และ csv
    if uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file, engine='openpyxl')
    elif uploaded_file.name.endswith('.xls'):
        df = pd.read_excel(uploaded_file, engine='xlrd')
    else:
        df = pd.read_csv(uploaded_file)
    
    st.subheader("📋 ข้อมูลดิบที่อัปโหลดเข้าสู่ระบบ")
    st.dataframe(df)

    st.subheader("✨ ข้อมูลที่จัดสรรพร้อมนำเข้า ERP (Mapped Data)")
    mapped_df = pd.DataFrame()
    mapped_df['Vendor_Code'] = df.iloc[:, 0] if len(df.columns) > 0 else "N/A"
    mapped_df['Vendor_Name'] = df.iloc[:, 1] if len(df.columns) > 1 else "N/A"
    mapped_df['Tax_ID'] = df.iloc[:, 2] if len(df.columns) > 2 else "N/A"
    
    st.dataframe(mapped_df)
    st.success(f"ตรวจสอบเสร็จสิ้น: พบข้อมูลทั้งหมด {len(mapped_df)} รายการ")
