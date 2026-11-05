"""APEX // F1 — Modern Glassmorphic Design System Tokens & Presentation Layer.
Binds configurable design tokens [FONT_FAMILY], [PRIMARY_COLOR], [SECONDARY_COLOR],
[ACCENT_COLOR], [VIDEO_URL], [LLM_PROJECT_REPO], and [ASSET_PATH].
Replaces brutalist stark boxes with depth-layered surfaces, frosted-glass containers,
subtle radial glows, and 12px-16px / 9999px border radii.
"""

from __future__ import annotations
import reflex as rx

# ==============================================================================
# CONFIGURABLE CLIENT PLACEHOLDERS & TOKENS
# ==============================================================================
FONT_FAMILY: str = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
FONT_MONO: str = "'JetBrains Mono', 'SF Mono', 'Fira Code', monospace"

PRIMARY_COLOR: str = "#0B0E14"       # Deep Atmospheric Carbon Void
SECONDARY_COLOR: str = "#141923"     # Midnight Translucent Slate
ACCENT_COLOR: str = "#E10600"        # Iconic F1 High-Velocity Red
ACCENT_COBALT: str = "#3B82F6"       # Electric Data Highlight
ACCENT_EMERALD: str = "#10B981"      # Sector 1 / Optimal Pace Green
ACCENT_AMBER: str = "#F59E0B"        # Sector 2 / Caution Amber

# Standardized Constructor Colors across all charts
COLOR_FERRARI: str = "#E10600"
COLOR_MCLAREN: str = "#FF8000"
COLOR_MERCEDES: str = "#00D2BE"
COLOR_REDBULL: str = "#3B82F6"
COLOR_WILLIAMS: str = "#64C4FF"
COLOR_LOTUS: str = "#F59E0B"
COLOR_OTHER: str = "#64748B"

CONSTRUCTOR_COLORS = {
    "Ferrari": COLOR_FERRARI,
    "McLaren": COLOR_MCLAREN,
    "Mercedes": COLOR_MERCEDES,
    "Red Bull": COLOR_REDBULL,
    "Williams": COLOR_WILLIAMS,
    "Team Lotus": COLOR_LOTUS,
    "Lotus": COLOR_LOTUS,
    "Renault": "#FCD34D",
    "Benetton": "#06B6D4",
    "Brabham": "#818CF8",
    "Tyrrell": "#38BDF8",
    "Other": COLOR_OTHER,
}

# Colorblind-safe Categorical Palettes
ERA_COLORS = {
    "1950-1982 Ground Effect": "#38BDF8",
    "1983-2005 V10 / Turbo": "#F59E0B",
    "2006-2013 V8 Aero": "#A855F7",
    "2014-2026 Hybrid Era": "#E10600",
}

# Client Reference Placeholders
VIDEO_URL: str = "https://f1-preview.internal/reference-video"
LLM_PROJECT_REPO: str = "https://github.com/internal/data-hardware-analytics"
ASSET_PATH: str = "/assets"

# Glassmorphic Surface Palette
SURFACE_GLASS: str = "rgba(18, 24, 38, 0.72)"
SURFACE_GLASS_HOVER: str = "rgba(24, 32, 50, 0.85)"
SURFACE_ELEVATED: str = "rgba(26, 34, 52, 0.65)"
SURFACE_TERMINAL: str = "rgba(10, 13, 20, 0.94)"

# Border Tokens
BORDER_HAIRLINE: str = "rgba(255, 255, 255, 0.08)"
BORDER_HIGHLIGHT: str = "rgba(255, 255, 255, 0.16)"
BORDER_ACCENT_GLOW: str = "rgba(225, 6, 0, 0.35)"

# Text Hierarchy Tokens (Refined, WCAG AA Compliant)
TEXT_PRIMARY: str = "#F3F4F6"        # Crisp Off-White
TEXT_SECONDARY: str = "#D1D5DB"      # 75% White Opacity Equivalent for High Legibility
TEXT_MUTED: str = "#9CA3AF"          # Slate Technical Grey

# ==============================================================================
# REUSABLE PRESENTATION LAYER STYLES
# ==============================================================================

BASE_PAGE_STYLE = {
    "background_color": PRIMARY_COLOR,
    "background_image": (
        "radial-gradient(circle at 50% 0%, rgba(225, 6, 0, 0.07) 0%, transparent 45%), "
        "radial-gradient(circle at 85% 30%, rgba(59, 130, 246, 0.05) 0%, transparent 40%), "
        "radial-gradient(circle at 15% 70%, rgba(225, 6, 0, 0.04) 0%, transparent 45%)"
    ),
    "color": TEXT_PRIMARY,
    "font_family": FONT_FAMILY,
    "min_height": "100vh",
    "letter_spacing": "-0.012em",
    "padding": "0",
    "margin": "0",
    "box_sizing": "border-box",
}

# Floating Pill Navigation Bar
FLOATING_NAV_STYLE = {
    "background_color": "rgba(14, 18, 27, 0.85)",
    "backdrop_filter": "blur(20px)",
    "-webkit-backdrop-filter": "blur(20px)",
    "border": f"1px solid {BORDER_HIGHLIGHT}",
    "border_radius": "9999px",
    "box_shadow": "0 10px 30px -10px rgba(0, 0, 0, 0.5), 0 0 20px 0 rgba(255, 255, 255, 0.03)",
    "padding": "6px 14px",
    "transition": "all 0.3s cubic-bezier(0.16, 1, 0.3, 1)",
}

# Depth-Layered Glass Card (16px border-radius)
GLASS_CARD_STYLE = {
    "background_color": SURFACE_GLASS,
    "backdrop_filter": "blur(16px)",
    "-webkit-backdrop-filter": "blur(16px)",
    "border": f"1px solid {BORDER_HAIRLINE}",
    "border_radius": "16px",
    "box_shadow": "0 8px 32px 0 rgba(0, 0, 0, 0.36), inset 0 1px 0 0 rgba(255, 255, 255, 0.05)",
    "padding": "1.75rem",
    "transition": "border-color 0.25s ease, box-shadow 0.25s ease, transform 0.25s ease",
    "_hover": {
        "border_color": BORDER_HIGHLIGHT,
        "box_shadow": "0 12px 40px 0 rgba(0, 0, 0, 0.45), inset 0 1px 0 0 rgba(255, 255, 255, 0.08)",
    },
}

# Compact Sub-Card (12px border-radius)
GLASS_SUB_CARD = {
    "background_color": SURFACE_ELEVATED,
    "backdrop_filter": "blur(12px)",
    "-webkit-backdrop-filter": "blur(12px)",
    "border": f"1px solid {BORDER_HAIRLINE}",
    "border_radius": "12px",
    "padding": "1.25rem",
    "transition": "all 0.2s ease",
}

# Primary Pill Button with Directional Glow
BUTTON_PILL_PRIMARY = {
    "background_color": ACCENT_COLOR,
    "color": "#FFFFFF",
    "font_family": FONT_MONO,
    "font_size": "12px",
    "font_weight": "600",
    "letter_spacing": "0.06em",
    "min_height": "46px",
    "min_width": "46px",
    "padding": "0 1.75rem",
    "border_radius": "9999px",
    "border": f"1px solid {ACCENT_COLOR}",
    "cursor": "pointer",
    "box_shadow": f"0 4px 20px -2px {BORDER_ACCENT_GLOW}",
    "transition": "all 0.25s cubic-bezier(0.16, 1, 0.3, 1)",
    "_hover": {
        "background_color": "#FF1E1E",
        "border_color": "#FF1E1E",
        "box_shadow": "0 6px 28px -2px rgba(225, 6, 0, 0.55)",
        "transform": "translateY(-1px)",
    },
}

# Secondary Frosted Pill Button
BUTTON_PILL_SECONDARY = {
    "background_color": "rgba(255, 255, 255, 0.05)",
    "color": TEXT_PRIMARY,
    "font_family": FONT_MONO,
    "font_size": "12px",
    "font_weight": "500",
    "letter_spacing": "0.06em",
    "min_height": "46px",
    "min_width": "46px",
    "padding": "0 1.75rem",
    "border_radius": "9999px",
    "border": f"1px solid {BORDER_HIGHLIGHT}",
    "cursor": "pointer",
    "backdrop_filter": "blur(10px)",
    "transition": "all 0.25s cubic-bezier(0.16, 1, 0.3, 1)",
    "_hover": {
        "background_color": "rgba(255, 255, 255, 0.12)",
        "border_color": "rgba(255, 255, 255, 0.25)",
        "color": "#FFFFFF",
        "transform": "translateY(-1px)",
    },
}

# Eyebrow Badge (11-12px, weight 500, letter-spacing 0.08em)
EYEBROW_BADGE_STYLE = {
    "font_family": FONT_MONO,
    "font_size": "11px",
    "font_weight": "500",
    "text_transform": "uppercase",
    "letter_spacing": "0.08em",
    "color": ACCENT_COLOR,
    "background_color": "rgba(225, 6, 0, 0.12)",
    "border": "1px solid rgba(225, 6, 0, 0.25)",
    "border_radius": "9999px",
    "padding": "4px 14px",
    "display": "inline-flex",
    "align_items": "center",
    "gap": "6px",
}

# macOS Terminal Window Shell (16px border-radius)
MACOS_TERMINAL_SHELL = {
    "background_color": SURFACE_TERMINAL,
    "backdrop_filter": "blur(20px)",
    "-webkit-backdrop-filter": "blur(20px)",
    "border": f"1px solid {BORDER_HIGHLIGHT}",
    "border_radius": "16px",
    "box_shadow": "0 20px 50px -10px rgba(0, 0, 0, 0.7), inset 0 1px 0 0 rgba(255, 255, 255, 0.08)",
    "overflow": "hidden",
}
