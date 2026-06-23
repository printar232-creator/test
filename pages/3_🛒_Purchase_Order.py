import streamlit as st
import pandas as pd

st.title("🛒 Module: ข้อมูลใบสั่งซื้อค้างส่ง (Open Purchase Orders)")

# 1. ตรวจสอบว่ามีไฟล์ดิบจากหน้าหลักเข้ามาเก็บไว้ในระบบหรือยัง
if 'main_upload_file' in st.session_state and st.session_state['main_upload_file'] is not None:
    
    # 2. ถ้ามีไฟล์ดิบ และหน้านี้ยังไม่เคยดึง Sheet 2 ให้ทำการดึงและเก็บไว้แยกต่างหาก
    if 'df_po_sheet2' not in st.session_state:
        try:
            # สั่งแกะเอาเฉพาะ Sheet ที่ 2 (index 1) มาเก็บไว้ใช้เฉพาะหน้านี้
            st.session_state['df_po_sheet2'] = pd.read_excel(st.session_state['main_upload_file'], sheet_name=1, header=None)
        except Exception as e:
            st.error(f"❌ ไม่สามารถดึงข้อมูล Sheet ที่ 2 ได้: {e}")
            st.info("💡 คำแนะนำ: ตรวจสอบว่าไฟล์ Excel ที่อัปโหลดมีอย่างน้อย 2 Sheet หรือไม่")

# 3. ส่วนการแสดงผล (ข้อมูลดึงจากความจำเฉพาะหน้านี้ สลับหน้าแล้วไม่หาย)
if 'df_po_sheet2' in st.session_state:
    df = st.session_state['df_po_sheet2']
    
    st.subheader("📋 ข้อมูลดิบจาก Sheet ที่ 2 (ดึงอัตโนมัติจากไฟล์หน้าหลัก)")
    st.dataframe(df)

    st.subheader("✨ ข้อมูลที่จัดสรรพร้อมนำเข้า ERP (Mapped Data - ทุกคอลัมน์)")
    
    if df.empty:
        st.warning("⚠️ พบข้อมูลในระบบ แต่ไม่มีรายการข้อมูลใน Sheet นี้ (0 แถว)")
    else:
        # 🟢 ส่วนที่แก้ไข: วนลูปดึงข้อมูลมาทุกคอลัมน์ตามไฟล์จริง
        mapped_data = {}
        for col_idx in range(df.shape[1]):
            # ตั้งชื่อคอลัมน์ชั่วคราวเป็น Column_0, Column_1, ... ให้เหมือนกับโครงสร้างข้อมูลดิบ
            mapped_data[f'Column_{col_idx}'] = df.iloc[:, col_idx]
            
        mapped_df = pd.DataFrame(mapped_data)
        
        st.dataframe(mapped_df)
        st.success(f"จับคู่ข้อมูล Transaction PO จาก Sheet ที่ 2 สำเร็จทั้งหมด {df.shape[1]} คอลัมน์ (รวม {len(df)} รายการ)")
else:
    st.warning("⚠️ ยังไม่มีข้อมูลในระบบ หรือระบบหาไฟล์จากหน้าหลักไม่เจอ กรุณาอัปโหลดไฟล์ที่หน้าหลัก (app.py) ก่อนเริ่มใช้งาน")
