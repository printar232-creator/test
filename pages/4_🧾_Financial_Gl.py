import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="G/L Balances Module", page_icon="💰", layout="wide")
st.title("🧾 Module: สมุดบัญชีแยกประเภทและยอดหมุนเวียน (G/L Balances)")

# 1. ตรวจสอบสถานะข้อมูลจากหน้าหลัก
has_df = 'df_gl' in st.session_state
has_raw_file = 'upload_g' in st.session_state and st.session_state['upload_g'] is not None

if has_df or has_raw_file:
    
    df = None
    file_gl_raw = st.session_state.get("upload_g")
    
    # 2. เคสที่ 1: ตรวจพบไฟล์ดิบในระบบ (และเป็น Excel)
    if file_gl_raw is not None and hasattr(file_gl_raw, 'name') and file_gl_raw.name.endswith(('.xlsx', '.xls')):
        try:
            file_bytes = file_gl_raw.getvalue()
            selected_engine = 'openpyxl' if file_gl_raw.name.endswith('.xlsx') else 'xlrd'
            excel_file = pd.ExcelFile(io.BytesIO(file_bytes), engine=selected_engine)
            all_sheets = excel_file.sheet_names
            
            st.markdown("---")
            st.markdown("### 🔍 ตรวจพบแผ่นงานในไฟล์ของคุณ")
            
            # 🟢 [จุดแก้ไขวิกฤต] ใช้ key="gl_sheet_choice" เพื่อล็อกค่าที่เลือกไว้ไม่ให้หายไปตอน Rerun
            # และหา index ล่าสุดที่ผู้ใช้เคยเลือกไว้ (ถ้าไม่มี ให้เริ่มที่ลำดับ 2 หรือ 1 ตามเงื่อนไขคุณ)
            if "gl_sheet_choice" in st.session_state and st.session_state["gl_sheet_choice"] in all_sheets:
                default_index = all_sheets.index(st.session_state["gl_sheet_choice"])
            else:
                default_index = 1 if len(all_sheets) > 1 else 0

            selected_sheet = st.selectbox(
                "กรุณาเลือกแผ่นงาน (Sheet) ที่ถูกต้องสำหรับหน้าสมุดบัญชีแยกประเภท:",
                options=all_sheets,
                index=default_index,
                key="gl_sheet_choice"  # บังคับจำสเตท
            )
            
            # บังคับอ่านข้อมูลจากแผ่นงานที่ผู้ใช้กดเลือกในปัจจุบัน
            df = pd.read_excel(io.BytesIO(file_bytes), sheet_name=selected_sheet, header=None, engine=selected_engine)
            st.success(f"📋 ดึงข้อมูลจากแผ่นงาน: **'{selected_sheet}'** สำเร็จ")
            
        except Exception as e:
            st.error(f"⚠️ ไม่สามารถเจาะอ่านแผ่นงานเพิ่มเติมได้เนื่องจากเทคนิคไฟล์: {e}")
            df = st.session_state.get('df_gl')
            
    # 3. เคสที่ 2: เป็นไฟล์ .csv หรือระบบไม่สามารถดึงไฟล์ดิบย้อนหลังได้
    else:
        df = st.session_state.get('df_gl')
        if file_gl_raw and hasattr(file_gl_raw, 'name') and file_gl_raw.name.endswith('.csv'):
            st.info("ℹ️ ตรวจพบเป็นไฟล์เดี่ยว (.csv) ระบบจึงดึงข้อมูลแผ่นงานหลักมาใช้งานโดยอัตโนมัติ")
        else:
            st.info("📊 แสดงผลข้อมูลเริ่มต้นจากศูนย์กลาง (Default Sheet)")

    # --- ส่วนการนำข้อมูลไปใช้งานต่อ (คงเดิม) ---
    if df is not None:
        st.subheader("📋 ข้อมูลดิบที่ระบบอ่านได้ในปัจจุบัน")
        st.dataframe(df, use_container_width=True)

        st.subheader("✨ ข้อมูลที่จัดสรรพร้อมนำเข้า ERP (Mapped Data)")
        
        mapped_df = pd.DataFrame()
        mapped_df['GL_Account_No'] = df.iloc[:, 0] if len(df.columns) > 0 else "N/A"
        mapped_df['Account_Name'] = df.iloc[:, 1] if len(df.columns) > 1 else "N/A"
        mapped_df['Debit_Amount'] = df.iloc[:, 2] if len(df.columns) > 2 else 0
        mapped_df['Credit_Amount'] = df.iloc[:, 3] if len(df.columns) > 3 else 0
        
        mapped_df['Debit_Amount'] = pd.to_numeric(mapped_df['Debit_Amount'], errors='coerce').fillna(0)
        mapped_df['Credit_Amount'] = pd.to_numeric(mapped_df['Credit_Amount'], errors='coerce').fillna(0)
        
        st.dataframe(mapped_df, use_container_width=True)
        
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
