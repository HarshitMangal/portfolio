import sys
from pathlib import Path
import shutil
from playwright.sync_api import sync_playwright

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=EB+Garamond:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Lora:ital,wght@0,400;0,600;0,700;1,400;1,600&display=swap');

  @page {
    size: A4;
    margin: 10mm 12mm 10mm 12mm;
  }

  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  body {
    font-family: 'EB Garamond', 'Lora', 'Times New Roman', Georgia, serif;
    color: #000000;
    font-size: 9.6pt;
    line-height: 1.28;
    background: #ffffff;
  }

  a {
    color: #000000;
    text-decoration: underline;
  }

  /* Jake's Header */
  .header {
    text-align: center;
    margin-bottom: 4px;
  }

  .header h1 {
    font-size: 23pt;
    font-weight: 700;
    font-variant: small-caps;
    letter-spacing: 0.5px;
    margin-bottom: 2px;
    line-height: 1.1;
  }

  .contact-bar {
    font-size: 9.2pt;
    color: #111;
  }

  .contact-bar span {
    margin: 0 4px;
    color: #333;
  }

  /* Jake's Section Title */
  .section-title {
    font-size: 11.2pt;
    font-weight: 700;
    font-variant: small-caps;
    letter-spacing: 0.4px;
    color: #000000;
    border-bottom: 0.8px solid #000000;
    padding-bottom: 1px;
    margin-top: 6px;
    margin-bottom: 3px;
  }

  /* Subheadings & Project Headings */
  .item {
    margin-bottom: 4px;
  }

  .item-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    font-size: 9.7pt;
  }

  .item-title {
    font-weight: 700;
    color: #000000;
  }

  .item-subtitle {
    font-style: italic;
    color: #111;
    font-size: 9.2pt;
  }

  .item-date, .item-location {
    font-size: 9.2pt;
    color: #111;
  }

  .tech-inline {
    font-style: italic;
    font-weight: 400;
  }

  ul {
    list-style-type: disc;
    margin-left: 17px;
    margin-top: 1.5px;
  }

  li {
    margin-bottom: 1.2px;
    font-size: 9.3pt;
    color: #111;
    line-height: 1.26;
  }

  .skills-list {
    font-size: 9.3pt;
    line-height: 1.32;
    padding-left: 2px;
  }

  .skills-row {
    margin-bottom: 1.5px;
  }

  .skills-label {
    font-weight: 700;
  }
</style>
</head>
<body>

  <!-- Header -->
  <div class="header">
    <h1>Harshit Mangal</h1>
    <div class="contact-bar">
      +91-7413021531
      <span>|</span>
      <a href="mailto:mangalharsh54@gmail.com">mangalharsh54@gmail.com</a>
      <span>|</span>
      <a href="https://harshitmangal.github.io/portfolio/">Portfolio</a>
      <span>|</span>
      <a href="https://linkedin.com/in/harshit-mangal">LinkedIn</a>
      <span>|</span>
      <a href="https://github.com/HarshitMangal">GitHub</a>
      <span>|</span>
      <a href="https://leetcode.com/u/Harshit_mangal/">LeetCode</a>
    </div>
  </div>

  <!-- Education -->
  <div class="section-title">Education</div>
  <div class="item">
    <div class="item-header">
      <span class="item-title">MBM University</span>
      <span class="item-location">Jodhpur, Rajasthan</span>
    </div>
    <div class="item-header">
      <span class="item-subtitle">Bachelor of Technology in Information Technology — CGPA: 7.2</span>
      <span class="item-date">Aug. 2023 – May 2027</span>
    </div>
  </div>

  <!-- Technical Skills -->
  <div class="section-title">Technical Skills</div>
  <div class="skills-list">
    <div class="skills-row"><span class="skills-label">Languages:</span> C++, Python, C, Java, JavaScript, SQL</div>
    <div class="skills-row"><span class="skills-label">Web Development:</span> HTML, CSS, React, Node.js, Express, Tailwind CSS, RESTful APIs</div>
    <div class="skills-row"><span class="skills-label">Databases & Tools:</span> MongoDB, MySQL, SQLite, Git, GitHub, Postman, Linux</div>
    <div class="skills-row"><span class="skills-label">Core Concepts:</span> Data Structures & Algorithms, OOPs, DBMS, Operating Systems, Computer Networks</div>
  </div>

  <!-- Projects -->
  <div class="section-title">Projects</div>

  <div class="item">
    <div class="item-header">
      <span>
        <strong class="item-title">ShopSphere</strong>
        <span> | </span>
        <span class="tech-inline">React, Node.js, Express, MongoDB, Redux, Razorpay</span>
      </span>
      <span class="item-date">2026</span>
    </div>
    <ul>
      <li>Developed a full-stack e-commerce web application featuring user authentication, product search, filtering, and shopping cart management.</li>
      <li>Implemented RESTful APIs for catalog and order handling; integrated Razorpay payment gateway for secure checkout processing.</li>
    </ul>
  </div>

  <div class="item">
    <div class="item-header">
      <span>
        <strong class="item-title">AI Document Assistant</strong>
        <span> | </span>
        <span class="tech-inline">Python, Streamlit, Ollama, FAISS, PyMuPDF</span>
      </span>
      <span class="item-date">2026</span>
    </div>
    <ul>
      <li>Built an interactive local document Q&A tool allowing users to upload PDF documents and query contents offline using local LLMs.</li>
      <li>Extracted text with PyMuPDF, generated vector embeddings, and implemented fast similarity search using FAISS for accurate retrieval.</li>
    </ul>
  </div>

  <div class="item">
    <div class="item-header">
      <span>
        <strong class="item-title">Wanderlust</strong>
        <span> | </span>
        <span class="tech-inline">React, Node.js, Express, MongoDB, Cloudinary</span>
      </span>
      <span class="item-date">2025</span>
    </div>
    <ul>
      <li>Built a responsive rental property listing web application with user authentication, property creation, and user review system.</li>
      <li>Integrated Cloudinary for optimized media management and designed clean MVC architecture with MongoDB for data persistence.</li>
    </ul>
  </div>

  <!-- Experience -->
  <div class="section-title">Experience</div>
  <div class="item">
    <div class="item-header">
      <span class="item-title">Frontend Web Development Intern</span>
      <span class="item-date">June 2025 – July 2025</span>
    </div>
    <div class="item-header">
      <span class="item-subtitle">CodTech IT Solutions Pvt. Ltd.</span>
      <span class="item-location">Remote</span>
    </div>
    <ul>
      <li>Designed and developed responsive, cross-browser web interfaces for user-facing applications using HTML5, CSS3, JavaScript, and React.</li>
      <li>Collaborated with senior developers using Git version control, integrated backend REST APIs, and improved page load performance.</li>
    </ul>
  </div>

  <!-- Achievements -->
  <div class="section-title">Achievements</div>
  <ul>
    <li><strong><a href="https://leetcode.com/u/Harshit_mangal/">LeetCode Knight</a>:</strong> Rating 1905–1931 (Top 3.8% globally, 1350+ DSA problems solved).</li>
    <li><strong><a href="https://auth.geeksforgeeks.org/user/harshitmangal">GeeksforGeeks College Rank 1</a>:</strong> Ranked #1 in MBM University with 1100+ coding problems solved.</li>
    <li><strong><a href="https://www.wemakedevs.org/certificates/VA2N7YMWDX">Winner — Environmental Hacks</a>:</strong> Winner at national hackathon organized by WeMakeDevs & AWS.</li>
    <li><strong>Amazon ML Challenge:</strong> Secured All India Rank 165 competing against teams across India.</li>
  </ul>

  <!-- Certifications -->
  <div class="section-title">Certifications</div>
  <ul>
    <li><a href="https://media.geeksforgeeks.org/courses/certificates/22a599fc4a5676f802aa4a2ee4cc3c7f.pdf">160 Days of Problem Solving</a> — GeeksforGeeks (2025)</li>
    <li><a href="https://www.hackerrank.com/certificates/227251652361">Problem Solving (Intermediate)</a> & <a href="https://www.hackerrank.com/certificates/9fe36f33fe64">Problem Solving (Basic)</a> — HackerRank (2026)</li>
  </ul>

</body>
</html>
"""

def generate_pdf():
    dest_portfolio = Path("C:/Users/Lenovo/OneDrive/Desktop/harshit-portfolio/Harshit_Mangal_Resume.pdf")
    dest_portfolio_latest = Path("C:/Users/Lenovo/OneDrive/Desktop/harshit-portfolio/Harshit_Mangal_Resume_Latest.pdf")
    dest_desktop = Path("C:/Users/Lenovo/OneDrive/Desktop/Harshit_Mangal_Resume.pdf")

    print("Generating Jake's Resume PDF...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_content(HTML_TEMPLATE, wait_until="networkidle")

        page.pdf(
            path=str(dest_portfolio),
            format="A4",
            print_background=True,
            prefer_css_page_size=True
        )
        browser.close()

    # Also copy to Latest and Desktop
    shutil.copy(dest_portfolio, dest_portfolio_latest)
    shutil.copy(dest_portfolio, dest_desktop)

    print(f"SUCCESS! Jake's Resume generated and copied to all locations!")

if __name__ == "__main__":
    generate_pdf()
