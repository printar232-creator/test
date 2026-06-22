import streamlit as st

st.set_page_config(page_title="ERP Data Preprocessing Hub", page_icon="⚙️", layout="wide")

st.title("⚙️ ระบบจัดสรรและตรวจสอบข้อมูลก่อนนำเข้า ERP")
st.markdown("---")

st.write("""
### ยินดีต้อนรับสู่ระบบเตรียมข้อมูล ERP (Data Cleansing & Mapping Tool)
กรุณาเลือกเมนูด้านข้างเพื่ออัปโหลดและตรวจสอบข้อมูลในแต่ละโมดูล (Module) โดยระบบจะทำการ Mapping ข้อมูลให้พร้อมใช้งานก่อนนำเข้าสู่ระบบ ERP จริง

#### 📥 ขั้นตอนการทำงาน:
1. เลือกหน้าโมดูลที่ต้องการจาก Sidebar ด้านซ้าย
2. อัปโหลดไฟล์ข้อมูล (`.csv` หรือ `.xlsx`) ที่ได้จากระบบเก่าหรือแบบฟอร์มดิบ
3. ระบบจะแปลงหัวตาราง (Schema Mapping) และตรวจสอบความถูกต้อง (Data Validation) ให้ทันที
""")
