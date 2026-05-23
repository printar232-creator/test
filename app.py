import streamlit as st

st.set_page_config(
    page_title="ASIAN MINERAL RESOURCES CO., LTD.",
    layout="wide"
)

# ==================================================
# CSS
# ==================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}

.main {
    background-color: #f4f6f9;
}

.block-container {
    padding-top: 0rem;
    padding-left: 2rem;
    padding-right: 2rem;
    padding-bottom: 2rem;
}

/* HEADER */

.header {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    padding: 70px 20px;
    text-align: center;
    color: white;
    border-radius: 0 0 25px 25px;
    margin-bottom: 25px;
}

.header h1 {
    font-size: 46px;
    margin-bottom: 10px;
}

.header p {
    font-size: 22px;
    opacity: 0.9;
}

/* SECTION */

.section {
    background: white;
    padding: 35px;
    border-radius: 16px;
    margin-bottom: 30px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.05);
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
    border-radius: 12px;
    border-left: 5px solid #2a5298;
    height: 100%;
}

.card h3 {
    color: #1e3c72;
    margin-bottom: 10px;
}

/* HIGHLIGHT */

.highlight {
    background: #eef3fc;
    border: 1px solid #b8d1f3;
    padding: 20px;
    border-radius: 12px;
}

/* PARTNER */

.partner {
    background: #ececec;
    padding: 10px 18px;
    border-radius: 22px;
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
    border-radius: 20px 20px 0 0;
    margin-top: 40px;
}

/* BUTTONS */

.stButton>button {
    width: 100%;
    border-radius: 10px;
    border: none;
    background-color: #2a5298;
    color: white;
    font-weight: bold;
    padding: 10px;
}

.stButton>button:hover {
    background-color: #1e3c72;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# HEADER
# ==================================================

st.markdown("""
<div class="header">
    <h1>บริษัท เอเซี่ยน มินเนอรัล รีซอสเซส จำกัด</h1>
    <p>ASIAN MINERAL RESOURCES CO., LTD.</p>
</div>
""", unsafe_allow_html=True)

# ==================================================
# MENU
# ==================================================

menu = st.radio(
    "เมนู",
    [
        "เกี่ยวกับเรา",
        "จุดแข็ง",
        "ผลิตภัณฑ์",
        "พันธมิตร",
        "ติดต่อ"
    ],
    horizontal=True
)

# ==================================================
# ABOUT
# ==================================================

if menu == "เกี่ยวกับเรา":

    st.markdown('<div class="section">', unsafe_allow_html=True)

    st.markdown("""
    <div class="section-title">
    เกี่ยวกับเรา (About Us)
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2,1])

    with col1:
        st.write("""
บริษัท เอเซี่ยน มินเนอรัล รีซอสเซส จำกัด ก่อตั้งขึ้นในปี พ.ศ. 2527
ด้วยความมุ่งมั่นในการดำเนินธุรกิจด้านการทำเหมืองแร่ แต่งแร่
และประมวลผลแร่อุตสาหกรรมคุณภาพสูง

ตลอดระยะเวลากว่า 35 ปี บริษัทฯ ได้เติบโตอย่างมั่นคง
และได้รับความไว้วางใจจากลูกค้าระดับสากล
ทั้งในด้านคุณภาพสินค้าและความซื่อสัตย์ในการดำเนินธุรกิจ

ปัจจุบันบริษัทมีสัดส่วนการส่งออกกว่า 70%
ครอบคลุมภูมิภาคเอเชีย ตะวันออกกลาง แอฟริกา
และยุโรป
""")

    with col2:
        st.markdown("""
        <div class="highlight">

        <h4>🎖️ การรับรอง</h4>

        <ul>
            <li>ได้รับ BOI</li>
            <li>ใบอนุญาตแต่งแร่ถูกต้อง</li>
            <li>ผู้ส่งออกแร่แบร์ไรต์</li>
        </ul>

        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# STRENGTHS
# ==================================================

elif menu == "จุดแข็ง":

    st.markdown('<div class="section">', unsafe_allow_html=True)

    st.markdown("""
    <div class="section-title">
    จุดแข็งและศักยภาพ
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="card">

        <h3>🏭 ความเป็นเลิศด้านการผลิต</h3>

        <ul>
            <li>เครื่องจักรทันสมัย</li>
            <li>โรงงานมาตรฐาน</li>
            <li>ลานตากแร่กว่า 5,000 ตร.ม.</li>
            <li>ทีมงานมืออาชีพ</li>
        </ul>

        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">

        <h3>🌏 ความมั่นคงด้านตลาด</h3>

        <p>
        บริษัทมีแหล่งวัตถุดิบจากหลายประเทศ
        เช่น จีน และปากีสถาน
        พร้อมฐานลูกค้าทั่วโลก
        </p>

        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# PRODUCTS
# ==================================================

elif menu == "ผลิตภัณฑ์":

    st.markdown('<div class="section">', unsafe_allow_html=True)

    st.markdown("""
    <div class="section-title">
    ผลิตภัณฑ์หลัก
    </div>
    """, unsafe_allow_html=True)

    products = [
        (
            "BARYTES",
            "แร่แบร์ไรต์คุณภาพสูง ใช้ในอุตสาหกรรมสี พลาสติก และขุดเจาะน้ำมัน"
        ),
        (
            "TALC POWDER",
            "ผงทัลคัมเกรดพรีเมียม สำหรับสี พลาสติก ยาง และเครื่องสำอาง"
        ),
        (
            "DOLOMITE",
            "โดโลไมต์บริสุทธิ์สูง เหมาะสำหรับเซรามิกส์ และบรรจุภัณฑ์"
        ),
        (
            "CALCIUM CARBONATE",
            "แคลเซียมคาร์บอเนตคุณภาพสูง สำหรับกระดาษ สี และอุตสาหกรรมต่างๆ"
        )
    ]

    cols = st.columns(2)

    for i, product in enumerate(products):

        with cols[i % 2]:

            st.markdown(f"""
            <div class="card">

            <h3>{product[0]}</h3>

            <p>{product[1]}</p>

            </div>
            """, unsafe_allow_html=True)

            st.write("")

    st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# PARTNERS
# ==================================================

elif menu == "พันธมิตร":

    st.markdown('<div class="section">', unsafe_allow_html=True)

    st.markdown("""
    <div class="section-title">
    พันธมิตรระดับโลก
    </div>
    """, unsafe_allow_html=True)

    st.write("""
บริษัทได้รับความไว้วางใจจากองค์กรและแบรนด์ระดับโลก
มายาวนานกว่า 20 ปี
""")

    partners = [
        "JOTUN",
        "AKZO NOBEL",
        "SCHLUMBERGER",
        "SHELL",
        "PETRONAS",
        "CHEVRON",
        "BRENTAG",
        "OMYA"
    ]

    html = ""

    for p in partners:
        html += f'<span class="partner">{p}</span>'

    st.markdown(html, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# CONTACT
# ==================================================

elif menu == "ติดต่อ":

    st.markdown('<div class="section">', unsafe_allow_html=True)

    st.markdown("""
    <div class="section-title">
    ติดต่อเรา
    </div>
    """, unsafe_allow_html=True)

    st.write("""
📍 สำนักงานใหญ่  
256/1 ถนนนางลิ้นจี่ แขวงช่องนนทรี เขตยานนาวา กรุงเทพมหานคร

🏭 โรงงาน  
188 หมู่ 4 ตำบลหน้าพระลาน อำเภอเฉลิมพระเกียรติ จังหวัดสระบุรี

📞 โทรศัพท์: 02-XXX-XXXX

📧 Email: info@asianmineral.com
""")

    st.button("ติดต่อฝ่ายขาย")

    st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# FOOTER
# ==================================================

st.markdown("""
<div class="footer">

<p>
© บริษัท เอเซี่ยน มินเนอรัล รีซอสเซส จำกัด
</p>

<p>
ASIAN MINERAL RESOURCES CO., LTD.
</p>

</div>
""", unsafe_allow_html=True)
