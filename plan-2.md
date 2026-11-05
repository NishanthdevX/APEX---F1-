ROLE
You are a Senior Data-Visualization Engineer and UI/UX Designer. You are working on "APEX // F1", a Data Analysis & Visualization (DAV) project built in pure Python (Reflex, Polars, Plotly, Rich) with an R statistical engine, on the Kaggle "Formula 1 World Championship (1950–2026)" dataset. The project is graded and presented as a DAV project, so the data, the charts, and the clarity of the insights matter more than decoration.

GOAL
Improve the existing app so that:
(a) the charts are varied, correct, readable and animated,
(b) the simulator works correctly and is understandable,
(c) the typography is subtle and refined,
(d) a first-time visitor can understand every section without prior F1 or statistics knowledge.
Keep the current dark, glassmorphic F1 look, the floating pill navbar, and the existing file structure. Do not rebuild from scratch.

STEP 0: AUDIT FIRST (no code changes yet)
1. Run the app (`python -m reflex run`) and read every file in apex_f1/, r_analytics/ and data/.
2. If the reference screen recording is available, watch it and list every visible bug: chart collisions, broken or empty charts, sliders that do nothing, NaN or "undefined" values, console or WebSocket errors, layout overflow.
3. Output a short numbered audit (file, problem, planned fix) before editing. Fix everything on the list.

STEP 1: CHART OVERHAUL (variety and correctness)
Replace the "everything is a line or scatter" feel with the chart type that best fits each question. Add a chart-type switcher where it makes sense. Minimum set:
- Constructor dynasties: horizontal bar chart race, top 10 constructors by cumulative points or wins up to the selected year, re-sorted each year. Also offer a stacked area or line view of share by era.
- Driver greatness (R era-adjusted Z-score): horizontal ranked bar or lollipop chart of the top 15 drivers, with a toggle for vertical columns. Add a bubble quadrant (Z-score vs win share, sized by titles) as a second view.
- Wins by season: vertical grouped or stacked column chart, one bar per season, colored by constructor.
- Lap pace: box or violin plot of lap milliseconds by era or circuit, and a line chart of pace decay by lap number (stint).
- Circuits: a bar chart of the most-raced circuits, plus an optional map or scatter of lat/lng from circuits.csv.
- A correlation or consistency heatmap (for example constructor by decade, win share) with an annotated color scale.
Every chart must have:
- A takeaway title that states the insight (for example "Ferrari and McLaren have led more seasons than any other teams"), not just a label.
- A subtitle that gives the unit, the period and the data source file.
- Direct data labels where there are 10 bars or fewer. Legends only when unavoidable, placed horizontally above the plot with enough top margin so nothing overlaps.
- Consistent constructor colors across all charts (Ferrari #E10600, McLaren #FF8000, Mercedes #00D2BE, Red Bull #3B82F6, Williams #64C4FF, Lotus #F59E0B, "Other" neutral gray). Use a colorblind-safe palette for non-team categories.
- Labeled axes with units, sorted categories, thousands separators, no chartjunk, subtle gridlines (rgba(255,255,255,0.05)).
- Rich hover tooltips with plain-language fields (name, season, value, rank).
- Hick's Law: at most 10 categories shown, with the rest grouped into "Other (click to expand)".

STEP 2: CHART ANIMATIONS
Use Plotly frames or layout transitions where they work. Do not fake animation with timers that re-render the whole page.
- Bar chart race: Plotly animation frames per season, a Play/Pause button, a season slider, and a speed control (0.5x/1x/2x). Easing "cubic-in-out", about 500–700ms per frame, with bars smoothly reordering.
- On scroll into view, charts do an entrance animation (bars grow from the baseline, lines draw left to right, bubbles scale in), staggered by 60–80ms. Use CSS or IntersectionObserver through Reflex's native hooks, with no heavy libraries.
- Switching tabs or chart types uses a smooth transition: a 200ms fade/slide plus a Plotly transition, with no layout jump.
- Hover micro-interactions: highlight the hovered series and dim the others.
- Respect `prefers-reduced-motion` by disabling the animations and showing the final state.
- Keep interactions under 150ms by pre-computing Polars aggregates once at startup and caching them. Never recompute heavy joins inside @rx.var on every slider tick.

STEP 3: FIX THE SIMULATOR (Lap Pace and Tyre Strategy)
Audit it as a real analytical tool and make it trustworthy:
1. Every output must come from a documented formula grounded in the data (the lap_times.csv median pace per circuit or era, plus a clearly labeled linear or quadratic degradation model fitted on the actual data, ideally with the R loess/lm output). If a parameter such as tyre compound is not in the dataset, label it "illustrative model assumption" in the UI. Do not present invented numbers as real data.
2. Handle all edge cases without ever showing NaN, undefined, negative lap times or a blank panel. Use sensible defaults, clamp the slider ranges, and show an empty-state message.
3. Controls: driver or constructor selector, circuit selector, tyre compound toggle (Soft/Medium/Hard), stint-length slider, fuel-load slider, and a Reset button. Each control has a visible label, a live value badge and a one-line helper text.
4. Output panel: a clear verdict badge (Optimal / Caution / Critical) with a plain-English reason, a stint-health progress bar, three metric cards (predicted lap time as m:ss.mmm, delta vs. baseline, laps until the performance cliff), and a small line chart of predicted lap time per lap that animates when inputs change.
5. Add a collapsible "How is this calculated?" panel showing the formula and the data used.
6. Updates must feel instant (<150ms) and must not throw WebSocket or state errors when sliders are dragged quickly (debounce if needed).

STEP 4: TYPOGRAPHY (subtle and refined)
- Remove the heavy, shouty look: no weight 800/900, no all-caps headlines, and no oversized negative tracking.
- Use [FONT_FAMILY] (default: Inter) with a scale of: hero title weight 600, clamp(2.25rem, 4.5vw, 3.5rem), line-height 1.1, letter-spacing -0.02em; section titles weight 600 at 1.5–1.75rem; body weight 400 at 16px, line-height 1.6, color at about 75% white opacity; captions at 13–14px.
- Use a monospace font (JetBrains Mono) only for numbers, tick labels and the terminal, at weight 400–500, with tabular numerals.
- Uppercase is allowed only for tiny eyebrow labels (11–12px, letter-spacing 0.08em, weight 500).
- Check that contrast meets WCAG AA at minimum.

STEP 5: USER-FRIENDLY UNDERSTANDING (this is a DAV project, so explain the data)
- Add a plain-English one-line intro under every section: what you are looking at, why it matters, and what to try.
- Add a small "How to read this chart" info popover on each chart (what the axes mean, what bigger bubbles or bars mean).
- Add an "Insight" callout under each chart with 1–2 data-driven sentences, generated from the actual data (not hardcoded), for example "Ferrari has won X championships, the most of any team".
- Explain jargon with tooltips or a short glossary: Z-score, win share, era-adjusted, pace decay, stint, dynasty.
- Reduce clutter: one main idea per screen, generous whitespace (64–96px between sections), at most 3 KPI cards per row.
- Add a short "Methodology and Data" section: the dataset files used, row counts, the R and Python split, how the Z-score is computed, known limitations (for example lap times only exist from 1996 onward, scoring systems changed) and a link or download button for the processed CSVs.
- Add loading skeletons, empty states, and friendly error messages (for example a WebSocket reconnect hint).
- Clear navigation: a sticky floating navbar with active-section highlighting and smooth anchor scrolling, plus a visible "back to top".
- Add data-quality notes where they are relevant (missing laps, retired drivers, pre-1996 gaps).

STEP 6: R PLUS PYTHON ANALYSIS INTEGRITY
- Show clearly in the UI which results come from R (Z-scores, loess pace curves, survival or consistency stats) and which come from Python (joins, aggregates).
- If Rscript is unavailable, fall back to Polars automatically and show a visible badge, "Computed in Python fallback".
- Add at least one statistical summary visible in the UI (for example a confidence interval, a correlation coefficient, or a hypothesis-test p-value for pace differences between eras).

STEP 7: ROBUSTNESS, RESPONSIVENESS, ACCESSIBILITY
- Fix any "Cannot connect to server / ws://localhost:8000/_event" issues: check rxconfig.py (api_url, ports), long-running state handlers, and startup data loading.
- Responsive at <640px, 641–1024px and >1024px. No horizontal overflow. Charts resize and keep their legends readable on mobile, and touch targets are at least 44–48px.
- All controls have aria-labels. Tabs use proper roles. Charts have text alternatives (aria-label or a hidden data summary). Keyboard focus rings are visible.
- Keep the Rich pit-wall terminal, but match its SVG theme to the dark UI and keep the Run/Replay button working.

CONSTRAINTS
- Pure Python (Reflex, Plotly, Polars, Rich) plus the R script. Do not add heavy JS frameworks or chart libraries. Small CSS and JS snippets through Reflex are acceptable.
- Do not change the dataset or fabricate data. Anything that is an assumption must be labeled as such in the UI.
- Do not delete or rename existing files unless necessary. Keep the code modular, typed and commented.
- Use placeholders for unknown values: [FONT_FAMILY], [PRIMARY_COLOR], [SECONDARY_COLOR], [ACCENT_COLOR], [ASSET_PATH]. Do not invent them.

VERIFICATION (mandatory before you finish)
1. `python -m reflex run` starts with no errors or warnings in the terminal or browser console.
2. Click through every tab, slider, chip and button. Confirm that no value shows NaN, undefined or empty, and no chart overlaps its legend or labels.
3. Test at 390px, 768px and 1440px widths.
4. Confirm that the animations play smoothly and that reduced-motion mode works.
5. Check the contrast ratios and that every chart has a title, axis labels and a takeaway line.

OUTPUT FORMAT
1. Audit list (before changes).
2. Implementation, done file by file, with brief explanations.
3. A changelog table (file, section, what changed, why).
4. A short "How to run and test" section.
5. A list of any assumptions or limitations that remain.