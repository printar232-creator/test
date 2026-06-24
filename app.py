import streamlit as st
import pandas as pd

st.set_page_config(page_title="ERP Data Hub", page_icon="⚙️", layout="wide")

st.title("⚙️ ศูนย์กลางการอัปโหลดและจัดสรรข้อมูล ERP")
st.markdown("---")

st.write("### 📥 ขั้นตอน: อัปโหลดไฟล์ทั้ง 4 ให้ครบ จากนั้นเลือกดูข้อมูลในแต่ละโมดูลที่แถบด้านซ้าย")

# ฟังก์ชันกลางสำหรับอ่านไฟล์รองรับ xlsx, xls, csv
def load_data(file):
    if file.name.endswith('.xlsx'):
        return pd.read_excel(file, engine='openpyxl', header=None) # เพิ่ม header=None
    elif file.name.endswith('.xls'):
        return pd.read_excel(file, engine='xlrd', header=None)     # เพิ่ม header=None
    else:
        return pd.read_csv(file, header=None)                      # เพิ่ม header=None

# สร้าง Layout กล่องอัปโหลดแบบ 2x2 เพื่อความสวยงาม
col1, col2 = st.columns(2)

with col1:
    # 1. Vendor File
    file_vendor = st.file_uploader("1. อัปโหลดไฟล์ Vendor Master (.csv, .xlsx, .xls)", type=['csv', 'xlsx', 'xls'], key="upload_v")
    if file_vendor:
        st.session_state['df_vendor'] = load_data(file_vendor)
        # 🟢 ส่วนที่เพิ่ม: แอบเก็บไฟล์ดิบไว้เพื่อส่งข้ามหน้าไปให้ Module VM แกะ Sheet 2
        st.session_state['VM_upload_file'] = file_vendor
        st.success("✅ บันทึกข้อมูล Vendor แล้ว")

    # 2. Item File
    file_item = st.file_uploader("2. อัปโหลดไฟล์ Item Master (.csv, .xlsx, .xls)", type=['csv', 'xlsx', 'xls'], key="upload_i")
    if file_item:
        st.session_state['df_item'] = load_data(file_item)
        # 🟢 ส่วนที่เพิ่ม: แอบเก็บไฟล์ดิบไว้เพื่อส่งข้ามหน้าไปให้ Module IM แกะ Sheet 2
        st.session_state['IM_upload_file'] = file_item
        st.success("✅ บันทึกข้อมูล Item แล้ว")

with col2:
    # 3. Purchase Order File
    file_po = st.file_uploader("3. อัปโหลดไฟล์ Open PO (.csv, .xlsx, .xls)", type=['csv', 'xlsx', 'xls'], key="upload_p")
    if file_po:
        st.session_state['df_po'] = load_data(file_po)
        # 🟢 ส่วนที่เพิ่ม: แอบเก็บไฟล์ดิบไว้เพื่อส่งข้ามหน้าไปให้ Module PO แกะ Sheet 2
        st.session_state['main_upload_file'] = file_po
        st.success("✅ บันทึกข้อมูล Purchase Order แล้ว")

    # 4. Financial GL File
    file_gl = st.file_uploader("4. อัปโหลดไฟล์ G/L Balances (.csv, .xlsx, .xls)", type=['csv', 'xlsx', 'xls'], key="upload_g")
    if file_gl:
        st.session_state['df_gl'] = load_data(file_gl)
        # 🟢 ส่วนที่เพิ่ม: แอบเก็บไฟล์ดิบไว้เพื่อส่งข้ามหน้าไปให้ Module GL แกะ Sheet 2
        st.session_state['gl_upload_file'] = file_gl
        st.success("✅ บันทึกข้อมูล Financial G/L แล้ว")

st.markdown("---")
st.info("💡 เมื่ออัปโหลดไฟล์เรียบร้อยแล้ว ข้อมูลจะถูกล็อกไว้ในระบบ คุณสามารถคลิกเมนูใน Sidebar ด้านซ้ายเพื่อเข้าไปดูการ Mapping ข้อมูลของแต่ละหน้าได้เลย โดยข้อมูลจะไม่หายไปไหน")
