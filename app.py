import streamlit as st

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="ASIAN MINERAL RESOURCES CO., LTD.",
    layout="wide"
)

# โหลด CSS
with open("assets/style.css", "r", encoding="utf-8") as f:
    css = f.read()

st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# HTML Content
html_content = """
<header>
    <h1>บริษัท เอเซี่ยน มินเนอรัล รีซอสเซส จำกัด</h1>
    <p>ASIAN MINERAL RESOURCES CO., LTD.</p>
</header>

<nav>
    <a href="#about">เกี่ยวกับเรา</a>
    <a href="#strengths">จุดแข็งของเรา</a>
    <a href="#products">ผลิตภัณฑ์</a>
    <a href="#partners">พันธมิตรระดับโลก</a>
</nav>

<div class="container">

    <div id="about" class="section">
        <h2 class="section-title">เกี่ยวกับเรา (About Us)</h2>

        <div class="grid-2">

            <div>
                <p style="margin-bottom: 15px; text-indent: 30px;">
                    บริษัท เอเซี่ยน มินเนอรัล รีซอสเซส จำกัด ก่อตั้งขึ้นในปี พ.ศ. 2527
                    ด้วยความมุ่งมั่นในการดำเนินธุรกิจหลักด้านการทำเหมืองแร่
                    แต่งแร่ และประมวลผลแร่อุตสาหกรรมที่มีคุณภาพสูง
                </p>

                <p style="text-indent: 30px;">
                    ตลอดระยะเวลากว่า 35 ปีในอุตสาหกรรม บริษัทฯ ได้เติบโตอย่างต่อเนื่อง
                    และมั่นคง มีชื่อเสียงเป็นที่ยอมรับอย่างกว้างขวาง
                </p>
            </div>

            <div>
                <div class="highlight-box">
                    <strong>🎖️ การรับรองและความภาคภูมิใจ</strong>

                    <ul style="margin-top: 10px; padding-left: 20px;">
                        <li>ได้รับการส่งเสริมการลงทุนจาก BOI</li>
                        <li>ได้รับใบอนุญาตแต่งแร่อย่างถูกต้อง</li>
                        <li>เป็นผู้ส่งออกแร่แบร์ไรต์คุณภาพสูง</li>
                    </ul>
                </div>
            </div>

        </div>
    </div>

    <div id="strengths" class="section">

        <h2 class="section-title">จุดแข็งและศักยภาพของบริษัท</h2>

        <div class="grid-2">

            <div class="factory-info">
                <h3>🏭 ความเป็นเลิศทางการผลิตและโครงสร้างพื้นฐาน</h3>

                <ul>
                    <li>เทคโนโลยีทันสมัย</li>
                    <li>ระบบโรงงานมาตรฐาน</li>
                    <li>ลานตากแร่ขนาดใหญ่</li>
                    <li>ทีมงานมืออาชีพ</li>
                </ul>
            </div>

            <div>
                <h3>🌐 ความมั่นคงด้านวัตถุดิบและการตลาด</h3>

                <p>
                    บริษัทมีฐานการตลาดแข็งแกร่ง
                    ส่งออกสินค้าไปยังต่างประเทศทั่วโลก
                </p>
            </div>

        </div>

    </div>

    <div id="products" class="section">

        <h2 class="section-title">ผลิตภัณฑ์หลัก (Our Products)</h2>

        <div class="grid-4">

            <div class="card">
                <h3>1. BARYTES</h3>
                <p>แร่แบร์ไรต์คุณภาพสูง</p>
            </div>

            <div class="card">
                <h3>2. TALC POWDER</h3>
                <p>ผงทัลคัมเกรดพรีเมียม</p>
            </div>

            <div class="card">
                <h3>3. DOLOMITE</h3>
                <p>ผงโดโลไมต์คุณภาพสูง</p>
            </div>

            <div class="card">
                <h3>4. CALCIUM CARBONATE</h3>
                <p>แคลเซียมคาร์บอเนตเกรดแปรรูป</p>
            </div>

        </div>

    </div>

    <div id="partners" class="section">

        <h2 class="section-title">พันธมิตรระดับโลก</h2>

        <div class="partner-list">
            <span class="partner-item">JOTUN</span>
            <span class="partner-item">AKZO NOBEL</span>
            <span class="partner-item">SHELL</span>
            <span class="partner-item">PETRONAS</span>
            <span class="partner-item">BRENTAG</span>
        </div>

    </div>

</div>

<footer>
    <p>
        &copy; บริษัท เอเซี่ยน มินเนอรัล รีซอสเซส จำกัด
    </p>
</footer>
"""

st.markdown(html_content, unsafe_allow_html=True)
