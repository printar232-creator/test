import streamlit as st
import pandas as pd

st.title("📦 Module: ข้อมูลสินค้าและวัตถุดิบ (Item Master)")

if 'df_item' in st.session_state and not st.session_state['df_item'].empty:
    df = st.session_state['df_item']
    num_rows = len(df)
    
    st.subheader("📋 ข้อมูลดิบที่ดึงมาจาก Session State")
    st.dataframe(df, use_container_width=True)

    st.subheader("✨ ข้อมูลที่จัดสรรพร้อมนำเข้า ERP (Mapped Data)")
    
    # สร้าง DataFrame ใหม่ที่มีจำนวนแถวเท่าข้อมูลดิบ
    mapped_df = pd.DataFrame(index=range(num_rows))
    
    # 🎯 แมปปิ้งข้อมูลตามตำแหน่งคอลัมน์ในรูปภาพ (Index เริ่มจาก 0)
    # คอลัมน์ที่ 5 (Index 4) คือ 'รหัส' -> Item_Code
    mapped_df['Item_Code'] = df.iloc[:, 4] if len(df.columns) > 4 else "N/A"
    
    # คอลัมน์ที่ 4 (Index 3) คือ 'รายการ' -> Item_Description
    mapped_df['Item_Description'] = df.iloc[:, 3] if len(df.columns) > 3 else "N/A"
    
    # ในรูปภาพไม่มีคอลัมน์ "หน่วยนับ" โดยตรง จึงกำหนด Default เป็น "Pcs" หรือ "คอยระบุข้อมูลเพิ่ม"
    mapped_df['Base_UOM'] = "Pcs" 
    
    # (ตัวเลือกเพิ่มเติม) หากต้องการแสดงข้อมูลอื่นๆ เพิ่มเติมเพื่อให้ครบถ้วนก่อนเข้า ERP
    # mapped_df['Price_Per_Unit'] = df.iloc[:, 6] if len(df.columns) > 6 else 0 # คอลัมน์ 'ราคา/หน่วย'
    
    # แสดงผลตารางที่แมปข้อมูลแล้ว
    st.dataframe(mapped_df, use_container_width=True)
    st.success(f"✅ จัดสรรข้อมูลเสร็จสิ้น: พบสินค้าทั้งหมด {num_rows} รายการ")
    
    # ปุ่มดาวน์โหลดไฟล์สำหรับนำไปใช้งานต่อ
    csv = mapped_df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 ดาวน์โหลดไฟล์สำหรับ ERP (.csv)",
        data=csv,
        file_name="ERP_Item_Master.csv",
        mime="text/csv"
    )

else:
    st.warning("⚠️ ยังไม่มีข้อมูลในระบบ กรุณากลับไปอัปโหลดไฟล์ที่หน้าหลัก (app.py) ก่อนเริ่มใช้งาน")
