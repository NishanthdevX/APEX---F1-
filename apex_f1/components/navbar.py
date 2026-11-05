"""APEX // F1 — Centered Floating Pill Navigation Header.
Features frosted-glass background, subtle border highlight, 9999px border-radius,
and active-tab pill indicators with anchor navigation.
"""

from __future__ import annotations
import reflex as rx
from apex_f1.styles import (
    FLOATING_NAV_STYLE,
    FONT_MONO,
    ACCENT_COLOR,
    ACCENT_COBALT,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    TEXT_MUTED,
    BORDER_HIGHLIGHT,
    BUTTON_PILL_PRIMARY,
)
from apex_f1.state import ApexState


def nav_tab(label: str, target_stage: int, anchor_id: str) -> rx.Component:
    """Active pill indicator for navigation links."""
    is_active = ApexState.active_stage == target_stage
    return rx.link(
        rx.box(
            rx.text(
                label,
                font_family=FONT_MONO,
                font_size="11.5px",
                font_weight=rx.cond(is_active, "600", "400"),
                letter_spacing="0.04em",
                color=rx.cond(is_active, "#FFFFFF", TEXT_SECONDARY),
            ),
            padding="6px 14px",
            border_radius="9999px",
            background_color=rx.cond(is_active, "rgba(255, 255, 255, 0.12)", "transparent"),
            border=rx.cond(is_active, "1px solid rgba(255, 255, 255, 0.18)", "1px solid transparent"),
            transition="all 0.2s ease",
            _hover={
                "color": "#FFFFFF",
                "background_color": "rgba(255, 255, 255, 0.08)",
            },
        ),
        href=anchor_id,
        on_click=ApexState.set_stage(target_stage),
        text_decoration="none",
        cursor="pointer",
        aria_label=f"Navigate to {label}",
    )


def navbar() -> rx.Component:
    """Centered floating frosted-glass pill navbar with 9999px border radius."""
    return rx.box(
        rx.hstack(
            # Brand & System Identity
            rx.hstack(
                rx.box(
                    rx.text("APEX", font_weight="800", font_size="16px", color=TEXT_PRIMARY, letter_spacing="-0.03em"),
                    rx.text("//", font_weight="800", font_size="16px", color=ACCENT_COLOR, margin_x="3px"),
                    rx.text("F1", font_weight="800", font_size="16px", color=TEXT_PRIMARY, letter_spacing="-0.03em"),
                    display="flex",
                    align_items="center",
                ),
                rx.box(
                    rx.text(
                        "1950–2026",
                        font_family=FONT_MONO,
                        font_size="10px",
                        font_weight="500",
                        color=TEXT_MUTED,
                        padding="2px 7px",
                        border_radius="9999px",
                        background_color="rgba(255, 255, 255, 0.05)",
                        border="1px solid rgba(255, 255, 255, 0.08)",
                    ),
                    margin_left="10px",
                    display=["none", "none", "block"],
                ),
                align="center",
            ),
            # Center Segmented Pill Switcher (Hick's Law: 4 Clear Anchors)
            rx.hstack(
                nav_tab("01 // DYNASTIES", 1, "#dynasties"),
                nav_tab("02 // SIMULATOR", 3, "#simulator"),
                nav_tab("03 // METHODOLOGY", 5, "#methodology"),
                nav_tab("04 // PIT-WALL", 1, "#pitwall"),
                spacing="1",
                display=["none", "none", "flex"],
                align="center",
                padding="2px",
                border_radius="9999px",
                background_color="rgba(255, 255, 255, 0.03)",
                border=f"1px solid {BORDER_HIGHLIGHT}",
            ),
            # Pill CTA Button with Directional Glow
            rx.link(
                rx.button(
                    rx.hstack(
                        rx.text("Launch Simulator", font_size="11.5px"),
                        rx.text("⚡", font_size="11px", margin_left="2px"),
                        align="center",
                        spacing="1",
                    ),
                    style=BUTTON_PILL_PRIMARY,
                    height="36px",
                    padding="0 1.25rem",
                    aria_label="Launch interactive pace simulator",
                ),
                href="#simulator",
                text_decoration="none",
            ),
            justify="between",
            align="center",
            width="100%",
        ),
        style=FLOATING_NAV_STYLE,
        position="sticky",
        top="16px",
        z_index="100",
        max_width="1020px",
        margin="0 auto 1.5rem auto",
        width="calc(100% - 2rem)",
    )
