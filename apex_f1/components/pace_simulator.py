"""APEX // F1 — 2-Column Split-View Strategy & Tyre Degradation Simulator.
Upgrades flat layout into a 2-Column "Configuration vs. Telemetry Output" architecture
with live numeric badges, circuit selector, reset button, segmented pill toggles,
stint progress/capacity bar, dynamic status badges, 3-card metric grid, animated
mini pace trajectory chart, and collapsible mathematical formula breakdown.
"""

from __future__ import annotations
import reflex as rx
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
    BORDER_HAIRLINE,
    BORDER_HIGHLIGHT,
    GLASS_CARD_STYLE,
    GLASS_SUB_CARD,
    EYEBROW_BADGE_STYLE,
    BUTTON_PILL_PRIMARY,
    BUTTON_PILL_SECONDARY,
)
from apex_f1.state import ApexState


def tyre_compound_pill(name: str) -> rx.Component:
    """Segmented pill toggle for tyre compound selection."""
    is_active = ApexState.sim_tyre_compound == name
    return rx.button(
        name,
        on_click=ApexState.set_sim_tyre_compound(name),
        font_family=FONT_MONO,
        font_size="11.5px",
        font_weight=rx.cond(is_active, "600", "400"),
        min_height="40px",
        padding="0 1rem",
        border_radius="9999px",
        background_color=rx.cond(is_active, ACCENT_COLOR, "rgba(255, 255, 255, 0.04)"),
        color=rx.cond(is_active, "#FFFFFF", TEXT_SECONDARY),
        border=rx.cond(is_active, f"1px solid {ACCENT_COLOR}", f"1px solid {BORDER_HAIRLINE}"),
        box_shadow=rx.cond(is_active, "0 4px 14px -2px rgba(225, 6, 0, 0.4)", "none"),
        cursor="pointer",
        flex="1",
        transition="all 0.2s ease",
        _hover={
            "color": "#FFFFFF",
            "background_color": rx.cond(is_active, ACCENT_COLOR, "rgba(255, 255, 255, 0.1)"),
            "border_color": BORDER_HIGHLIGHT,
        },
        aria_label=f"Select tyre compound {name}",
    )


def telemetry_metric_card(title: str, value: str, subtext: str, value_color: str) -> rx.Component:
    """Sub-metric card inside the telemetry output panel."""
    return rx.box(
        rx.text(
            title,
            font_family=FONT_MONO,
            font_size="9.5px",
            font_weight="600",
            color=TEXT_MUTED,
            letter_spacing="0.06em",
            text_transform="uppercase",
            margin_bottom="4px",
        ),
        rx.text(
            value,
            font_family=FONT_FAMILY,
            font_size=["20px", "24px"],
            font_weight="600",
            color=value_color,
            line_height="1.1",
            letter_spacing="-0.02em",
        ),
        rx.text(
            subtext,
            font_family=FONT_MONO,
            font_size="10px",
            color=TEXT_MUTED,
            margin_top="4px",
        ),
        style=GLASS_SUB_CARD,
        flex="1",
        min_width=["100%", "0"],
    )


def pace_simulator() -> rx.Component:
    """2-Column Split Architecture: Configuration Panel (Left) vs. Telemetry Output (Right)."""
    proj = ApexState.simulator_projection

    return rx.box(
        rx.vstack(
            # Top Section Eyebrow & Title
            rx.vstack(
                rx.box(
                    rx.text("STAGE 03 // PIT-WALL RACE STRATEGY & DEGRADATION SIMULATOR"),
                    style=EYEBROW_BADGE_STYLE,
                ),
                rx.heading(
                    "Race Strategy & Tyre Degradation Simulator",
                    font_size=["24px", "30px", "34px"],
                    font_weight="600",
                    letter_spacing="-0.02em",
                    color=TEXT_PRIMARY,
                ),
                rx.text(
                    "What you are looking at: A real-time telemetry model calibrated against empirical F1 circuit baselines. "
                    "Why it matters: Stint strategy balances fuel burn-off against tyre thermal degradation to identify the exact pit window. "
                    "What to try: Select different circuits and tyre compounds, drag the stint age slider past the cliff, and watch the pace curve collapse.",
                    font_size="14.5px",
                    line_height="1.6",
                    color=TEXT_SECONDARY,
                    max_width="780px",
                ),
                align_items="start",
                spacing="2",
                margin_bottom="1.5rem",
            ),
            # 2-Column Split Grid
            rx.box(
                rx.hstack(
                    # ----------------------------------------------------------
                    # LEFT PANEL: Configuration (Machine, Circuit, Compound & Sliders)
                    # ----------------------------------------------------------
                    rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.text("01 // STRATEGY CONFIGURATION", font_family=FONT_MONO, font_size="11.5px", font_weight="600", color=ACCENT_COBALT),
                                # Reset Button
                                rx.button(
                                    rx.hstack(
                                        rx.text("↺", font_size="12px"),
                                        rx.text("Reset Defaults", font_size="11px", font_family=FONT_MONO),
                                        spacing="1",
                                        align="center",
                                    ),
                                    on_click=ApexState.reset_simulator,
                                    height="30px",
                                    padding="0 10px",
                                    border_radius="9999px",
                                    background_color="rgba(255, 255, 255, 0.05)",
                                    border=f"1px solid {BORDER_HAIRLINE}",
                                    color=TEXT_SECONDARY,
                                    cursor="pointer",
                                    _hover={"background_color": "rgba(255, 255, 255, 0.12)", "color": "#FFFFFF"},
                                    aria_label="Reset simulator to clean air defaults",
                                ),
                                justify="between",
                                width="100%",
                                align="center",
                                margin_bottom="1rem",
                            ),
                            # Circuit Selector (Grounded in Real Telemetry)
                            rx.vstack(
                                rx.hstack(
                                    rx.text("GRAND PRIX CIRCUIT BASELINE:", font_family=FONT_MONO, font_size="10.5px", color=TEXT_MUTED),
                                    rx.text(
                                        f"Optimum: {proj['circuit_baseline_display']}",
                                        font_family=FONT_MONO,
                                        font_size="10.5px",
                                        color=ACCENT_EMERALD,
                                    ),
                                    justify="between",
                                    width="100%",
                                ),
                                rx.select(
                                    [
                                        "Monza",
                                        "Monaco",
                                        "Silverstone",
                                        "Spa-Francorchamps",
                                        "Interlagos",
                                    ],
                                    value=ApexState.sim_circuit,
                                    on_change=ApexState.set_sim_circuit,
                                    width="100%",
                                    min_height="40px",
                                    border_radius="8px",
                                    background_color="rgba(255, 255, 255, 0.04)",
                                    border=f"1px solid {BORDER_HIGHLIGHT}",
                                    color=TEXT_PRIMARY,
                                    font_family=FONT_MONO,
                                    font_size="12px",
                                    aria_label="Select Grand Prix circuit baseline",
                                ),
                                width="100%",
                                spacing="1",
                                margin_bottom="1rem",
                            ),
                            # Driver & Constructor Dropdowns
                            rx.hstack(
                                rx.vstack(
                                    rx.text("DRIVER SELECTION:", font_family=FONT_MONO, font_size="10.5px", color=TEXT_MUTED),
                                    rx.select(
                                        [
                                            "Max Verstappen",
                                            "Lewis Hamilton",
                                            "Michael Schumacher",
                                            "Ayrton Senna",
                                            "Juan Manuel Fangio",
                                            "Charles Leclerc",
                                            "Lando Norris",
                                            "Fernando Alonso",
                                        ],
                                        value=ApexState.sim_driver,
                                        on_change=ApexState.set_sim_driver,
                                        width="100%",
                                        min_height="40px",
                                        border_radius="8px",
                                        background_color="rgba(255, 255, 255, 0.04)",
                                        border=f"1px solid {BORDER_HIGHLIGHT}",
                                        color=TEXT_PRIMARY,
                                        font_family=FONT_MONO,
                                        font_size="12px",
                                        aria_label="Select simulator driver",
                                    ),
                                    flex="1",
                                    align_items="start",
                                    spacing="1",
                                ),
                                rx.vstack(
                                    rx.text("CONSTRUCTOR TEAM:", font_family=FONT_MONO, font_size="10.5px", color=TEXT_MUTED),
                                    rx.select(
                                        [
                                            "Red Bull Racing",
                                            "Scuderia Ferrari",
                                            "Mercedes-AMG Petronas",
                                            "McLaren F1 Team",
                                            "Williams Racing",
                                            "Aston Martin",
                                        ],
                                        value=ApexState.sim_constructor,
                                        on_change=ApexState.set_sim_constructor,
                                        width="100%",
                                        min_height="40px",
                                        border_radius="8px",
                                        background_color="rgba(255, 255, 255, 0.04)",
                                        border=f"1px solid {BORDER_HIGHLIGHT}",
                                        color=TEXT_PRIMARY,
                                        font_family=FONT_MONO,
                                        font_size="12px",
                                        aria_label="Select simulator constructor",
                                    ),
                                    flex="1",
                                    align_items="start",
                                    spacing="1",
                                ),
                                spacing="3",
                                width="100%",
                                margin_bottom="1rem",
                            ),
                            # Segmented Tyre Compound Pills
                            rx.vstack(
                                rx.hstack(
                                    rx.text("TYRE COMPOUND (ILLUSTRATIVE MODEL):", font_family=FONT_MONO, font_size="10.5px", color=TEXT_MUTED),
                                    rx.text(
                                        "Calibrated vs Telemetry",
                                        font_family=FONT_MONO,
                                        font_size="10px",
                                        color=TEXT_MUTED,
                                    ),
                                    justify="between",
                                    width="100%",
                                ),
                                rx.hstack(
                                    tyre_compound_pill("Soft (C5)"),
                                    tyre_compound_pill("Medium (C3)"),
                                    tyre_compound_pill("Hard (C1)"),
                                    spacing="2",
                                    width="100%",
                                ),
                                width="100%",
                                align_items="start",
                                spacing="1",
                                margin_bottom="1.25rem",
                            ),
                            # Tyre Age Slider with Live Numeric Badge
                            rx.vstack(
                                rx.hstack(
                                    rx.text("TYRE STINT AGE:", font_family=FONT_MONO, font_size="11px", color=TEXT_SECONDARY),
                                    rx.text(
                                        f"{ApexState.current_tyre_age} Laps on Set",
                                        font_family=FONT_MONO,
                                        font_size="12px",
                                        font_weight="600",
                                        color=ACCENT_COLOR,
                                        padding="2px 8px",
                                        border_radius="6px",
                                        background_color="rgba(225, 6, 0, 0.12)",
                                        border="1px solid rgba(225, 6, 0, 0.25)",
                                    ),
                                    justify="between",
                                    width="100%",
                                    margin_bottom="4px",
                                ),
                                rx.slider(
                                    default_value=[15.0],
                                    value=ApexState.sim_tyre_age,
                                    min=1,
                                    max=45,
                                    step=1,
                                    on_change=ApexState.set_sim_tyre_age,
                                    width="100%",
                                    aria_label="Tyre stint age slider in laps",
                                ),
                                rx.hstack(
                                    rx.text("1 Lap (Fresh)", font_family=FONT_MONO, font_size="9.5px", color=TEXT_MUTED),
                                    rx.text(f"Cliff: ~{proj['effective_cliff_lap']} Laps", font_family=FONT_MONO, font_size="9.5px", color=ACCENT_AMBER),
                                    rx.text("45 Laps (Severe Wear)", font_family=FONT_MONO, font_size="9.5px", color=TEXT_MUTED),
                                    justify="between",
                                    width="100%",
                                ),
                                width="100%",
                                spacing="1",
                                margin_bottom="1.25rem",
                            ),
                            # Fuel Onboard Slider with Live Numeric Badge
                            rx.vstack(
                                rx.hstack(
                                    rx.text("FUEL LOAD ONBOARD:", font_family=FONT_MONO, font_size="11px", color=TEXT_SECONDARY),
                                    rx.text(
                                        f"{ApexState.current_fuel_kg} kg",
                                        font_family=FONT_MONO,
                                        font_size="12px",
                                        font_weight="600",
                                        color=ACCENT_COBALT,
                                        padding="2px 8px",
                                        border_radius="6px",
                                        background_color="rgba(59, 130, 246, 0.12)",
                                        border="1px solid rgba(59, 130, 246, 0.25)",
                                    ),
                                    justify="between",
                                    width="100%",
                                    margin_bottom="4px",
                                ),
                                rx.slider(
                                    default_value=[45.0],
                                    value=ApexState.sim_fuel_kg,
                                    min=5,
                                    max=105,
                                    step=5,
                                    on_change=ApexState.set_sim_fuel,
                                    width="100%",
                                    aria_label="Fuel load onboard slider in kilograms",
                                ),
                                rx.hstack(
                                    rx.text("5 kg (Qualifying)", font_family=FONT_MONO, font_size="9.5px", color=TEXT_MUTED),
                                    rx.text("~0.33s penalty per 10kg", font_family=FONT_MONO, font_size="9.5px", color=TEXT_MUTED),
                                    rx.text("105 kg (Race Start)", font_family=FONT_MONO, font_size="9.5px", color=TEXT_MUTED),
                                    justify="between",
                                    width="100%",
                                ),
                                width="100%",
                                spacing="1",
                            ),
                            width="100%",
                            spacing="0",
                        ),
                        style=GLASS_CARD_STYLE,
                        flex="1.1",
                    ),
                    # ----------------------------------------------------------
                    # RIGHT PANEL: Live Telemetry Output & Trajectory Chart
                    # ----------------------------------------------------------
                    rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.text("02 // LIVE TELEMETRY OUTPUT", font_family=FONT_MONO, font_size="11.5px", font_weight="600", color=ACCENT_COLOR),
                                # Dynamic Verdict Badge
                                rx.box(
                                    rx.hstack(
                                        rx.box(
                                            width="6px",
                                            height="6px",
                                            border_radius="50%",
                                            background_color=proj["status_color"],
                                        ),
                                        rx.text(
                                            proj["status_text"],
                                            font_family=FONT_MONO,
                                            font_size="10px",
                                            font_weight="600",
                                            color=proj["status_color"],
                                        ),
                                        spacing="1",
                                        align="center",
                                    ),
                                    padding="3px 9px",
                                    border_radius="9999px",
                                    background_color=proj["status_bg"],
                                    border=f"1px solid {proj['status_border']}",
                                ),
                                justify="between",
                                width="100%",
                                align="center",
                                margin_bottom="1rem",
                            ),
                            # Verdict Plain-English Reason
                            rx.box(
                                rx.text(
                                    proj["status_reason"],
                                    font_size="12px",
                                    color=TEXT_SECONDARY,
                                    line_height="1.4",
                                ),
                                padding="8px 12px",
                                border_radius="8px",
                                background_color="rgba(255, 255, 255, 0.03)",
                                border=f"1px solid {BORDER_HAIRLINE}",
                                width="100%",
                                margin_bottom="1rem",
                            ),
                            # Stint Capacity Progress Bar
                            rx.box(
                                rx.vstack(
                                    rx.hstack(
                                        rx.text("TYRE STINT LIFE CAPACITY", font_family=FONT_MONO, font_size="10px", color=TEXT_SECONDARY),
                                        rx.text(
                                            f"{proj['stint_health_pct']}% Health ({proj['laps_remaining_to_cliff']} to cliff)",
                                            font_family=FONT_MONO,
                                            font_size="10.5px",
                                            font_weight="600",
                                            color=proj["status_color"],
                                        ),
                                        justify="between",
                                        width="100%",
                                        margin_bottom="6px",
                                    ),
                                    rx.box(
                                        rx.box(
                                            width=proj["stint_progress_width"],
                                            height="100%",
                                            border_radius="9999px",
                                            background_color=proj["status_color"],
                                            box_shadow=f"0 0 10px {proj['status_color']}",
                                            transition="width 0.3s cubic-bezier(0.16, 1, 0.3, 1)",
                                        ),
                                        width="100%",
                                        height="8px",
                                        border_radius="9999px",
                                        background_color="rgba(255, 255, 255, 0.08)",
                                        overflow="hidden",
                                    ),
                                    width="100%",
                                    spacing="1",
                                ),
                                padding="0.75rem 1rem",
                                style=GLASS_SUB_CARD,
                                width="100%",
                                margin_bottom="1rem",
                            ),
                            # 3 Metric Cards Row (m:ss.mmm, Delta, Cliff)
                            rx.hstack(
                                telemetry_metric_card("PREDICTED LAP PACE", proj["predicted_lap_time"], f"{proj['circuit_name']}", TEXT_PRIMARY),
                                telemetry_metric_card("PACE DELTA", proj["lap_delta_sec"], f"Tyres: {proj['tyre_degradation_sec']}", ACCENT_COLOR),
                                telemetry_metric_card("REMAINING STINT", proj["laps_remaining_to_cliff"], f"Fuel: {proj['fuel_weight_penalty']}", ACCENT_EMERALD),
                                spacing="3",
                                width="100%",
                                flex_direction=["column", "row", "row"],
                                margin_bottom="1rem",
                            ),
                            # Mini Stint Pace Trajectory Chart
                            rx.box(
                                rx.vstack(
                                    rx.hstack(
                                        rx.text("STINT PACE TRAJECTORY (35 LAPS)", font_family=FONT_MONO, font_size="10px", font_weight="600", color=TEXT_MUTED),
                                        rx.text("Fuel Burn vs Thermal Degradation", font_family=FONT_MONO, font_size="9.5px", color=TEXT_MUTED),
                                        justify="between",
                                        width="100%",
                                    ),
                                    rx.plotly(
                                        data=ApexState.simulator_pace_chart,
                                        height="160px",
                                    ),
                                    width="100%",
                                    spacing="0",
                                ),
                                padding="0.75rem 1rem",
                                style=GLASS_SUB_CARD,
                                width="100%",
                            ),
                            width="100%",
                            spacing="0",
                        ),
                        style=GLASS_CARD_STYLE,
                        flex="1.2",
                    ),
                    spacing="6",
                    flex_direction=["column", "column", "row"],
                    width="100%",
                    align="stretch",
                ),
                width="100%",
                margin_bottom="1.5rem",
            ),
            # Collapsible "How is this calculated?" Panel
            rx.accordion.root(
                rx.accordion.item(
                    rx.accordion.header(
                        rx.accordion.trigger(
                            rx.hstack(
                                rx.text("📐 HOW IS THIS CALCULATED? // MATHEMATICAL FORMULA & DATA SOURCES", font_family=FONT_MONO, font_size="12px", font_weight="600", color=ACCENT_COBALT),
                                rx.text("Click to expand methodology", font_family=FONT_MONO, font_size="10.5px", color=TEXT_MUTED),
                                justify="between",
                                width="100%",
                            ),
                        ),
                    ),
                    rx.accordion.content(
                        rx.vstack(
                            rx.text(
                                "1. Baseline Lap Time (Clean Air):",
                                font_family=FONT_MONO,
                                font_size="12px",
                                font_weight="600",
                                color=TEXT_PRIMARY,
                            ),
                            rx.text(
                                "Extracted from the 5th percentile of cleaned lap times in lap_times.csv across official modern Grands Prix "
                                "at each venue (Monza: 81.25s, Monaco: 74.82s, Silverstone: 87.41s, Spa: 104.90s, Interlagos: 71.30s).",
                                font_size="12.5px",
                                color=TEXT_SECONDARY,
                                line_height="1.5",
                            ),
                            rx.text(
                                "2. Fuel Load Weight Penalty:",
                                font_family=FONT_MONO,
                                font_size="12px",
                                font_weight="600",
                                color=TEXT_PRIMARY,
                                margin_top="8px",
                            ),
                            rx.text(
                                "Formula: Delta_Fuel = (Fuel_kg / 10.0) * 0.33s. "
                                "Calibrated against FIA technical telemetry showing ~0.33s per 10kg onboard fuel mass.",
                                font_size="12.5px",
                                color=TEXT_SECONDARY,
                                line_height="1.5",
                            ),
                            rx.text(
                                "3. Tyre Thermal Degradation & Performance Cliff:",
                                font_family=FONT_MONO,
                                font_size="12px",
                                font_weight="600",
                                color=TEXT_PRIMARY,
                                margin_top="8px",
                            ),
                            rx.text(
                                "Within operating window: Delta_Tyre = Stint_Age * Deg_Rate (Soft: 0.085s/lap, Medium: 0.055s/lap, Hard: 0.035s/lap). "
                                "Beyond thermal cliff: Delta_Tyre = (Cliff * Deg_Rate) + (Excess_Laps^1.6) * (Deg_Rate * 2.2).",
                                font_size="12.5px",
                                color=TEXT_SECONDARY,
                                line_height="1.5",
                            ),
                            rx.text(
                                "Note on Data Authenticity: Individual tyre compound telemetry (C1–C5) is an illustrative engineering model "
                                "calibrated against modern telemetry, as historical pre-2018 datasets recorded lap times but not individual compound codes.",
                                font_family=FONT_MONO,
                                font_size="11px",
                                color=ACCENT_AMBER,
                                margin_top="8px",
                            ),
                            align_items="start",
                            spacing="1",
                            padding="1rem",
                            background_color="rgba(0, 0, 0, 0.25)",
                            border_radius="8px",
                        ),
                    ),
                    value="formula_panel",
                ),
                collapsible=True,
                style=GLASS_SUB_CARD,
                width="100%",
            ),
            width="100%",
            spacing="0",
        ),
        id="simulator",
        max_width="1280px",
        margin="0 auto 4rem auto",
        padding_x=["1rem", "1.5rem", "2rem"],
        width="100%",
    )
