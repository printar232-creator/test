import streamlit as st

st.set_page_config(
    page_title="ASIAN MINERAL RESOURCES",
    layout="wide"
)

st.markdown("""
<style>

.main {
    background-color: #f4f6f9;
}

.block-container {
    padding-top: 0rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

/* HEADER */
.header {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    padding: 70px 20px;
    text-align: center;
    color: white;
    border-radius: 0 0 20px 20px;
}

.header h1 {
    font-size: 46px;
}

.header p {
    font-size: 20px;
}

/* SECTION */
.section {
    background: white;
    padding: 35px;
    margin-top: 30px;
    border-radius: 15px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.05);
}

.section-title {
    color: #1e3c72;
    font-size: 30px;
    border-bottom: 3px solid #2a5298;
    padding-bottom: 10px;
    margin-bottom: 25px;
}

/* CARD */
.card {
    background: #f4f7fc;
    padding: 25px;
    border-radius: 12px;
    border-left: 5px solid #2a5298;
    height: 100%;
}

/* PARTNER */
.partner {
    background: #ececec;
    padding: 10px 18px;
    border-radius: 20px;
    display: inline-block;
    margin: 5px;
    font-weight: 500;
}

/* FOOTER */
.footer {
    background: #222;
    color: #ccc;
    text-align: center;
    padding: 30px;
    margin-top: 50px;
    border-radius: 20px 20px 0 0;
}

</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("""
<div class="header">
    <h1>บริษัท เอเซี่ยน มินเนอรัล รีซอสเซส จำกัด</h1>
    <p>ASIAN MINERAL RESOURCES CO., LTD.</p>
</div>
""", unsafe_allow_html=True)

# ABOUT
st.markdown('<div class="section">', unsafe_allow_html=True)

st.markdown("""
<div class="section-title">
เกี่ยวกับเรา
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2,1])

with col1:
    st.write("""
บริษัทดำเนินธุรกิจด้านเหมืองแร่ แต่งแร่ และแปรรูปแร่อุตสาหกรรมคุณภาพสูง
มากกว่า 35 ปี พร้อมส่งออกไปยังตลาดทั่วโลก
""")

with col2:
    st.info("""
🎖️ ได้รับ BOI  
🏭 โรงงานมาตรฐาน  
🌏 ส่งออกหลายประเทศ
""")

st.markdown("</div>", unsafe_allow_html=True)

# PRODUCTS
st.markdown('<div class="section">', unsafe_allow_html=True)

st.markdown("""
<div class="section-title">
ผลิตภัณฑ์หลัก
</div>
""", unsafe_allow_html=True)

products = [
    ("BARYTES", "แร่แบร์ไรต์คุณภาพสูง"),
    ("TALC POWDER", "ผงทัลคัม"),
    ("DOLOMITE", "โดโลไมต์"),
    ("CALCIUM CARBONATE", "แคลเซียมคาร์บอเนต")
]

cols = st.columns(4)

for col, p in zip(cols, products):
    with col:
        st.markdown(f"""
        <div class="card">
            <h3>{p[0]}</h3>
            <p>{p[1]}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# PARTNERS
st.markdown('<div class="section">', unsafe_allow_html=True)

st.markdown("""
<div class="section-title">
พันธมิตรระดับโลก
</div>
""", unsafe_allow_html=True)

partners = [
    "JOTUN",
    "AKZO NOBEL",
    "SHELL",
    "PETRONAS",
    "CHEVRON",
    "BRENTAG"
]

html = ""

for p in partners:
    html += f'<span class="partner">{p}</span>'

st.markdown(html, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# FOOTER
st.markdown("""
<div class="footer">
บริษัท เอเซี่ยน มินเนอรัล รีซอสเซส จำกัด
</div>
""", unsafe_allow_html=True)
