"""APEX // F1 — Modern Glassmorphic Hero Presentation.
Features centered eyebrow badge, clamp display typography (weight 600) with gradient accent,
dual pill CTAs with directional micro-interactions, unified glassmorphic metric banner,
and a 3-card quick-feature preview row.
"""

from __future__ import annotations
import reflex as rx
from apex_f1.styles import (
    FONT_FAMILY,
    FONT_MONO,
    ACCENT_COLOR,
    ACCENT_COBALT,
    ACCENT_EMERALD,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    TEXT_MUTED,
    BORDER_HAIRLINE,
    BORDER_HIGHLIGHT,
    GLASS_CARD_STYLE,
    GLASS_SUB_CARD,
    BUTTON_PILL_PRIMARY,
    BUTTON_PILL_SECONDARY,
    EYEBROW_BADGE_STYLE,
)
from apex_f1.state import ApexState


def glass_kpi_cell(number: str, label: str, subtext: str, is_last: bool = False) -> rx.Component:
    """Cell inside the unified rounded glassmorphic metric banner."""
    return rx.box(
        rx.text(
            label,
            font_family=FONT_MONO,
            font_size="10.5px",
            font_weight="600",
            color=ACCENT_COBALT,
            letter_spacing="0.08em",
            text_transform="uppercase",
            margin_bottom="6px",
        ),
        rx.text(
            number,
            font_family=FONT_FAMILY,
            font_size=["28px", "34px", "38px"],
            font_weight="600",
            line_height="1.1",
            color=TEXT_PRIMARY,
            letter_spacing="-0.02em",
        ),
        rx.text(
            subtext,
            font_family=FONT_MONO,
            font_size="11.5px",
            color=TEXT_MUTED,
            margin_top="6px",
        ),
        padding=["1.25rem", "1.75rem"],
        flex="1",
        border_right=["none", "none", rx.cond(is_last, "none", f"1px solid {BORDER_HAIRLINE}")],
        border_bottom=[rx.cond(is_last, "none", f"1px solid {BORDER_HAIRLINE}"), rx.cond(is_last, "none", f"1px solid {BORDER_HAIRLINE}"), "none"],
        text_align=["center", "center", "left"],
    )


def quick_feature_card(num: str, title: str, desc: str, tag: str, tag_color: str) -> rx.Component:
    """Quick-feature preview card below the hero fold."""
    return rx.box(
        rx.hstack(
            rx.text(num, font_family=FONT_MONO, font_size="12px", font_weight="700", color=tag_color),
            rx.text(
                tag,
                font_family=FONT_MONO,
                font_size="9.5px",
                font_weight="600",
                padding="2px 7px",
                border_radius="9999px",
                background_color="rgba(255, 255, 255, 0.06)",
                border=f"1px solid {BORDER_HAIRLINE}",
                color=TEXT_SECONDARY,
            ),
            justify="between",
            margin_bottom="8px",
        ),
        rx.heading(
            title,
            font_size="15px",
            font_weight="600",
            color=TEXT_PRIMARY,
            margin_bottom="4px",
            letter_spacing="-0.01em",
        ),
        rx.text(
            desc,
            font_size="12.5px",
            line_height="1.5",
            color=TEXT_MUTED,
        ),
        style=GLASS_SUB_CARD,
        flex="1",
        min_width=["100%", "260px"],
        _hover={
            "border_color": BORDER_HIGHLIGHT,
            "transform": "translateY(-2px)",
        },
    )


def hero() -> rx.Component:
    """Centered Modern Glassmorphic Hero Banner."""
    return rx.box(
        rx.vstack(
            # Centered Eyebrow Badge
            rx.box(
                rx.hstack(
                    rx.box(
                        width="7px",
                        height="7px",
                        background_color=ACCENT_COLOR,
                        border_radius="50%",
                        box_shadow=f"0 0 10px {ACCENT_COLOR}",
                    ),
                    rx.text("FORMULA 1 WORLD CHAMPIONSHIP // 1950–2026"),
                    spacing="2",
                    align="center",
                ),
                style=EYEBROW_BADGE_STYLE,
                margin_bottom="18px",
            ),
            # Centered Display Title (Scale: weight 600, clamp(2.25rem, 4.5vw, 3.5rem))
            rx.heading(
                "Decode 76 Years of ",
                rx.text.span(
                    "Formula 1 Speed & Telemetry.",
                    background_image=f"linear-gradient(135deg, {ACCENT_COLOR} 20%, #FF8000 65%, #FFFFFF 100%)",
                    background_clip="text",
                    color="transparent",
                ),
                font_size="clamp(2.25rem, 4.5vw, 3.5rem)",
                font_weight="600",
                line_height="1.1",
                letter_spacing="-0.02em",
                text_align="center",
                max_width="920px",
                margin_bottom="16px",
            ),
            # Concise Subtitle
            rx.text(
                "Unifying 76 championship seasons into an era-adjusted mathematical index. "
                "Compare Fangio, Clark, Senna, Schumacher, Hamilton, and Verstappen on a standardized within-season Z-score scale "
                "while scrubbing 636,000+ millisecond lap records in sub-50ms query time.",
                font_size=["14.5px", "15.5px"],
                line_height="1.6",
                color=TEXT_SECONDARY,
                text_align="center",
                max_width="720px",
                margin_bottom="26px",
            ),
            # Dual Pill CTA Buttons with Directional Micro-Interactions
            rx.hstack(
                rx.link(
                    rx.button(
                        rx.hstack(
                            rx.text("Explore Telemetry"),
                            rx.text("→", font_size="13px", margin_left="2px"),
                            align="center",
                            spacing="1",
                        ),
                        style=BUTTON_PILL_PRIMARY,
                        aria_label="Explore live F1 telemetry and dynasties",
                    ),
                    href="#dynasties",
                    text_decoration="none",
                ),
                rx.link(
                    rx.button(
                        rx.hstack(
                            rx.text("Launch Simulator"),
                            rx.text("⚡", font_size="12px", margin_left="2px"),
                            align="center",
                            spacing="1",
                        ),
                        style=BUTTON_PILL_SECONDARY,
                        aria_label="Launch interactive pace and tyre simulator",
                    ),
                    href="#simulator",
                    text_decoration="none",
                ),
                spacing="3",
                justify="center",
                wrap="wrap",
                margin_bottom="44px",
            ),
            # Unified Rounded Glassmorphic Metric Banner
            rx.box(
                rx.hstack(
                    glass_kpi_cell("1,167", "GRANDS PRIX INDEXED", "Silverstone 1950 to Modern 2026", is_last=False),
                    glass_kpi_cell("77 SEASONS", "REGULATION ERAS NORMALIZED", "Ground Effect, V10, V8 & Hybrids", is_last=False),
                    glass_kpi_cell("636,494", "LAP RECORDS PROCESSED", "<50ms Ingestion via Polars Core", is_last=True),
                    spacing="0",
                    width="100%",
                    flex_direction=["column", "column", "row"],
                ),
                style=GLASS_CARD_STYLE,
                padding="0.5rem",
                width="100%",
                max_width="1140px",
                margin_bottom="28px",
            ),
            # 3-Card Quick-Feature Preview Row Below the Fold
            rx.hstack(
                quick_feature_card(
                    "01",
                    "Within-Season Z-Score",
                    "Normalizes Fangio's 8-pt wins against modern 25-pt sprint victories on an identical statistical scale.",
                    "R STATS CORE",
                    ACCENT_COLOR,
                ),
                quick_feature_card(
                    "02",
                    "Pace Decay Modeling",
                    "Filters safety-car outliers (>1.25x median) across 28,000+ Monza laps to isolate pure tyre degradation.",
                    "IQR FILTER",
                    ACCENT_COBALT,
                ),
                quick_feature_card(
                    "03",
                    "Sub-50ms Speed",
                    "Pre-aggregated relational queries compiled with Polars for instant, responsive slider interaction.",
                    "POLARS CORE",
                    ACCENT_EMERALD,
                ),
                spacing="4",
                width="100%",
                max_width="1140px",
                flex_direction=["column", "row", "row"],
            ),
            align="center",
            width="100%",
            padding_y=["2rem", "3rem", "4rem"],
        ),
        max_width="1280px",
        margin="0 auto",
        padding_x=["1rem", "1.5rem", "2rem"],
        width="100%",
    )
