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

    # ✨ 2. จัดสรรข้อมูลเข้าสู่โครงสร้างที่นำคอลัมน์ 1, 4, 6, 10 ออกแล้ว
    st.subheader("✨ ข้อมูลที่จัดสรรพร้อมนำเข้า ERP (Mapped Data - ปรับปรุงคอลัมน์)")
    
    mapped_df = pd.DataFrame()
    total_cols = len(cleaned_df.columns)
    
    # ดึงคอลัมน์เฉพาะที่เหลืออยู่ (เอา 0, 2, 3, 5, 7, 8, 10, 11 ตามลำดับ index จริง)
    # Note: คอลัมน์ที่ถูกถอดออกตามลำดับที่คุณแจ้งคือ index: 1 (Buyer), 4 (Item_Code), 6 (Base_UOM), 9 (Total_Value)
    if total_cols > 1: mapped_df['Buyer'] = cleaned_df.iloc[:, 1]             # ผู้ซื้อ
    if total_cols > 2: mapped_df['Received_From'] = cleaned_df.iloc[:, 2]     # ได้รับจาก
    if total_cols > 5: mapped_df['Quantity'] = cleaned_df.iloc[:, 5]          # จำนวน
    if total_cols > 7: mapped_df['Price_Per_Unit'] = cleaned_df.iloc[:, 7]    # ราคา/หน่วย
    if total_cols > 8: mapped_df['Amount'] = cleaned_df.iloc[:, 8]            # จำนวนเงิน
    if total_cols > 10: mapped_df['PO_Number'] = cleaned_df.iloc[:, 10]       # PO.
    if total_cols > 11: mapped_df['Remarks'] = cleaned_df.iloc[:, 11]         # หมายเหตุ

    # ==========================================
    # 🧼 ล้างข้อมูลแถวหัวตารางและแถว None ด้านบนสุดออก
    # ==========================================
    # ใช้คอลัมน์แรกที่มีใน mapped_df (เช่น Buyer) ในการเช็คเพื่อตัดแถวที่เป็นค่าว่าง (None) ออก
    if not mapped_df.empty:
        first_valid_col = mapped_df.columns[0]
        mapped_df = mapped_df.dropna(subset=[first_valid_col], how='all')
        
        # ป้องกันคำที่เป็นหัวข้อตารางเดิมหลุดรอดมาเป็นเนื้อข้อมูล
        mapped_df = mapped_df[~mapped_df[first_valid_col].astype(str).str.contains('ผู้ซื้อ|วันที่|รายการ', na=False)]
        
    # รีเซ็ต Index ของตารางใหม่ให้เริ่มต้นที่ 0 อย่างสวยงาม
    mapped_df = mapped_df.reset_index(drop=True)

    # แสดงผลตารางที่ปรับแต่งคอลัมน์แล้ว
    st.dataframe(mapped_df, use_container_width=True)
    st.success(f"✅ จัดสรรข้อมูลเสร็จสิ้น: ปรับปรุงคอลัมน์และดึงข้อมูลมาได้ทั้งหมด {len(mapped_df)} รายการ")
    
    # ปุ่มดาวน์โหลดไฟล์สำหรับนำไปใช้งานต่อ
    csv = mapped_df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 ดาวน์โหลดไฟล์สำหรับ ERP (.csv)",
        data=csv,
        file_name="ERP_Custom_Mapped_Data.csv",
        mime="text/csv"
    )

else:
    st.warning("⚠️ ยังไม่มีข้อมูลในระบบ กรุณากลับไปอัปโหลดไฟล์ที่หน้าหลัก (app.py) ก่อนเริ่มใช้งาน")
