import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Production & Materials Module", layout="wide")

st.title("🏭 Module: จัดสรรข้อมูลการผลิตและวัตถุดิบ (Production & Materials)")

df_raw = None

# 1. 🟢 ตรวจสอบและดึงไฟล์ดิบจากคีย์ 'VM_upload_file' (อ้างอิงจาก df_vendor เดิม)
if 'VM_upload_file' in st.session_state and st.session_state['VM_upload_file'] is not None:
    file_prod_raw = st.session_state['VM_upload_file']
    
    # เช็คว่าเป็นไฟล์ Excel หรือไม่ เพื่อดึงรายชื่อ Sheet
    if hasattr(file_prod_raw, 'name') and file_prod_raw.name.endswith(('.xlsx', '.xls')):
        
        # ตัวดักจับ: หากมีการอัปโหลดไฟล์ใหม่เข้ามา ให้ล้างโครงสร้างชีตเดิมทิ้งเพื่ออัปเดตข้อมูลล่าสุด
        current_file_id = f"{file_prod_raw.name}_{file_prod_raw.size}"
        if 'last_prod_file_id' not in st.session_state or st.session_state['last_prod_file_id'] != current_file_id:
            st.session_state['last_prod_file_id'] = current_file_id
            if 'prod_sheets_dict' in st.session_state:
                del st.session_state['prod_sheets_dict']
                
        # แกะโครงสร้าง Sheet ทั้งหมดเก็บลง Session State
        if 'prod_sheets_dict' not in st.session_state:
            try:
                file_prod_raw.seek(0)  # Reset Pointer ป้องกันไฟล์ว่างเปล่า
                file_bytes = file_prod_raw.getvalue()
                selected_engine = 'openpyxl' if file_prod_raw.name.endswith('.xlsx') else 'xlrd'
                
                st.session_state['prod_sheets_dict'] = pd.read_excel(
                    io.BytesIO(file_bytes),
                    sheet_name=None,  # อ่านมาทุกแผ่นงาน
                    header=None,
                    engine=selected_engine
                )
            except Exception as e:
                st.error(f"❌ ไม่สามารถดึงโครงสร้างแผ่นงานได้: {e}")

# 2. 📊 ส่วนแสดงผลแถบเลือกแผ่นงาน (Sheet Selector)
if 'prod_sheets_dict' in st.session_state:
    sheets_data = st.session_state['prod_sheets_dict']
    all_sheets = list(sheets_data.keys())
    
    st.markdown("---")
    st.markdown("### 🔍 ตรวจพบแผ่นงานในไฟล์ของคุณ")
    
    # จัดการตำแหน่งการเลือกเริ่มต้น (Default Index)
    if "prod_sheet_choice" in st.session_state and st.session_state["prod_sheet_choice"] in all_sheets:
        default_index = all_sheets.index(st.session_state["prod_sheet_choice"])
    else:
        default_index = 0
        if len(all_sheets) > 0:
            st.session_state["prod_sheet_choice"] = all_sheets[0]
            
    # สร้างกล่อง Dropdown เลือก Sheet เหมือนกับหน้าอื่นๆ
    selected_sheet = st.selectbox(
        "กรุณาเลือกแผ่นงาน (Sheet) ที่ถูกต้องสำหรับหน้าข้อมูลการผลิตและวัตถุดิบ:",
        options=all_sheets,
        index=default_index,
        key="prod_sheet_choice"
    )
    
    df_raw = sheets_data[selected_sheet]
    st.success(f"📋 ดึงข้อมูลจากแผ่นงาน: **'{selected_sheet}'** สำเร็จ")

elif 'df_vendor' in st.session_state:
    df_raw = st.session_state['df_vendor']
    st.info("ℹ️ ตรวจพบเป็นข้อมูลจากไฟล์เดี่ยว (.csv) ระบบดึงข้อมูลแผ่นงานหลักมาใช้งานโดยอัตโนมัติ")
else:
    st.warning("⚠️ ยังไม่มีข้อมูลในระบบ กรุณากลับไปอัปโหลดไฟล์ในช่อง '1. อัปโหลดไฟล์ Vendor Master' ที่หน้าหลักก่อนเริ่มใช้งาน")


# 3. ⚙️ ส่วนจัดการและจัดสรรข้อมูล (Mapping Data)
if df_raw is not None:
    st.subheader("📋 ข้อมูลดิบที่ดึงมาจากแผ่นงาน")
    st.dataframe(df_raw, use_container_width=True)
    
    # --- ตัดแถวที่ 0-3 ออก และรีเซ็ตดัชนี ---
    df = df_raw.iloc[4:].reset_index(drop=True)
    
    st.subheader("✨ ข้อมูลที่จัดสรรตามโครงสร้าง ERP Standard (Mapped Data)")
    
    # สร้าง Dataframe ใหม่เพื่อ Map คอลลัมน์ (เฉพาะคอลลัมน์ที่ต้องการเก็บไว้)
    mapped_df = pd.DataFrame()
    num_cols = len(df.columns)
    
    # --- ฝั่งข้อมูลทั่วไปและ PRODUCT ---
    mapped_df['DATE'] = df.iloc[:, 0] if num_cols > 0 else "N/A"
    mapped_df['FAC'] = df.iloc[:, 1] if num_cols > 1 else "N/A"
    mapped_df['PRODUCT_NAME'] = df.iloc[:, 2] if num_cols > 2 else "N/A"
    # ❌ เอาออก: df.iloc[:, 3] (PRODUCT_CODE)
    mapped_df['ORDER'] = df.iloc[:, 4] if num_cols > 4 else "N/A"
    
    # --- ฝั่ง RAW MATERIAL ---
    mapped_df['RM_SOURCE'] = df.iloc[:, 5] if num_cols > 5 else "N/A"
    # ❌ เอาออก: df.iloc[:, 6] (RM_CODE)
    # ❌ เอาออก: df.iloc[:, 7] (RM_R)
    # ❌ เอาออก: df.iloc[:, 8] (RM_S)
    mapped_df['RM_QTY_KG'] = df.iloc[:, 9] if num_cols > 9 else 0
    
    # --- ฝั่งข้อมูลส่วนเพิ่มด้านขวา ---
    mapped_df['P_QTY_KG'] = df.iloc[:, 10] if num_cols > 10 else 0
    # ❌ เอาออก: df.iloc[:, 11] (PROD_CODE)
    mapped_df['BAG'] = df.iloc[:, 12] if num_cols > 12 else "N/A"
    # ❌ เอาออก: df.iloc[:, 13] (BAG_CODE)
    mapped_df['SHRINK'] = df.iloc[:, 14] if num_cols > 14 else "N/A"
    # mapped_df['PALLETS'] = df.iloc[:, 15] if num_cols > 15 else "N/A" # มีการพิมพ์แก้ในโค้ดเดิมคุณ
    mapped_df['PALLETS'] = df.iloc[:, 15] if num_cols > 15 else "N/A"
    mapped_df['PRICE'] = df.iloc[:, 16] if num_cols > 16 else 0
    mapped_df['NOTE'] = df.iloc[:, 17] if num_cols > 17 else ""
    
    # ทำ Data Validation และแปลง Type เฉพาะคอลลัมน์ตัวเลขที่เหลืออยู่
    mapped_df['RM_QTY_KG'] = pd.to_numeric(mapped_df['RM_QTY_KG'], errors='coerce').fillna(0)
    mapped_df['PRICE'] = pd.to_numeric(mapped_df['PRICE'], errors='coerce').fillna(0)
    
    # แสดงผลตารางแบบเต็มความกว้างหน้าจอ
    st.dataframe(mapped_df, use_container_width=True)
    
    # คำนวณยอดรวมวัตถุดิบ
    rm_qty = mapped_df['RM_QTY_KG'].sum()
    
    # แสดงผล Metric
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="📊 ยอดรวมวัตถุดิบทั้งหมด (RAW MATERIAL)", value=f"{rm_qty:,.2f} KG")
    with col2:
        st.metric(label="📦 สถานะโมดูล", value="เอาคอลลัมน์ที่ไม่จำเป็นออกแล้ว")
        
    st.success(f"⚡ จัดสรรโครงสร้างข้อมูลสำเร็จ ทั้งหมด {len(mapped_df)} รายการ (คัดกรองเหลือเฉพาะคอลลัมน์ที่จำเป็น)")
