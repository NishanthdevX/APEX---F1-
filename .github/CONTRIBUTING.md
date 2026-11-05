# Contributing to APEX // F1

Thank you for your interest in contributing to **APEX // F1** — the Formula 1 World Championship (1950–2026) Multi-Mode Analytics & Real-Time Strategy Platform.

This project is built under the **GNU General Public License v3.0 (GPL-3.0)** and adheres to strict **Data Analysis & Visualization (DAV)** engineering standards.

---

## 🏛️ Architecture Overview

The codebase is structured into three unified layers:
1. **Frontend & Reactive UI:** Pure Python with [Reflex](https://reflex.dev) and [Plotly](https://plotly.com/python/).
2. **High-Speed Relational Joins:** [Polars](https://pola.rs) for multi-table relational processing in `<50ms`.
3. **Statistical Modeling:** [Rscript](https://www.r-project.org/) (`r_analytics/f1_statistical_engine.R`) with automated Polars fallback for Within-Season Z-Score era normalization and ANOVA hypothesis testing.

---

## 🛠️ Development Setup

### 1. Prerequisites
- **Python 3.10+** (Tested on Python 3.11, 3.12, and 3.14)
- **R (Optional, Recommended):** `Rscript` available in PATH.
- **Node / Bun:** Managed automatically by Reflex.

### 2. Local Installation
```bash
# Clone the repository
git clone https://github.com/NishanthdevX/APEX-F1.git
cd APEX-F1

# Create and activate virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Running Locally
```bash
python -m reflex run
```
- Frontend UI: `http://localhost:3000`
- Backend API: `http://localhost:8001`

---

## 📐 DAV Design Principles

Every visualization added to APEX-F1 must adhere to the following:
1. **Takeaway Titles:** State the insight or finding (e.g. *"Ferrari and McLaren lead cumulative victories"*), never just a generic axis label.
2. **Explicit Subtitles:** Always disclose the unit of measurement, the time period, and the exact source file in `Dataset/`.
3. **Zero Collision:** Legends must never collide with data bars or lines. Place legends above plots with ample top margin, or use direct labels on bars when $\le 10$ series are shown.
4. **Hick's Law:** Limit categorical series to $\le 10$. Group remaining entries into "Other".
5. **Color Consistency:**
   - Ferrari: `#E10600`
   - McLaren: `#FF8000`
   - Mercedes: `#00D2BE`
   - Red Bull: `#3B82F6`
   - Williams: `#64C4FF`
   - Lotus: `#F59E0B`
   - Other / Neutral: `#64748B`

---

## 🧪 Testing Checklist Before Submitting a PR
Before submitting a pull request, run:
```bash
# 1. Verify R and Polars statistical pipelines
python test_f1_engine.py

# 2. Test full Reflex compilation
python -m reflex compile
```
Ensure all tests pass and your changes satisfy the PR template checklist.

