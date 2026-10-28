import sys
from pathlib import Path
import shutil
from playwright.sync_api import sync_playwright
import fitz

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400;1,500;1,600&display=swap');

  @page {
    size: A4;
    margin: 8mm 12mm 8mm 12mm;
  }

  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    -webkit-font-smoothing: antialiased;
  }

  body {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    color: #1e293b;
    font-size: 9.3pt;
    line-height: 1.36;
    background: #ffffff;
  }

  a {
    color: #0284c7;
    text-decoration: none;
    font-weight: 500;
  }
  a:hover {
    text-decoration: underline;
  }

  /* Header */
  .header {
    text-align: center;
    margin-bottom: 6px;
    padding-bottom: 4px;
  }

  .header h1 {
    font-size: 21pt;
    font-weight: 800;
    letter-spacing: -0.4px;
    color: #0f172a;
    margin-bottom: 4px;
    line-height: 1.1;
  }

  .contact-bar {
    font-size: 9.1pt;
    color: #475569;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
    gap: 2px 6px;
  }

  .contact-bar span.sep {
    color: #94a3b8;
    font-weight: 300;
  }

  /* Section Title */
  .section-title {
    font-size: 10.2pt;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #0f172a;
    border-bottom: 1.5px solid #0284c7;
    padding-bottom: 2px;
    margin-top: 7px;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  /* Item Layouts */
  .item {
    margin-bottom: 5px;
  }

  .item-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
  }

  .item-title {
    font-weight: 700;
    font-size: 9.7pt;
    color: #0f172a;
  }

  .item-subtitle {
    font-weight: 500;
    color: #334155;
    font-size: 9.2pt;
  }

  .item-date, .item-location {
    font-size: 8.8pt;
    color: #64748b;
    font-weight: 500;
    white-space: nowrap;
  }

  .link-tag {
    font-size: 8.4pt;
    font-weight: 600;
    color: #0284c7;
    background: #f0f9ff;
    padding: 1px 5px;
    border-radius: 4px;
    border: 1px solid #bae6fd;
    margin-left: 4px;
  }

  .tech-stack {
    font-size: 8.8pt;
    color: #475569;
    font-style: italic;
    margin-top: 1px;
    margin-bottom: 2px;
  }

  ul {
    list-style-type: none;
    padding-left: 0;
    margin-top: 2px;
  }

  li {
    position: relative;
    padding-left: 14px;
    margin-bottom: 2px;
    font-size: 9.1pt;
    color: #1e293b;
    line-height: 1.34;
  }

  li::before {
    content: "•";
    position: absolute;
    left: 3px;
    top: -0.5px;
    color: #0284c7;
    font-size: 11pt;
  }

  /* Skills Section */
  .skills-box {
    display: flex;
    flex-direction: column;
    gap: 2.5px;
    font-size: 9.1pt;
  }

  .skills-row {
    display: flex;
    line-height: 1.34;
  }

  .skills-label {
    font-weight: 700;
    color: #0f172a;
    min-width: 140px;
  }

  .skills-val {
    color: #334155;
    flex: 1;
  }

  /* Achievements */
  .ach-title {
    font-weight: 700;
    color: #0f172a;
  }
</style>
</head>
<body>

  <!-- Header -->
  <div class="header">
    <h1>Harshit Mangal</h1>
    <div class="contact-bar">
      <span>+91-7413021531</span>
      <span class="sep">|</span>
      <a href="mailto:mangalharsh54@gmail.com">mangalharsh54@gmail.com</a>
      <span class="sep">|</span>
      <a href="https://harshitmangal.github.io/portfolio/">Portfolio</a>
      <span class="sep">|</span>
      <a href="https://linkedin.com/in/harshit-mangal">LinkedIn</a>
      <span class="sep">|</span>
      <a href="https://github.com/HarshitMangal">GitHub</a>
      <span class="sep">|</span>
      <a href="https://leetcode.com/u/Harshit_mangal/">LeetCode</a>
    </div>
  </div>

  <!-- Education -->
  <div class="section-title">Education</div>
  <div class="item">
    <div class="item-row">
      <span class="item-title">MBM University</span>
      <span class="item-date">Aug. 2023 – May 2027</span>
    </div>
    <div class="item-row">
      <span class="item-subtitle">Bachelor of Technology in Information Technology — <strong>CGPA: 7.2</strong></span>
      <span class="item-location">Jodhpur, Rajasthan</span>
    </div>
  </div>

  <!-- Technical Skills -->
  <div class="section-title">Technical Skills</div>
  <div class="skills-box">
    <div class="skills-row">
      <span class="skills-label">Languages:</span>
      <span class="skills-val">C++, Python, C, Java, JavaScript, SQL</span>
    </div>
    <div class="skills-row">
      <span class="skills-label">Web Development:</span>
      <span class="skills-val">HTML5, CSS3, React, Node.js, Express, Tailwind CSS, RESTful APIs</span>
    </div>
    <div class="skills-row">
      <span class="skills-label">Databases & Tools:</span>
      <span class="skills-val">MongoDB, MySQL, SQLite, Git, GitHub, Postman, Linux</span>
    </div>
    <div class="skills-row">
      <span class="skills-label">Core Fundamentals:</span>
      <span class="skills-val">Data Structures & Algorithms, OOPs, DBMS, Operating Systems, Computer Networks</span>
    </div>
  </div>

  <!-- Projects -->
  <div class="section-title">Projects</div>

  <div class="item">
    <div class="item-row">
      <div>
        <span class="item-title">ShopSphere — E-Commerce Web Application</span>
        <a href="https://flipcart-clone-mu.vercel.app" class="link-tag">Live Demo ↗</a>
        <a href="https://github.com/HarshitMangal/Flipcart-Clone" class="link-tag">GitHub ↗</a>
      </div>
      <span class="item-date">2026</span>
    </div>
    <div class="tech-stack">React, Node.js, Express, MongoDB, Redux, Razorpay</div>
    <ul>
      <li>Built a responsive full-stack e-commerce web platform featuring user authentication, product search, category filtering, and shopping cart management.</li>
      <li>Implemented RESTful backend APIs for catalog and order workflows; integrated Razorpay payment gateway for secure checkout processing.</li>
    </ul>
  </div>

  <div class="item">
    <div class="item-row">
      <div>
        <span class="item-title">AI Document Assistant — Offline Q&A System</span>
        <a href="https://github.com/HarshitMangal/AI-Document-Chatbot" class="link-tag">GitHub ↗</a>
      </div>
      <span class="item-date">2026</span>
    </div>
    <div class="tech-stack">Python, Streamlit, Ollama, FAISS, PyMuPDF</div>
    <ul>
      <li>Engineered an interactive local document Q&A assistant allowing users to upload PDF documents and ask queries in natural language completely offline.</li>
      <li>Extracted document text with PyMuPDF, generated vector embeddings, and implemented fast similarity search using FAISS for accurate answer retrieval.</li>
    </ul>
  </div>

  <div class="item">
    <div class="item-row">
      <div>
        <span class="item-title">Wanderlust — Rental Property SaaS</span>
        <a href="https://major-project-wht3.onrender.com" class="link-tag">Live Demo ↗</a>
        <a href="https://github.com/HarshitMangal/major_project" class="link-tag">GitHub ↗</a>
      </div>
      <span class="item-date">2025</span>
    </div>
    <div class="tech-stack">React, Node.js, Express, MongoDB, Cloudinary</div>
    <ul>
      <li>Built an Airbnb-style accommodation booking platform with user authentication, property listings, and an interactive review system.</li>
      <li>Integrated Cloudinary for image optimization and cloud storage; structured clean MVC architecture with MongoDB for data persistence.</li>
    </ul>
  </div>

  <!-- Experience -->
  <div class="section-title">Experience</div>
  <div class="item">
    <div class="item-row">
      <span class="item-title">Frontend Web Development Intern</span>
      <span class="item-date">June 2025 – July 2025</span>
    </div>
    <div class="item-row">
      <span class="item-subtitle">CodTech IT Solutions Pvt. Ltd.</span>
      <span class="item-location">Remote</span>
    </div>
    <ul>
      <li>Designed and developed responsive, mobile-first web interfaces for user-facing applications using HTML5, CSS3, JavaScript, and React.</li>
      <li>Collaborated using Git version control, integrated backend REST APIs, and optimized frontend components for enhanced performance.</li>
    </ul>
  </div>

  <!-- Achievements -->
  <div class="section-title">Achievements</div>
  <ul>
    <li><span class="ach-title"><a href="https://leetcode.com/u/Harshit_mangal/">LeetCode Knight</a>:</span> Earned Knight Badge with peak rating 1905–1931 (Top 3.8% globally, 1350+ DSA problems solved).</li>
    <li><span class="ach-title"><a href="https://auth.geeksforgeeks.org/user/harshitmangal">GeeksforGeeks College Rank 1</a>:</span> Ranked #1 across MBM University with 1100+ coding problems solved.</li>
    <li><span class="ach-title"><a href="https://www.wemakedevs.org/certificates/VA2N7YMWDX">Winner — Environmental Hacks</a>:</span> 1st Place Winner at national hackathon organized by WeMakeDevs & AWS.</li>
    <li><span class="ach-title">Amazon ML Challenge:</span> Secured All India Rank 165 competing against teams nationwide.</li>
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
    preview_img = Path("C:/Users/Lenovo/OneDrive/Desktop/harshit-portfolio/resume_preview.png")

    print("Generating modern executive resume PDF...")

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

    shutil.copy(dest_portfolio, dest_portfolio_latest)
    shutil.copy(dest_portfolio, dest_desktop)

    # Render image preview to inspect visual quality
    doc = fitz.open(str(dest_portfolio))
    print(f"Total pages: {len(doc)}")
    for page_idx in range(len(doc)):
        page = doc[page_idx]
        pix = page.get_pixmap(dpi=150)
        pix.save(str(preview_img))
        print(f"Saved preview of page {page_idx+1} to {preview_img}")

    print("SUCCESS! Generated executive resume!")

if __name__ == "__main__":
    generate_pdf()
