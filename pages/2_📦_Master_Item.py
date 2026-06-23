import streamlit as st
import pandas as pd

st.title("📦 Module: ข้อมูลสินค้าและวัตถุดิบ (Item Master)")

if 'df_item' in st.session_state and not st.session_state['df_item'].empty:
    # 1. คัดลอกข้อมูลมาประมวลผล
    raw_df = st.session_state['df_item'].copy()
    
    st.subheader("📋 ข้อมูลดิบที่ดึงมาจาก Session State")
    st.dataframe(raw_df, use_container_width=True)

    # 2. ล้างช่องว่างและแถวขยะ (ลบแถวที่เป็นช่องว่างทั้งหมดออกก่อน)
    cleaned_df = raw_df.dropna(how='all').reset_index(drop=True)
    
    # 3. ตรวจสอบและตัดแถวที่เป็นหัวตารางภาษาไทยออก (ถ้าแถวแรกมีคำว่า 'รหัส' หรือ 'รายการ')
    if len(cleaned_df) > 0:
        first_row_str = cleaned_df.iloc[0].astype(str).tolist()
        if any('รหัส' in str(val) or 'รายการ' in str(val) for val in first_row_str):
            cleaned_df = cleaned_df.iloc[1:].reset_index(drop=True)

    st.subheader("✨ ข้อมูลที่จัดสรรพร้อมนำเข้า ERP (Mapped Data)")
    
    # สร้าง DataFrame สำหรับ ERP
    mapped_df = pd.DataFrame()
    
    # ดึงข้อมูลตามโครงสร้างคอลัมน์จริงจากภาพแรก (รหัสอยู่คอลัมน์ที่ 5, รายการอยู่คอลัมน์ที่ 4)
    # ใช้ `.iloc` บนตารางที่คลีนแล้ว จะปลอดภัยและไม่หลุดตำแหน่ง
    if len(cleaned_df.columns) > 4:
        mapped_df['Item_Code'] = cleaned_df.iloc[:, 4]        # คอลัมน์ "รหัส"
    else:
        mapped_df['Item_Code'] = "N/A"
        
    if len(cleaned_df.columns) > 3:
        mapped_df['Item_Description'] = cleaned_df.iloc[:, 3] # คอลัมน์ "รายการ"
    else:
        mapped_df['Item_Description'] = "N/A"
        
    mapped_df['Base_UOM'] = "Pcs"                             # หน่วยนับเริ่มต้น

    # เคลียร์ค่าว่างที่อาจหลงเหลือในตารางใหม่
    mapped_df = mapped_df.dropna(subset=['Item_Code', 'Item_Description'], how='all')
    mapped_df = mapped_df.reset_index(drop=True)

    # แสดงผลตารางที่แมปข้อมูลแล้ว
    st.dataframe(mapped_df, use_container_width=True)
    st.success(f"✅ จัดสรรข้อมูลเสร็จสิ้น: พบสินค้าทั้งหมด {len(mapped_df)} รายการ")
    
    # ปุ่มดาวน์โหลดไฟล์สำหรับนำไปใช้งานต่อ
    csv = mapped_df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 ดาวน์โหลดไฟล์สำหรับ ERP (.csv)",
        data=csv,
        file_name="ERP_Item_Master.csv",
        mime="text/csv"
    )

else:
    st.warning("⚠️ ยังไม่มีข้อมูลในระบบ กรุณากลับไปอัปโหลดไฟล์ที่หน้าหลัก (app.py) ก่อนเริ่มใช้งาน")
