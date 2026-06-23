import streamlit as st
import pandas as pd

st.title("📦 Module: ข้อมูลสินค้าและวัตถุดิบ (Item Master)")

if 'df_item' in st.session_state and not st.session_state['df_item'].empty:
    # คัดลอกข้อมูลดิบมาใช้งาน
    raw_df = st.session_state['df_item'].copy()
    
    # เคลียร์แถวที่เป็นช่องว่างออกให้หมด
    cleaned_df = raw_df.dropna(how='all').reset_index(drop=True)
    
    # 📋 1. แสดงผลข้อมูลดิบทุกคอลัมน์ตามที่เก็บอยู่ใน Session State ปัจจุบัน
    st.subheader("📋 ข้อมูลดิบจากไฟล์ (ทุกคอลัมน์)")
    st.dataframe(cleaned_df, use_container_width=True)

    # ✨ 2. จัดสรรข้อมูลเข้าสู่โครงสร้าง ERP (Mapped Data)
    st.subheader("✨ ข้อมูลที่จัดสรรพร้อมนำเข้า ERP (Mapped Data)")
    
    mapped_df = pd.DataFrame()
    
    # ตรวจสอบจำนวนคอลัมน์เพื่อป้องกัน Error และดึงข้อมูลตามตำแหน่งจริงในรูปภาพ
    total_cols = len(cleaned_df.columns)
    
    # ดึงคอลัมน์รหัสสินค้า (จากช่อง Col_4 หรือตำแหน่ง Index 4)
    if total_cols > 4:
        mapped_df['Item_Code'] = cleaned_df.iloc[:, 4]
    else:
        mapped_df['Item_Code'] = "None"
        
    # ดึงคอลัมน์รายละเอียดสินค้า (จากช่อง Col_3 หรือตำแหน่ง Index 3)
    if total_cols > 3:
        mapped_df['Item_Description'] = cleaned_df.iloc[:, 3]
    else:
        mapped_df['Item_Description'] = "None"
        
    # ดึงคอลัมน์หน่วยนับ (จากช่อง Col_6 เช่น ใบ, ตัว หรือตำแหน่ง Index 6)
    if total_cols > 6:
        mapped_df['Base_UOM'] = cleaned_df.iloc[:, 6]
    else:
        mapped_df['Base_UOM'] = "Pcs"

    # ==========================================
    # 🧼 ล้างข้อมูลแถวหัวตารางเดิมที่อาจหลุดมา (เช่น คำว่า 'รหัส', 'รายการ' หรือค่าว่าง)
    # ==========================================
    # ลบแถวที่เนื้อหาเป็นหัวข้อตัวอักษรภาษาไทยออกไป ไม่ให้ปนกับรหัสสินค้าจริง
    mapped_df = mapped_df[~mapped_df['Item_Description'].astype(str).str.contains('รายการ|วันที่', na=False)]
    mapped_df = mapped_df[~mapped_df['Item_Code'].astype(str).str.contains('รหัส', na=False)]
    
    # แทนที่ค่าเครื่องหมายขีด '-' ด้วย 'N/A' หรือจะกรองทิ้งก็ได้ (ในภาพ ไม้พาเลท ไม่มีรหัส)
    # mapped_df['Item_Code'] = mapped_df['Item_Code'].replace('-', 'N/A')
    
    mapped_df = mapped_df.reset_index(drop=True)

    # แสดงผลตารางที่แมปเสร็จสมบูรณ์
    st.dataframe(mapped_df, use_container_width=True)
    st.success(f"✅ จัดสรรข้อมูลเสร็จสิ้น: ดึงข้อมูลสินค้ามาได้ทั้งหมด {len(mapped_df)} รายการ")
    
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
