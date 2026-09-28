# Sales KPI Dashboard (Streamlit Web App)

An interactive analytics **web application** built with Streamlit — filterable
KPI cards, time-series and breakdown charts, and a detail table. This is the
kind of self-service, browser-based dashboard I build to complement Power BI,
demonstrating my web-app development with full interactivity.

![web app](https://img.shields.io/badge/type-web%20app-brightgreen)

## Run it
```bash
pip install -r requirements.txt
streamlit run app.py
```
Then open the local URL Streamlit prints (usually http://localhost:8501).

## Structure
- `data.py` — data generation + KPI logic (importable / testable)
- `app.py` — Streamlit UI layer

## Stack
`streamlit` · `pandas` · `numpy`

---
Part of my portfolio — [github.com/syedjawaadali](https://github.com/syedjawaadali)
