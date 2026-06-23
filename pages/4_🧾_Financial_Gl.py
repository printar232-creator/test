import streamlit as st
import pandas as pd

st.title("🧾 Module: สมุดบัญชีแยกประเภทและยอดหมุนเวียน (G/L Balances)")

# ตรวจสอบว่ามีข้อมูลถูกอัปโหลดเข้ามาจาก app.py หรือยัง
if 'df_gl' in st.session_state:
    
    # --- 🟢 จุดสำคัญ: ดึงข้อมูลจาก Sheet 2 แบบอ้อม โดยดึงจากไฟล์ดิบที่ค้างอยู่ใน Widget Memory ---
    # โค้ดส่วนนี้จะทำงานเฉพาะเมื่อไฟล์เป็น Excel (.xlsx, .xls) เท่านั้น
    try:
        # ดึงตัวแทนไฟล์ดิบที่ค้างอยู่ในระบบของ Streamlit จากหน้า app.py (แกะจาก key "upload_g")
        file_gl_raw = st.session_state.get("upload_g") 
        
        if file_gl_raw and file_gl_raw.name.endswith(('.xlsx', '.xls')):
            # สั่งอ่านข้อมูลจาก Sheet ลำดับที่ 2 (index=1) และตั้งค่า header=None เพื่อให้เหมือนกับฟังก์ชันหลัก
            df = pd.read_excel(file_gl_raw, sheet_name=1, header=None)
        else:
            # หากเป็นไฟล์ .csv (ซึ่งไม่มี Sheet 2) ให้ใช้ข้อมูลจาก df_gl ตามปกติเพื่อป้องกันโปรแกรมพัง
            df = st.session_state['df_gl']
            
    except Exception as e:
        # กรณีฉุกเฉินหากดึงแผ่นงานที่ 2 ไม่สำเร็จ ให้ถอยกลับไปใช้ Sheet แรกที่เป็นตัวตั้งต้น
        df = st.session_state['df_gl']
        st.warning(f"⚠️ ไม่สามารถโหลด Sheet 2 ได้ (ระบบจึงใช้ข้อมูลจาก Sheet แรกแทน): {e}")
    # ----------------------------------------------------------------------------------

    st.subheader("📋 ข้อมูลดิบที่ดึงมาจาก Sheet 2")
    st.dataframe(df)

    st.subheader("✨ ข้อมูลที่จัดสรรพร้อมนำเข้า ERP (Mapped Data)")
    
    # 1. จัดสรรข้อมูลใส่ DataFrame ใหม่
    mapped_df = pd.DataFrame()
    mapped_df['GL_Account_No'] = df.iloc[:, 0] if len(df.columns) > 0 else "N/A"
    mapped_df['Account_Name'] = df.iloc[:, 1] if len(df.columns) > 1 else "N/A"
    mapped_df['Debit_Amount'] = df.iloc[:, 2] if len(df.columns) > 2 else 0
    mapped_df['Credit_Amount'] = df.iloc[:, 3] if len(df.columns) > 3 else 0
    
    # 2. แปลงข้อมูลใน DataFrame ให้เป็นตัวเลขทันที (คลีนข้อมูลก่อนแสดงผล)
    mapped_df['Debit_Amount'] = pd.to_numeric(mapped_df['Debit_Amount'], errors='coerce').fillna(0)
    mapped_df['Credit_Amount'] = pd.to_numeric(mapped_df['Credit_Amount'], errors='coerce').fillna(0)
    
    # 3. แสดงผลตารางที่คลีนแล้ว
    st.dataframe(mapped_df)
    
    # 4. คำนวณยอดรวม
    total_debit = mapped_df['Debit_Amount'].sum()
    total_credit = mapped_df['Credit_Amount'].sum()
    balance_diff = total_debit - total_credit
    
    # 5. แสดงผลลัพธ์แบบงบดุล (แบ่งคอลัมน์สวยงาม)
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
