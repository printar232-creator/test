import streamlit as st
import pandas as pd

st.set_page_config(page_title="Production & Materials Module", layout="wide")

st.title("🏭 Module: จัดสรรข้อมูลการผลิตและวัตถุดิบ (Production & Materials)")

# ตรวจสอบว่ามีข้อมูลถูกอัปโหลดมาจากหน้าหลักหรือยัง
if 'df_vendor' in st.session_state:
    df_raw = st.session_state['df_vendor']
    
    st.subheader("📋 ข้อมูลดิบที่ดึงมาจากหน้าหลัก")
    st.dataframe(df_raw, use_container_width=True)
    
    # --- ตัดแถวที่ 0-3 ออก และรีเซ็ตดัชนี ---
    df = df_raw.iloc[4:].reset_index(drop=True)
    
    st.subheader("✨ ข้อมูลที่จัดสรรตามโครงสร้าง ERP Standard (Mapped Data)")
    
    # สร้าง Dataframe ใหม่เพื่อ Map คอลลัมน์
    mapped_df = pd.DataFrame()
    num_cols = len(df.columns)
    
    # --- ฝั่งข้อมูลทั่วไปและ PRODUCT ---
    mapped_df['DATE'] = df.iloc[:, 0] if num_cols > 0 else "N/A"
    mapped_df['FAC'] = df.iloc[:, 1] if num_cols > 1 else "N/A"
    mapped_df['PRODUCT_NAME'] = df.iloc[:, 2] if num_cols > 2 else "N/A"
    mapped_df['PRODUCT_CODE'] = df.iloc[:, 3] if num_cols > 3 else "N/A"
    mapped_df['ORDER'] = df.iloc[:, 4] if num_cols > 4 else "N/A"
    
    # --- ฝั่ง RAW MATERIAL ---
    mapped_df['RM_SOURCE'] = df.iloc[:, 5] if num_cols > 5 else "N/A"
    mapped_df['RM_CODE'] = df.iloc[:, 6] if num_cols > 6 else "N/A"
    mapped_df['RM_R'] = df.iloc[:, 7] if num_cols > 7 else "N/A"
    mapped_df['RM_S'] = df.iloc[:, 8] if num_cols > 8 else "N/A"
    mapped_df['RM_QTY_KG'] = df.iloc[:, 9] if num_cols > 9 else 0
    
    # --- ฝั่งข้อมูลส่วนเพิ่มด้านขวา ---
    mapped_df['PROD_QTY_KG'] = df.iloc[:, 10] if num_cols > 10 else 0
    mapped_df['PROD_CODE'] = df.iloc[:, 11] if num_cols > 11 else "N/A"
    mapped_df['BAG'] = df.iloc[:, 12] if num_cols > 12 else "N/A"
    mapped_df['BAG_CODE'] = df.iloc[:, 13] if num_cols > 13 else "N/A"
    mapped_df['SHRINK'] = df.iloc[:, 14] if num_cols > 14 else "N/A"
    mapped_df['PALLETS'] = df.iloc[:, 15] if num_cols > 15 else "N/A"
    mapped_df['PRICE'] = df.iloc[:, 16] if num_cols > 16 else 0
    mapped_df['NOTE'] = df.iloc[:, 17] if num_cols > 17 else ""
    
    # ทำ Data Validation และแปลง Type ให้ถูกต้องในตัวตารางเลย
    mapped_df['RM_QTY_KG'] = pd.to_numeric(mapped_df['RM_QTY_KG'], errors='coerce').fillna(0)
    mapped_df['PROD_QTY_KG'] = pd.to_numeric(mapped_df['PROD_QTY_KG'], errors='coerce').fillna(0)
    mapped_df['PRICE'] = pd.to_numeric(mapped_df['PRICE'], errors='coerce').fillna(0)
    
    # แสดงผลตารางแบบเต็มความกว้างหน้าจอ
    st.dataframe(mapped_df, use_container_width=True)
    
    # คำนวณยอดรวม
    rm_qty = mapped_df['RM_QTY_KG'].sum()
    prod_qty = mapped_df['PROD_QTY_KG'].sum()
    
    # แสดงผล Metric
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="📊 ยอดรวมวัตถุดิบทั้งหมด (RAW MATERIAL)", value=f"{rm_qty:,.2f} KG")
    with col2:
        st.metric(label="📦 ยอดรวมสินค้าสำเร็จรูป (PRODUCT)", value=f"{prod_qty:,.2f} KG")
        
    st.success(f"⚡ จัดสรรโครงสร้างข้อมูลสำเร็จ ทั้งหมด {len(mapped_df)} รายการ")

else:
    st.warning("⚠️ ยังไม่มีข้อมูลในระบบ กรุณากลับไปอัปโหลดไฟล์ที่หน้าหลัก (app.py) ก่อนเริ่มใช้งาน")
