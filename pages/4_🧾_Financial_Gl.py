import streamlit as st
import pandas as pd
import io

st.title("🧾 Module: สมุดบัญชีแยกประเภทและยอดหมุนเวียน (G/L Balances)")

if 'df_gl' in st.session_state:
    
    # บังคับดึงข้อมูล Sheet 2 แบบตรวจสอบเชิงลึก
    try:
        # ดึงไฟล์ดิบจากคีย์หลัก
        file_gl_raw = st.session_state.get("upload_g")
        
        if file_gl_raw is not None:
            # ใช้ io.BytesIO เพื่ออ่านข้อมูลจาก Buffer ซ้ำอีกครั้งได้อย่างปลอดภัย
            file_bytes = file_gl_raw.getvalue()
            
            # ตรวจสอบชื่อแผ่นงานทั้งหมดที่มีในไฟล์ เพื่อค้นหาแผ่นงานลำดับที่ 2
            excel_file = pd.ExcelFile(io.BytesIO(file_bytes))
            sheet_names = excel_file.sheet_names
            
            if len(sheet_names) > 1:
                # บังคับอ่านแผ่นงานลำดับที่ 2 (Index 1) ชี้ชัดเจน
                df = pd.read_excel(io.BytesIO(file_bytes), sheet_name=1, header=None)
                # 💡 TIP: หากคุณทราบชื่อแผ่นงานแน่นอน เช่น "Sheet2" สามารถแก้เป็น sheet_name="ชื่อชีต" ได้เช่นกัน
            else:
                st.error("❌ ไฟล์ Excel นี้มีเพียงแค่ 1 แผ่นงาน (Sheet) ไม่พบ Sheet 2")
                df = st.session_state['df_gl']
        else:
            df = st.session_state['df_gl']
            
    except Exception as e:
        df = st.session_state['df_gl']
        st.warning(f"⚠️ เกิดข้อผิดพลาดในการเจาะอ่าน Sheet 2: {e}")

    # --- ส่วนแสดงผลและคำนวณคงเดิมเพื่อไม่ให้ระบบรวน ---
    st.subheader("📋 ข้อมูลดิบที่ดึงมาจาก Sheet 2")
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
