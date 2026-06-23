import streamlit as st
import pandas as pd
import io

st.title("🧾 Module: สมุดบัญชีแยกประเภทและยอดหมุนเวียน (G/L Balances)")

# 🟢 [จุดแก้ไขสำคัญ] ล็อกตัวไฟล์ดิบไว้ใน Session State ของหน้าย่อยทันทีเพื่อป้องกันการเลือนหาย
if "upload_g" in st.session_state and st.session_state["upload_g"] is not None:
    # ฝากไฟล์ดิบเข้าตัวแปรส่วนตัวของโมดูลนี้
    st.session_state["gl_file_backup"] = st.session_state["upload_g"]

# ตรวจสอบว่ามีข้อมูลจากหน้าหลักหรือมีไฟล์สำรองหรือไม่
if 'df_gl' in st.session_state or "gl_file_backup" in st.session_state:
    
    df = None
    
    try:
        # เรียกใช้ไฟล์จากตัวจำค่าสำรองที่เราล็อกไว้
        file_gl_raw = st.session_state.get("gl_file_backup")
        
        if file_gl_raw is not None:
            # ใช้การเข้าถึงข้อมูลแบบ Binary สดๆ 
            file_bytes = file_gl_raw.getvalue() if hasattr(file_gl_raw, 'getvalue') else file_gl_raw
            
            # บังคับอ่านด้วยสเปกที่เจาะลึก
            excel_file = pd.ExcelFile(io.BytesIO(file_bytes))
            sheet_names = excel_file.sheet_names
            
            if len(sheet_names) > 1:
                # เจาะจงเลือก Sheet ลำดับที่ 2 (Index 1)
                target_sheet = sheet_names[1]
                st.info(f"📂 ค้นพบแผ่นงานทั้งหมด: {sheet_names} -> กำลังเจาะจงอ่านแผ่นงานที่ 2 คือ: **{target_sheet}**")
                
                # อ่านไฟล์โดยบังคับ Engine ให้ชัดเจน
                df = pd.read_excel(io.BytesIO(file_bytes), sheet_name=1, header=None, engine='openpyxl')
            else:
                st.error(f"❌ ไฟล์นี้มีแค่ Sheet เดียวคือ '{sheet_names[0]}' ไม่พบ Sheet อื่นๆ ในไฟล์")
                df = st.session_state.get('df_gl')
        else:
            df = st.session_state.get('df_gl')
            
    except Exception as e:
        st.warning(f"⚠️ กำลังสลับไปใช้ระบบสำรองอัตโนมัติเนื่องจาก: {e}")
        df = st.session_state.get('df_gl')

    # ประมวลผลและจัดทำ Mapped Data
    if df is not None:
        st.subheader("📋 ข้อมูลดิบที่ดึงมาจาก Sheet ลำดับที่ 2")
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
