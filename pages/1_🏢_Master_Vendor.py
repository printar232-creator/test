import streamlit as st
import pandas as pd
import numpy as np

st.title("🏭 Module: ข้อมูลการผลิตและวัตถุดิบ (Production & Materials)")

if 'df_vendor' in st.session_state:
    # ดึงไฟล์ดิบที่อัปโหลดมาจากหน้าหลัก
    raw_df = st.session_state['df_vendor'].copy()
    
    st.subheader("📋 ข้อมูลดิบจากไฟล์")
    st.dataframe(raw_df)

    st.subheader("✨ ข้อมูลที่ดึงหัวข้อและตัดแถวส่วนเกินอัตโนมัติ")
    
    try:
        # 1. จัดการหัวตารางซ้อนกัน (แถวที่ 1 และ แถวที่ 2 ในรูปภาพ)
        # เติมค่า None ให้เป็น String เปล่าเพื่อไม่ให้เกิดคำว่า 'nan' ในหัวข้อ
        row1 = raw_df.iloc[1].fillna('').astype(str).values
        row2 = raw_df.iloc[2].fillna('').astype(str).values
        
        # รวมหัวข้อเข้าด้วยกัน เช่น 'RAW MATERIAL' + '_' + 'SOURCE' -> 'RAW MATERIAL_SOURCE'
        new_headers = []
        for r1, r2 in zip(row1, row2):
            r1_clean = r1.strip()
            r2_clean = r2.strip()
            
            if r1_clean and r2_clean:
                if r1_clean == r2_clean:
                    header_name = r1_clean
                else:
                    header_name = f"{r1_clean}_{r2_clean}"
            elif r1_clean:
                header_name = r1_clean
            elif r2_clean:
                header_name = r2_clean
            else:
                header_name = "UNNAMED"
            new_headers.append(header_name)
            
        # 2. สร้าง Dataframe ใหม่โดยใช้ข้อมูลตั้งแต่แถวที่ 3 เป็นต้นไป (Index 3+)
        clean_df = raw_df.iloc[3:].copy()
        
        # 3. นำหัวข้อที่ดึงมาสวมกลับเข้าไปเป็น Header ของตาราง
        clean_df.columns = new_headers
        
        # รีเซ็ตลำดับแถว (Index) ให้เริ่มจาก 0 ใหม่เพื่อความสวยงาม
        clean_df = clean_df.reset_index(drop=True)
        
        # แสดงผลตารางที่คลีนแล้ว
        st.dataframe(clean_df)
        st.success(f"⚡ ดึงหัวตารางจากไฟล์สำเร็จ พบข้อมูลทั้งหมด {len(clean_df)} รายการ")
        
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการดึงหัวตาราง: {e}")
        st.info("💡 คำแนะนำ: ตรวจสอบให้แน่ใจว่าไฟล์ที่อัปโหลดมีโครงสร้างแถวหัวตารางเหมือนกับในรูปภาพ")
        
else:
    st.warning("⚠️ ยังไม่มีข้อมูลในระบบ กรุณากลับไปอัปโหลดไฟล์ที่หน้าหลัก (app.py) ก่อนเริ่มใช้งาน")
