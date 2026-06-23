import streamlit as st
import pandas as pd

st.title("🛒 Module: ข้อมูลใบสั่งซื้อค้างส่ง (Open Purchase Orders)")

# --- ตรวจสอบโครงสร้างไฟล์หลัก เพื่อหาไฟล์ดิบที่อัปโหลดมาจาก app.py ---
# โดยปกติ Streamlit จะเก็บไฟล์อัปโหลดไว้ใน Session State อัตโนมัติ (มักจะใช้คีย์ตามชื่อตัวแปรหรือคีย์ที่ตั้งไว้)
# โค้ดนี้จะค้นหาไฟล์ดิบที่ถูกส่งมาจากหน้าแรกให้เองครับ

found_file = None

# ค้นหาไฟล์ Excel ใน session_state ที่อัปโหลดมาจากหน้าแรก
for key, value in st.session_state.items():
    # ตรวจสอบว่าเป็นวัตถุไฟล์ที่อัปโหลดมาหรือไม่ (มักจะมีแอตทริบิวต์ name และหมวดหมู่ของไฟล์)
    if hasattr(value, 'name') and any(value.name.endswith(ext) for ext in ['.xlsx', '.xls']):
        found_file = value
        break

# ถ้าระบบเจอไฟล์ดิบจากหน้าแรก และยังไม่เคยโหลด Sheet 2 มาเก็บไว้ในหน้านี้
if found_file is not None and 'df_po_sheet2' not in st.session_state:
    try:
        # แอบอ่าน Sheet 2 (index 1) จากไฟล์ดิบนั้นตรงนี้เลย ไม่กระทบหน้าอื่นแน่นอน
        st.session_state['df_po_sheet2'] = pd.read_excel(found_file, sheet_name=1)
    except Exception as e:
        st.error(f"❌ ไม่สามารถดึงข้อมูล Sheet ที่ 2 จากไฟล์ที่อัปโหลดได้: {e}")

# --- ส่วนการแสดงผล (ดึงข้อมูลจากความจำประจำเป็นของหน้านี้เอง ข้อมูลจึงไม่หายเมื่อเปลี่ยนหน้า) ---
if 'df_po_sheet2' in st.session_state:
    df = st.session_state['df_po_sheet2']
    
    st.subheader("📋 ข้อมูลดิบจาก Sheet ที่ 2 (ดึงอัตโนมัติจากไฟล์หน้าหลัก)")
    st.dataframe(df)

    st.subheader("✨ ข้อมูลที่จัดสรรพร้อมนำเข้า ERP (Mapped Data)")
    
    if df.empty:
        st.warning("⚠️ พบข้อมูลในระบบ แต่ไม่มีรายการข้อมูลใน Sheet นี้ (0 แถว)")
    else:
        num_rows = len(df)
        
        # จัดสรรข้อมูลตามลำดับคอลัมน์จาก Sheet ที่ 2
        mapped_data = {
            'PO_Number': df.iloc[:, 0] if df.shape[1] > 0 else ["N/A"] * num_rows,
            'PO_Date': df.iloc[:, 1] if df.shape[1] > 1 else ["N/A"] * num_rows,
            'Vendor_Code': df.iloc[:, 2] if df.shape[1] > 2 else ["N/A"] * num_rows,
            'Quantity_Ordered': df.iloc[:, 3] if df.shape[1] > 3 else [0] * num_rows
        }
        
        mapped_df = pd.DataFrame(mapped_data)
        
        st.dataframe(mapped_df)
        st.success(f"จับคู่ข้อมูล Transaction PO จาก Sheet ที่ 2 สำเร็จ ทั้งหมด {num_rows} รายการ")
else:
    st.warning("⚠️ ยังไม่มีข้อมูลในระบบ หรือระบบหาไฟล์จากหน้าหลักไม่เจอ กรุณาอัปโหลดไฟล์ที่หน้าหลัก (app.py) ก่อนเริ่มใช้งาน")
