import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Open Purchase Orders Module", page_icon="🛒", layout="wide")
st.title("🛒 Module: ข้อมูลใบสั่งซื้อค้างส่ง (Open Purchase Orders)")

df = None

if 'main_upload_file' in st.session_state and st.session_state['main_upload_file'] is not None:
    file_po_raw = st.session_state['main_upload_file']
    if hasattr(file_po_raw, 'name') and file_po_raw.name.endswith(('.xlsx', '.xls')):
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

if 'po_sheets_dict' in st.session_state:
    sheets_data = st.session_state['po_sheets_dict']
    all_sheets = list(sheets_data.keys())
    st.markdown("---")
    st.markdown("### 🔍 ตรวจพบแผ่นงานในไฟล์ของคุณ")
    if "po_sheet_choice" in st.session_state and st.session_state["po_sheet_choice"] in all_sheets:
        default_index = all_sheets.index(st.session_state["po_sheet_choice"])
    else:
        default_index = 1 if len(all_sheets) > 1 else 0
        if len(all_sheets) > 1:
            st.session_state["po_sheet_choice"] = all_sheets[1]
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

if df is not None:
    st.subheader("📋 ข้อมูลดิบที่ระบบอ่านได้ในปัจจุบัน")
    st.dataframe(df, use_container_width=True)
    st.subheader("✨ ข้อมูลที่จัดสรรพร้อมนำเข้า ERP (Mapped Data)")
    if df.empty:
        st.warning("⚠️ พบข้อมูลในระบบ แต่ไม่มีรายการข้อมูลในแผ่นงานนี้ (0 แถว)")
    else:
        start_row = 0
        for idx, row in df.iterrows():
            row_str = row.astype(str).values
            if any(keyword in s for s in row_str for keyword in ['วันที่', 'Date', 'ใบสั่งซื้อ', 'PO', 'ออเดอร์', 'ลูกค้า']):
                start_row = idx
                break
        clean_df = df.iloc[start_row:].reset_index(drop=True)
        headers = clean_df.iloc[0].fillna("").astype(str).tolist()
        headers = [f"คอลัมน์_{i}" if h == "" else h for i, h in enumerate(headers)]
        mapped_df = clean_df.iloc[1:].reset_index(drop=True)
        mapped_df.columns = headers
        st.dataframe(mapped_df, use_container_width=True)
        qty_col = None
        for col in mapped_df.columns:
            if any(keyword in col for keyword in ['จำนวน', 'Qty', 'Quantity', 'MT', 'ยอดรวม', 'Amount']):
                qty_col = col
                break
        total_records = len(mapped_df)
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="📊 จำนวนรายการทั้งหมดที่พบ", value=f"{total_records:,} รายการ")
        with col2:
            if qty_col:
                numeric_series = pd.to_numeric(mapped_df[qty_col], errors='coerce').fillna(0)
                total_sum = numeric_series.sum()
                st.metric(label=f"📦 ยอดรวมในคอลัมน์ ({qty_col})", value=f"{total_sum:,.2f}")
            else:
                st.metric(label="📦 ยอดรวมเชิงปริมาณ", value="ไม่พบคอลัมน์ตัวเลขบนไฟล์นี้")
        st.success(f"🎉 ดึงและจัดสรรข้อมูลจากไฟล์จริงสำเร็จทั้งหมด {mapped_df.shape[1]} คอลัมน์")
