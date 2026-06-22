import streamlit as st
import pandas as pd

st.title("🏭 Module: ข้อมูลการผลิตและวัตถุดิบ (Production & Materials)")

if 'df_vendor' in st.session_state:
    raw_df = st.session_state['df_vendor'].copy()
    
    st.subheader("📋 ข้อมูลดิบจากไฟล์")
    st.dataframe(raw_df)

    st.subheader("✨ ข้อมูลที่ดึงหัวข้อและตัดแถวส่วนเกินอัตโนมัติ")
    
    try:
        # เนื่องจากตั้ง header=None แถวจะตรงตามลำดับจริงในไฟล์ Excel ดังนี้:
        # แถวที่ 0 = คำว่า Production
        # แถวที่ 1 = คำว่า DATE, FAC, PRODUCT, RAW MATERIAL, PRODUCT
        # แถวที่ 2 = คำว่า NAME, CODE, ORDER, SOURCE, CODE, R, S, QTY(KG)...
        row1 = raw_df.iloc[1].fillna('').astype(str).values
        row2 = raw_df.iloc[2].fillna('').astype(str).values
        
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
            
        # เคลียร์ปัญหาชื่อซ้ำ (De-duplicate) เช่น ถ้ามี CODE ซ้ำ จะแก้เป็น CODE_1, CODE_2 อัตโนมัติ
        final_headers = []
        counts = {}
        for h in new_headers:
            if h in counts:
                counts[h] += 1
                final_headers.append(f"{h}_{counts[h]}")
            else:
                counts[h] = 0
                final_headers.append(h)
                
        # ข้อมูลจริงจะเริ่มตั้งแต่แถวที่ 3 เป็นต้นไป (Index 3+)
        clean_df = raw_df.iloc[3:].copy()
        clean_df.columns = final_headers
        clean_df = clean_df.reset_index(drop=True)
        
        st.dataframe(clean_df)
        st.success(f"⚡ ดึงหัวตารางและแก้ไขชื่อคอลัมน์ซ้ำสำเร็จ ทั้งหมด {len(clean_df)} รายการ")
        
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการดึงหัวตาราง: {e}")
        
else:
    st.warning("⚠️ ยังไม่มีข้อมูลในระบบ กรุณากลับไปอัปโหลดไฟล์ที่หน้าหลัก (app.py) ก่อนเริ่มใช้งาน")
