"""APEX // F1 (1950–2026) — Modern Data-Driven Presentation Layer.
Master page index incorporating the floating pill navigation, glassmorphic hero banner,
multi-mode chart switcher with quadrant explorer, 2-column split-view strategy simulator,
methodology & statistical integrity section, macOS-styled rich pit-wall terminal,
and back-to-top navigation.
"""

from __future__ import annotations
import reflex as rx
from rxconfig import config
from apex_f1.styles import (
    BASE_PAGE_STYLE,
    FONT_FAMILY,
    FONT_MONO,
    ACCENT_COLOR,
    ACCENT_COBALT,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    TEXT_MUTED,
    BORDER_HAIRLINE,
    BORDER_HIGHLIGHT,
    SURFACE_GLASS,
    ASSET_PATH,
    VIDEO_URL,
    LLM_PROJECT_REPO,
)
from apex_f1.state import ApexState
from apex_f1.components.navbar import navbar
from apex_f1.components.hero import hero
from apex_f1.components.scroll_story import scroll_story
from apex_f1.components.pace_simulator import pace_simulator
from apex_f1.components.methodology import methodology
from apex_f1.components.rich_pitwall import rich_pitwall


def footer() -> rx.Component:
    """Modern frosted-glass footer with architecture and dataset attribution."""
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.hstack(
                    rx.text("APEX", font_weight="800", font_size="16px", color=TEXT_PRIMARY, letter_spacing="-0.03em"),
                    rx.text("//", font_weight="800", font_size="16px", color=ACCENT_COLOR, margin_x="3px"),
                    rx.text("F1", font_weight="800", font_size="16px", color=TEXT_PRIMARY, letter_spacing="-0.03em"),
                    display="flex",
                    align_items="center",
                ),
                rx.text(
                    "FIA WORLD CHAMPIONSHIP STATISTICAL TELEMETRY PLATFORM (1950–2026)",
                    font_family=FONT_MONO,
                    font_size="11px",
                    color=TEXT_MUTED,
                ),
                align_items="start",
                spacing="1",
            ),
            rx.hstack(
                rx.text("TECH STACK:", font_family=FONT_MONO, font_size="11px", color=TEXT_MUTED),
                rx.text("REFLEX + POLARS + R STATS + RICH SVG", font_family=FONT_MONO, font_size="11px", font_weight="600", color=ACCENT_COBALT),
                spacing="2",
            ),
            rx.text(
                "DATASET: FORMULA 1 HISTORICAL CORPUS // 1,167 GRANDS PRIX",
                font_family=FONT_MONO,
                font_size="11px",
                color=TEXT_MUTED,
            ),
            justify="between",
            align="center",
            width="100%",
            max_width="1280px",
            margin="0 auto",
            padding_x=["1rem", "1.5rem", "2rem"],
            padding_y="2.5rem",
            wrap="wrap",
        ),
        border_top=f"1px solid {BORDER_HAIRLINE}",
        background_color="rgba(10, 13, 20, 0.85)",
        backdrop_filter="blur(16px)",
        width="100%",
    )


def back_to_top_button() -> rx.Component:
    """Floating back to top shortcut."""
    return rx.link(
        rx.button(
            rx.hstack(
                rx.text("↑", font_size="13px", font_weight="700"),
                rx.text("Top", font_family=FONT_MONO, font_size="11px"),
                spacing="1",
                align="center",
            ),
            position="fixed",
            bottom="24px",
            right="24px",
            z_index="99",
            min_height="36px",
            padding="0 14px",
            border_radius="9999px",
            background_color="rgba(14, 18, 27, 0.85)",
            backdrop_filter="blur(16px)",
            border="1px solid rgba(255, 255, 255, 0.16)",
            box_shadow="0 8px 24px rgba(0, 0, 0, 0.5)",
            color="#F3F4F6",
            cursor="pointer",
            _hover={"background_color": ACCENT_COLOR, "border_color": ACCENT_COLOR},
            aria_label="Scroll back to top of page",
        ),
        href="#",
        text_decoration="none",
    )


def index() -> rx.Component:
    """Master presentation layout."""
    return rx.box(
        navbar(),
        hero(),
        scroll_story(),
        pace_simulator(),
        methodology(),
        rich_pitwall(),
        footer(),
        back_to_top_button(),
        style=BASE_PAGE_STYLE,
    )


app = rx.App(
    style=BASE_PAGE_STYLE,
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin="anonymous"),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(
    index,
    route="/",
    title="APEX // F1 (1950–2026) — Telemetry & Analytics Platform",
    description="Formula 1 World Championship (1950–2026) Multi-Mode Telemetry & Strategy Analytics Engine.",
)
