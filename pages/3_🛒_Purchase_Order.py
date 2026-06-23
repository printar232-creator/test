import streamlit as st
import pandas as pd

st.title("🛒 Module: ข้อมูลใบสั่งซื้อค้างส่ง (Open Purchase Orders) - ไฟล์ที่ 2")

# 🔄 เปลี่ยนมาดึงข้อมูลจากตัวแปรไฟล์ที่ 2 ('df_po_file2')
if 'df_po_file2' in st.session_state:
    df = st.session_state['df_po_file2']
    
    st.subheader("📋 ข้อมูลดิบที่ดึงมาจาก Session State (ไฟล์ที่ 2)")
    st.dataframe(df, use_container_width=True)

    st.subheader("✨ ข้อมูลที่จัดสรรพร้อมนำเข้า ERP (Mapped Data)")
    
    # ตรวจสอบจำนวนคอลัมน์ที่มีอยู่จริงเพื่อความปลอดภัย (Prevent Index Error)
    num_cols = len(df.columns)
    
    # สร้าง Mapped DataFrame จากไฟล์ที่ 2
    mapped_data = {
        'PO_Number': df.iloc[:, 0] if num_cols > 0 else pd.Series([None] * len(df)),
        'PO_Date': df.iloc[:, 1] if num_cols > 1 else pd.Series([None] * len(df)),
        'Vendor_Code': df.iloc[:, 2] if num_cols > 2 else pd.Series([None] * len(df)),
        'Quantity_Ordered': df.iloc[:, 3] if num_cols > 3 else pd.Series([0] * len(df))
    }
    
    mapped_df = pd.DataFrame(mapped_data)
    
    # แสดงผลตารางที่ทำการ Mapping ข้อมูลแล้ว
    st.dataframe(mapped_df, use_container_width=True)
    st.success("✅ จับคู่ข้อมูล Transaction PO จากไฟล์ที่ 2 สำเร็จ")
    
    # ปุ่มดาวน์โหลดไฟล์สำหรับนำไปใช้ต่อในระบบ ERP (รองรับภาษาไทยใน Excel)
    csv = mapped_df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 ดาวน์โหลดข้อมูลไฟล์ที่ 2 เพื่อนำเข้า ERP (CSV)",
        data=csv,
        file_name="ready_to_erp_po_file2.csv",
        mime="text/csv"
    )

else:
    # เตือนผู้ใช้ให้กลับไปอัปโหลดไฟล์ที่ 2 ก่อน
    st.warning("⚠️ ยังไม่มีข้อมูลไฟล์ที่ 2 ในระบบ กรุณากลับไปอัปโหลดไฟล์ที่ 2 ที่หน้าหลัก (app.py) ก่อนเริ่มใช้งาน")
