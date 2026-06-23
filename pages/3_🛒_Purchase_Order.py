import streamlit as st
import pandas as pd

st.title("🛒 Module: ข้อมูลใบสั่งซื้อค้างส่ง (Open Purchase Orders)")

# ตรวจสอบว่ามีไฟล์อัปโหลดเก็บไว้ใน session หรือมีข้อมูลเดิมอยู่หรือไม่
# (โค้ดนี้จะรองรับทั้งกรณีที่เก็บไฟล์ดิบ หรือต้องการอ่านใหม่ในหน้านี้โดยตรง)
if 'uploaded_file' in st.session_state or 'df_po' in st.session_state:
    
    # ดึง Dataframe มาแสดงผล
    try:
        # หากใน app.py มีการเก็บไฟล์อัปโหลดดิบไว้ (เช่น st.session_state['uploaded_file'] = uploaded_file)
        if 'uploaded_file' in st.session_state and st.session_state['uploaded_file'] is not None:
            # ทำการอ่าน Sheet ที่ 2 (index คือ 1) ตรงนี้เลย ไม่กระทบหน้าอื่นแน่นอน
            df = pd.read_excel(st.session_state['uploaded_file'], sheet_name=1)
        else:
            # Fallback หากไม่มีไฟล์ดิบ แต่มี df_po เดิม
            df = st.session_state['df_po']
            
        st.subheader("📋 ข้อมูลดิบจาก Sheet ที่ 2 (ดึงเฉพาะโมดูลนี้)")
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
    st.warning("⚠️ ยังไม่มีข้อมูลในระบบ กรุณากลับไปอัปโหลดไฟล์ที่หน้าหลัก (app.py) ก่อนเริ่มใช้งาน")
