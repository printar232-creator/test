import streamlit as st
import pandas as pd

st.title("🏢 Module: ข้อมูลคู่ค้า (Vendor Master Data)")

# ตรวจสอบว่ามีข้อมูลถูกอัปโหลดมาจากหน้าหลักหรือยัง
if 'df_vendor' in st.session_state:
    df = st.session_state['df_vendor']
    
    st.subheader("📋 ข้อมูลดิบที่ดึงมาจาก Session State")
    st.dataframe(df)

    st.subheader("✨ ข้อมูลที่จัดสรรพร้อมนำเข้า ERP (Mapped Data)")
    mapped_df = pd.DataFrame()
    mapped_df['Vendor_Code'] = df.iloc[:, 0] if len(df.columns) > 0 else "N/A"
    mapped_df['Vendor_Name'] = df.iloc[:, 1] if len(df.columns) > 1 else "N/A"
    mapped_df['Tax_ID'] = df.iloc[:, 2] if len(df.columns) > 2 else "N/A"
    
    st.dataframe(mapped_df)
    st.success(f"ตรวจสอบเสร็จสิ้น: พบข้อมูลทั้งหมด {len(mapped_df)} รายการ")
else:
    st.warning("⚠️ ยังไม่มีข้อมูลในระบบ กรุณากลับไปอัปโหลดไฟล์ที่หน้าหลัก (app.py) ก่อนเริ่มใช้งาน")
