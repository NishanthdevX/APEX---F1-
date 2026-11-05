<div align="center">

# 🏎️ APEX // F1

### Formula 1 World Championship Analytics & Race Strategy Platform

**An interactive data analysis and visualization platform exploring Formula 1 history from 1950 to 2026.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![R](https://img.shields.io/badge/Statistics-R-276DC3?logo=r&logoColor=white)](https://www.r-project.org/)
[![Reflex](https://img.shields.io/badge/Web%20App-Reflex-000000?logo=reflex&logoColor=white)](https://reflex.dev/)
[![Polars](https://img.shields.io/badge/Data%20Processing-Polars-CD792C?logo=polars&logoColor=white)](https://pola.rs/)
[![Plotly](https://img.shields.io/badge/Visualization-Plotly-3F4F75?logo=plotly&logoColor=white)](https://plotly.com/)
[![License](https://img.shields.io/badge/License-GPL--3.0-blue.svg)](LICENSE)

[Overview](#overview) · [Features](#key-features) · [Tech Stack](#technology-stack) · [Architecture](#system-architecture) · [Methodology](#statistical-methodology) · [Dataset](#dataset) · [Getting Started](#getting-started)

</div>

---

## <a id="overview"></a>📌 Overview

**APEX // F1** is an interactive Formula 1 data analysis and visualization platform built to explore more than seven decades of motorsport history. It transforms historical race data into an analytical experience where users can investigate driver performance, constructor dominance, circuit history, lap-time behaviour, and race-strategy trade-offs.

The project brings together two complementary parts of the data stack:

- **R powers the statistical engine** — performing statistical calculations and analysis such as within-season Z-score normalization, trend estimation, and hypothesis testing.
- **Python and Reflex power the application** — coordinating the data pipeline, managing application state, and presenting the results through an interactive web interface.

Python's data ecosystem, including **Polars**, supports efficient tabular processing and relational joins (`<50ms`). **Plotly** provides interactive charts with zero legend collisions, while **Rich** is used to create terminal-style telemetry output that can be rendered as SVG.

Rather than treating Formula 1 statistics as isolated records, APEX // F1 connects the data to questions such as:

- How can a driver's performance be compared across seasons with different points systems?
- Which constructors have dominated particular periods of Formula 1 history?
- How have lap-time distributions changed across engine eras?
- Which circuits have hosted the most races?
- How do fuel load and tyre degradation influence a simulated race stint?

> **Project focus:** Data analysis, statistical computing, data engineering, and interactive visualization — brought together in a Formula 1-themed analytical platform.

---

## ✨ Project Highlights

| Area | What the project explores |
|---|---|
| **Historical analysis** | Formula 1 race, driver, constructor, and championship data across 1950–2026 |
| **Driver comparison** | Season-normalized performance, career wins, and a composite dominance index |
| **Constructor analysis** | Season victories, historical win share, dynasties, and decade-level consistency |
| **Lap-time analysis** | Lap pace distributions, outlier filtering, and comparisons across engine eras |
| **Circuit analysis** | Circuit longevity, race-hosting frequency, and geographic locations |
| **Race strategy** | An interactive model of fuel-mass penalties and tyre degradation over a stint |
| **Interactive application** | A Reflex web interface with Plotly charts and a terminal-inspired telemetry panel |

The source dataset contains **76 years of championship history** (1,168 races), with **636,495 lap records** in the supplied data snapshot.

---

## <a id="key-features"></a>🏁 Key Features

### 1. Dynasties & Constructor Performance

Explore how competitive eras have shifted between Formula 1 constructors.

- **Historical bar-chart race:** Move through championship seasons (1950–2026) and observe real-time changes in cumulative constructor victories.
- **Season victory comparisons:** Compare constructor wins across individual seasons using stacked columns.
- **Dynasty and win-share views:** Examine how much of a season's competitive success is concentrated among leading constructors.
- **Decade consistency heatmap:** Compare constructor win shares across 8 decades, from the 1950s through the 2020s.

### 2. Driver Greatness Explorer

Driver statistics are presented with additional context to make comparisons across different seasons more meaningful.

- **Ranked driver views:** Explore leading drivers by career victories and standardized performance measures.
- **Career wins vs. normalized dominance:** Compare career success against a season-level Z-score measure.
- **Within-season normalization:** Standardize a driver's points relative to the field in that season, rather than comparing raw points alone.
- **Composite dominance index:** Combine peak performance ($45\%$), career consistency ($35\%$), and achievement-related inputs ($20\%$) into one project-defined score.

### 3. Pace & Engine-Era Analysis

Use historical lap-time records to investigate pace distributions and differences between broad power-unit eras.

- Compare lap-time distributions across **V10, V8, and hybrid** periods.
- Inspect pace variation using box plots and related statistical visualizations.
- Explore stint-level pace decay and lap-time trends.
- Apply data-cleaning and outlier-filtering steps ($0.85\times$ to $1.25\times$ median) before selected comparisons.

*Note:* The lap-time analysis is based on official per-lap records available from 1996 onward; it does not provide equivalent lap-by-lap telemetry for every season since 1950.

### 4. Circuit Longevity & Geography

Explore the venues that have shaped Formula 1 history.

- Identify frequently used circuits (Monza leads worldwide with 76 hosted Grands Prix).
- Compare the number of races hosted at different venues.
- Display circuit locations using latitude and longitude coordinate scatters across 6 continents.

### 5. Interactive Race-Strategy Simulator

The simulator provides an interactive split-view tool to explore how fuel load and tyre age influence lap pace over a race stint.

**Inputs and controls include:**
- Circuit selection with clean-air lap-time baselines (Monza `1:21.250`, Monaco `1:14.820`, Silverstone `1:27.410`, Spa `1:44.900`, Interlagos `1:11.300`).
- Tyre compound selection: Soft (C5), Medium (C3), or Hard (C1).
- Stint length and lap-by-lap pace projection.
- Fuel-load burn-off and its modeled lap-time effect ($\sim 0.33\text{s per 10kg}$).
- Stint health capacity bar and dynamic status badge (`Optimal`, `Caution`, or `Critical`).
- Mini Plotly trajectory chart displaying the 35-lap pace progression.
- Reset button to restore clean-air defaults instantly.

*Note:* The simulator uses an illustrative engineering model calibrated against modern telemetry. Its compound degradation parameters and fuel assumptions should be treated as modeling choices, not as official FIA or team telemetry.

### 6. Pit-Wall Terminal Console

A terminal-inspired panel gives the application a motorsport engineering feel.

- Styled as a macOS-like console with traffic light window controls.
- Uses Python's `rich` library to create formatted terminal output and hierarchy trees.
- Exports terminal output as SVG for display in the interface with zero pixelation.
- Includes an interactive `[ ▶ RUN TELEMETRY ↻ ]` trigger to run the telemetry workflow.

---

## <a id="technology-stack"></a>🧱 Technology Stack

The project uses R for statistical analysis and a Python-based web application for data handling, state management, and visualization.

| Technology | Role in APEX // F1 |
|---|---|
| **R** | Statistical engine for normalization, statistical analysis, and trend calculations |
| **Python** | Application logic, data orchestration, and integration between components |
| **Reflex** | Reactive web application framework and UI state management |
| **Polars** | Tabular data processing, transformations, and sub-50ms relational joins |
| **Plotly** | Interactive charts, multi-mode figures, and responsive data visualizations |
| **Rich** | Styled terminal output, hierarchy trees, and SVG telemetry rendering |
| **Git** | Version control and collaborative engineering |

### Why use both R and Python?

R and Python serve complementary purposes in this project:

- **R is the analytical layer.** It is used for statistical methods that benefit from a dedicated statistical-computing workflow (Z-score distributions, LOESS curves, ANOVA).
- **Python is the application layer.** It loads and prepares data, connects the statistical workflow to the application, manages interactive state, and serves the web experience through Reflex.
- **Reflex connects the analysis to the user.** It allows charts, controls, and simulator inputs to respond to user interaction without building a separate frontend in JavaScript.

This separation keeps the statistical work distinct from the presentation layer while allowing both to operate seamlessly as one application.

---

## <a id="system-architecture"></a>🏛️ System Architecture

The application follows a data-to-insight workflow: source CSV files are processed, analytical calculations are performed, and the resulting values are displayed in the interactive Reflex interface.

```mermaid
flowchart TD
    A["Formula 1 Kaggle dataset<br>CSV tables"] --> B["Python data layer (data_bridge.py)"]
    B --> C["Polars processing<br>Cleaning, joins, transformations"]
    B --> D["R statistical engine<br>f1_statistical_engine.R"]
    C --> E["Prepared datasets and caches"]
    D --> F["Statistical results<br>Z-scores, trends, tests"]
    E --> G["Reflex application state (state.py)"]
    F --> G
    H["Race strategy model"] --> G
    G --> I["Plotly visualizations"]
    G --> J["Reflex user interface"]
    G --> K["Rich terminal output<br>SVG rendering"]
```

### Architecture Layers

| Layer | Main components | Responsibility |
|---|---|---|
| **Data source** | Kaggle CSV dataset | Historical race, driver, constructor, circuit, standings, and lap-time records |
| **Data processing** | Python, Polars | Load, clean, join, transform, and prepare relational data in `<50ms` |
| **Statistical analysis** | R, SciPy | Run statistical calculations and produce normalized analytical measures |
| **Application logic** | Reflex state, Python | Manage user input, chart selection, cached results, and simulator state |
| **Visualization** | Plotly, Reflex, Rich | Present interactive charts, dashboards, and terminal-style telemetry |

---

## <a id="statistical-methodology"></a>📐 Statistical Methodology

A central challenge in historical Formula 1 analysis is that the sport has not used one consistent scoring system throughout its history. Race calendars, points allocation, regulations, and competitive conditions have changed over time. Directly comparing raw season points can therefore be misleading.

APEX // F1 uses statistical methods to add context to the comparisons.

### 1. Within-Season Z-Score Normalization

A driver's season points are standardized against the distribution of points scored by the drivers in that same season.

For season $t$:
- $X_{i,t}$ is the points total for driver $i$ in season $t$.
- $\mu_t$ is the mean points total for the season.
- $\sigma_t$ is the standard deviation of season points.
- $Z_{i,t}$ is the standardized score for the driver.

$$Z_{i,t} = \frac{X_{i,t} - \mu_t}{\sigma_t}$$

The season mean and standard deviation are calculated as:

$$\mu_t = \frac{1}{N_t}\sum_{i=1}^{N_t}X_{i,t}$$

$$\sigma_t = \sqrt{\frac{1}{N_t-1}\sum_{i=1}^{N_t}(X_{i,t}-\mu_t)^2}$$

**Why it matters:** A Z-score expresses how far a driver's points total is from the season's average in standard-deviation units. It provides a relative, within-season measure that is more informative for cross-era exploration than raw points alone.

### 2. Composite Driver Dominance Index

The project defines a composite index that combines peak dominance, average career performance, and achievement-related inputs:

$$\text{Dominance Index} = 0.45 \cdot Z_{\text{peak}} + 0.35 \cdot \bar{Z}_{\text{career}} + 0.20 \cdot \ln(1 + 2 W_{\text{total}} + 5 T_{\text{total}})$$

Where:
- $Z_{\text{peak}}$ represents the driver's peak season-level normalized performance.
- $\bar{Z}_{\text{career}}$ represents average normalized performance over career seasons.
- $W_{\text{total}}$ represents total career wins.
- $T_{\text{total}}$ represents World Championship titles.

The weights are part of the project's scoring design. The index is a comparative analytical measure, not an official Formula 1 ranking.

### 3. Fuel-Mass Lap-Time Penalty

The simulator estimates the lap-time penalty associated with fuel carried by the car:

$$\Delta t_{\text{fuel}} = \left(\frac{m_{\text{fuel}}}{10.0}\right) \times 0.33\text{ seconds}$$

The current model assumes fuel burn-off of approximately **$1.60\text{ kg per lap}$**.

### 4. Non-Linear Tyre Degradation Model

The simulator models a gradual increase in lap time as a tyre stint ages, followed by a steeper non-linear loss after a configured degradation cliff:

$$\Delta t_{\text{tyre}}(l) = \begin{cases} l \cdot r_{\text{deg}}, & l \le L_{\text{cliff}} \\ L_{\text{cliff}} \cdot r_{\text{deg}} + (l - L_{\text{cliff}})^{1.6} \cdot (2.2 \cdot r_{\text{deg}}), & l > L_{\text{cliff}} \end{cases}$$

Where:
- $l$ is the tyre stint age in laps.
- $r_{\text{deg}}$ is the compound's baseline degradation rate (Soft: $0.085$, Medium: $0.055$, Hard: $0.035\text{ s/lap}$).
- $L_{\text{cliff}}$ is the configured point at which the compound suffers severe thermal drop-off.

### 5. Statistical Hypothesis Testing

The project includes a one-way ANOVA comparison of lap-time groups across engine eras (Monza dataset):

$$H_0: \mu_{\text{V10}} = \mu_{\text{V8}} = \mu_{\text{Hybrid}}$$

$$H_1: \text{At least one group mean differs}$$

**Reported ANOVA Results:**

| Statistic | Reported result | Interpretation |
|---|---:|---|
| **ANOVA F-statistic** | `42.98` | Ratio of variance between eras vs within eras |
| **p-value** | `$2.51 \times 10^{-19}$` | Statistically significant at $\alpha = 0.001$ |
| **Sample size** | `28,141` | Cleaned Monza laps across eras |

The p-value is well below the significance threshold, providing strong empirical evidence of lap pace differences across engine regulations.

### 6. Grid Position and Finishing Position Correlation

The project reports a Pearson correlation analysis between qualifying grid position and final race finish:

| Statistic | Reported result | Interpretation |
|---|---:|---|
| **Pearson correlation ($r$)** | `0.451` | Moderate-to-strong positive association |
| **p-value** | `$< 1.0 \times 10^{-15}$` | Statistically significant relationship |
| **Sample size ($N$)** | `26,002` | Valid race entries (1950–2026) |

---

## <a id="dataset"></a>🗃️ Dataset

### Source

The project uses the Formula 1 World Championship dataset published on Kaggle:

**[Formula 1 World Championship (1950–2026) — Kaggle](https://www.kaggle.com/datasets/samuelpombourcq/formula-1-world-championship-1950-2026)**

### Primary Tables Used

| File | Records | Coverage | Analytical Role |
|---|---:|---|---|
| `races.csv` | 1,168 | 1950–2026 | Grand Prix dates, seasons, rounds, and calendar eras |
| `results.csv` | 26,270 | 1950–2026 | Race results, grid positions, points, and finishing status |
| `lap_times.csv` | 636,495 | 1996–2026 | Lap-level millisecond timing for pace and stint analysis |
| `drivers.csv` | 835 | 1950–2026 | Driver profiles, nationalities, and abbreviations |
| `constructors.csv` | 206 | 1950–2026 | Constructor identities, origins, and chassis marques |
| `circuits.csv` | 79 | 1950–2026 | Circuit details, hosting counts, and geographic coordinates |
| `constructor_standings.csv` | 13,681 | 1958–2026 | Historical constructor championship standings |
| `driver_standings.csv` | 35,025 | 1950–2026 | Driver championship standings and points progression |

The project supports datasets located in either `./Dataset/` or `./data/`.

---

## <a id="getting-started"></a>⚡ Getting Started

Follow these steps to run APEX // F1 locally.

### Prerequisites

- **Python 3.10 or later** (tested on Python 3.11, 3.12, and 3.14).
- **R and `Rscript`** (recommended for native Z-score calculation; an automated Polars fallback engages if Rscript is missing).
- **Git**.

### 1. Clone the Repository

```bash
git clone https://github.com/NishanthdevX/DAV-Project.git
cd APEX-F1
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv .venv
```

**Windows — PowerShell:**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS:**
```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Verify the Analytical Pipeline

```bash
python test_f1_engine.py
```

This runs the project's data engine and statistical verification harness.

### 5. Launch the Reflex Application

```bash
python -m reflex run
```

When the application starts, open:

| Service | Local address | Status |
|---|---|---|
| **Reflex Web Interface** | [http://localhost:3000](http://localhost:3000) | Frontend UI |
| **Backend API Endpoint** | [http://localhost:8001/ping](http://localhost:8001/ping) | Returns `"pong"` |

---

## <a id="project-structure"></a>📂 Project Structure

```text
APEX-F1/
│
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                    # Automated CI test and compile workflow
│   │   └── codeql.yml                # CodeQL security analysis workflow
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md             # Bug reporting template
│   │   ├── feature_request.md        # Feature request template
│   │   └── config.yml                # Issue configuration
│   ├── PULL_REQUEST_TEMPLATE.md      # PR verification checklist
│   ├── CONTRIBUTING.md               # Contributor guide and architecture
│   ├── dependabot.yml                # Weekly dependency maintenance
│   └── SECURITY.md                   # Security vulnerability policy
│
├── apex_f1/
│   ├── __init__.py
│   ├── apex_f1.py                    # Master presentation layout and routing
│   ├── data_bridge.py                # Polars joins, pre-computed caches, Rich SVG
│   ├── state.py                      # Reactive state, Plotly figure vars, simulator
│   ├── styles.py                     # Design tokens, constructor colors, typography
│   └── components/
│       ├── __init__.py
│       ├── hero.py                   # Hero section and KPI presentation
│       ├── navbar.py                 # Floating pill navigation component
│       ├── scroll_story.py           # Multi-mode chart switcher & card grid
│       ├── pace_simulator.py         # Race strategy and stint simulator
│       ├── methodology.py            # Statistical methodology, tables & glossary
│       └── rich_pitwall.py           # macOS-inspired Rich SVG telemetry console
│
├── Dataset/                          # Kaggle Formula 1 relational tables
│   ├── circuits.csv
│   ├── races.csv
│   ├── results.csv
│   ├── lap_times.csv
│   └── ...
│
├── r_analytics/
│   └── f1_statistical_engine.R       # R statistical engine (Z-score & LOESS)
│
├── assets/
│   └── favicon.ico
│
├── requirements.txt                  # Python dependencies
├── rxconfig.py                       # Reflex configuration (ports 3000 & 8001)
├── test_f1_engine.py                 # Verification and test harness
├── f1_pitwall_telemetry.svg          # Sample vector telemetry output
├── LICENSE                           # GNU General Public License v3.0
└── README.md                         # Project documentation
```

---

## <a id="visual-design"></a>🎨 Visual Design & Color Tokens

APEX // F1 uses a dark, motorsport-inspired visual language compliant with **WCAG AA** accessibility standards:

| Design Token | Value | Role |
|---|---|---|
| **Carbon Void** | `#0B0E14` | Primary atmospheric background |
| **Midnight Slate** | `#141923` | Surface and panel base |
| **Glass Surface** | `rgba(18, 24, 38, 0.72)` | Translucent blur cards (`16px`) |
| **Scuderia Crimson** | `#E10600` | Primary Formula 1 accent & Ferrari |
| **Papaya Orange** | `#FF8000` | McLaren accent |
| **Silver Arrow** | `#00D2BE` | Mercedes accent |
| **Oracle Blue** | `#3B82F6` | Red Bull Racing & data highlights |
| **Heritage Cyan** | `#64C4FF` | Williams Racing accent |
| **Lotus Gold** | `#F59E0B` | Team Lotus & caution sector |
| **Sector Green** | `#10B981` | Optimal pace & statistical verification |

---

## <a id="testing-and-verification"></a>🧪 Testing and Verification

Run the project verification suite before submitting changes:

```bash
# 1. Test data bridge and statistical engine
python test_f1_engine.py

# 2. Verify Reflex application compilation
python -m reflex compile
```

---

## <a id="limitations"></a>⚠️ Limitations & Responsible Interpretation

- **Historical comparisons are not perfectly equivalent.** Z-score normalization provides within-season context, but it cannot account for every difference in regulations, team strength, mechanical reliability, calendar length, or competitive depth.
- **Lap-time data is incomplete across the full historical period.** The official millisecond lap-time table starts in 1996, so per-lap pace analysis is restricted to the seasons represented there (1996–2026).
- **The strategy simulator is an illustrative model.** Fuel penalties and tyre degradation slopes are simplified mathematical assumptions designed for exploration.
- **The dominance index is project-defined.** Its weights reflect this project's analytical design; it is not an official FIA driver rating.

---

## <a id="contributing"></a>🤝 Contributing

Contributions, suggestions, and improvements are welcome under the **GNU General Public License v3.0**.

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Make your changes and verify tests pass:
   ```bash
   python test_f1_engine.py
   python -m reflex compile
   ```
4. Commit your work and open a pull request. See [CONTRIBUTING.md](.github/CONTRIBUTING.md) for detailed guidelines.

---

## <a id="license"></a>📚 Data Attribution & License

### Dataset Attribution
The Formula 1 dataset used by this project is sourced from:  
[Samuel Pombourcq — Formula 1 World Championship 1950–2026 (Kaggle)](https://www.kaggle.com/datasets/samuelpombourcq/formula-1-world-championship-1950-2026)

### Project License
The project source code is distributed under the **GNU General Public License v3.0 (GPL-3.0)**. See the [`LICENSE`](LICENSE) file for the complete license text.

### Disclaimer
APEX // F1 is an independent educational and analytical project. It is not affiliated with, endorsed by, or sponsored by Formula 1, the FIA, or any Formula 1 team. Formula 1 names and related marks belong to their respective owners.

---

<div align="center">

**Built with 🏁 for Formula 1 fans, data scientists, and visualization engineers.**

*Turning 76 years of racing history into mathematical insight.*

</div>
