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
    df_raw = st.session_state['df_po_sheet2']
    
    if df_raw.empty:
        st.warning("⚠️ พบข้อมูลในระบบ แต่ไม่มีรายการข้อมูลใน Sheet นี้ (0 แถว)")
    else:
        # --- 🟢 ส่วนที่แก้ไข: ดันแถวแรกขึ้นเป็นหัวข้อคอลัมน์ (Header Replacement) ---
        # นำค่าในแถวแรก (index 0) มาแปลงเป็นลิสต์ชื่อคอลัมน์
        new_header = df_raw.iloc[0].astype(str).tolist()
        
        # ตัดแถวแรกทิ้ง (เหลือตั้งแต่แถว index 1 เป็นต้นไป) แล้วตั้งชื่อคอลัมน์ใหม่
        df_cleaned = df_raw.iloc[1:].copy()
        df_cleaned.columns = new_header
        
        # รีเซ็ต index ของแถวใหม่ให้เริ่มจาก 0 จะได้ดูง่ายๆ
        df_cleaned.reset_index(drop=True, inplace=self_or_df=df_cleaned)
        
        st.subheader("📋 ข้อมูลดิบจาก Sheet ที่ 2 (ดึงอัตโนมัติจากไฟล์หน้าหลัก)")
        st.dataframe(df_cleaned)

        st.subheader("✨ ข้อมูลที่จัดสรรพร้อมนำเข้า ERP (Mapped Data)")
        
        # แสดงผลตารางเดียวกันที่จัดเรียงความสวยงามเรียบร้อยแล้ว
        st.dataframe(df_cleaned)
        st.success(f"จัดรูปแบบหัวคอลัมน์สำเร็จ! พบข้อมูลทั้งหมด {len(df_cleaned)} รายการ")
else:
    st.warning("⚠️ ยังไม่มีข้อมูลในระบบ หรือระบบหาไฟล์จากหน้าหลักไม่เจอ กรุณาอัปโหลดไฟล์ที่หน้าหลัก (app.py) ก่อนเริ่มใช้งาน")
