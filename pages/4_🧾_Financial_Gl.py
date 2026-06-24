# --- ส่วนการคำนวณและจัดสรรข้อมูลบัญชี (อัปเดตตามโครงสร้างไฟล์จริงในรูปภาพ) ---
if df is not None:
    st.subheader("📋 ข้อมูลดิบที่ระบบอ่านได้ในปัจจุบัน")
    st.dataframe(df, use_container_width=True)

    st.subheader("✨ ข้อมูลที่จัดสรรพร้อมนำเข้า ERP (Mapped Data)")
    
    # กรองเอาเฉพาะแถวที่ 6 เป็นต้นไป (เนื่องจากแถว 0-5 เป็นหัวรายงานภาษาไทย ทำให้ติด Error หรือค่าว่าง)
    # และรีเซ็ตอินเดกซ์ใหม่ให้เริ่มจาก 0
    clean_df = df.iloc[6:].reset_index(drop=True)
    
    mapped_df = pd.DataFrame()
    
    # 1. ดึงคอลัมน์ที่ 1 (index 1) มาเป็น GL_Account_No
    mapped_df['GL_Account_No'] = clean_df.iloc[:, 1] if len(clean_df.columns) > 1 else "N/A"
    
    # 2. ดึงคอลัมน์ที่ 2 (index 2) มาเป็น Account_Name
    mapped_df['Account_Name'] = clean_df.iloc[:, 2] if len(clean_df.columns) > 2 else "N/A"
    
    # 3. ดึงคอลัมน์ที่ 6 (index 6) มาเป็น Debit_Amount (ตัวเลขจำนวน)
    mapped_df['Debit_Amount'] = clean_df.iloc[:, 6] if len(clean_df.columns) > 6 else 0
    
    # 4. กำหนด Credit_Amount ให้เป็น 0 (หรือเปลี่ยนดัชนีคอลัมน์หากมีคอลัมน์อื่นเพิ่มเติม)
    mapped_df['Credit_Amount'] = 0 
    
    # แปลงข้อมูลตัวเลขให้ถูกต้อง ป้องกัน Text/String หลุดเข้ามา
    mapped_df['Debit_Amount'] = pd.to_numeric(mapped_df['Debit_Amount'], errors='coerce').fillna(0)
    mapped_df['Credit_Amount'] = pd.to_numeric(mapped_df['Credit_Amount'], errors='coerce').fillna(0)
    
    # แสดงตาราง Mapped Data ที่สะอาดและดึงข้อมูลมาตรงตามแถวแล้ว
    st.dataframe(mapped_df, use_container_width=True)
    
    # คำนวณยอดสรุป
    total_debit = mapped_df['Debit_Amount'].sum()
    total_credit = mapped_df['Credit_Amount'].sum()
    balance_diff = total_debit - total_credit
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="ยอดรวม Debit", value=f"{total_debit:,.2f} บาท")
    with col2:
        st.metric(label="ยอดรวม Credit", value=f"{total_credit:,.2f} บาท")
    with col3:
        st.metric(
            label="ผลต่าง (ต้องเป็น 0)", 
            value=f"{balance_diff:,.2f} บาท",
            delta=f"{balance_diff:,.2f} บาท" if balance_diff != 0 else None,
            delta_color="inverse" if balance_diff != 0 else "normal"
        )
