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
    
    # --- แก้ไขโค้ดส่วนการคำนวณใหม่ตรงนี้ ---
    # ใช้ errors='coerce' เพื่อเปลี่ยนค่าที่แปลงไม่ได้ให้เป็น NaN แล้วเติมด้วย 0 (.fillna(0))
    debit_values = pd.to_numeric(mapped_df['Debit_Amount'], errors='coerce').fillna(0)
    credit_values = pd.to_numeric(mapped_df['Credit_Amount'], errors='coerce').fillna(0)
    
    total_debit = debit_values.sum()
    total_credit = credit_values.sum()
    
    st.metric(label="ผลต่าง Debit/Credit (ต้องเป็น 0)", value=f"{total_debit - total_credit:,.2f} บาท")
