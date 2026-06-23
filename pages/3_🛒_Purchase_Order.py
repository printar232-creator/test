import streamlit as st
import pandas as pd

st.title("🛒 Module: ข้อมูลใบสั่งซื้อค้างส่ง (Open Purchase Orders)")

if 'df_po' in st.session_state:
    df = st.session_state['df_po']
    
    st.subheader("📋 ข้อมูลดิบที่ดึงมาจาก Session State")
    st.dataframe(df)

    st.subheader("✨ ข้อมูลที่จัดสรรพร้อมนำเข้า ERP (Mapped Data)")
    
    num_rows = len(df)
    
    mapped_data = {
        'PO_Number': df.iloc[:, 0] if len(df.columns) > 0 else ["N/A"] * num_rows,
        'PO_Date': df.iloc[:, 1] if len(df.columns) > 1 else ["N/A"] * num_rows,
        'Vendor_Code': df.iloc[:, 2] if len(df.columns) > 2 else ["N/A"] * num_rows,
        'Quantity_Ordered': df.iloc[:, 3] if len(df.columns) > 3 else [0] * num_rows
    }
    
    mapped_df = pd.DataFrame(mapped_data)
    
    st.dataframe(mapped_df)
    st.success("จับคู่ข้อมูล Transaction PO สำเร็จ")
else:
    st.warning("⚠️ ยังไม่มีข้อมูลในระบบ กรุณากลับไปอัปโหลดไฟล์ที่หน้าหลัก (app.py) ก่อนเริ่มใช้งาน")
