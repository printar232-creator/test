import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Open Purchase Orders Module", page_icon="🛒", layout="wide")
st.title("🛒 Module: ข้อมูลใบสั่งซื้อค้างส่ง (Open Purchase Orders)")

# ประกาศตัวแปรเริ่มต้นด้านบนสุดเพื่อความปลอดภัย ป้องกัน NameError 100%
df = None

# 1. ตรวจสอบว่ามีไฟล์ดิบจากหน้าหลักเข้ามาเก็บไว้ในระบบหรือยัง
if 'main_upload_file' in st.session_state and st.session_state['main_upload_file'] is not None:
    file_po_raw = st.session_state['main_upload_file']
    
    if hasattr(file_po_raw, 'name') and file_po_raw.name.endswith(('.xlsx', '.xls')):
        # 2. แกะแผ่นงานทั้งหมดเก็บลงหน่วยความจำรอบแรก (ใช้คีย์ po_sheets_dict เฉพาะหน้านี้)
        if 'po_sheets_dict' not in st.session_state:
            try:
                file_po_raw.seek(0)
                file_bytes = file_po_raw.getvalue()
                selected_engine = 'openpyxl' if file_po_raw.name.endswith('.xlsx') else 'xlrd'
                
                st.session_state['po_sheets_dict'] = pd.read_excel(
                    io.BytesIO(file_bytes), 
                    sheet_name=None, 
                    header=None, 
                    engine=selected_engine
                )
            except Exception as e:
                st.error(f"❌ ไม่สามารถดึงโครงสร้างแผ่นงานได้: {e}")

# 3. ส่วนการตรวจสอบและแสดงผลแถบเลือกแผ่นงาน (Sheet Selector)
if 'po_sheets_dict' in st.session_state:
    sheets_data = st.session_state['po_sheets_dict']
    all_sheets = list(sheets_data.keys())
    
    st.markdown("---")
    st.markdown("### 🔍 ตรวจพบแผ่นงานในไฟล์ของคุณ")
    
    # ตั้งค่าเริ่มต้นชี้ไปที่ Sheet ลำดับที่ 2 (Index 1) เสมอตอนเปิดมาครั้งแรก
    if "po_sheet_choice" in st.session_state and st.session_state["po_sheet_choice"] in all_sheets:
        default_index = all_sheets.index(st.session_state["po_sheet_choice"])
    else:
        default_index = 1 if len(all_sheets) > 1 else 0
        if len(all_sheets) > 1:
            st.session_state["po_sheet_choice"] = all_sheets[1]

    # คอมโบกรองเลือกแผ่นงาน
    selected_sheet = st.selectbox(
        "กรุณาเลือกแผ่นงาน (Sheet) ที่ถูกต้องสำหรับหน้าข้อมูลใบสั่งซื้อค้างส่ง:",
        options=all_sheets,
        index=default_index,
        key="po_sheet_choice"
    )
    
    df = sheets_data[selected_sheet]
    st.success(f"📋 ดึงข้อมูลจากแผ่นงาน: **'{selected_sheet}'** สำเร็จ")

elif 'df_po' in st.session_state:
    df = st.session_state['df_po']
    st.info("ℹ️ ตรวจพบเป็นข้อมูลจากไฟล์เดี่ยว (.csv) ระบบดึงข้อมูลแผ่นงานหลักมาใช้งานโดยอัตโนมัติ")
else:
    st.warning("⚠️ ยังไม่มีข้อมูลในระบบ กรุณาอัปโหลดไฟล์ที่หน้าหลัก (app.py) ก่อนเริ่มใช้งาน")


# --- 4. ส่วนการคำนวณและดึงข้อมูลจากไฟล์ดิบจริงทั้งหมด ---
if df is not None:
    st.subheader("📋 ข้อมูลดิบที่ระบบอ่านได้ในปัจจุบัน")
    st.dataframe(df, use_container_width=True)

    st.subheader("✨ ข้อมูลที่จัดสรรพร้อมนำเข้า
