import streamlit as st
import pandas as pd

st.title("📦 Module: ข้อมูลสินค้าและวัตถุดิบ (Item Master)")

if 'df_item' in st.session_state and not st.session_state['df_item'].empty:
    # คัดลอกข้อมูลดิบมาประมวลผล
    raw_df = st.session_state['df_item'].copy()
    
    # ==========================================
    # 🧼 STEP 1: จัดการเซ็ตหัวตารางภาษาไทยให้ถูกต้อง
    # ==========================================
    # ลบแถวที่เป็นช่องว่างทั้งหมดออกก่อน (พวก Row 0 ที่เป็น None)
    cleaned_df = raw_df.dropna(how='all').reset_index(drop=True)
    
    if len(cleaned_df) > 0:
        # ตรวจสอบว่า แถวแรกสุด มีคำว่า 'วันที่' หรือ 'รหัส' หรือไม่ 
        # ถ้าใช่ แสดงว่าแถวนี้คือ "หัวตารางภาษาไทย" ที่เราต้องการนำมาใช้เป็นคอลัมน์
        first_row = cleaned_df.iloc[0].astype(str).tolist()
        if any(kw in str(val) for kw in ['วันที่', 'ผู้ซื้อ', 'รหัส', 'รายการ'] for val in first_row):
            # ดึงข้อความในแถวแรกมาทำเป็นชื่อคอลัมน์ (Columns Name)
            new_columns = cleaned_df.iloc[0].tolist()
            
            # ป้องกันกรณีบางคอลัมน์เป็นค่าว่าง (None/NaN) ให้ตั้งชื่อแทนด้วย Index ตัวเลข
            new_columns = [str(col) if pd.notna(col) and str(col).strip() != "" else f"Col_{i}" for i, col in enumerate(new_columns)]
            
            cleaned_df.columns = new_columns
            # ตัดแถวแรกที่เป็นหัวตารางออกไป (เพราะเอาขึ้นไปเป็นชื่อคอลัมน์แล้ว)
            cleaned_df = cleaned_df.iloc[1:].reset_index(drop=True)

    # ==========================================
    # 📋 STEP 2: แสดงผลข้อมูลดิบทุกคอลัมน์ (หลังคลีนหัวตารางแล้ว)
    # ==========================================
    st.subheader("📋 ข้อมูลดิบจากไฟล์ (ทุกคอลัมน์)")
    st.dataframe(cleaned_df, use_container_width=True)

    # ==========================================
    # ✨ STEP 3: ข้อมูลที่จัดสรรพร้อมนำเข้า ERP (Mapped Data)
    # ==========================================
    st.subheader("✨ ข้อมูลที่จัดสรรพร้อมนำเข้า ERP (Mapped Data)")
    
    mapped_df = pd.DataFrame()
    
    # ดึงข้อมูลจากคอลัมน์ที่ตั้งชื่อใหม่แล้วอย่างปลอดภัย
    # โค้ดจะพยายามหาคำว่า 'รหัส' และ 'รายการ' จากชื่อคอลัมน์ภาษาไทยใหม่ทันที
    code_col = [c for c in cleaned_df.columns if 'รหัส' in c]
    desc_col = [c for c in cleaned_df.columns if 'รายการ' in c]
    uom_col = [c for c in cleaned_df.columns if 'หน่วย' in c] # ลองหาคอลัมน์หน่วยนับ (ใบ, ตัว) จากตารางดิบ
    
    # 🎯 แมปค่าเข้าสู่คอลัมน์ ERP
    mapped_df['Item_Code'] = cleaned_df[code_col[0]] if code_col else "N/A"
    mapped_df['Item_Description'] = cleaned_df[desc_col[0]] if desc_col else "N/A"
    
    # ถ้าในตารางดิบมีหน่วยนับ (เช่น ใบ, ตัว) ให้เอามาใช้แทน "Pcs" ได้เลยครับ
    mapped_df['Base_UOM'] = cleaned_df[uom_col[0]] if uom_col else "Pcs"

    # จัดการล้างแถวที่ข้อมูลหลักเป็นค่าว่างออกเพื่อความสะอาด
    mapped_df = mapped_df.dropna(subset=['Item_Code', 'Item_Description'], how='all')
    # ป้องกันค่าที่เป็นเครื่องหมายขีด '-' หรือคำว่างๆ หลุดไปเป็นรหัสสินค้า
    mapped_df = mapped_df[mapped_df['Item_Code'].astype(str).str.strip() != "-"]
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
