import streamlit as st
import pandas as pd

st.title("🧾 Module: สมุดบัญชีแยกประเภทและยอดหมุนเวียน (G/L Balances)")

if 'df_gl' in st.session_state:
    df = st.session_state['df_gl']
    
    st.subheader("📋 ข้อมูลดิบที่ดึงมาจาก Session State")
    st.dataframe(df)

    st.subheader("✨ ข้อมูลที่จัดสรรพร้อมนำเข้า ERP (Mapped Data)")
    mapped_df = pd.DataFrame()
    mapped_df['GL_Account_No'] = df.iloc[:, 0] if len(df.columns) > 0 else "N/A"
    mapped_df['Account_Name'] = df.iloc[:, 1] if len(df.columns) > 1 else "N/A"
    mapped_df['Debit_Amount'] = df.iloc[:, 2] if len(df.columns) > 2 else 0
    mapped_df['Credit_Amount'] = df.iloc[:, 3] if len(df.columns) > 3 else 0
    
    st.dataframe(mapped_df)
    
    total_debit = pd.to_numeric(mapped_df['Debit_Amount']).sum()
    total_credit = pd.to_numeric(mapped_df['Credit_Amount']).sum()
    st.metric(label="ผลต่าง Debit/Credit (ต้องเป็น 0)", value=f"{total_debit - total_credit:,.2f} บาท")
else:
    st.warning("⚠️ ยังไม่มีข้อมูลในระบบ กรุณากลับไปอัปโหลดไฟล์ที่หน้าหลัก (app.py) ก่อนเริ่มใช้งาน")
