import streamlit as st
import pandas as pd
import io

st.title("🧾 Module: สมุดบัญชีแยกประเภทและยอดหมุนเวียน (G/L Balances)")

# ตรวจสอบการอัปโหลดไฟล์จากหน้าหลัก
if 'df_gl' in st.session_state or "upload_g" in st.session_state:
    
    file_gl_raw = st.session_state.get("upload_g")
    df = None
    
    if file_gl_raw is not None:
        try:
            # ดึงไบต์ไฟล์สดเพื่อเข้าไปอ่านโครงสร้างแผ่นงานทั้งหมดที่มี
            file_bytes = file_gl_raw.getvalue()
            excel_file = pd.ExcelFile(io.BytesIO(file_bytes))
            all_sheets = excel_file.sheet_names
            
            st.markdown("---")
            st.markdown("### 🔍 ตรวจพบแผ่นงานในไฟล์ของคุณ")
            
            # 🟢 [จุดเด็ดขาด] สร้าง Dropdown ให้ผู้ใช้เลือก Sheet เองเพื่อบังคับสั่งโหลดใหม่ตามต้องการ
            selected_sheet = st.selectbox(
                "กรุณาเลือกแผ่นงาน (Sheet) ที่ถูกต้องสำหรับหน้าสมุดบัญชีแยกประเภท:",
                options=all_sheets,
                index=1 if len(all_sheets) > 1 else 0  # ตั้งค่าเริ่มต้นให้ชี้ไปที่ Sheet ลำดับที่ 2
            )
            
            # บังคับอ่านข้อมูลจากแผ่นงานที่เลือกทันที
            df = pd.read_excel(io.BytesIO(file_bytes), sheet_name=selected_sheet, header=None, engine='openpyxl')
            st.success(f"📋 ดึงข้อมูลจากแผ่นงาน: **'{selected_sheet}'** สำเร็จ")
            
        except Exception as e:
            st.error(f"❌ ระบบไม่สามารถเจาะอ่านไฟล์ Excel ได้: {e}")
            df = st.session_state.get('df_gl')
    else:
        # กรณีที่เป็นไฟล์ประเภทอื่นที่ไม่ใช่ Excel (.csv)
        df = st.session_state.get('df_gl')
        st.info("ℹ️ ตรวจพบเป็นไฟล์เดี่ยว (.csv) ระบบจึงดึงข้อมูลแผ่นงานหลักมาใช้งานโดยอัตโนมัติ")

    # --- ส่วนการนำข้อมูลไปใช้งานต่อ (คงเดิมเพื่อไม่ให้ระบบรวน) ---
    if df is not None:
        st.subheader("📋 ข้อมูลดิบที่ระบบอ่านได้ในปัจจุบัน")
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
