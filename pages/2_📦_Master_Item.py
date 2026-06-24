import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Item Master Module", page_icon="📦", layout="wide")
st.title("📦 Module: ข้อมูลสินค้าและวัตถุดิบ (Item Master)")

df = None

# 1. ตรวจสอบว่ามีไฟล์ดิบจากหน้าหลักเข้ามาเก็บไว้ในระบบหรือยัง
if 'main_upload_file' in st.session_state and st.session_state['main_upload_file'] is not None:
    file_item_raw = st.session_state['main_upload_file']
    if hasattr(file_item_raw, 'name') and file_item_raw.name.endswith(('.xlsx', '.xls')):
        # ใช้คีย์แยกเฉพาะของหน้า item ป้องกันสเตทตีกัน
        if 'item_sheets_dict' not in st.session_state:
            try:
                file_item_raw.seek(0)
                file_bytes = file_item_raw.getvalue()
                selected_engine = 'openpyxl' if file_item_raw.name.endswith('.xlsx') else 'xlrd'
                st.session_state['item_sheets_dict'] = pd.read_excel(
                    io.BytesIO(file_bytes),
                    sheet_name=None,
                    header=None,
                    engine=selected_engine
                )
            except Exception as e:
                st.error(f"❌ ไม่สามารถดึงโครงสร้างแผ่นงานได้: {e}")

# 2. ส่วนการตรวจสอบและแสดงผลแถบเลือกแผ่นงาน (Sheet Selector)
if 'item_sheets_dict' in st.session_state:
    sheets_data = st.session_state['item_sheets_dict']
    all_sheets = list(sheets_data.keys())
    st.markdown("---")
    st.markdown("### 🔍 ตรวจพบแผ่นงานในไฟล์ของคุณ")
    
    if "item_sheet_choice" in st.session_state and st.session_state["item_sheet_choice"] in all_sheets:
        default_index = all_sheets.index(st.session_state["item_sheet_choice"])
    else:
        default_index = 0  # หน้า Item Master ตั้งต้นที่ Sheet แรกสุด
        if len(all_sheets) > 0:
            st.session_state["item_sheet_choice"] = all_sheets[0]
            
    selected_sheet = st.selectbox(
        "กรุณาเลือกแผ่นงาน (Sheet) ที่ถูกต้องสำหรับหน้าข้อมูลสินค้าและวัตถุดิบ:",
        options=all_sheets,
        index=default_index,
        key="item_sheet_choice"
    )
    df = sheets_data[selected_sheet]
    st.success(f"📋 ดึงข้อมูลจากแผ่นงาน: **'{selected_sheet}'** สำเร็จ")
elif 'df_item' in st.session_state:
    df = st.session_state['df_item']
    st.info("ℹ️ ตรวจพบเป็นข้อมูลจากไฟล์เดี่ยว (.csv) ระบบดึงข้อมูลแผ่นงานหลักมาใช้งานโดยอัตโนมัติ")
else:
    st.warning("⚠️ ยังไม่มีข้อมูลในระบบ กรุณากลับไปอัปโหลดไฟล์ที่หน้าหลัก (app.py) ก่อนเริ่มใช้งาน")

# 3. ส่วนการคำนวณและดึงข้อมูลมา Mapping คอลัมน์
if df is not None:
    cleaned_df = df.dropna(how='all').reset_index(drop=True)
    
    st.subheader("📋 ข้อมูลดิบจากไฟล์ (ทุกคอลัมน์)")
    st.dataframe(cleaned_df, use_container_width=True)

    st.subheader("✨ ข้อมูลที่จัดสรรพร้อมนำเข้า ERP (Mapped Data - ทุกคอลัมน์)")
    
    if cleaned_df.empty:
        st.warning("⚠️ พบข้อมูลในระบบ แต่ไม่มีรายการข้อมูลในแผ่นงานนี้ (0 แถว)")
    else:
        # ใช้ Vectorized หาจุดตัดแถวหัวตารางอัตโนมัติ ป้องกัน Text ผิดพลาด
        keywords = ['รายการ', 'วันที่', 'Date', 'Received', 'Item']
        mask = cleaned_df.astype(str).apply(lambda row: row.str.contains('|'.join(keywords)).any(), axis=1)
        start_row = mask.idxmax() if mask.any() else 0
        
        # ตัดข้อมูลตั้งแต่แถวที่เจอหัวตารางเป็นต้นไป
        working_df = cleaned_df.iloc[start_row:].reset_index(drop=True)
        
        mapped_df = pd.DataFrame()
        total_cols = len(working_df.columns)
        
        # จับคู่คอลัมน์ตามโครงสร้างเดิมของคุณอย่างแม่นยำ (อิงตาม Index)
        if total_cols > 0: mapped_df['Date'] = working_df.iloc[:, 0]
        if total_cols > 2: mapped_df['Received_From'] = working_df.iloc[:, 2]
        if total_cols > 3: mapped_df['Item_Description'] = working_df.iloc[:, 3]
        if total_cols > 5: mapped_df['Quantity'] = working_df.iloc[:, 5]
        if total_cols > 7: mapped_df['Price_Per_Unit'] = working_df.iloc[:, 7]
        if total_cols > 8: mapped_df['Amount'] = working_df.iloc[:, 8]
        if total_cols > 9: mapped_df['Total_Value'] = working_df.iloc[:, 9]
        if total_cols > 10: mapped_df['PO_Number'] = working_df.iloc[:, 10]
        if total_cols > 11: mapped_df['Remarks'] = working_df.iloc[:, 11]

        # 🧼 ล้างข้อมูลแถวหัวตารางหรือแถวที่มีช่องว่าง (ตรรกะเดิมของคุณ)
        if 'Item_Description' in mapped_df.columns:
            mapped_df = mapped_df.dropna(subset=['Item_Description'], how='all')
            mapped_df = mapped_df[~mapped_df['Item_Description'].astype(str).str.contains('รายการ|วันที่', na=False)]
        
        mapped_df = mapped_df.reset_index(drop=True)

        # แสดงผลตารางที่คลีนเสร็จแล้ว
        st.dataframe(mapped_df, use_container_width=True)
        st.success(f"✅ จัดสรรข้อมูลเสร็จสิ้น: ดึงข้อมูลมาครบทุกคอลัมน์รวมทั้งหมด {len(mapped_df)} รายการ")
        
        # ปุ่มดาวน์โหลดไฟล์ (.csv) พร้อม BOM ป้องกันภาษาไทยเพี้ยน
        csv = mapped_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 ดาวน์โหลดไฟล์สำหรับ ERP (.csv)",
            data=csv,
            file_name="ERP_Full_Item_Master.csv",
            mime="text/csv"
        )
