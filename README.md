# LedgerPulse  — Autonomous Treasury & Billing OS

[![GitHub release](https://img.shields.io/badge/release-v1.0.0-blue.svg)](https://github.com/Aishwarya-369/LedgerPulse/releases)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PayPal](https://img.shields.io/badge/PayPal-Orders_v2_Rails-00457C?logo=paypal&logoColor=white)](https://developer.paypal.com/)
[![Google Gemini](https://img.shields.io/badge/AI-Google_Gemini_1.5-8E75C2?logo=google&logoColor=white)](https://ai.google.dev/)

An autonomous financial operating system unifying conversational Google Gemini AI billing intelligence, real-time multi-currency VAT compliance, dynamic milestone splitting, and instant settlement rails powered by PayPal.

---

## 🌟 Core Architecture & Key Features

* **🎙️ Voice-to-Invoice Dictation:** Real-time Web Speech recognition capturing natural commercial terms, converting spoken parameters directly into structured invoice data.
* **⚡ Gemini Fiscal Intelligence:** Leverages Google Gemini to parse ambiguous commercial instructions, auto-extract client billing entities, calculate line-item breakdowns, and resolve foreign VAT rules dynamically.
* **💳 Dynamic Settlement Rails:** Features an interactive billing toggle supporting 100% full settlement alongside a dynamic 50% milestone retainer split, re-rendering live PayPal Smart Payment buttons on the fly.
* **📲 Omnichannel Dispatch:**
  * **Scan-to-Pay QR Modal:** Real-time mobile checkout QR code generation for instant terminal payment.
  * **WhatsApp Integration:** Deep-linked direct dispatch populated with transaction identifiers and amounts.
  * **Corporate Mailer:** Automated generation of formal corporate billing notifications.
* **📊 Continuous Audit Register:** Local SQLite audit ledger recording transaction states, timestamps, order IDs, and gross tax sums with one-click enterprise CSV export.
* **🔒 Enterprise Onboarding & Security:** Standalone authentication suite with client-side credential verification, format validation, and session state retention.

---

## 🛠️ Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Backend** | Python 3.11+, FastAPI, Uvicorn, SQLite3 |
| **Intelligence** | Google Gemini API (`google-genai` / `gemini-1.5-flash`) |
| **Settlement** | PayPal REST Orders v2 API & PayPal Smart Payment Buttons SDK (Sandbox) |
| **Frontend** | Semantic HTML5, Tailwind CSS, Modern Vanilla ES6 JavaScript |
| **Progressive Web App** | Service Worker (`sw.js`), Web App Manifest (`manifest.json`) |

---

## 📁 Repository Structure

```text
LedgerPulse/
├── backend/
│   ├── app/
│   │   ├── routers/
│   │   │   └── api.py              # FastAPI endpoints for billing, PayPal, and ledger
│   │   ├── services/
│   │   │   ├── db_service.py       # SQLite transaction models and operations
│   │   │   ├── gemini_service.py   # Google Gemini prompt engineering & parsing
│   │   │   └── paypal_service.py   # PayPal Orders v2 token & order execution
│   │   └── config.py               # Settings and environment bindings
│   └── main.py                     # FastAPI application entry point & static routes
├── frontend/
│   ├── js/
│   │   └── app.js                  # Speech recognition, PayPal SDK, and UI state
│   ├── static/
│   │   └── icons/                  # Vector assets and PWA pulse icons
│   ├── index.html                  # Core operational billing console
│   ├── landing.html                # Product showcase and overview
│   ├── login.html                  # Corporate authentication and access portal
│   ├── manifest.json               # Web application manifest configuration
│   └── sw.js                       # Service worker caching and offline handler
├── make_icon.py                    # Programmatic icon generation script
├── requirements.txt                # Production dependency declarations
└── README.md                       # System documentation
