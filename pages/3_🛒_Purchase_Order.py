import streamlit as st
import pandas as pd

st.title("🛒 Module: ข้อมูลใบสั่งซื้อค้างส่ง (Open Purchase Orders)")

# 1. ตรวจสอบว่ามีไฟล์ดิบจากหน้าหลักเข้ามาเก็บไว้ในระบบหรือยัง
if 'main_upload_file' in st.session_state and st.session_state['main_upload_file'] is not None:
    
    # 2. ถ้ามีไฟล์ดิบ และหน้านี้ยังไม่เคยดึง Sheet 2 ให้ทำการดึงและเก็บไว้ในคีย์ของตัวเองแยกต่างหาก
    if 'df_po_sheet2' not in st.session_state:
        try:
            # สั่งแกะเอาเฉพาะ Sheet ที่ 2 (index 1) มาเก็บไว้ใช้เฉพาะหน้านี้
            st.session_state['df_po_sheet2'] = pd.read_excel(st.session_state['main_upload_file'], sheet_name=1)
        except Exception as e:
            st.error(f"❌ ไม่สามารถดึงข้อมูล Sheet ที่ 2 ได้: {e}")
            st.info("💡 คำแนะนำ: ตรวจสอบว่าไฟล์ Excel ที่อัปโหลดมีอย่างน้อย 2 Sheet หรือไม่")

# 3. ส่วนการแสดงผล (ข้อมูลจะถูกดึงจากหน่วยความจำหน้านี้เอง สลับหน้าข้อมูลก็ไม่หาย)
if 'df_po_sheet2' in st.session_state:
    df = st.session_state['df_po_sheet2']
    
    st.subheader("📋 ข้อมูลดิบจาก Sheet ที่ 2 (ดึงอัตโนมัติจากไฟล์หน้าหลัก)")
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
else:
    st.warning("⚠️ ยังไม่มีข้อมูลในระบบ หรือระบบหาไฟล์จากหน้าหลักไม่เจอ กรุณาอัปโหลดไฟล์ที่หน้าหลัก (app.py) ก่อนเริ่มใช้งาน")
