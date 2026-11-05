"""APEX // F1 — macOS-Inspired Rich Pit-Wall Terminal Component.
Styles the Python `rich` terminal SVG output inside a sleek macOS window shell
with window control dots, title bar, and interactive [ ▶ Run Telemetry ] trigger.
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
    MACOS_TERMINAL_SHELL,
    EYEBROW_BADGE_STYLE,
    BUTTON_PILL_PRIMARY,
    ASSET_PATH,
)
from apex_f1.state import ApexState


def macos_window_dot(color: str) -> rx.Component:
    """macOS window traffic light control dot."""
    return rx.box(
        width="11px",
        height="11px",
        border_radius="50%",
        background_color=color,
        border="1px solid rgba(0, 0, 0, 0.2)",
    )


def rich_pitwall() -> rx.Component:
    """macOS-inspired terminal window shell with interactive action trigger and live Rich SVG."""
    return rx.box(
        rx.vstack(
            # Top Section Eyebrow & Title
            rx.hstack(
                rx.vstack(
                    rx.box(
                        rx.text("STEP 02 // POLARS + RICH FIA PIT-WALL BRIDGE"),
                        style=EYEBROW_BADGE_STYLE,
                    ),
                    rx.heading(
                        "Live Pit-Wall Telemetry Console",
                        font_size=["24px", "30px", "34px"],
                        font_weight="600",
                        letter_spacing="-0.02em",
                        color=TEXT_PRIMARY,
                    ),
                    rx.text(
                        "Relational tables joined in <50ms with Polars and rendered via rich.console.Console(record=True). "
                        "Live SVG vector export embedded directly in the React DOM with zero pixelation.",
                        font_size="13.5px",
                        color=TEXT_SECONDARY,
                        max_width="720px",
                    ),
                    align_items="start",
                    spacing="2",
                ),
                # Interactive Action Trigger [ ▶ Run Telemetry ] / [ ↻ Replay ]
                rx.button(
                    rx.hstack(
                        rx.text("▶", font_size="11px"),
                        rx.text("RUN TELEMETRY"),
                        rx.text("↻", font_size="13px", margin_left="4px"),
                        spacing="1",
                        align="center",
                    ),
                    on_click=ApexState.trigger_telemetry_run,
                    style=BUTTON_PILL_PRIMARY,
                    height="42px",
                    padding="0 1.25rem",
                    aria_label="Run live telemetry pipeline",
                ),
                justify="between",
                align="center",
                width="100%",
                wrap="wrap",
                margin_bottom="1.5rem",
            ),
            # macOS-Inspired Terminal Window Container
            rx.box(
                # Top macOS Window Title Bar
                rx.hstack(
                    # Left Traffic Light Window Dots
                    rx.hstack(
                        macos_window_dot("#FF5F56"),  # Close
                        macos_window_dot("#FFBD2E"),  # Minimize
                        macos_window_dot("#27C93F"),  # Maximize
                        spacing="2",
                        align="center",
                    ),
                    # Center Window Title
                    rx.hstack(
                        rx.text(
                            "zsh — f1_pitwall_telemetry.py — 94×28",
                            font_family=FONT_MONO,
                            font_size="11.5px",
                            font_weight="600",
                            color=TEXT_SECONDARY,
                        ),
                        spacing="2",
                        align="center",
                    ),
                    # Right Execution Status
                    rx.hstack(
                        rx.box(
                            width="6px",
                            height="6px",
                            border_radius="50%",
                            background_color=ACCENT_EMERALD,
                            box_shadow=f"0 0 8px {ACCENT_EMERALD}",
                        ),
                        rx.text(
                            ApexState.telemetry_status,
                            font_family=FONT_MONO,
                            font_size="10.5px",
                            font_weight="700",
                            color=ACCENT_EMERALD,
                        ),
                        spacing="2",
                        align="center",
                    ),
                    justify="between",
                    align="center",
                    width="100%",
                    padding="12px 18px",
                    background_color="rgba(14, 18, 27, 0.95)",
                    border_bottom=f"1px solid {BORDER_HAIRLINE}",
                ),
                # Terminal Content (Embedded Rich SVG)
                rx.box(
                    rx.html(
                        ApexState.pitwall_svg,
                    ),
                    width="100%",
                    overflow_x="auto",
                    padding=["1rem", "1.5rem"],
                    background_color="rgba(10, 13, 20, 0.96)",
                ),
                # Bottom Terminal Status / Telemetry Footer
                rx.hstack(
                    rx.hstack(
                        rx.text("TERMINAL CORE:", font_family=FONT_MONO, font_size="11px", color=TEXT_MUTED),
                        rx.text("PYTHON RICH 14.3 + POLARS 2.1", font_family=FONT_MONO, font_size="11px", font_weight="700", color=TEXT_PRIMARY),
                        spacing="2",
                    ),
                    rx.hstack(
                        rx.text("TIMESTAMP:", font_family=FONT_MONO, font_size="11px", color=TEXT_MUTED),
                        rx.text(ApexState.last_telemetry_timestamp, font_family=FONT_MONO, font_size="11px", font_weight="700", color=ACCENT_COBALT),
                        spacing="2",
                    ),
                    rx.hstack(
                        rx.text("PIPELINE LATENCY:", font_family=FONT_MONO, font_size="11px", color=TEXT_MUTED),
                        rx.text("<42MS (DOHERTY LEVEL)", font_family=FONT_MONO, font_size="11px", font_weight="700", color=ACCENT_EMERALD),
                        spacing="2",
                    ),
                    justify="between",
                    align="center",
                    width="100%",
                    wrap="wrap",
                    padding="10px 18px",
                    background_color="rgba(14, 18, 27, 0.95)",
                    border_top=f"1px solid {BORDER_HAIRLINE}",
                ),
                style=MACOS_TERMINAL_SHELL,
                width="100%",
            ),
            width="100%",
            spacing="0",
        ),
        id="pitwall",
        max_width="1280px",
        margin="0 auto 4rem auto",
        padding_x=["1rem", "1.5rem", "2rem"],
        width="100%",
    )
