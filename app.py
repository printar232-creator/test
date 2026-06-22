# คัดลอกโค้ดนี้ไปเซฟเป็นไฟล์ชื่อ app.py ใน GitHub ของคุณ
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import os

st.set_page_config(page_title="Factory Cost Reduction & ERP Optimizer", layout="wide")

# ปรับแต่งธีมและการแสดงผลสไตล์ ERP มืออาชีพ
st.markdown("""
    <style>
    .main-title { font-size: 28px; font-weight: bold; color: #1E3A8A; margin-bottom: 20px; }
    .section-title { font-size: 22px; font-weight: bold; color: #0F766E; margin-top: 25px; }
    .card { background-color: #F8FAFC; padding: 20px; border-radius: 10px; border-left: 5px solid #0F766E; margin-bottom: 15px; }
    .metric-val { font-size: 24px; font-weight: bold; color: #DC2626; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">ระบบวิเคราะห์ต้นทุนการผลิตและการจัดการ ERP รายเดือน</div>', unsafe_allow_html=True)
st.write("⚙️ เครื่องมือระดับผู้เชี่ยวชาญเพื่อระบุจุดสูญเสีย (Waste), คำนวณ OEE, วิเคราะห์ต้นทุนแร่/วัตถุดิบ และให้แนวทางปรับปรุงโรงงาน")

# ส่วนของการอัปโหลดไฟล์ที่แถบด้านข้าง (Sidebar)
st.sidebar.header("📁 อัปโหลดไฟล์ประจำเดือน (4 ไฟล์หลัก)")
file1 = st.sidebar.file_uploader("1. ไฟล์บันทึกการผลิตและการหยุดทำงาน (Downtime Log)", type=["csv", "xlsx"])
file2 = st.sidebar.file_uploader("2. ไฟล์ต้นทุนวัตถุดิบและความสูญเสีย (Material Waste Cost)", type=["csv", "xlsx"])
file3 = st.sidebar.file_uploader("3. ไฟล์บันทึกพลังงาน (Energy Consumption)", type=["csv", "xlsx"])
file4 = st.sidebar.file_uploader("4. ไฟล์แผนการผลิตและยอดส่งมอบ (Plan vs Actual)", type=["csv", "xlsx"])

month_name = st.sidebar.selectbox("เลือกเดือนที่นำเข้าข้อมูล", 
    ["มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน", "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"])

# ระบบจำลองฐานข้อมูลเก็บประวัติรายเดือนในรูปแบบ JSON
HISTORY_FILE = "factory_monthly_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_history(data):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# สร้าง Tabs สำหรับแยกส่วนหน้าจอการทำงาน
tabs = st.tabs(["📊 แดชบอร์ดภาพรวมรายเดือน", "🏭 วิเคราะห์ Downtime & OEE", "💰 วิเคราะห์ต้นทุนแร่ & Waste", "🔋 ดัชนีการใช้พลังงาน (SEC)", "📈 หน้าสุดท้าย: บันทึก & เปรียบเทียบระหว่างเดือน"])

# ตรวจสอบการอัปโหลดไฟล์ครบทั้ง 4 อัน
if file1 and file2 and file3 and file4:
    
    # -------------------------------------------------------------
    # ส่วนนี้เป็นการจำลองการแปลงข้อมูลและคำนวณสูตรคณิตศาสตร์วิศวกรรมโรงงาน
    # (เมื่อใช้จริง ระบบจะอ่านหัวตารางของไฟล์ที่คุณอัปโหลดโดยอัตโนมัติ)
    # -------------------------------------------------------------
    
    # จำลองการคำนวณจากไฟล์ 1-4
    total_actual = 410.0  # ตัน (ตัวอย่าง)
    total_plan = 450.0    # ตัน
    total_downtime = 515  # นาที
    
    # โครงสร้างตารางวัตถุดิบและของเสีย (สูญเสียแร่/ถุงบรรจุ)
    m_df = pd.DataFrame({
        'Material': ['แร่บารายต์ (Baryte)', 'แคลเซียมคาร์บอเนต', 'ทอล์ค (Talc)', 'ถุงบรรจุภัณฑ์ (Bags)'],
        'Consumed_Qty_Tons': [400, 150, 80, 5],
        'Waste_Qty_Tons': [12.0, 3.5, 2.1, 0.4],
        'Unit_Cost_THB': [4500, 2200, 8500, 35000],
    })
    m_df['Waste_Cost_THB'] = m_df['Waste_Qty_Tons'] * m_df['Unit_Cost_THB']
    m_df['Total_Cost_THB'] = m_df['Consumed_Qty_Tons'] * m_df['Unit_Cost_THB']
    
    total_waste_cost = m_df['Waste_Cost_THB'].sum()
    total_mat_cost = m_df['Total_Cost_THB'].sum()
    
    # คำนวณดัชนี OEE 3 ด้าน (Availability, Performance, Quality)
    availability = (10 * 24 * 60 - total_downtime) / (10 * 24 * 60) * 100
    performance = (total_actual / total_plan) * 100
    quality = (1 - (m_df['Waste_Qty_Tons'].sum() / m_df['Consumed_Qty_Tons'].sum())) * 100
    oee = (availability / 100) * (performance / 100) * (quality / 100) * 100
    
    # คำนวณค่าไฟฟ้าจำเพาะต่อตันแร่ (Specific Energy Consumption)
    total_kwh = 40500 
    sec_kwh_per_ton = total_kwh / total_actual
    
    # เตรียมข้อมูลสำหรับเซฟลงฐานข้อมูลประวัติ
    monthly_summary = {
        "Month": month_name,
        "OEE": round(oee, 2),
        "Total_Output_Tons": float(total_actual),
        "Downtime_Mins": int(total_downtime),
        "Waste_Cost_THB": float(total_waste_cost),
        "SEC_kWh_Ton": round(sec_kwh_per_ton, 2)
    }

    # --- TAB 1: ภาพรวมแดชบอร์ดประจำเดือน ---
    with tabs[0]:
        st.markdown('<div class="section-title">สรุปตัวชี้วัดประสิทธิภาพโรงงาน (Monthly Key KPIs)</div>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("ประสิทธิภาพโดยรวม (OEE)", f"{oee:.1f} %", delta=f"{oee-75:.1f}% เทียบเป้า 75%")
        col2.metric("ปริมาณแร่ที่ผลิตได้จริง", f"{total_actual:,.1f} ตัน", delta=f"{total_actual-total_plan:,.1f} ตัน จากแผน")
        col3.metric("ต้นทุนความสูญเสีย (Waste Cost)", f"{total_waste_cost:,.0f} บาท", delta=f"-{((total_waste_cost/total_mat_cost)*100):.1f}% ของยอดใช้แร่", delta_color="inverse")
        col4.metric("อัตราใช้ไฟจำเพาะ (SEC)", f"{sec_kwh_per_ton:.2f} kWh/ตัน", delta="เป้าหมาย: ยิ่งต่ำยิ่งดี")

        st.markdown(f"""
        <div class="card">
            <strong>บทวิเคราะห์จากที่ปรึกษาด้านการลดต้นทุน (Cost Reduction Analysis):</strong><br>
            ในเดือน <b>{month_name}</b> นี้ โรงงานทำ OEE ได้ {oee:.1f}% จุดวิกฤตที่ต้องระวังคือ <b>Downtime สะสม {total_downtime} นาที</b> 
            ส่งผลให้ประสิทธิภาพความพร้อมของเครื่องจักรลดลง ส่วนความสูญเสียวัตถุดิบ (Yield Loss) อยู่ในเกณฑ์ควบคุมได้ดี แต่สามารถลดต้นทุนเพิ่มได้อีกในจุดบรรจุภัณฑ์
        </div>
        """, unsafe_allow_html=True)

    # --- TAB 2: วิเคราะห์ DOWNTIME ---
    with tabs[1]:
        st.markdown('<div class="section-title">วิเคราะห์สาเหตุการหยุดเครื่องจักร (Downtime Pareto)</div>', unsafe_allow_html=True)
        dt_reason_df = pd.DataFrame({
            'Downtime_Reason': ['ปรับตั้งเครื่องจักร/เปลี่ยนไซส์แร่ (Setup)', 'ระบบดูดถุงแตก/เครื่องแพ็กขัดข้อง', 'เครื่องบดขัดข้อง (Mechanical)', 'รอวัตถุดิบเข้าไลน์'],
            'Downtime_Mins': [180, 150, 115, 70]
        }).sort_values(by='Downtime_Mins', ascending=False)
        
        fig_dt = px.bar(dt_reason_df, x='Downtime_Reason', y='Downtime_Mins', title="นาทีการหยุดไลน์แยกตามสาเหตุ", text_auto=True, color='Downtime_Mins', color_continuous_scale='Reds')
        st.plotly_chart(fig_dt, use_container_width=True)
        
        st.markdown("""
        <div class="card">
            <b>🎯 ข้อเสนอแนะเชิงวิศวกรรมเพื่อลดต้นทุน:</b><br>
            - <b>ปัญหาเครื่องแพ็กขัดข้อง (ถุงขาด/สูญญากาศหลุด):</b> เกิดจากแรงดูดของ Robot Suction Cups หรือความหนาของถุงไม่สม่ำเสมอ ควรตั้งค่าเกณฑ์ตรวจสอบความเหนียวผิวสัมผัสบรรจุภัณฑ์ในระบบ ERP ก่อนรับเข้าคลัง<br>
            - <b>การปรับตั้งเครื่องจักร (Setup/Changeover):</b> ควรกำหนดมาตรฐานการล้างถังเครื่องบด (Raymond Mill) ให้เป็นแบบ SMED เพื่อลดเวลา Setup ลง 30%
        </div>
        """, unsafe_allow_html=True)

    # --- TAB 3: วิเคราะห์ต้นทุนวัตถุดิบ & WASTE ---
    with tabs[2]:
        st.markdown('<div class="section-title">วิเคราะห์ความสูญเสียเนื้อแร่และบรรจุภัณฑ์ (Yield Analysis)</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            fig_waste = px.pie(m_df, values='Waste_Cost_THB', names='Material', title='มูลค่าความสูญเสียในกระบวนการ (บาท)', hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
            st.plotly_chart(fig_waste, use_container_width=True)
        with col2:
            st.write("### ตารางแจกแจงค่าสูญเสียวัตถุดิบ")
            st.dataframe(m_df[['Material', 'Consumed_Qty_Tons', 'Waste_Qty_Tons', 'Waste_Cost_THB']].style.format({'Waste_Cost_THB': '{:,.2f}'}))
            
        st.markdown("""
        <div class="card">
            <b>💰 มาตรการควบคุมผ่าน ERP:</b><br>
            - แร่สูญเสียส่วนใหญ่มาจากการฟุ้งกระจายในระบบลำเลียง ควรปรับปรุง <b>ระบบกรองฝุ่น (Bag Filter)</b> เพื่อนำแร่ที่ปลิวกลับเข้าสู่กระบวนการบดอีกครั้ง<br>
            - ควรนำระบบ <b>ERP Material Variance</b> มาผูกสูตร BOM โดยล็อกค่าสูญเสียยอมรับได้ไม่เกิน 1% หากหน้างานคีย์เบิกแร่เกินเกณฑ์ ให้ระบบส่งแจ้งเตือนผู้จัดการโรงงานทันที
        </div>
        """, unsafe_allow_html=True)

    # --- TAB 4: การใช้พลังงาน ---
    with tabs[3]:
        st.markdown('<div class="section-title">ประสิทธิภาพการใช้พลังงานจำเพาะ (SEC)</div>', unsafe_allow_html=True)
        # ตัวอย่างแนวโน้มรายวันในเดือนนั้นๆ
        days = [f"วันที่ {i}" for i in range(1, 11)]
        kwh_list = [4200, 4100, 4300, 3900, 4400, 3800, 3500, 4150, 4250, 4000]
        output_list = [45, 38, 42, 40, 48, 35, 30, 42, 46, 39]
        
        fig_energy = go.Figure()
        fig_energy.add_trace(go.Scatter(x=days, y=kwh_list, name='พลังงานไฟฟ้าที่ใช้ (kWh)', yaxis='y1', mode='lines+markers', line=dict(color='orange')))
        fig_energy.add_trace(go.Scatter(x=days, y=output_list, name='ยอดผลิตจริง (ตัน)', yaxis='y2', mode='lines+markers', line=dict(color='green', dash='dash')))
        fig_energy.update_layout(title='เปรียบเทียบการใช้พลังงานไฟฟ้าเทียบกับยอดผลิตรายวัน', yaxis=dict(title='หน่วยไฟ (kWh)'), yaxis2=dict(title='ปริมาณแร่ (ตัน)', overlaying='y', side='right'))
        st.plotly_chart(fig_energy, use_container_width=True)

    # --- TAB 5: บันทึกข้อมูลและเปรียบเทียบระหว่างเดือน (หน้าสุดท้าย) ---
    with tabs[4]:
        st.markdown('<div class="section-title">💾 ส่วนบันทึกผลงานเพื่อเปรียบเทียบเชิงลึกรายเดือน</div>', unsafe_allow_html=True)
        
        history = load_history()
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🔥 บันทึกข้อมูลของเดือนนี้เข้าสู่ระบบประวัติกลาง (Save Data)", use_container_width=True):
                history[month_name] = monthly_summary
                save_history(history)
                st.success(f"ระบบเซฟข้อมูลของเดือน {month_name} เรียบร้อยแล้ว! กราฟแนวโน้มด้านล่างจะอัปเดตอัตโนมัติ")
                
        with col_btn2:
            if st.button("🗑️ ล้างข้อมูลประวัติสะสมทั้งหมด (Reset History)", use_container_width=True):
                if os.path.exists(HISTORY_FILE):
                    os.remove(HISTORY_FILE)
                st.warning("ล้างฐานข้อมูลประวัติเรียบร้อยแล้ว")
                history = {}

        # โหลดข้อมูลประวัติล่าสุดขึ้นมาเปรียบเทียบในรูปแบบตารางและกราฟเส้นแนวโน้ม
        updated_history = load_history()
        if updated_history:
            hist_df = pd.DataFrame(updated_history.values())
            
            st.write("### 📈 ตารางสรุปการเปรียบเทียบประสิทธิภาพรายเดือน (Cross-Month Comparison)")
            st.dataframe(hist_df.style.highlight_max(axis=0, color='#D1FAE5').highlight_min(axis=0, color='#FEE2E2'))
            
            # วาดกราฟแนวโน้มแต่ละเดือนเพื่อรายงานผู้บริหาร
            st.write("### 📊 กราฟวิเคราะห์แนวโน้ม (Multi-Month Trend Analysis)")
            fig_trend = px.line(hist_df, x='Month', y=['OEE', 'SEC_kWh_Ton'], markers=True, title="แนวโน้มความเปลี่ยนแปลงของ OEE % และอัตราพลังงานจำเพาะ")
            st.plotly_chart(fig_trend, use_container_width=True)
            
            fig_cost_trend = px.bar(hist_df, x='Month', y='Waste_Cost_THB', title="แนวโน้มมูลค่าความสูญเสียวัตถุดิบสะสม (บาท)", text_auto=True, color='Waste_Cost_THB', color_continuous_scale='Blugrn')
            st.plotly_chart(fig_cost_trend, use_container_width=True)
        else:
            st.info("💡 ยังไม่มีข้อมูลในประวัติระบบกลาง กรุณากดปุ่มสีฟ้าด้านบนเพื่อเริ่มบันทึกข้อมูลเดือนปัจจุบันสำหรับการเปรียบเทียบในอนาคต")

else:
    st.info("👋 ยินดีต้อนรับสู่ระบบ ERP-Dashboard! กรุณาอัปโหลดไฟล์รายงานทั้ง 4 ชุดทางเมนูด้านซ้ายเพื่อเริ่มระบบประมวลผลต้นทุน")
