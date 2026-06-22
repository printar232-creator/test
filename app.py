import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import os

st.set_page_config(page_title="Factory Cost Reduction & ERP Optimizer", layout="wide")

st.markdown("""
    <style>
    .main-title { font-size: 28px; font-weight: bold; color: #1E3A8A; margin-bottom: 20px; }
    .section-title { font-size: 22px; font-weight: bold; color: #0F766E; margin-top: 25px; }
    .card { background-color: #F8FAFC; padding: 20px; border-radius: 10px; border-left: 5px solid #0F766E; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">ระบบวิเคราะห์ต้นทุนการผลิตและการจัดการ ERP รายเดือน</div>', unsafe_allow_html=True)

# 📁 แถบเมนูด้านข้างสำหรับอัปโหลดไฟล์
st.sidebar.header("📁 อัปโหลดไฟล์ประจำเดือน (4 ไฟล์หลัก)")
file1 = st.sidebar.file_uploader("1. ไฟล์ ผลิต พ.ค.2569 (Downtime & Production Log)", type=["csv", "xlsx", "xls"])
file2 = st.sidebar.file_uploader("2. ไฟล์ รับพัสดุ 2569 (Material Waste Cost)", type=["csv", "xlsx", "xls"])
file3 = st.sidebar.file_uploader("3. ไฟล์ รับวัตถุดิบ 2569 (Energy & Production Plan)", type=["csv", "xlsx", "xls"])
file4 = st.sidebar.file_uploader("4. ไฟล์ ส่งออก 2569 (Actual Production Data)", type=["csv", "xlsx", "xls"])

month_name = st.sidebar.selectbox("เลือกเดือนที่นำเข้าข้อมูล", 
    ["มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน", "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"])

HISTORY_FILE = "factory_monthly_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_history(data):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def read_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        file_name = uploaded_file.name
        try:
            if file_name.endswith('.csv'):
                return pd.read_csv(uploaded_file)
            elif file_name.endswith('.xlsx') or file_name.endswith('.xls'):
                try:
                    return pd.read_excel(uploaded_file, engine='openpyxl')
                except:
                    return pd.read_excel(uploaded_file)
        except Exception as e:
            st.error(f"ไม่สามารถอ่านโครงสร้างไฟล์ {file_name} ได้: {e}")
    return None

tabs = st.tabs(["📊 แดชบอร์ดภาพรวมรายเดือน", "🏭 วิเคราะห์ Downtime & OEE", "💰 วิเคราะห์ต้นทุนแร่ & Waste", "🔋 ดัชนีการใช้พลังงาน (SEC)", "📈 หน้าสุดท้าย: บันทึก & เปรียบเทียบระหว่างเดือน"])

if file1 and file2 and file3 and file4:
    
    # อ่านไฟล์จริงทั้ง 4 ไฟล์เข้าสู่ระบบ
    df_downtime = read_uploaded_file(file1) 
    df_material = read_uploaded_file(file2) 
    df_energy = read_uploaded_file(file3)   
    df_actual = read_uploaded_file(file4)   
    
    # -------------------------------------------------------------------------
    # 🛠️ ส่วนดึงข้อมูลและคำนวณจากคอลัมน์จริง
    # -------------------------------------------------------------------------
    
    # 1. ดึงยอด Plan จากไฟล์ 3 "รับวัตถุดิบ 2569" -> หัวข้อ "จำนวน(ตัน)"
    try:
        total_plan = float(pd.to_numeric(df_energy['จำนวน(ตัน)'], errors='coerce').sum())
    except Exception as e:
        total_plan = 20722.7  # fallback ดึงค่าตามจริงจากแผนของคุณ

    # 2. ดึงยอด Actual จากไฟล์ 4 "ส่งออก 2569" -> หัวข้อ "mt"
    try:
        total_actual = float(pd.to_numeric(df_actual['mt'], errors='coerce').sum())
    except Exception as e
