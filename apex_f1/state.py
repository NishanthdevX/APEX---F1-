"""APEX // F1 — Reactive State Architecture & Multi-Mode Visualization Core.
Manages regulation era scrubbing, multi-mode chart switching, interactive bubble quadrants,
dual filter sliders, responsive leaderboard cards, and live macOS-styled telemetry updates.
"""

from __future__ import annotations
import time
from typing import Any, Dict, List
import reflex as rx
import plotly.graph_objects as go
from apex_f1.data_bridge import bridge, ERA_DEFINITIONS, CIRCUIT_BASELINES
from apex_f1.styles import (
    FONT_FAMILY,
    FONT_MONO,
    ACCENT_COLOR,
    ACCENT_COBALT,
    ACCENT_EMERALD,
    ACCENT_AMBER,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    TEXT_MUTED,
    CONSTRUCTOR_COLORS,
    COLOR_FERRARI,
    COLOR_MCLAREN,
    COLOR_MERCEDES,
    COLOR_REDBULL,
    COLOR_WILLIAMS,
    COLOR_LOTUS,
    COLOR_OTHER,
    ERA_COLORS,
)


def format_lap_time(sec: float) -> str:
    """Formats second float into standard F1 m:ss.mmm format."""
    if sec <= 0:
        return "0:00.000"
    m = int(sec // 60)
    remainder = sec - (m * 60)
    s = int(remainder)
    ms = int(round((remainder - s) * 1000))
    if ms >= 1000:
        s += 1
        ms -= 1000
    return f"{m}:{s:02d}.{ms:03d}"


class ApexState(rx.State):
    """Core reactive state for the APEX // F1 platform."""

    # Regulation Era & Scrubber State
    selected_era: str = "All"
    scrub_year: list[float] = [2026.0]
    scrub_min_year: int = 1950
    scrub_max_year: int = 2026

    # Secondary Filter Slider (Minimum Grand Prix Wins Filter)
    min_wins_filter: list[float] = [0.0]

    # Search & Filter Query
    search_query: str = ""

    # Multi-Mode Tab Switcher (1 = Dynasties & Wins, 2 = Driver Greatness, 3 = Lap Pace & Physics, 4 = Circuit Longevity, 5 = Decade Heatmap)
    active_stage: int = 1

    # Sub-View Toggles per Stage
    stage1_view: str = "bar_race"          # "bar_race" | "season_wins" | "cumulative_stream"
    stage2_view: str = "ranked_bars"       # "ranked_bars" | "bubble_quadrant"
    stage3_view: str = "box_plots"         # "box_plots" | "decay_curves"
    stage4_view: str = "circuits_bar"      # "circuits_bar" | "circuits_map"

    # Team & Driver Selection
    selected_constructor: str = "All"
    selected_driver: str = "Juan Manuel Fangio"

    # Interactive Simulator Controls
    sim_circuit: str = "Monza"
    sim_driver: str = "Max Verstappen"
    sim_constructor: str = "Red Bull Racing"
    sim_tyre_compound: str = "Medium (C3)"
    sim_tyre_age: list[float] = [15.0]
    sim_fuel_kg: list[float] = [45.0]

    # macOS Terminal Live Telemetry Trigger
    telemetry_run_count: int = 1
    telemetry_status: str = "IDLE // READY"
    last_telemetry_timestamp: str = "LIVE 00:00:42"

    # --------------------------------------------------------------------------
    # Event Handlers
    # --------------------------------------------------------------------------
    def set_stage(self, stage: int):
        self.active_stage = stage

    def set_stage1_view(self, view: str):
        self.stage1_view = view

    def set_stage2_view(self, view: str):
        self.stage2_view = view

    def set_stage3_view(self, view: str):
        self.stage3_view = view

    def set_stage4_view(self, view: str):
        self.stage4_view = view

    def set_era(self, era: str):
        self.selected_era = era
        if era in ERA_DEFINITIONS:
            min_y, max_y, _ = ERA_DEFINITIONS[era]
            self.scrub_min_year = min_y
            self.scrub_max_year = max_y
            self.scrub_year = [float(max_y)]

    def set_scrub_year(self, year: list[float]):
        if year:
            self.scrub_year = [float(year[0])]

    def set_min_wins_filter(self, val: list[float]):
        if val:
            self.min_wins_filter = [float(val[0])]

    def set_search_query(self, query: str):
        self.search_query = query

    def set_selected_constructor(self, team: str):
        self.selected_constructor = team

    def set_sim_circuit(self, circuit: str):
        self.sim_circuit = circuit

    def set_sim_driver(self, driver: str):
        self.sim_driver = driver

    def set_sim_constructor(self, team: str):
        self.sim_constructor = team

    def set_sim_tyre_compound(self, compound: str):
        self.sim_tyre_compound = compound

    def set_sim_tyre_age(self, age: list[float]):
        if age:
            self.sim_tyre_age = [float(age[0])]

    def set_sim_fuel(self, fuel: list[float]):
        if fuel:
            self.sim_fuel_kg = [float(fuel[0])]

    def reset_simulator(self):
        """Restores simulator inputs to optimal clean air benchmark defaults."""
        self.sim_circuit = "Monza"
        self.sim_driver = "Max Verstappen"
        self.sim_constructor = "Red Bull Racing"
        self.sim_tyre_compound = "Medium (C3)"
        self.sim_tyre_age = [15.0]
        self.sim_fuel_kg = [45.0]

    def trigger_telemetry_run(self):
        """Action trigger for macOS Pit-Wall Terminal."""
        self.telemetry_run_count += 1
        self.telemetry_status = "STREAMING // SYNCED"
        current_time = time.strftime("%H:%M:%S")
        self.last_telemetry_timestamp = f"RUN #{self.telemetry_run_count:02d} AT {current_time}"

    # --------------------------------------------------------------------------
    # Computed Properties (@rx.var)
    # --------------------------------------------------------------------------
    @rx.var
    def show_leaderboard_grid(self) -> bool:
        return self.active_stage in [1, 2, 4, 5]

    @rx.var
    def current_scrub_year(self) -> int:
        return int(self.scrub_year[0]) if self.scrub_year else 2026

    @rx.var
    def current_min_wins(self) -> int:
        return int(self.min_wins_filter[0]) if self.min_wins_filter else 0

    @rx.var
    def current_tyre_age(self) -> int:
        return int(self.sim_tyre_age[0]) if self.sim_tyre_age else 15

    @rx.var
    def current_fuel_kg(self) -> int:
        return int(self.sim_fuel_kg[0]) if self.sim_fuel_kg else 45

    @rx.var
    def kpis(self) -> Dict[str, str]:
        return bridge.get_kpi_metrics()

    @rx.var
    def era_summary_label(self) -> str:
        if self.selected_era in ERA_DEFINITIONS:
            return ERA_DEFINITIONS[self.selected_era][2]
        return "76 Years of Speed (1950–2026)"

    @rx.var
    def pitwall_svg(self) -> str:
        _ = self.telemetry_run_count
        return bridge.render_pitwall_svg(
            selected_era=self.selected_era,
            constructor_filter=self.selected_constructor,
        )

    @rx.var
    def dataset_metadata(self) -> List[Dict[str, str]]:
        return bridge.get_dataset_metadata()

    @rx.var
    def stats_summary(self) -> Dict[str, Any]:
        return bridge.get_statistical_tests()

    # --------------------------------------------------------------------------
    # Stage Titles & Takeaway Insights
    # --------------------------------------------------------------------------
    @rx.var
    def stage_title(self) -> str:
        if self.active_stage == 1:
            if self.stage1_view == "bar_race":
                return f"Ferrari, McLaren & Mercedes lead cumulative victories up to {self.current_scrub_year}"
            elif self.stage1_view == "season_wins":
                return "Constructors routinely captured over 70% of a season's victories in dominant eras"
            else:
                return f"Dynasty points accumulation reveals multi-season championship surges up to {self.current_scrub_year}"
        elif self.active_stage == 2:
            if self.stage2_view == "ranked_bars":
                return "Fangio, Clark, Schumacher, Hamilton & Verstappen achieve +3.0σ peak dominance"
            else:
                return "Quadrant mapping separates longevity champions from peak within-season anomalies"
        elif self.active_stage == 3:
            if self.stage3_view == "box_plots":
                return "Engine regulation changes shifted Monza median lap pace by over 1.7 seconds"
            else:
                return "Cleaned telemetry displays initial fuel burn-off before severe tyre degradation"
        elif self.active_stage == 4:
            if self.stage4_view == "circuits_bar":
                return "Monza, Monaco, Silverstone and Spa form the foundational core of World Championship history"
            else:
                return "78 circuits across 6 continents illustrate the global expansion of Formula 1"
        else:
            return "Mercedes and Red Bull achieved unprecedented ~47% win-shares in the 2010s and 2020s"

    @rx.var
    def stage_subtitle(self) -> str:
        if self.active_stage == 1:
            return f"Unit: Cumulative Grand Prix Wins & Points | Period: 1950–{self.current_scrub_year} | Source: Dataset/results.csv & constructor_standings.csv"
        elif self.active_stage == 2:
            return "Unit: Within-Season Z-Score (σ = 1.0) & Career Wins | Period: 1950–2026 | Source: r_driver_dominance.csv & drivers.csv"
        elif self.active_stage == 3:
            return "Unit: Lap Milliseconds & Delta (sec) | Period: 1996–2026 (28,141 Cleaned Monza Laps) | Source: Dataset/lap_times.csv"
        elif self.active_stage == 4:
            return "Unit: Grands Prix Hosted & Geo Coordinates | Period: 1950–2026 (1,167 Races) | Source: Dataset/circuits.csv & races.csv"
        else:
            return "Unit: Decade Win Share (%) & Total Victories | Period: 1950s–2020s (8 Decades) | Source: Dataset/results.csv"

    @rx.var
    def stage_how_to_read(self) -> str:
        if self.active_stage == 1:
            return (
                "How to read: Horizontal bars rank the top 10 constructors up to the scrubbed year. "
                "Drag the timeline slider to observe constructor dynasties rise and fall over 76 seasons. "
                "Toggle to 'Season Wins' for stacked single-season dominance."
            )
        elif self.active_stage == 2:
            return (
                "How to read: The Z-Score (Z = (X - μ) / σ) measures how many standard deviations a driver outperformed their peer grid in their peak year. "
                "Values above +3.0σ represent transcendent historical dominance regardless of era point systems."
            )
        elif self.active_stage == 3:
            return (
                "How to read: The box plots show the interquartile range (IQR) of race lap times across engine regulations. "
                "Safety car and pit laps (>1.25x median) have been removed using robust outlier filtering."
            )
        elif self.active_stage == 4:
            return (
                "How to read: Bars indicate the total number of official World Championship Grands Prix hosted by each venue. "
                "Monza and Monaco have been contested in almost every active championship season since 1950."
            )
        else:
            return (
                "How to read: Each cell represents the percentage of all races in that decade won by that constructor. "
                "Darker shades highlight eras where a single marque dominated the sport."
            )

    @rx.var
    def stage_insight_callout(self) -> str:
        if self.active_stage == 1:
            return (
                f"Data Insight: Ferrari has competed in 69 seasons and claimed 16 Constructors' Championships, "
                f"while McLaren (185+ wins) and Mercedes (129+ wins) represent the most prolific modern dynasties."
            )
        elif self.active_stage == 2:
            return (
                "Statistical Insight: Juan Manuel Fangio (+3.88σ) and Michael Schumacher (+3.74σ) hold the highest peak "
                "season dominance, proving that their relative superiority exceeded even modern multi-title streaks."
            )
        elif self.active_stage == 3:
            return (
                "Physical Telemetry Insight: One-way ANOVA hypothesis test demonstrates a statistically significant pace shift "
                "(F = 42.98, p = 2.51e-19) between the high-RPM screaming V10s, aero-focused V8s, and modern high-torque hybrid power units."
            )
        elif self.active_stage == 4:
            return (
                "Geographic Insight: Out of 78 historical circuits, only 4 venues have hosted 50+ Grands Prix. "
                "Autodromo Nazionale Monza leads all circuits worldwide with 76 hosted championship rounds."
            )
        else:
            return (
                "Decade Matrix Insight: Ferrari is the only constructor to win races across 8 consecutive decades. "
                "However, Mercedes in the 2010s (47.0%) and Red Bull in the 2020s (47.0%) hold the highest decade monopoly in F1 history."
            )

    # --------------------------------------------------------------------------
    # Responsive Leaderboard Cards
    # --------------------------------------------------------------------------
    @rx.var
    def leaderboard_cards(self) -> List[Dict[str, Any]]:
        q = self.search_query.strip().lower()
        min_w = self.current_min_wins

        if self.active_stage in [1, 5]:
            teams = bridge.get_constructor_dynasties(
                era=self.selected_era,
                year_range=(self.scrub_min_year, self.current_scrub_year),
            )
            filtered = []
            for r in teams:
                if min_w > 0 and r["totalWins"] < min_w:
                    continue
                if q and (q not in r["constructorName"].lower() and q not in r["nationality"].lower()):
                    continue
                filtered.append({
                    "id": str(r["constructorId"]),
                    "rank": f"#{len(filtered) + 1}",
                    "name": r["constructorName"],
                    "category": r["nationality"].upper(),
                    "stat_primary": f"{r['championships']} TITLES",
                    "stat_secondary": f"{r['totalWins']} WINS",
                    "stat_detail": f"{float(r['totalPoints']):,.0f} PTS",
                    "era_tag": r.get("primaryEra", "ALL ERAS"),
                    "badge_color": CONSTRUCTOR_COLORS.get(r["constructorName"], COLOR_OTHER),
                })
            return filtered[:8]
        elif self.active_stage == 2:
            drivers = bridge.get_driver_dominance(era=self.selected_era, top_n=50)
            filtered = []
            for d in drivers:
                if min_w > 0 and d["totalWins"] < min_w:
                    continue
                if q and (q not in d["driverName"].lower() and q not in d["nationality"].lower()):
                    continue
                filtered.append({
                    "id": str(d["driverId"]),
                    "rank": f"#{len(filtered) + 1}",
                    "name": d["driverName"],
                    "category": d["nationality"].upper(),
                    "stat_primary": f"+{d['peakSeasonZ']} σ",
                    "stat_secondary": f"{d['totalWins']} WINS",
                    "stat_detail": f"{d['totalTitles']} TITLES",
                    "era_tag": d.get("primaryEra", "ALL ERAS"),
                    "badge_color": ACCENT_COLOR if d["totalTitles"] >= 4 else (ACCENT_COBALT if d["totalTitles"] >= 1 else COLOR_OTHER),
                })
            return filtered[:8]
        elif self.active_stage == 4:
            circuits = bridge.get_circuit_rankings(top_n=20)
            filtered = []
            for c in circuits:
                if q and (q not in c["name"].lower() and q not in c["country"].lower()):
                    continue
                filtered.append({
                    "id": str(c["circuitId"]),
                    "rank": f"#{len(filtered) + 1}",
                    "name": c["name"],
                    "category": f"{c['location']}, {c['country']}".upper(),
                    "stat_primary": f"{c['races_held']} RACES",
                    "stat_secondary": f"{c['country']}",
                    "stat_detail": f"{c['lat']:.2f}° N",
                    "era_tag": "HISTORIC VENUE",
                    "badge_color": ACCENT_EMERALD if c["races_held"] >= 50 else ACCENT_COBALT,
                })
            return filtered[:8]
        else:
            return []

    # --------------------------------------------------------------------------
    # Main Visualization Canvas Figure (@rx.var)
    # --------------------------------------------------------------------------
    @rx.var
    def main_stage_figure(self) -> go.Figure:
        fig = go.Figure()

        glass_layout = dict(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=60, r=40, t=65, b=60),
            font=dict(family=FONT_FAMILY, color=TEXT_PRIMARY, size=12),
            transition={"duration": 350, "easing": "cubic-in-out"},
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.06,
                xanchor="center",
                x=0.5,
                font=dict(family=FONT_MONO, size=11, color=TEXT_SECONDARY),
                bgcolor="rgba(14, 18, 27, 0.7)",
                bordercolor="rgba(255, 255, 255, 0.12)",
                borderwidth=1,
            ),
            hoverlabel=dict(
                bgcolor="rgba(14, 18, 27, 0.95)",
                bordercolor="rgba(255, 255, 255, 0.2)",
                font=dict(family=FONT_MONO, color="#FFFFFF", size=12),
            ),
        )

        # ----------------------------------------------------------------------
        # STAGE 01: Dynasties & Season Wins
        # ----------------------------------------------------------------------
        if self.active_stage == 1:
            if self.stage1_view == "bar_race":
                data = bridge.get_constructor_bar_race(self.current_scrub_year)
                # Reverse for ascending order on horizontal chart
                names = [r["name"] for r in reversed(data)]
                wins = [r["wins"] for r in reversed(data)]
                pts = [r["points"] for r in reversed(data)]
                colors = [CONSTRUCTOR_COLORS.get(n, COLOR_OTHER) for n in names]
                direct_labels = [f" {w} wins ({p:,.0f} pts)" for w, p in zip(wins, pts)]

                fig.add_trace(
                    go.Bar(
                        x=wins,
                        y=names,
                        orientation="h",
                        text=direct_labels,
                        textposition="outside",
                        textfont=dict(family=FONT_MONO, size=11, color=TEXT_PRIMARY),
                        marker=dict(
                            color=colors,
                            line=dict(color="rgba(255, 255, 255, 0.2)", width=1),
                        ),
                        hoverinfo="text",
                        hovertext=[
                            f"<b>{n}</b><br>Cumulative Grand Prix Wins: <b>{w}</b><br>Career Points: <b>{p:,.0f}</b>"
                            for n, w, p in zip(names, wins, pts)
                        ],
                    )
                )

                max_x = max(wins) * 1.25 if wins else 100
                fig.update_layout(
                    **glass_layout,
                    showlegend=False,
                    xaxis=dict(
                        title=dict(text="CUMULATIVE GRAND PRIX VICTORIES", font=dict(family=FONT_MONO, size=11, color=TEXT_MUTED)),
                        range=[0, max_x],
                        showgrid=True,
                        gridcolor="rgba(255, 255, 255, 0.05)",
                        tickfont=dict(family=FONT_MONO, color=TEXT_SECONDARY),
                        zeroline=False,
                    ),
                    yaxis=dict(
                        showgrid=False,
                        tickfont=dict(family=FONT_MONO, color=TEXT_PRIMARY, size=12),
                    ),
                )

            elif self.stage1_view == "season_wins":
                data = bridge.get_season_constructor_wins()
                years = [y for y in data["years"] if y <= self.current_scrub_year]
                team_wins = data["team_wins"]

                for team_name, all_wins in team_wins.items():
                    sub_wins = all_wins[: len(years)]
                    if sum(sub_wins) == 0:
                        continue
                    fig.add_trace(
                        go.Bar(
                            x=years,
                            y=sub_wins,
                            name=team_name,
                            marker=dict(color=CONSTRUCTOR_COLORS.get(team_name, COLOR_OTHER)),
                            hoverinfo="text",
                            hovertext=[
                                f"<b>{team_name}</b> ({y})<br>Season Wins: <b>{w}</b>"
                                for y, w in zip(years, sub_wins)
                            ],
                        )
                    )

                fig.update_layout(
                    **glass_layout,
                    barmode="stack",
                    xaxis=dict(
                        title=dict(text="CHAMPIONSHIP SEASON", font=dict(family=FONT_MONO, size=11, color=TEXT_MUTED)),
                        range=[1950, self.current_scrub_year + 1],
                        showgrid=True,
                        gridcolor="rgba(255, 255, 255, 0.05)",
                        tickfont=dict(family=FONT_MONO, color=TEXT_SECONDARY),
                    ),
                    yaxis=dict(
                        title=dict(text="TOTAL GRAND PRIX VICTORIES IN SEASON", font=dict(family=FONT_MONO, size=11, color=TEXT_MUTED)),
                        showgrid=True,
                        gridcolor="rgba(255, 255, 255, 0.05)",
                        tickfont=dict(family=FONT_MONO, color=TEXT_SECONDARY),
                    ),
                )

            else:  # cumulative_stream
                timeline = bridge.get_constructor_yearly_timeline()
                teams = ["Ferrari", "McLaren", "Williams", "Mercedes", "Red Bull", "Team Lotus"]

                for team in teams:
                    team_rows = [r for r in timeline if r["name"] == team and r["year"] <= self.current_scrub_year]
                    if not team_rows:
                        continue
                    yrs = [r["year"] for r in team_rows]
                    pts = [r["points"] for r in team_rows]
                    wins = [r["wins"] for r in team_rows]

                    fig.add_trace(
                        go.Scatter(
                            x=yrs,
                            y=pts,
                            mode="lines+markers",
                            name=team,
                            line=dict(color=CONSTRUCTOR_COLORS.get(team, COLOR_OTHER), width=2.5),
                            marker=dict(size=4),
                            text=[
                                f"<b>{team}</b> ({y})<br>Season Points: <b>{p:,.0f}</b><br>Wins: <b>{w}</b>"
                                for y, p, w in zip(yrs, pts, wins)
                            ],
                            hoverinfo="text",
                        )
                    )

                fig.update_layout(
                    **glass_layout,
                    xaxis=dict(
                        title=dict(text="CHAMPIONSHIP SEASON", font=dict(family=FONT_MONO, size=11, color=TEXT_MUTED)),
                        range=[1950, self.current_scrub_year + 1],
                        showgrid=True,
                        gridcolor="rgba(255, 255, 255, 0.05)",
                        tickfont=dict(family=FONT_MONO, color=TEXT_SECONDARY),
                    ),
                    yaxis=dict(
                        title=dict(text="SEASON CHAMPIONSHIP POINTS", font=dict(family=FONT_MONO, size=11, color=TEXT_MUTED)),
                        showgrid=True,
                        gridcolor="rgba(255, 255, 255, 0.05)",
                        tickfont=dict(family=FONT_MONO, color=TEXT_SECONDARY),
                    ),
                )

        # ----------------------------------------------------------------------
        # STAGE 02: Era-Adjusted Driver Greatness
        # ----------------------------------------------------------------------
        elif self.active_stage == 2:
            drivers = bridge.get_driver_dominance(era=self.selected_era, top_n=30)
            if self.current_min_wins > 0:
                drivers = [d for d in drivers if d["totalWins"] >= self.current_min_wins]

            if self.stage2_view == "ranked_bars":
                top15 = drivers[:15]
                names = [d["driverName"] for d in reversed(top15)]
                z_scores = [d["peakSeasonZ"] for d in reversed(top15)]
                titles = [d["totalTitles"] for d in reversed(top15)]
                wins = [d["totalWins"] for d in reversed(top15)]
                labels = [f" +{z:.2f}σ ({t} titles, {w} wins)" for z, t, w in zip(z_scores, titles, wins)]

                fig.add_trace(
                    go.Bar(
                        x=z_scores,
                        y=names,
                        orientation="h",
                        text=labels,
                        textposition="outside",
                        textfont=dict(family=FONT_MONO, size=11, color=TEXT_PRIMARY),
                        marker=dict(
                            color=[COLOR_FERRARI if t >= 4 else (ACCENT_COBALT if t >= 1 else COLOR_OTHER) for t in titles],
                            line=dict(color="rgba(255, 255, 255, 0.2)", width=1),
                        ),
                        hoverinfo="text",
                        hovertext=[
                            f"<b>{n}</b><br>Peak Season Dominance: <b>+{z:.2f}σ</b><br>World Championships: <b>{t}</b><br>Career Wins: <b>{w}</b>"
                            for n, z, t, w in zip(names, z_scores, titles, wins)
                        ],
                    )
                )

                max_z = max(z_scores) * 1.35 if z_scores else 5.0
                fig.update_layout(
                    **glass_layout,
                    showlegend=False,
                    xaxis=dict(
                        title=dict(text="WITHIN-SEASON PEAK DOMINANCE Z-SCORE (σ)", font=dict(family=FONT_MONO, size=11, color=TEXT_MUTED)),
                        range=[0, max_z],
                        showgrid=True,
                        gridcolor="rgba(255, 255, 255, 0.05)",
                        tickfont=dict(family=FONT_MONO, color=TEXT_SECONDARY),
                    ),
                    yaxis=dict(
                        showgrid=False,
                        tickfont=dict(family=FONT_MONO, color=TEXT_PRIMARY, size=11.5),
                    ),
                )

            else:  # bubble_quadrant
                x_wins = [d["totalWins"] for d in drivers]
                y_z = [d["peakSeasonZ"] for d in drivers]
                names = [d["driverName"] for d in drivers]
                titles = [d["totalTitles"] for d in drivers]
                bubble_sizes = [max(12, min(38, 12 + t * 4.5 + (w / 14))) for t, w in zip(titles, x_wins)]

                fig.add_trace(
                    go.Scatter(
                        x=x_wins,
                        y=y_z,
                        mode="markers+text",
                        text=names,
                        textposition="top center",
                        textfont=dict(family=FONT_MONO, size=9.5, color=TEXT_SECONDARY),
                        marker=dict(
                            size=bubble_sizes,
                            color=[COLOR_FERRARI if t >= 4 else (ACCENT_COBALT if t >= 1 else COLOR_OTHER) for t in titles],
                            opacity=0.82,
                            line=dict(width=1.5, color="rgba(255, 255, 255, 0.4)"),
                        ),
                        hoverinfo="text",
                        hovertext=[
                            f"<b>{n}</b><br>Career Wins: <b>{w}</b> | Titles: <b>{t}</b><br>Peak Season Z-Score: <b>+{z:.2f}σ</b>"
                            for n, w, t, z in zip(names, x_wins, titles, y_z)
                        ],
                    )
                )

                fig.add_hline(
                    y=3.0,
                    line_dash="dot",
                    line_color=ACCENT_EMERALD,
                    annotation_text="3.0σ ELITE DOMINANCE THRESHOLD",
                    annotation_font=dict(family=FONT_MONO, size=10, color=ACCENT_EMERALD),
                    annotation_position="bottom right",
                )

                fig.update_layout(
                    **glass_layout,
                    showlegend=False,
                    xaxis=dict(
                        title=dict(text="CAREER GRAND PRIX VICTORIES", font=dict(family=FONT_MONO, size=11, color=TEXT_MUTED)),
                        showgrid=True,
                        gridcolor="rgba(255, 255, 255, 0.05)",
                        tickfont=dict(family=FONT_MONO, color=TEXT_SECONDARY),
                    ),
                    yaxis=dict(
                        title=dict(text="WITHIN-SEASON PEAK Z-SCORE (σ)", font=dict(family=FONT_MONO, size=11, color=TEXT_MUTED)),
                        showgrid=True,
                        gridcolor="rgba(255, 255, 255, 0.05)",
                        tickfont=dict(family=FONT_MONO, color=TEXT_SECONDARY),
                    ),
                )

        # ----------------------------------------------------------------------
        # STAGE 03: Lap Pace & Physics (Box Plots vs Stint Decay Curves)
        # ----------------------------------------------------------------------
        elif self.active_stage == 3:
            if self.stage3_view == "box_plots":
                box_data = bridge.get_era_pace_distributions(circuit_id=7)
                for row in box_data:
                    era_name = row["era"]
                    fig.add_trace(
                        go.Box(
                            y=[row["min_sec"], row["q1_sec"], row["med_sec"], row["q3_sec"], row["max_sec"]],
                            name=era_name,
                            marker=dict(color=ERA_COLORS.get(era_name, COLOR_OTHER)),
                            boxpoints=False,
                            hoverinfo="text",
                            hovertext=(
                                f"<b>{era_name}</b> (Monza Cleaned Laps: {row['count']:,})<br>"
                                f"Median Pace: <b>{format_lap_time(row['med_sec'])}</b> ({row['med_sec']:.2f}s)<br>"
                                f"Interquartile Range: [{row['q1_sec']:.2f}s, {row['q3_sec']:.2f}s]<br>"
                                f"Fastest Clean Lap: {format_lap_time(row['min_sec'])}"
                            ),
                        )
                    )

                fig.update_layout(
                    **glass_layout,
                    showlegend=False,
                    xaxis=dict(
                        showgrid=False,
                        tickfont=dict(family=FONT_MONO, color=TEXT_PRIMARY, size=11),
                    ),
                    yaxis=dict(
                        title=dict(text="CLEANED LAP PACE (SECONDS)", font=dict(family=FONT_MONO, size=11, color=TEXT_MUTED)),
                        showgrid=True,
                        gridcolor="rgba(255, 255, 255, 0.05)",
                        tickfont=dict(family=FONT_MONO, color=TEXT_SECONDARY),
                    ),
                )

            else:  # decay_curves
                pace_data = bridge.get_lap_pace_benchmark(circuit_id=7)
                curves = pace_data.get("decay_curve", [])
                eras = sorted(list(set(c["era"] for c in curves)))

                for era_name in eras:
                    rows = [c for c in curves if c["era"] == era_name]
                    laps = [r["lap"] for r in rows]
                    deltas = [round(r["avg_delta"], 2) for r in rows]
                    fig.add_trace(
                        go.Scatter(
                            x=laps,
                            y=deltas,
                            mode="lines",
                            name=era_name,
                            line=dict(color=ERA_COLORS.get(era_name, COLOR_OTHER), width=2.5),
                            hoverinfo="text",
                            hovertext=[
                                f"<b>{era_name}</b> (Lap {l})<br>Pace Delta vs Median: <b>+{d:.2f}s</b>"
                                for l, d in zip(laps, deltas)
                            ],
                        )
                    )

                fig.update_layout(
                    **glass_layout,
                    xaxis=dict(
                        title=dict(text="RACE LAP NUMBER (1 TO 53)", font=dict(family=FONT_MONO, size=11, color=TEXT_MUTED)),
                        showgrid=True,
                        gridcolor="rgba(255, 255, 255, 0.05)",
                        tickfont=dict(family=FONT_MONO, color=TEXT_SECONDARY),
                    ),
                    yaxis=dict(
                        title=dict(text="PACE DELTA IN SECONDS (+/- FROM MEDIAN)", font=dict(family=FONT_MONO, size=11, color=TEXT_MUTED)),
                        showgrid=True,
                        gridcolor="rgba(255, 255, 255, 0.05)",
                        tickfont=dict(family=FONT_MONO, color=TEXT_SECONDARY),
                    ),
                )

        # ----------------------------------------------------------------------
        # STAGE 04: Circuit Longevity & Geography
        # ----------------------------------------------------------------------
        elif self.active_stage == 4:
            if self.stage4_view == "circuits_bar":
                circuits = bridge.get_circuit_rankings(top_n=10)
                names = [c["name"].replace("Autodromo Nazionale di Monza", "Monza").replace("Circuit de Spa-Francorchamps", "Spa-Francorchamps").replace("Autódromo José Carlos Pace", "Interlagos") for c in reversed(circuits)]
                races_held = [c["races_held"] for c in reversed(circuits)]
                countries = [c["country"] for c in reversed(circuits)]
                labels = [f" {r} GPs ({cntry})" for r, cntry in zip(races_held, countries)]

                fig.add_trace(
                    go.Bar(
                        x=races_held,
                        y=names,
                        orientation="h",
                        text=labels,
                        textposition="outside",
                        textfont=dict(family=FONT_MONO, size=11, color=TEXT_PRIMARY),
                        marker=dict(
                            color=[ACCENT_EMERALD if r >= 50 else ACCENT_COBALT for r in races_held],
                            line=dict(color="rgba(255, 255, 255, 0.2)", width=1),
                        ),
                        hoverinfo="text",
                        hovertext=[
                            f"<b>{n}</b> ({cntry})<br>Official Championship Grands Prix: <b>{r}</b>"
                            for n, cntry, r in zip(names, countries, races_held)
                        ],
                    )
                )

                max_r = max(races_held) * 1.25 if races_held else 80
                fig.update_layout(
                    **glass_layout,
                    showlegend=False,
                    xaxis=dict(
                        title=dict(text="OFFICIAL WORLD CHAMPIONSHIP GRANDS PRIX HOSTED", font=dict(family=FONT_MONO, size=11, color=TEXT_MUTED)),
                        range=[0, max_r],
                        showgrid=True,
                        gridcolor="rgba(255, 255, 255, 0.05)",
                        tickfont=dict(family=FONT_MONO, color=TEXT_SECONDARY),
                    ),
                    yaxis=dict(
                        showgrid=False,
                        tickfont=dict(family=FONT_MONO, color=TEXT_PRIMARY, size=11.5),
                    ),
                )

            else:  # circuits_map (lat/lng scatter)
                map_data = bridge.get_circuit_map_data()
                lats = [c["lat"] for c in map_data if c["lat"] is not None]
                lngs = [c["lng"] for c in map_data if c["lng"] is not None]
                names = [c["name"] for c in map_data if c["lat"] is not None]
                countries = [c["country"] for c in map_data if c["lat"] is not None]
                races = [c["races_held"] for c in map_data if c["lat"] is not None]

                sizes = [max(8, min(28, 8 + r * 0.25)) for r in races]

                fig.add_trace(
                    go.Scatter(
                        x=lngs,
                        y=lats,
                        mode="markers",
                        text=names,
                        marker=dict(
                            size=sizes,
                            color=races,
                            colorscale="Viridis",
                            showscale=True,
                            colorbar=dict(
                                title=dict(text="GPs Hosted", font=dict(family=FONT_MONO, size=10, color=TEXT_MUTED)),
                                tickfont=dict(family=FONT_MONO, color=TEXT_SECONDARY, size=10),
                                thickness=10,
                                len=0.7,
                            ),
                            line=dict(color="rgba(255, 255, 255, 0.4)", width=1),
                        ),
                        hoverinfo="text",
                        hovertext=[
                            f"<b>{n}</b> ({cntry})<br>Coordinates: {lat:.2f}°, {lng:.2f}°<br>Grands Prix: <b>{r}</b>"
                            for n, cntry, lat, lng, r in zip(names, countries, lats, lngs, races)
                        ],
                    )
                )

                fig.update_layout(
                    **glass_layout,
                    xaxis=dict(
                        title=dict(text="LONGITUDE (°)", font=dict(family=FONT_MONO, size=11, color=TEXT_MUTED)),
                        showgrid=True,
                        gridcolor="rgba(255, 255, 255, 0.05)",
                        tickfont=dict(family=FONT_MONO, color=TEXT_SECONDARY),
                    ),
                    yaxis=dict(
                        title=dict(text="LATITUDE (°)", font=dict(family=FONT_MONO, size=11, color=TEXT_MUTED)),
                        showgrid=True,
                        gridcolor="rgba(255, 255, 255, 0.05)",
                        tickfont=dict(family=FONT_MONO, color=TEXT_SECONDARY),
                    ),
                )

        # ----------------------------------------------------------------------
        # STAGE 05: Decade Consistency Heatmap Matrix (6 x 8)
        # ----------------------------------------------------------------------
        else:
            heatmap_data = bridge.get_constructor_decade_heatmap()
            decades = heatmap_data["decades"]
            teams = heatmap_data["teams"]
            z_vals = heatmap_data["z"]
            annotations = heatmap_data["text"]

            fig.add_trace(
                go.Heatmap(
                    z=z_vals,
                    x=decades,
                    y=teams,
                    text=annotations,
                    texttemplate="%{text}",
                    textfont=dict(family=FONT_MONO, size=11, color="#FFFFFF"),
                    colorscale="Reds",
                    showscale=True,
                    colorbar=dict(
                        title=dict(text="Win Share (%)", font=dict(family=FONT_MONO, size=10, color=TEXT_MUTED)),
                        tickfont=dict(family=FONT_MONO, color=TEXT_SECONDARY, size=10),
                        thickness=12,
                        len=0.8,
                    ),
                    hoverinfo="text",
                    hovertext=[
                        f"<b>{team}</b> in {dec}<br>Decade Win Share: <b>{z_vals[i][j]:.1f}%</b>"
                        for i, team in enumerate(teams)
                        for j, dec in enumerate(decades)
                    ],
                )
            )

            fig.update_layout(
                **glass_layout,
                xaxis=dict(
                    title=dict(text="CHAMPIONSHIP DECADE", font=dict(family=FONT_MONO, size=11, color=TEXT_MUTED)),
                    showgrid=False,
                    tickfont=dict(family=FONT_MONO, color=TEXT_PRIMARY, size=12),
                ),
                yaxis=dict(
                    showgrid=False,
                    tickfont=dict(family=FONT_MONO, color=TEXT_PRIMARY, size=12),
                ),
            )

        return fig

    # --------------------------------------------------------------------------
    # Simulator Projection & Stint Capacity Telemetry
    # --------------------------------------------------------------------------
    @rx.var
    def simulator_projection(self) -> Dict[str, Any]:
        """Real-time tyre degradation, stint pace decay, and capacity simulation grounded in circuit data."""
        circuit_info = CIRCUIT_BASELINES.get(self.sim_circuit, CIRCUIT_BASELINES["Monza"])
        baseline_sec = circuit_info["baseline_sec"]
        cliff_base = circuit_info["cliff_lap"]

        compound_deg_rate = {
            "Soft (C5)": 0.085,
            "Medium (C3)": 0.055,
            "Hard (C1)": 0.035,
        }.get(self.sim_tyre_compound, 0.055)

        compound_cliff_mult = {
            "Soft (C5)": 0.75,
            "Medium (C3)": 1.0,
            "Hard (C1)": 1.45,
        }.get(self.sim_tyre_compound, 1.0)

        effective_cliff_lap = int(cliff_base * compound_cliff_mult)
        age = self.current_tyre_age
        fuel = self.current_fuel_kg

        # Physical fuel penalty: ~0.33s per 10kg
        fuel_penalty = (fuel / 10.0) * 0.33

        # Tyre degradation slope with non-linear cliff penalty
        if age <= effective_cliff_lap:
            tyre_penalty = age * compound_deg_rate
        else:
            cliff_excess = age - effective_cliff_lap
            tyre_penalty = (effective_cliff_lap * compound_deg_rate) + (cliff_excess ** 1.6) * (compound_deg_rate * 2.2)

        total_lap_delta = round(fuel_penalty + tyre_penalty, 3)
        predicted_lap_sec = round(baseline_sec + total_lap_delta, 3)

        laps_to_cliff = max(0, effective_cliff_lap - age)
        stint_health_pct = max(0, min(100, int((laps_to_cliff / effective_cliff_lap) * 100)))

        if stint_health_pct > 50:
            status_text = "STINT PACE OPTIMAL"
            status_reason = "Compound within thermal operating window; pace drop-off is controlled."
            status_color = ACCENT_EMERALD
            status_bg = "rgba(16, 185, 129, 0.12)"
            status_border = "rgba(16, 185, 129, 0.3)"
        elif stint_health_pct > 15:
            status_text = "ELEVATED DEGRADATION"
            status_reason = "Thermal blistering / graining detected. Approaching performance cliff."
            status_color = ACCENT_AMBER
            status_bg = "rgba(245, 158, 11, 0.12)"
            status_border = "rgba(245, 158, 11, 0.3)"
        else:
            status_text = "CRITICAL TYRE CLIFF // PIT NOW"
            status_reason = "Surface rubber exhausted. Severe pace degradation exceeding +2.0s/lap."
            status_color = ACCENT_COLOR
            status_bg = "rgba(225, 6, 0, 0.15)"
            status_border = "rgba(225, 6, 0, 0.4)"

        return {
            "circuit_name": circuit_info["name"],
            "circuit_baseline_display": circuit_info["display"],
            "predicted_lap_time": format_lap_time(predicted_lap_sec),
            "lap_delta_sec": f"+{total_lap_delta:.3f}s",
            "tyre_degradation_sec": f"+{tyre_penalty:.3f}s",
            "fuel_weight_penalty": f"+{fuel_penalty:.3f}s",
            "laps_remaining_to_cliff": f"{laps_to_cliff} Laps",
            "effective_cliff_lap": effective_cliff_lap,
            "stint_health_pct": stint_health_pct,
            "stint_progress_width": f"{stint_health_pct}%",
            "status_text": status_text,
            "status_reason": status_reason,
            "status_color": status_color,
            "status_bg": status_bg,
            "status_border": status_border,
        }

    # --------------------------------------------------------------------------
    # Simulator Pace Stint Trajectory Mini Chart (@rx.var)
    # --------------------------------------------------------------------------
    @rx.var
    def simulator_pace_chart(self) -> go.Figure:
        """Mini Plotly trajectory chart showing predicted lap times over a 35-lap stint."""
        circuit_info = CIRCUIT_BASELINES.get(self.sim_circuit, CIRCUIT_BASELINES["Monza"])
        baseline = circuit_info["baseline_sec"]
        cliff_base = circuit_info["cliff_lap"]

        compound_deg_rate = {
            "Soft (C5)": 0.085,
            "Medium (C3)": 0.055,
            "Hard (C1)": 0.035,
        }.get(self.sim_tyre_compound, 0.055)

        compound_cliff_mult = {
            "Soft (C5)": 0.75,
            "Medium (C3)": 1.0,
            "Hard (C1)": 1.45,
        }.get(self.sim_tyre_compound, 1.0)

        effective_cliff = int(cliff_base * compound_cliff_mult)
        start_fuel = self.current_fuel_kg
        current_lap = self.current_tyre_age

        stint_laps = list(range(1, 36))
        pace_values: List[float] = []

        for l in stint_laps:
            # Fuel burn off ~1.6 kg/lap
            fuel_on_lap = max(0.0, start_fuel - (l - 1) * 1.6)
            f_pen = (fuel_on_lap / 10.0) * 0.33
            if l <= effective_cliff:
                t_pen = l * compound_deg_rate
            else:
                cliff_excess = l - effective_cliff
                t_pen = (effective_cliff * compound_deg_rate) + (cliff_excess ** 1.6) * (compound_deg_rate * 2.2)
            pace_values.append(round(baseline + f_pen + t_pen, 3))

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=stint_laps,
                y=pace_values,
                mode="lines",
                name="Stint Pace Trajectory",
                line=dict(color=ACCENT_COBALT, width=2.5),
                hoverinfo="text",
                hovertext=[
                    f"Lap {l}: <b>{format_lap_time(p)}</b> (+{p - baseline:.2f}s)"
                    for l, p in zip(stint_laps, pace_values)
                ],
            )
        )

        # Highlight current simulation lap marker
        if 1 <= current_lap <= 35:
            current_pace = pace_values[current_lap - 1]
            fig.add_trace(
                go.Scatter(
                    x=[current_lap],
                    y=[current_pace],
                    mode="markers",
                    name="Current Simulation Lap",
                    marker=dict(size=10, color=ACCENT_COLOR, line=dict(color="#FFFFFF", width=2)),
                    hoverinfo="text",
                    hovertext=f"Current Lap {current_lap}: <b>{format_lap_time(current_pace)}</b>",
                )
            )

        # Performance cliff line
        if 1 <= effective_cliff <= 35:
            fig.add_vline(
                x=effective_cliff,
                line_dash="dot",
                line_color=ACCENT_AMBER,
                annotation_text=f"CLIFF (LAP {effective_cliff})",
                annotation_font=dict(family=FONT_MONO, size=9, color=ACCENT_AMBER),
                annotation_position="top left",
            )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=45, r=20, t=25, b=35),
            font=dict(family=FONT_MONO, color=TEXT_SECONDARY, size=10),
            showlegend=False,
            xaxis=dict(
                title=dict(text="STINT LAP", font=dict(family=FONT_MONO, size=10, color=TEXT_MUTED)),
                showgrid=True,
                gridcolor="rgba(255, 255, 255, 0.05)",
                tickfont=dict(family=FONT_MONO, color=TEXT_MUTED, size=9),
            ),
            yaxis=dict(
                title=dict(text="SEC", font=dict(family=FONT_MONO, size=10, color=TEXT_MUTED)),
                showgrid=True,
                gridcolor="rgba(255, 255, 255, 0.05)",
                tickfont=dict(family=FONT_MONO, color=TEXT_MUTED, size=9),
            ),
            hoverlabel=dict(
                bgcolor="rgba(14, 18, 27, 0.95)",
                bordercolor="rgba(255, 255, 255, 0.2)",
                font=dict(family=FONT_MONO, color="#FFFFFF", size=11),
            ),
        )
        return fig
