import streamlit as st

st.set_page_config(
    page_title="ASIAN MINERAL RESOURCES CO., LTD.",
    layout="wide"
)

# ======================
# CSS STYLE
# ======================

st.markdown("""
<style>

html, body, [class*="css"]  {
    font-family: 'Segoe UI', sans-serif;
    background-color: #f4f6f9;
}

/* remove streamlit top padding */
.block-container {
    padding-top: 0rem;
    padding-left: 0rem;
    padding-right: 0rem;
}

/* HEADER */
.header {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    padding: 60px 20px;
    text-align: center;
    color: white;
}

.header h1 {
    font-size: 48px;
    margin-bottom: 10px;
}

.header p {
    font-size: 20px;
    opacity: 0.9;
}

/* NAVBAR */
.navbar {
    background-color: #1f1f1f;
    padding: 15px;
    text-align: center;
    position: sticky;
    top: 0;
    z-index: 999;
}

.navbar a {
    color: white;
    text-decoration: none;
    margin: 0 15px;
    font-weight: 600;
    font-size: 16px;
}

/* SECTION */
.section {
    background: white;
    margin: 30px auto;
    padding: 40px;
    border-radius: 14px;
    max-width: 1200px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
}

.section-title {
    color: #1e3c72;
    font-size: 32px;
    margin-bottom: 25px;
    border-bottom: 3px solid #2a5298;
    padding-bottom: 10px;
}

/* CARD */
.card {
    background: #f4f7fc;
    padding: 25px;
    border-radius: 10px;
    border-left: 6px solid #2a5298;
    height: 100%;
}

.card h3 {
    color: #1e3c72;
}

/* HIGHLIGHT */
.highlight {
    background: #eef3fc;
    padding: 25px;
    border-radius: 10px;
    border: 1px solid #bfd2f2;
}

/* PARTNER */
.partner {
    background: #ececec;
    padding: 10px 18px;
    border-radius: 25px;
    display: inline-block;
    margin: 6px;
    font-weight: 500;
}

/* FOOTER */
.footer {
    background: #222;
    color: #ccc;
    text-align: center;
    padding: 30px;
    margin-top: 50px;
}

/* MOBILE */
@media(max-width:768px){

    .header h1{
        font-size:32px;
    }

    .section{
        padding:20px;
        margin:15px;
    }

}

</style>
""", unsafe_allow_html=True)

# ======================
# HEADER
# ======================

st.markdown("""
<div class="header">
    <h1>บริษัท เอเซี่ยน มินเนอรัล รีซอสเซส จำกัด</h1>
    <p>ASIAN MINERAL RESOURCES CO., LTD.</p>
</div>
""", unsafe_allow_html=True)

# ======================
# NAVBAR
# ======================

st.markdown("""
<div class="navbar">
    <a href="#about">เกี่ยวกับเรา</a>
    <a href="#strengths">จุดแข็ง</a>
    <a href="#products">ผลิตภัณฑ์</a>
    <a href="#partners">พันธมิตร</a>
</div>
""", unsafe_allow_html=True)

# ======================
# ABOUT
# ======================

st.markdown('<div id="about" class="section">', unsafe_allow_html=True)

st.markdown("""
<div class="section-title">
เกี่ยวกับเรา (About Us)
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2,1])

with col1:
    st.write("""
บริษัท เอเซี่ยน มินเนอรัล รีซอสเซส จำกัด ก่อตั้งขึ้นในปี พ.ศ. 2527
ดำเนินธุรกิจด้านการทำเหมืองแร่ แต่งแร่ และแปรรูปแร่อุตสาหกรรมคุณภาพสูง
เพื่อรองรับทั้งตลาดในประเทศและต่างประเทศ

ตลอดระยะเวลากว่า 35 ปี บริษัทได้รับความเชื่อมั่นจากลูกค้าระดับสากล
ด้วยมาตรฐานคุณภาพและความซื่อสัตย์ในการดำเนินธุรกิจ
""")

with col2:
    st.markdown("""
    <div class="highlight">
    <h4>🎖️ การรับรอง</h4>

    <ul>
        <li>ได้รับ BOI</li>
        <li>ใบอนุญาตแต่งแร่ถูกต้อง</li>
        <li>ผู้ส่งออกแร่คุณภาพสูง</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ======================
# STRENGTHS
# ======================

st.markdown('<div id="strengths" class="section">', unsafe_allow_html=True)

st.markdown("""
<div class="section-title">
จุดแข็งและศักยภาพ
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:

    st.markdown("""
    <div class="card">
    <h3>🏭 โรงงานและการผลิต</h3>

    <ul>
        <li>เครื่องจักรทันสมัย</li>
        <li>ระบบโรงงานมาตรฐาน</li>
        <li>ลานตากแร่ขนาดใหญ่</li>
        <li>ทีมงานมืออาชีพ</li>
    </ul>

    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown("""
    <div class="card">
    <h3>🌏 การตลาดและวัตถุดิบ</h3>

    <p>
    มีแหล่งวัตถุดิบจากหลายประเทศ
    และส่งออกสินค้ากว่า 70%
    ไปยังตลาดทั่วโลก
    </p>

    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ======================
# PRODUCTS
# ======================

st.markdown('<div id="products" class="section">', unsafe_allow_html=True)

st.markdown("""
<div class="section-title">
ผลิตภัณฑ์หลัก
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

products = [
    ("BARYTES", "แร่แบร์ไรต์คุณภาพสูง"),
    ("TALC POWDER", "ผงทัลคัมเกรดพรีเมียม"),
    ("DOLOMITE", "โดโลไมต์คุณภาพสูง"),
    ("CALCIUM CARBONATE", "แคลเซียมคาร์บอเนต")
]

cols = [col1, col2, col3, col4]

for col, product in zip(cols, products):

    with col:
        st.markdown(f"""
        <div class="card">
            <h3>{product[0]}</h3>
            <p>{product[1]}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ======================
# PARTNERS
# ======================

st.markdown('<div id="partners" class="section">', unsafe_allow_html=True)

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
    "BRENTAG",
    "OMYA",
    "CHEVRON"
]

partner_html = ""

for p in partners:
    partner_html += f'<span class="partner">{p}</span>'

st.markdown(partner_html, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ======================
# FOOTER
# ======================

st.markdown("""
<div class="footer">

<p>
บริษัท เอเซี่ยน มินเนอรัล รีซอสเซส จำกัด
</p>

<p>
สำนักงานใหญ่ กรุงเทพมหานคร
</p>

</div>
""", unsafe_allow_html=True)
