import streamlit as st
import pandas as pd
import io

st.title("🧾 Module: สมุดบัญชีแยกประเภทและยอดหมุนเวียน (G/L Balances)")

if 'df_gl' in st.session_state:
    
    # บังคับอ่านไฟล์จาก Memory และเคลียร์ตัวแปรชั่วคราวเพื่อไม่ให้ดึงอันเก่ามาใช้
    df = None
    
    try:
        file_gl_raw = st.session_state.get("upload_g")
        
        if file_gl_raw is not None:
            # ใช้ BytesIO อ่านข้อมูลสดๆ จากตัวไฟล์อัปโหลด
            file_bytes = file_gl_raw.getvalue()
            excel_file = pd.ExcelFile(io.BytesIO(file_bytes))
            sheet_names = excel_file.sheet_names
            
            # ตรวจสอบว่าในไฟล์มีกี่ Sheet
            if len(sheet_names) > 1:
                target_sheet = sheet_names[1] # เจาะจงเลือก Sheet ลำดับที่ 2
                
                # แสดงข้อความบอกให้ผู้ใช้ทราบว่าระบบกำลังอ่าน Sheet ไหนอยู่จริงๆ
                st.caption(f"📂 กำลังดึงข้อมูลจากแผ่นงานลำดับที่ 2 ชื่อว่า: **{target_sheet}**")
                
                # สั่งโหลดข้อมูลใหม่แบบบังคับเจาะชื่อ Sheet ตัวที่ 2
                df = pd.read_excel(io.BytesIO(file_bytes), sheet_name=target_sheet, header=None)
            else:
                st.error(f"❌ ไฟล์นี้มีแค่ Sheet เดียวคือ '{sheet_names[0]}' ไม่พบ Sheet ที่ 2 ในไฟล์ของคุณ")
                df = st.session_state['df_gl']
        else:
            df = st.session_state['df_gl']
            
    except Exception as e:
        st.warning(f"⚠️ เกิดข้อผิดพลาดในการเจาะอ่าน Sheet 2: {e}")
        df = st.session_state['df_gl']

    # ถ้าดึงข้อมูลมาได้สำเร็จ (ไม่เป็น None) ให้รันการ Mapping ต่อ
    if df is not None:
        st.subheader(f"📋 ข้อมูลดิบที่ดึงมาจาก Sheet ลำดับที่ 2")
        st.dataframe(df)

        st.subheader("✨ ข้อมูลที่จัดสรรพร้อมนำเข้า ERP (Mapped Data)")
        
        mapped_df = pd.DataFrame()
        mapped_df['GL_Account_No'] = df.iloc[:, 0] if len(df.columns) > 0 else "N/A"
        mapped_df['Account_Name'] = df.iloc[:, 1] if len(df.columns) > 1 else "N/A"
        mapped_df['Debit_Amount'] = df.iloc[:, 2] if len(df.columns) > 2 else 0
        mapped_df['Credit_Amount'] = df.iloc[:, 3] if len(df.columns) > 3 else 0
        
        mapped_df['Debit_Amount'] = pd.to_numeric(mapped_df['Debit_Amount'], errors='coerce').fillna(0)
        mapped_df['Credit_Amount'] = pd.to_numeric(mapped_df['Credit_Amount'], errors='coerce').fillna(0)
        
        st.dataframe(mapped_df)
        
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
else:
    st.warning("⚠️ ไม่พบข้อมูลใน Session State กรุณาอัปโหลดไฟล์ในหน้าหลักก่อน")
