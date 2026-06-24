import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="G/L Balances Module", page_icon="💰", layout="wide")
st.title("🧾 Module: สมุดบัญชีแยกประเภทและยอดหมุนเวียน (G/L Balances)")

# 🟢 บรรทัดที่ 7: ประกาศตัวแปรเริ่มต้นไว้ก่อนทันที เผื่อกรณีเซสชันยังไม่มีไฟล์ จะได้ไม่เกิด NameError ด้านล่าง
df = None

# 1. ดึงไฟล์ดิบจากคีย์ 'gl_upload_file' ที่ถูกบันทึกมาจากหน้าหลัก (app.py)
if 'gl_upload_file' in st.session_state and st.session_state['gl_upload_file'] is not None:
    file_gl_raw = st.session_state['gl_upload_file']
    
    # เช็คว่าเป็นไฟล์ Excel หรือไม่ เพื่อทำการดึงแผ่นงาน
    if hasattr(file_gl_raw, 'name') and file_gl_raw.name.endswith(('.xlsx', '.xls')):
        
        # 2. ถ้าหน้านี้ยังไม่เคยแกะข้อมูลแผ่นงาน ให้แกะอัตโนมัติรอบแรกก่อน
        if 'gl_sheets_dict' not in st.session_state:
            try:
                # รีเซ็ต pointer ของไฟล์ก่อนอ่าน
                file_gl_raw.seek(0)
                file_bytes = file_gl_raw.getvalue()
                selected_engine = 'openpyxl' if file_gl_raw.name.endswith('.xlsx') else 'xlrd'
                
                # อ่านทุก Sheet เก็บไว้เป็น Dictionary เพื่อความเร็วตอนเปลี่ยนหน้า
                st.session_state['gl_sheets_dict'] = pd.read_excel(
                    io.BytesIO(file_bytes), 
                    sheet_name=None, 
                    header=None, 
                    engine=selected_engine
                )
            except Exception as e:
                st.error(f"❌ ไม่สามารถดึงโครงสร้างแผ่นงานได้: {e}")

# 3. ส่วนการแสดงผลกรณีเป็น Excel และมีหลายแผ่นงาน
if 'gl_sheets_dict' in st.session_state:
    sheets_data = st.session_state['gl_sheets_dict']
    all_sheets = list(sheets_data.keys())
    
    st.markdown("---")
    st.markdown("### 🔍 ตรวจพบแผ่นงานในไฟล์ของคุณ")
    
    # ตั้งค่าเริ่มต้นให้ชี้ไปที่ Sheet ลำดับที่ 2 (index=1) เสมอตอนเปิดมาครั้งแรก
    if "gl_sheet_choice" in st.session_state and st.session_state["gl_sheet_choice"] in all_sheets:
        default_index = all_sheets.index(st.session_state["gl_sheet_choice"])
    else:
        default_index = 1 if len(all_sheets) > 1 else 0
        if len(all_sheets) > 1:
            st.session_state["gl_sheet_choice"] = all_sheets[1]

    # เมนูเลือก Sheet
    selected_sheet = st.selectbox(
        "กรุณาเลือกแผ่นงาน (Sheet) ที่ถูกต้องสำหรับหน้าสมุดบัญชีแยกประเภท:",
        options=all_sheets,
        index=default_index,
        key="gl_sheet_choice"
    )
    
    # กำหนดค่าให้ df จากแผ่นงานที่เลือก
    df = sheets_data[selected_sheet]
    st.success(f"📋 ดึงข้อมูลจากแผ่นงาน: **'{selected_sheet}'** สำเร็จ")

# 4. กรณีไฟล์ที่อัปโหลดมาเป็น .csv (ดึงข้อมูลตรงจาก df_gl ที่หน้าหลักส่งมาให้)
elif 'df_gl' in st.session_state:
    df = st.session_state['df_gl']
    st.info("ℹ️ ตรวจพบเป็นข้อมูลจากไฟล์เดี่ยว (.csv) ระบบดึงข้อมูลแผ่นงานหลักมาใช้งานโดยอัตโนมัติ")
else:
    st.warning("⚠️ ไม่พบข้อมูลในระบบ กรุณาอัปโหลดไฟล์ที่หน้าหลัก (app.py) ก่อนเริ่มใช้งาน")


# --- ส่วนการคำนวณและจัดสรรข้อมูล (ย้ายมาไว้ข้างล่างสุดหลังจากที่ได้ค่า df แน่นอนแล้ว) ---
if df is not None:
    st.subheader("📋 ข้อมูลดิบที่ระบบอ่านได้ในปัจจุบัน")
    st.dataframe(df, use_container_width=True)

    st.subheader("✨ ข้อมูลที่จัดสรรพร้อมนำเข้า ERP (Mapped Data)")
    
    # ข้าม 6 แถวแรกที่เป็นหัวรายงานภาษาไทย และรีเซ็ตอินเดกซ์ใหม่ให้เริ่มจาก 0
    clean_df = df.iloc[6:].reset_index(drop=True)
    
    # สร้าง DataFrame ใหม่เพื่อ mapping ตามโครงสร้างจริงจากรูปภาพ
    mapped_df = pd.DataFrame()
    
    mapped_df['วันที่ (Date)'] = clean_df.iloc[:, 0] if len(clean_df.columns) > 0 else "N/A"
    mapped_df['เลขที่เอกสาร (Doc No)'] = clean_df.iloc[:, 1] if len(clean_df.columns) > 1 else "N/A"
    mapped_df['ชื่อลูกค้า/คู่ค้า (Partner)'] = clean_df.iloc[:, 2] if len(clean_df.columns) > 2 else "N/A"
    mapped_df['เลขที่ PO (PO Number)'] = clean_df.iloc[:, 3] if len(clean_df.columns) > 3 else "N/A"
    mapped_df['ใบส่งสินค้า (Delivery No)'] = clean_df.iloc[:, 4] if len(clean_df.columns) > 4 else "N/A"
    mapped_df['รายละเอียดสินค้า (Description)'] = clean_df.iloc[:, 5] if len(clean_df.columns) > 5 else "N/A"
    mapped_df['จำนวน (Quantity)'] = clean_df.iloc[:, 6] if len(clean_df.columns) > 6 else 0
    mapped_df['หน่วย/ราคา (Unit/Price)'] = clean_df.iloc[:, 7] if len(clean_df.columns) > 7 else "N/A"
    
    # แปลงจำนวนเป็นตัวเลขเพื่อใช้คำนวณ Sum
    mapped_df['จำนวน (Quantity)'] = pd.to_numeric(mapped_df['จำนวน (Quantity)'], errors='coerce').fillna(0)
    
    # แสดงตารางผลลัพธ์
    st.dataframe(mapped_df, use_container_width=True)
    
    # คำนวณสรุปยอดรวมด้านล่างตาราง
    total_qty = mapped_df['จำนวน (Quantity)'].sum()
    total_records = len(mapped_df)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="📊 จำนวนรายการทั้งหมดที่พบ", value=f"{total_records:,} รายการ")
    with col2:
        st.metric(label="📦 ยอดรวมจำนวนสินค้าทั้งหมด (Total Qty)", value=f"{total_qty:,.2f}")
