# NovaTex O2C Simulator
### SAP SD Capstone Project — Order-to-Cash Working Model

**Student:** Mehul Shrivastava | **Roll No:** 23051680 | **Batch:** B.Tech CSE 2023–27

---

## About

An interactive web-based simulator demonstrating the complete **Order-to-Cash (O2C)** business cycle in SAP SD (Sales & Distribution). Built as a capstone project for the KIIT SAP Data Analytics course.

The app simulates all 7 stages of O2C for a fictional company — **NovaTex Industries Pvt. Ltd.** — processing a wholesale order from **Sharma Garments Pvt. Ltd.** for 500 units of cotton fabric.

---

## Project Structure

```
novatex_new/
├── frontend/
│   └── index.html       # Main UI — all styles & JS included
├── backend/
│   └── app.py           # Flask REST API
├── requirements.txt
└── README.md
```

---

## O2C Process Simulated

| Step | T-Code | Description |
|------|--------|-------------|
| 1 | VA11 | Create Inquiry |
| 2 | VA21 | Create Quotation |
| 3 | VA01 | Create Sales Order |
| 4 | VL01N | Outbound Delivery & PGI |
| 5 | VF01 | Billing / Invoice |
| 6 | F-28 | Post Incoming Payment |
| 7 | VA05/VF05/FBL5N/MB52 | Reports & Analytics |

---

## How to Run

### Option 1 — Frontend only (no server needed)
Just open `frontend/index.html` in any browser. Works completely offline.

### Option 2 — Full stack (with Flask backend)

**Step 1 — Create virtual environment**
```bash
python -m venv venv
```

**Step 2 — Activate it**
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

**Step 3 — Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 4 — Run Flask backend**
```bash
python backend/app.py
```

**Step 5 — Open frontend**
Open `frontend/index.html` in your browser.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Backend | Python 3, Flask, Flask-CORS |
| SAP Module | SAP SD (Sales & Distribution) |
| Process | Order-to-Cash (O2C) |

---

## Business Scenario

| Parameter | Value |
|-----------|-------|
| Company | NovaTex Industries Pvt. Ltd. |
| Customer | Sharma Garments Pvt. Ltd. |
| Material | COT-500 (Cotton Fabric) |
| Quantity | 500 units |
| Unit Price | ₹450 |
| Net Value | ₹2,25,000 |
| GST (18%) | ₹40,500 |
| Total Invoice | ₹2,65,500 |

---

## Documents
| File | Description |
|------|-------------|
| docs/NovaTex_O2C_Capstone_MehulShrivastava.pdf | Full project report (8 pages) |
| docs/O2C_Flowchart.png | O2C process flow diagram |

---

## License
This project is submitted for educational purposes — KIIT University SAP Capstone, April 2026.
