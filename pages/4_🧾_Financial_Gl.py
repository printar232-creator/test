# --- ส่วนการคำนวณและจัดสรรข้อมูลบัญชี (แก้ไขเพื่อดึงข้อมูลดิบจริงครบทุกคอลัมน์) ---
if df is not None:
    st.subheader("📋 ข้อมูลดิบที่ระบบอ่านได้ในปัจจุบัน")
    st.dataframe(df, use_container_width=True)

    st.subheader("✨ ข้อมูลที่จัดสรรพร้อมนำเข้า ERP (Mapped Data)")
    
    # ข้าม 6 แถวแรกที่เป็นหัวรายงานภาษาไทย และรีเซ็ตอินเด็กซ์ใหม่ให้เริ่มจาก 0
    clean_df = df.iloc[6:].reset_index(drop=True)
    
    # สร้าง DataFrame ใหม่เพื่อทำการ Map ข้อมูลตามโครงสร้างจริงในภาพ
    mapped_df = pd.DataFrame()
    
    # ดึงข้อมูลมาแสดงครบทุกคอลัมน์ตามโครงสร้างไฟล์จริง
    mapped_df['วันที่ (Date)'] = clean_df.iloc[:, 0] if len(clean_df.columns) > 0 else "N/A"
    mapped_df['เลขที่เอกสาร (Doc No)'] = clean_df.iloc[:, 1] if len(clean_df.columns) > 1 else "N/A"
    mapped_df['ชื่อลูกค้า/คู่ค้า (Partner)'] = clean_df.iloc[:, 2] if len(clean_df.columns) > 2 else "N/A"
    mapped_df['เลขที่ PO (PO Number)'] = clean_df.iloc[:, 3] if len(clean_df.columns) > 3 else "N/A"
    mapped_df['ใบส่งสินค้า (Delivery No)'] = clean_df.iloc[:, 4] if len(clean_df.columns) > 4 else "N/A"
    mapped_df['รายละเอียดสินค้า (Description)'] = clean_df.iloc[:, 5] if len(clean_df.columns) > 5 else "N/A"
    mapped_df['จำนวน (Quantity)'] = clean_df.iloc[:, 6] if len(clean_df.columns) > 6 else 0
    mapped_df['หน่วย/ราคา (Unit/Price)'] = clean_df.iloc[:, 7] if len(clean_df.columns) > 7 else "N/A"
    
    # แปลงคอลัมน์จำนวนให้เป็นตัวเลข เพื่อให้ระบบนำไปคำนวณผลรวม (Sum) ได้ถูกต้อง
    mapped_df['จำนวน (Quantity)'] = pd.to_numeric(mapped_df['จำนวน (Quantity)'], errors='coerce').fillna(0)
    
    # แสดงตารางผลลัพธ์การจัดสรรข้อมูลใหม่ทั้งหมด
    st.dataframe(mapped_df, use_container_width=True)
    
    # คำนวณสรุปยอดรวมของจำนวนสินค้า (Quantity) แทนผังบัญชีเดิม
    total_qty = mapped_df['จำนวน (Quantity)'].sum()
    total_records = len(mapped_df)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="📊 จำนวนรายการทั้งหมดที่พบ", value=f"{total_records:,} รายการ")
    with col2:
        st.metric(label="📦 ยอดรวมจำนวนสินค้าทั้งหมด (Total Qty)", value=f"{total_qty:,.2f}")
