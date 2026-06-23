import streamlit as st
import pandas as pd

st.title("📦 Module: ข้อมูลสินค้าและวัตถุดิบ (Item Master)")

if 'df_item' in st.session_state and not st.session_state['df_item'].empty:
    # คัดลอกข้อมูลดิบมาใช้งาน
    raw_df = st.session_state['df_item'].copy()
    
    # เคลียร์แถวที่เป็นช่องว่างทั้งหมดออก
    cleaned_df = raw_df.dropna(how='all').reset_index(drop=True)
    
    # 📋 1. แสดงผลข้อมูลดิบทุกคอลัมน์จาก Session State
    st.subheader("📋 ข้อมูลดิบจากไฟล์ (ทุกคอลัมน์)")
    st.dataframe(cleaned_df, use_container_width=True)

    # ✨ 2. จัดสรรข้อมูลเข้าสู่โครงสร้างที่ต้องการดึงมาทุกคอลัมน์
    st.subheader("✨ ข้อมูลที่จัดสรรพร้อมนำเข้า ERP (Mapped Data - ทุกคอลัมน์)")
    
    mapped_df = pd.DataFrame()
    total_cols = len(cleaned_df.columns)
    
    # ตรวจสอบโครงสร้างคอลัมน์และดึงมาแสดงผลให้ครบทุกช่องตามจริง
    if total_cols > 0: mapped_df['Date'] = cleaned_df.iloc[:, 0]              # วันที่
    #if total_cols > 1: mapped_df['Buyer'] = cleaned_df.iloc[:, 1]             # ผู้ซื้อ
    if total_cols > 2: mapped_df['Received_From'] = cleaned_df.iloc[:, 2]     # ได้รับจาก
    if total_cols > 3: mapped_df['Item_Description'] = cleaned_df.iloc[:, 3]  # รายการ
    #if total_cols > 4: mapped_df['Item_Code'] = cleaned_df.iloc[:, 4]         # รหัส
    if total_cols > 5: mapped_df['Quantity'] = cleaned_df.iloc[:, 5]          # จำนวน
    #if total_cols > 6: mapped_df['Base_UOM'] = cleaned_df.iloc[:, 6]          # หน่วย
    if total_cols > 7: mapped_df['Price_Per_Unit'] = cleaned_df.iloc[:, 7]    # ราคา/หน่วย
    if total_cols > 8: mapped_df['Amount'] = cleaned_df.iloc[:, 8]            # จำนวนเงิน
    if total_cols > 9: mapped_df['Total_Value'] = cleaned_df.iloc[:, 9]       # มูลค่ารวม
    if total_cols > 10: mapped_df['PO_Number'] = cleaned_df.iloc[:, 10]       # PO.
    if total_cols > 11: mapped_df['Remarks'] = cleaned_df.iloc[:, 11]         # หมายเหตุ

    # ==========================================
    # 🧼 ล้างข้อมูลแถวหัวตารางหรือแถวที่มีช่องว่าง (แก้ปัญหาช่องแรกขึ้น None)
    # ==========================================
    # 1. ลบแถวที่คอลัมน์สำคัญ (เช่น รายการ หรือ รหัส) มีค่าเป็นค่าว่าง (None/NaN) ออกไป
    mapped_df = mapped_df.dropna(subset=['Item_Description'], how='all')
    
    # 2. ป้องกันแถวที่เป็นข้อความหัวตารางเดิมหลุดติดมาในเนื้อข้อมูล
    mapped_df = mapped_df[~mapped_df['Item_Description'].astype(str).str.contains('รายการ|วันที่', na=False)]
    
    # รีเซ็ต index ของตารางใหม่หลังจากคลีนเรียบร้อย
    mapped_df = mapped_df.reset_index(drop=True)

    # แสดงผลตารางที่จัดสรรเสร็จสมบูรณ์ (ดึงมาครบทุกคอลัมน์ ไม่มีแถว None)
    st.dataframe(mapped_df, use_container_width=True)
    st.success(f"✅ จัดสรรข้อมูลเสร็จสิ้น: ดึงข้อมูลมาครบทุกคอลัมน์รวมทั้งหมด {len(mapped_df)} รายการ")
    
    # ปุ่มดาวน์โหลดไฟล์สำหรับนำไปใช้งานต่อ
    csv = mapped_df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 ดาวน์โหลดไฟล์สำหรับ ERP (.csv)",
        data=csv,
        file_name="ERP_Full_Item_Master.csv",
        mime="text/csv"
    )

else:
    st.warning("⚠️ ยังไม่มีข้อมูลในระบบ กรุณากลับไปอัปโหลดไฟล์ที่หน้าหลัก (app.py) ก่อนเริ่มใช้งาน")
