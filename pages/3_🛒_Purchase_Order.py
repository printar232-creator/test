import streamlit as st
import pandas as pd

st.title("🛒 Module: ข้อมูลใบสั่งซื้อค้างส่ง (Open Purchase Orders)")

# เพิ่มกล่องอัปโหลดไฟล์เฉพาะของหน้านี้ เพื่อดึง Sheet 2 โดยตรง ไม่กระทบหน้าอื่น
uploaded_file_po = st.file_uploader(
    "📂 อัปโหลดไฟล์ Excel (ระบบจะดึงข้อมูลจาก Sheet ที่ 2 ให้โดยอัตโนมัติ)", 
    type=["xlsx", "xls"],
    key="po_sheet2_uploader"
)

# ตรวจสอบว่ามีการอัปโหลดไฟล์ในหน้านี้หรือไม่
if uploaded_file_po is not None:
    try:
        # สั่งอ่าน Sheet ที่ 2 (index คือ 1) จากไฟล์ที่อัปโหลดตรงหน้านี้เลย
        df = pd.read_excel(uploaded_file_po, sheet_name=1)
        
        st.subheader("📋 ข้อมูลดิบจาก Sheet ที่ 2")
        st.dataframe(df)

        st.subheader("✨ ข้อมูลที่จัดสรรพร้อมนำเข้า ERP (Mapped Data)")
        
        if df.empty:
            st.warning("⚠️ พบข้อมูลในระบบ แต่ไม่มีรายการข้อมูลใน Sheet นี้ (0 แถว)")
        else:
            num_rows = len(df)
            
            # จัดสรรข้อมูลตามลำดับคอลัมน์จาก Sheet ที่ 2
            mapped_data = {
                'PO_Number': df.iloc[:, 0] if df.shape[1] > 0 else ["N/A"] * num_rows,
                'PO_Date': df.iloc[:, 1] if df.shape[1] > 1 else ["N/A"] * num_rows,
                'Vendor_Code': df.iloc[:, 2] if df.shape[1] > 2 else ["N/A"] * num_rows,
                'Quantity_Ordered': df.iloc[:, 3] if df.shape[1] > 3 else [0] * num_rows
            }
            
            mapped_df = pd.DataFrame(mapped_data)
            
            st.dataframe(mapped_df)
            st.success(f"จับคู่ข้อมูล Transaction PO จาก Sheet ที่ 2 สำเร็จ ทั้งหมด {num_rows} รายการ")
            
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการอ่าน Sheet ที่ 2: {e}")
        st.info("💡 คำแนะนำ: ตรวจสอบให้แน่ใจว่าไฟล์ Excel ที่อัปโหลดมีอย่างน้อย 2 Sheet")
else:
    st.info("💡 กรุณาอัปโหลดไฟล์ Excel ชุดเดียวกับหน้าหลักที่นี่อีกครั้ง เพื่อให้ระบบดึงข้อมูลจาก Sheet ที่ 2 แยกเฉพาะโมดูลนี้")
