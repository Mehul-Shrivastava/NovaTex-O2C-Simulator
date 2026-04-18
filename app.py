from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# ── In-memory store for simulation state ──────────────────────
simulation_state = {
    "current_step": 0,
    "documents": {}
}

# ── Document number counters ───────────────────────────────────
doc_counters = {
    "inquiry": 1,
    "quotation": 1,
    "sales_order": 1,
    "delivery": 1,
    "invoice": 1,
    "payment": 1
}

# ── ROUTES ────────────────────────────────────────────────────

@app.route("/")
def index():
    return jsonify({
        "app": "NovaTex O2C Simulator",
        "version": "1.0",
        "status": "running",
        "company": "NovaTex Industries Pvt. Ltd.",
        "module": "SAP SD — Order-to-Cash"
    })

@app.route("/api/status", methods=["GET"])
def get_status():
    return jsonify({
        "current_step": simulation_state["current_step"],
        "documents": simulation_state["documents"],
        "timestamp": datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    })

@app.route("/api/step/inquiry", methods=["POST"])
def create_inquiry():
    data = request.json or {}
    doc_id = f"INQ-2026-{doc_counters['inquiry']:03d}"
    doc_counters["inquiry"] += 1
    simulation_state["documents"]["inquiry"] = doc_id
    simulation_state["current_step"] = 1
    return jsonify({
        "success": True,
        "document": doc_id,
        "message": f"Inquiry {doc_id} created successfully",
        "data": {
            "inquiry_type": "IN",
            "customer": data.get("customer", "Sharma Garments Pvt. Ltd."),
            "material": data.get("material", "COT-500"),
            "quantity": data.get("quantity", 500),
            "sales_org": "NVTX_SO"
        }
    })

@app.route("/api/step/quotation", methods=["POST"])
def create_quotation():
    data = request.json or {}
    doc_id = f"QT-2026-{doc_counters['quotation']:03d}"
    doc_counters["quotation"] += 1
    simulation_state["documents"]["quotation"] = doc_id
    simulation_state["current_step"] = 2
    return jsonify({
        "success": True,
        "document": doc_id,
        "message": f"Quotation {doc_id} saved successfully",
        "data": {
            "quotation_type": "QT",
            "reference_inquiry": simulation_state["documents"].get("inquiry", "INQ-2026-001"),
            "unit_price": 450.00,
            "quantity": 500,
            "net_value": 225000.00,
            "validity_days": 30,
            "payment_terms": "NET30"
        }
    })

@app.route("/api/step/sales-order", methods=["POST"])
def create_sales_order():
    data = request.json or {}
    doc_id = f"SO-2026-{1089 + doc_counters['sales_order'] - 1}"
    doc_counters["sales_order"] += 1
    simulation_state["documents"]["sales_order"] = doc_id

    # Simulate credit check
    credit_limit = 500000
    order_value = 265500
    credit_ok = order_value <= credit_limit

    simulation_state["current_step"] = 3
    return jsonify({
        "success": True,
        "document": doc_id,
        "message": f"Sales Order {doc_id} created — Credit check PASSED",
        "data": {
            "order_type": "OR",
            "reference_quotation": simulation_state["documents"].get("quotation", "QT-2026-042"),
            "customer": "Sharma Garments Pvt. Ltd.",
            "material": "COT-500",
            "quantity": 500,
            "net_value": 225000.00,
            "credit_check": "PASSED" if credit_ok else "BLOCKED",
            "delivery_date": "28.04.2026"
        }
    })

@app.route("/api/step/delivery", methods=["POST"])
def create_delivery():
    doc_id = f"DEL-2026-{5521 + doc_counters['delivery'] - 1}"
    doc_counters["delivery"] += 1
    simulation_state["documents"]["delivery"] = doc_id
    simulation_state["current_step"] = 4
    return jsonify({
        "success": True,
        "document": doc_id,
        "message": f"Delivery {doc_id} — PGI posted successfully",
        "data": {
            "delivery_type": "LF",
            "reference_so": simulation_state["documents"].get("sales_order", "SO-2026-1089"),
            "plant": "NV01",
            "storage_location": "SL01",
            "picked_quantity": 500,
            "pgi_date": "28.04.2026",
            "accounting": {
                "debit": {"account": "Cost of Goods Sold", "amount": 150000},
                "credit": {"account": "Finished Goods Inventory", "amount": 150000}
            }
        }
    })

@app.route("/api/step/billing", methods=["POST"])
def create_billing():
    doc_id = f"INV-2026-{9901 + doc_counters['invoice'] - 1}"
    doc_counters["invoice"] += 1
    net_value = 225000
    gst = round(net_value * 0.18)
    total = net_value + gst
    simulation_state["documents"]["invoice"] = doc_id
    simulation_state["current_step"] = 5
    return jsonify({
        "success": True,
        "document": doc_id,
        "message": f"Invoice {doc_id} posted — AR debited ₹{total:,}",
        "data": {
            "billing_type": "F2",
            "reference_delivery": simulation_state["documents"].get("delivery", "DEL-2026-5521"),
            "net_value": net_value,
            "gst_18_percent": gst,
            "total_value": total,
            "due_date": "28.05.2026",
            "accounting": {
                "debit": {"account": "Accounts Receivable", "amount": total},
                "credits": [
                    {"account": "Revenue", "amount": net_value},
                    {"account": "GST Payable", "amount": gst}
                ]
            }
        }
    })

@app.route("/api/step/payment", methods=["POST"])
def post_payment():
    doc_id = f"PAY-2026-{3301 + doc_counters['payment'] - 1}"
    doc_counters["payment"] += 1
    amount = 265500
    simulation_state["documents"]["payment"] = doc_id
    simulation_state["current_step"] = 6
    return jsonify({
        "success": True,
        "document": doc_id,
        "message": f"Payment {doc_id} posted — Invoice fully cleared",
        "data": {
            "document_type": "DZ",
            "amount_received": amount,
            "payment_method": "NEFT",
            "reference_invoice": simulation_state["documents"].get("invoice", "INV-2026-9901"),
            "clearing_status": "FULLY CLEARED",
            "ar_balance": 0,
            "accounting": {
                "debit": {"account": "Bank Account (HDFC)", "amount": amount},
                "credit": {"account": "Accounts Receivable", "amount": amount}
            }
        }
    })

@app.route("/api/reports/sales-orders", methods=["GET"])
def report_sales_orders():
    return jsonify({
        "report": "VA05 — Sales Order List",
        "data": [
            {"so": "SO-2026-1089", "customer": "Sharma Garments", "material": "COT-500",
             "qty": 500, "net_value": 225000, "status": "Completed"},
            {"so": "SO-2026-1085", "customer": "Rathi Textiles", "material": "WOL-200",
             "qty": 200, "net_value": 80000, "status": "Completed"},
            {"so": "SO-2026-1091", "customer": "Delhi Fabrics", "material": "LIN-100",
             "qty": 300, "net_value": 120000, "status": "In Progress"},
        ]
    })

@app.route("/api/reports/billing", methods=["GET"])
def report_billing():
    return jsonify({
        "report": "VF05 — Billing Document List",
        "total_revenue": 425000,
        "data": [
            {"invoice": "INV-2026-9901", "customer": "Sharma Garments",
             "net": 225000, "gst": 40500, "total": 265500, "status": "Cleared"},
            {"invoice": "INV-2026-9895", "customer": "Rathi Textiles",
             "net": 80000, "gst": 14400, "total": 94400, "status": "Cleared"},
            {"invoice": "INV-2026-9908", "customer": "Delhi Fabrics",
             "net": 120000, "gst": 21600, "total": 141600, "status": "Open"},
        ]
    })

@app.route("/api/reports/stock", methods=["GET"])
def report_stock():
    return jsonify({
        "report": "MB52 — Warehouse Stock Overview",
        "plant": "NV01",
        "data": [
            {"material": "COT-500", "description": "Cotton Fabric", "stock": 300, "uom": "UN"},
            {"material": "WOL-200", "description": "Wool Blend",    "stock": 150, "uom": "UN"},
            {"material": "LIN-100", "description": "Linen Premium", "stock": 420, "uom": "UN"},
            {"material": "SLK-050", "description": "Silk Grade A",  "stock": 80,  "uom": "UN"},
        ]
    })

@app.route("/api/reset", methods=["POST"])
def reset():
    simulation_state["current_step"] = 0
    simulation_state["documents"] = {}
    return jsonify({"success": True, "message": "Simulation reset"})

# ── RUN ────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("  NovaTex O2C Simulator — Flask Backend")
    print("  Running on: http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, port=5000)
