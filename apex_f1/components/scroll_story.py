"""APEX // F1 — Multi-Mode Chart Switcher & Quadrant Explorer Section.
Features 5 numbered pill tab switchers, sub-view toggles, glassmorphic Plotly visualization
canvas with zero legend collision, takeaway titles, subtitles, "How to read" popovers,
dynamic data-driven insight callouts, dual filter sliders, and a responsive 4-column card grid.
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
)
from apex_f1.state import ApexState


def mode_tab_button(stage_num: int, label: str) -> rx.Component:
    """Numbered pill tab switcher (e.g. 1. Dynasties & Wins, 2. Driver Greatness, etc.)."""
    is_active = ApexState.active_stage == stage_num
    return rx.button(
        rx.hstack(
            rx.text(
                f"{stage_num}.",
                font_family=FONT_MONO,
                font_weight="700",
                color=rx.cond(is_active, "#FFFFFF", ACCENT_COBALT),
            ),
            rx.text(
                label,
                font_family=FONT_FAMILY,
                font_size="13px",
                font_weight=rx.cond(is_active, "600", "500"),
            ),
            spacing="1",
            align="center",
        ),
        on_click=ApexState.set_stage(stage_num),
        min_height="44px",
        padding="0 1.25rem",
        border_radius="9999px",
        background_color=rx.cond(is_active, ACCENT_COLOR, "rgba(255, 255, 255, 0.05)"),
        color=rx.cond(is_active, "#FFFFFF", TEXT_SECONDARY),
        border=rx.cond(is_active, f"1px solid {ACCENT_COLOR}", f"1px solid {BORDER_HAIRLINE}"),
        box_shadow=rx.cond(is_active, "0 4px 18px -2px rgba(225, 6, 0, 0.4)", "none"),
        cursor="pointer",
        transition="all 0.25s ease",
        _hover={
            "color": "#FFFFFF",
            "background_color": rx.cond(is_active, ACCENT_COLOR, "rgba(255, 255, 255, 0.1)"),
            "border_color": BORDER_HIGHLIGHT,
        },
        aria_label=f"Switch to visualization mode {label}",
    )


def subview_pill(label: str, is_active: rx.Var[bool], on_click_action: Any) -> rx.Component:
    """Sub-view toggle button for switching chart representations."""
    return rx.button(
        label,
        on_click=on_click_action,
        min_height="32px",
        padding="0 0.85rem",
        border_radius="9999px",
        font_family=FONT_MONO,
        font_size="11px",
        font_weight=rx.cond(is_active, "600", "400"),
        background_color=rx.cond(is_active, "rgba(59, 130, 246, 0.2)", "rgba(255, 255, 255, 0.03)"),
        color=rx.cond(is_active, "#FFFFFF", TEXT_MUTED),
        border=rx.cond(is_active, "1px solid rgba(59, 130, 246, 0.5)", f"1px solid {BORDER_HAIRLINE}"),
        cursor="pointer",
        transition="all 0.2s ease",
        _hover={
            "background_color": "rgba(255, 255, 255, 0.1)",
            "color": "#FFFFFF",
        },
        aria_label=f"Switch sub-view to {label}",
    )


def era_filter_pill(label: str, era_id: str) -> rx.Component:
    """Regulation era selector pill with frosted-glass styling."""
    is_active = ApexState.selected_era == era_id
    return rx.button(
        label,
        on_click=ApexState.set_era(era_id),
        min_height="34px",
        padding="0 0.9rem",
        border_radius="9999px",
        font_family=FONT_MONO,
        font_size="11px",
        font_weight=rx.cond(is_active, "600", "400"),
        background_color=rx.cond(is_active, "rgba(255, 255, 255, 0.14)", "rgba(255, 255, 255, 0.04)"),
        color=rx.cond(is_active, "#FFFFFF", TEXT_SECONDARY),
        border=rx.cond(is_active, f"1px solid {BORDER_HIGHLIGHT}", f"1px solid {BORDER_HAIRLINE}"),
        cursor="pointer",
        transition="all 0.2s ease",
        _hover={
            "background_color": "rgba(255, 255, 255, 0.1)",
            "color": "#FFFFFF",
        },
        aria_label=f"Filter era {label}",
    )


def leaderboard_card_item(item: dict) -> rx.Component:
    """Single card inside the responsive 4-column leaderboard card grid."""
    return rx.box(
        rx.hstack(
            rx.text(
                item["rank"],
                font_family=FONT_MONO,
                font_size="12px",
                font_weight="700",
                color=item["badge_color"],
                padding="2px 7px",
                border_radius="6px",
                background_color="rgba(255, 255, 255, 0.06)",
                border=f"1px solid {BORDER_HAIRLINE}",
            ),
            rx.text(
                item["era_tag"],
                font_family=FONT_MONO,
                font_size="9.5px",
                font_weight="500",
                color=TEXT_MUTED,
                padding="2px 6px",
                border_radius="4px",
                background_color="rgba(0, 0, 0, 0.3)",
            ),
            justify="between",
            align="center",
            width="100%",
            margin_bottom="10px",
        ),
        rx.heading(
            item["name"],
            font_size="15px",
            font_weight="600",
            color=TEXT_PRIMARY,
            letter_spacing="-0.01em",
            margin_bottom="2px",
            white_space="nowrap",
            overflow="hidden",
            text_overflow="ellipsis",
        ),
        rx.text(
            item["category"],
            font_family=FONT_MONO,
            font_size="10px",
            color=TEXT_MUTED,
            margin_bottom="12px",
        ),
        rx.hstack(
            rx.box(
                rx.text("PRIMARY INDEX", font_family=FONT_MONO, font_size="9px", color=TEXT_MUTED),
                rx.text(item["stat_primary"], font_family=FONT_MONO, font_size="12.5px", font_weight="600", color=ACCENT_COBALT),
            ),
            rx.box(
                rx.text("WINS / GPS", font_family=FONT_MONO, font_size="9px", color=TEXT_MUTED),
                rx.text(item["stat_secondary"], font_family=FONT_MONO, font_size="12.5px", font_weight="600", color=TEXT_PRIMARY),
            ),
            rx.box(
                rx.text("DETAIL", font_family=FONT_MONO, font_size="9px", color=TEXT_MUTED),
                rx.text(item["stat_detail"], font_family=FONT_MONO, font_size="12.5px", font_weight="600", color=ACCENT_EMERALD),
            ),
            justify="between",
            width="100%",
            padding_top="8px",
            border_top=f"1px solid {BORDER_HAIRLINE}",
        ),
        style=GLASS_SUB_CARD,
        _hover={
            "border_color": BORDER_HIGHLIGHT,
            "transform": "translateY(-2px)",
            "box_shadow": "0 8px 24px -4px rgba(0, 0, 0, 0.4)",
        },
    )


def scroll_story() -> rx.Component:
    """Multi-Mode Chart Switcher & Quadrant Explorer with Dual Sliders and 4-Column Grid."""
    return rx.box(
        rx.vstack(
            # Top Section Eyebrow & Title
            rx.vstack(
                rx.box(
                    rx.text("STAGE 04 // MULTI-MODE CHAMPIONSHIP DATA EXPLORER"),
                    style=EYEBROW_BADGE_STYLE,
                ),
                rx.heading(
                    "Championship Data Explorer",
                    font_size=["24px", "30px", "34px"],
                    font_weight="600",
                    letter_spacing="-0.02em",
                    color=TEXT_PRIMARY,
                ),
                rx.text(
                    "What you are looking at: 76 years of Formula 1 telemetry transformed into five distinct analytical dimensions. "
                    "Why it matters: Raw point totals skew historical comparisons due to changing scoring systems (8 pts in 1950 vs 25 pts today). "
                    "What to try: Switch between dynasty bar races, Z-score greatness quadrants, lap pace box plots, circuit maps, and decade heatmaps.",
                    font_size="14.5px",
                    line_height="1.6",
                    color=TEXT_SECONDARY,
                    max_width="780px",
                ),
                align_items="start",
                spacing="2",
                margin_bottom="1.5rem",
            ),
            # 5 Numbered Pill Tab Switchers
            rx.hstack(
                mode_tab_button(1, "Dynasties & Wins"),
                mode_tab_button(2, "Driver Greatness"),
                mode_tab_button(3, "Pace & Physics"),
                mode_tab_button(4, "Circuit Longevity"),
                mode_tab_button(5, "Decade Heatmap"),
                spacing="2",
                wrap="wrap",
                margin_bottom="1rem",
            ),
            # Sub-View Toggles & Regulation Era Row
            rx.hstack(
                # Dynamic Sub-View Toggles
                rx.cond(
                    ApexState.active_stage == 1,
                    rx.hstack(
                        subview_pill("Top 10 Bar Race", ApexState.stage1_view == "bar_race", ApexState.set_stage1_view("bar_race")),
                        subview_pill("Stacked Season Wins", ApexState.stage1_view == "season_wins", ApexState.set_stage1_view("season_wins")),
                        subview_pill("Dynasty Timeline", ApexState.stage1_view == "cumulative_stream", ApexState.set_stage1_view("cumulative_stream")),
                        spacing="2",
                    ),
                ),
                rx.cond(
                    ApexState.active_stage == 2,
                    rx.hstack(
                        subview_pill("Ranked Lollipop (Top 15)", ApexState.stage2_view == "ranked_bars", ApexState.set_stage2_view("ranked_bars")),
                        subview_pill("Bubble Quadrant", ApexState.stage2_view == "bubble_quadrant", ApexState.set_stage2_view("bubble_quadrant")),
                        spacing="2",
                    ),
                ),
                rx.cond(
                    ApexState.active_stage == 3,
                    rx.hstack(
                        subview_pill("Era Pace Box Plots", ApexState.stage3_view == "box_plots", ApexState.set_stage3_view("box_plots")),
                        subview_pill("Stint Pace Decay Curves", ApexState.stage3_view == "decay_curves", ApexState.set_stage3_view("decay_curves")),
                        spacing="2",
                    ),
                ),
                rx.cond(
                    ApexState.active_stage == 4,
                    rx.hstack(
                        subview_pill("Most-Raced Circuits", ApexState.stage4_view == "circuits_bar", ApexState.set_stage4_view("circuits_bar")),
                        subview_pill("Global Circuit Coordinates", ApexState.stage4_view == "circuits_map", ApexState.set_stage4_view("circuits_map")),
                        spacing="2",
                    ),
                ),
                # Era Pills
                rx.hstack(
                    era_filter_pill("All Eras", "All"),
                    era_filter_pill("1950–1982 Ground Effect", "1950-1982 Ground Effect"),
                    era_filter_pill("1983–2005 V10 / Turbo", "1983-2005 V10 / Turbo"),
                    era_filter_pill("2006–2013 V8 Aero", "2006-2013 V8 Aero"),
                    era_filter_pill("2014–2026 Hybrid", "2014-2026 Hybrid Era"),
                    spacing="2",
                    wrap="wrap",
                ),
                justify="between",
                align="center",
                width="100%",
                wrap="wrap",
                gap="3",
                margin_bottom="1.25rem",
            ),
            # Main Glassmorphic Visualization Canvas
            rx.box(
                rx.vstack(
                    # Header: Takeaway Title & Subtitle
                    rx.vstack(
                        rx.hstack(
                            rx.heading(
                                ApexState.stage_title,
                                font_size=["16px", "18px", "20px"],
                                font_weight="600",
                                color=TEXT_PRIMARY,
                                letter_spacing="-0.01em",
                            ),
                            rx.text(
                                "DOHERTY <50MS",
                                font_family=FONT_MONO,
                                font_size="10px",
                                font_weight="600",
                                padding="3px 9px",
                                border_radius="9999px",
                                background_color="rgba(16, 185, 129, 0.12)",
                                color=ACCENT_EMERALD,
                                border="1px solid rgba(16, 185, 129, 0.3)",
                                display=["none", "block"],
                            ),
                            justify="between",
                            align="center",
                            width="100%",
                        ),
                        rx.text(
                            ApexState.stage_subtitle,
                            font_family=FONT_MONO,
                            font_size="11.5px",
                            color=TEXT_MUTED,
                        ),
                        align_items="start",
                        spacing="1",
                        width="100%",
                        border_bottom=f"1px solid {BORDER_HAIRLINE}",
                        padding_bottom="12px",
                        margin_bottom="8px",
                    ),
                    # "How to read this chart" explanation accordion/box
                    rx.box(
                        rx.hstack(
                            rx.text("ℹ", font_size="12px", color=ACCENT_COBALT),
                            rx.text(
                                ApexState.stage_how_to_read,
                                font_size="12px",
                                color=TEXT_SECONDARY,
                                line_height="1.5",
                            ),
                            spacing="2",
                            align="start",
                        ),
                        padding="8px 12px",
                        border_radius="8px",
                        background_color="rgba(59, 130, 246, 0.06)",
                        border="1px solid rgba(59, 130, 246, 0.15)",
                        width="100%",
                        margin_bottom="12px",
                    ),
                    # Pinned Interactive Plotly Figure
                    rx.box(
                        rx.plotly(
                            data=ApexState.main_stage_figure,
                            height="500px",
                        ),
                        width="100%",
                        height="500px",
                    ),
                    # Bottom Insight Callout
                    rx.box(
                        rx.hstack(
                            rx.text("⚡", font_size="13px", color=ACCENT_AMBER),
                            rx.text(
                                ApexState.stage_insight_callout,
                                font_size="12.5px",
                                font_weight="500",
                                color=TEXT_PRIMARY,
                                line_height="1.5",
                            ),
                            spacing="2",
                            align="start",
                        ),
                        padding="10px 14px",
                        border_radius="10px",
                        background_color="rgba(245, 158, 11, 0.08)",
                        border="1px solid rgba(245, 158, 11, 0.2)",
                        width="100%",
                        margin_top="10px",
                    ),
                    width="100%",
                    spacing="0",
                ),
                style=GLASS_CARD_STYLE,
                width="100%",
                margin_bottom="2rem",
            ),
            # Dual Filter Sliders (Timeline Scrubber + Min Wins Filter)
            rx.box(
                rx.hstack(
                    # Left Slider: Timeline Scrubber (1950 to 2026)
                    rx.box(
                        rx.hstack(
                            rx.text("TIMELINE SCRUBBER (CHAMPIONSHIP YEAR):", font_family=FONT_MONO, font_size="11px", color=TEXT_SECONDARY),
                            rx.text(
                                f"{ApexState.current_scrub_year}",
                                font_family=FONT_MONO,
                                font_size="12.5px",
                                font_weight="700",
                                color=ACCENT_COBALT,
                                padding="2px 8px",
                                border_radius="6px",
                                background_color="rgba(59, 130, 246, 0.12)",
                                border="1px solid rgba(59, 130, 246, 0.25)",
                            ),
                            justify="between",
                            width="100%",
                            margin_bottom="6px",
                        ),
                        rx.slider(
                            default_value=[2026.0],
                            value=ApexState.scrub_year,
                            min=ApexState.scrub_min_year,
                            max=ApexState.scrub_max_year,
                            step=1,
                            on_change=ApexState.set_scrub_year,
                            width="100%",
                            aria_label="Championship season timeline slider",
                        ),
                        rx.hstack(
                            rx.text(f"{ApexState.scrub_min_year}", font_family=FONT_MONO, font_size="10px", color=TEXT_MUTED),
                            rx.text("DRAG TO SCRUB HISTORICAL SEASON CUMULATIVES", font_family=FONT_MONO, font_size="9.5px", color=TEXT_MUTED),
                            rx.text(f"{ApexState.scrub_max_year}", font_family=FONT_MONO, font_size="10px", color=TEXT_MUTED),
                            justify="between",
                            width="100%",
                        ),
                        flex="1",
                    ),
                    # Right Slider: Min Wins Sensitivity Filter
                    rx.box(
                        rx.hstack(
                            rx.text("MINIMUM CAREER WINS THRESHOLD:", font_family=FONT_MONO, font_size="11px", color=TEXT_SECONDARY),
                            rx.text(
                                f"≥ {ApexState.current_min_wins} WINS",
                                font_family=FONT_MONO,
                                font_size="12.5px",
                                font_weight="700",
                                color=ACCENT_COLOR,
                                padding="2px 8px",
                                border_radius="6px",
                                background_color="rgba(225, 6, 0, 0.12)",
                                border="1px solid rgba(225, 6, 0, 0.25)",
                            ),
                            justify="between",
                            width="100%",
                            margin_bottom="6px",
                        ),
                        rx.slider(
                            default_value=[0.0],
                            value=ApexState.min_wins_filter,
                            min=0,
                            max=40,
                            step=5,
                            on_change=ApexState.set_min_wins_filter,
                            width="100%",
                            aria_label="Minimum career wins filter slider",
                        ),
                        rx.hstack(
                            rx.text("0 WINS (ALL ENTRIES)", font_family=FONT_MONO, font_size="10px", color=TEXT_MUTED),
                            rx.text("FILTER OUTLIERS // ELITE ONLY", font_family=FONT_MONO, font_size="9.5px", color=TEXT_MUTED),
                            rx.text("40+ WINS", font_family=FONT_MONO, font_size="10px", color=TEXT_MUTED),
                            justify="between",
                            width="100%",
                        ),
                        flex="1",
                    ),
                    spacing="6",
                    flex_direction=["column", "column", "row"],
                    width="100%",
                ),
                style=GLASS_SUB_CARD,
                width="100%",
                margin_bottom="2rem",
            ),
            # Responsive 4-Column Card Grid Header & Search
            rx.cond(
                ApexState.show_leaderboard_grid,
                rx.vstack(
                    rx.hstack(
                        rx.vstack(
                            rx.text("COHORT LEADERBOARD // FILTERED STANDINGS", font_family=FONT_MONO, font_size="11px", font_weight="600", color=ACCENT_COBALT),
                            rx.text("Ranked standings synchronized with active timeline and win filters", font_size="12px", color=TEXT_MUTED),
                            align_items="start",
                            spacing="1",
                        ),
                        rx.input(
                            placeholder="Search driver or constructor...",
                            value=ApexState.search_query,
                            on_change=ApexState.set_search_query,
                            width=["100%", "260px"],
                            min_height="38px",
                            border_radius="9999px",
                            background_color="rgba(255, 255, 255, 0.05)",
                            border=f"1px solid {BORDER_HIGHLIGHT}",
                            font_family=FONT_MONO,
                            font_size="12px",
                            color=TEXT_PRIMARY,
                            padding_x="14px",
                            aria_label="Search driver or constructor name",
                        ),
                        justify="between",
                        align="center",
                        width="100%",
                        wrap="wrap",
                        margin_bottom="1.25rem",
                    ),
                    rx.grid(
                        rx.foreach(
                            ApexState.leaderboard_cards,
                            leaderboard_card_item,
                        ),
                        columns=rx.breakpoints(initial="1", sm="2", md="3", lg="4"),
                        spacing="4",
                        width="100%",
                    ),
                    width="100%",
                    spacing="0",
                ),
            ),
            width="100%",
            spacing="0",
        ),
        id="dynasties",
        max_width="1280px",
        margin="0 auto 4rem auto",
        padding_x=["1rem", "1.5rem", "2rem"],
        width="100%",
    )
