import streamlit as st
import pandas as pd

st.title("🛒 Module: ข้อมูลใบสั่งซื้อค้างส่ง (Open Purchase Orders)")

uploaded_file = st.file_uploader("อัปโหลดไฟล์ Open PO ข้อมูลดิบ", type=['csv', 'xlsx', 'xls'], key="po")

if uploaded_file:
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
    mapped_df['PO_Number'] = df.iloc[:, 0] if len(df.columns) > 0 else "N/A"
    mapped_df['PO_Date'] = df.iloc[:, 1] if len(df.columns) > 1 else "N/A"
    mapped_df['Vendor_Code'] = df.iloc[:, 2] if len(df.columns) > 2 else "N/A"
    mapped_df['Quantity_Ordered'] = df.iloc[:, 3] if len(df.columns) > 3 else 0
    
    st.dataframe(mapped_df)
    st.success("จับคู่ข้อมูล Transaction PO สำเร็จ")
