---
name: ui-ux-score-loop
description: Browser-based UI/UX improvement loop for one specified product flow. Use when the user asks to inspect, score, improve, or iteratively test a flow such as signup, login, password reset, checkout, create/edit/delete/share, onboarding, or another key UI path using screenshots, responsive breakpoints, light/dark modes, 0-100 UX rubric scores, and a dashboard state file.
---

# UI/UX Score Loop

Improve exactly one user flow by using browser evidence and 0-100 scores as the loop signal.

## Start Prompt

When the user invokes this skill, run this loop unless they ask only for advice:

```text
Run UI/UX Score Loop on [FLOW] at [URL] with one completion criterion: reach [TARGET]/100 flow score, improve by [PERCENT]%, or run [N] iterations. Use a real browser. Unless viewports are supplied, test phone 390x844, tablet 768x1024, and laptop 1440x900. If the app supports light/dark mode, test both; otherwise use the default mode. Create or refresh `.ui-ux-score-loop/dashboard.html` before scoring, then complete the flow once without editing as iteration 0, break it into pages and views, and screenshot every view at every breakpoint and mode. Score each view/breakpoint/mode 0-100 against the UI/UX principles, update the dashboard after each iteration, improve the lowest user-impactful safe score with manageable brand-consistent changes, rerun, rescore, record deltas, and repeat until the criterion is met, progress stalls, or approval is needed. Do not finish without clearly giving the user the dashboard path.
```

If the flow, URL, or completion criterion is missing, ask only for the missing input.

## Workflow

1. Confirm the flow, URL, concerns, off-limits areas, one completion criterion, any custom viewports, and whether light/dark mode is supported.
2. If custom viewports are not supplied, use phone 390x844, tablet 768x1024, and laptop 1440x900.
3. If the app supports light/dark mode, test both light and dark. If not, use one `default` mode.
4. Run the dashboard helper immediately so `.ui-ux-score-loop/dashboard.html`, `data/`, `screenshots/`, and the gitignore entry exist before evidence is captured.
5. Use a real browser to complete the flow once without editing as iteration 0 at each breakpoint/mode combination.
6. Break the flow into pages and views, including modals, popovers, drawers, empty, loading, error, and success states.
7. Screenshot every view at each breakpoint/mode.
8. Score each view/breakpoint/mode from 0-100 against the principles below.
9. Update and regenerate the dashboard with mode, breakpoint, view, page, flow, and principle averages.
10. Improve the lowest user-impactful, safely changeable principle/view/breakpoint/mode score with manageable related changes that clearly target the score.
11. Rerun the same flow, capture new screenshots for affected views, breakpoints, and modes, rescore, record deltas, and keep the iteration only if it improves the target without creating a worse problem elsewhere.

Stop when the completion criterion is met, two passes stall, or the next best change needs approval.

## Scoring

Use the full 0-100 range:

- 0-39: harmful or confusing.
- 40-59: weak; usable only with effort.
- 60-74: adequate, with clear friction.
- 75-89: strong, clear, low-friction.
- 90-100: excellent and hard to improve.

Score each view against: visual hierarchy, proximity, clarity, alignment, contrast, simplicity, whitespace, layout, balance and harmony, consistency, visual cues, depth and texture, color theory, typography, and interaction cost.

Always explain scores through serving the user: does this help the user accomplish their real goal with confidence, speed, and dignity?

## Guardrails

Do not overhaul the UI. Preserve brand, voice, information architecture, and working behavior. Do not add decorative AI slop, generic gradients, random cards, unnecessary animation, or novelty that does not help the flow. Ask before changing navigation, pricing, auth, destructive actions, business logic, or product strategy.

## Dashboard

Create loop state only under `.ui-ux-score-loop/`. This directory is intentionally ignored by git and must not be committed.

Run the dashboard helper before taking screenshots or writing ratings. The helper adds `.ui-ux-score-loop/` to the target repository's `.gitignore` before it creates files.

Use this structure:

- `.ui-ux-score-loop/dashboard.html`: generated Tailwind dashboard.
- `.ui-ux-score-loop/data/state.json`: structured source of truth for iterations, view scores, rubric scores, and next target.
- `.ui-ux-score-loop/data/ratings.md`: short human notes and rationale that should not clutter tables.
- `.ui-ux-score-loop/screenshots/iteration-000/{breakpoint}/{mode}/001-view-name.png`: baseline screenshots.
- `.ui-ux-score-loop/screenshots/iteration-001/{breakpoint}/{mode}/001-view-name.png`: first changed iteration screenshots.
- Continue with zero-padded iteration folders.

Name screenshots by the view's order in the flow. Use `001`, `002`, `003`, etc. so files sort naturally. Keep the same number for the same view across breakpoints and iterations.

Use `scripts/create_dashboard.py` to create or refresh the dashboard workspace:

```bash
python3 scripts/create_dashboard.py --flow "Signup"
```

To seed a custom viewport set, pass repeated viewport flags:

```bash
python3 scripts/create_dashboard.py --flow "Signup" --viewport phone:390x844 --viewport desktop:1728x1117 --mode light --mode dark
```

Use `assets/dashboard.html` as a template asset; do not paste it into chat unless the user asks.

Do not hand-edit `dashboard.html`. Update `data/state.json` and `data/ratings.md`, then rerun the script.

The dashboard must be information dense, not a written report. Keep the top minimal: flow, compact status chips, breakpoint filter, and light/dark filter. The main view must be one comparison matrix with iterations as columns and an obvious hierarchy: flow context rows, page band rows, then indented view groups. Each page band should show that page's average for each iteration. Each view group should show score, screenshot, notes, and rubric-rating rows across iterations. End each breakpoint/mode block with a flow average row.

## Final Answer Contract

Always deliver the dashboard explicitly. The final answer must include:

- The path to `.ui-ux-score-loop/dashboard.html`.
- The path to `.ui-ux-score-loop/data/state.json`.
- The screenshot root path.
- The completion status and current flow score or best available score.
- The next target if the loop is not complete.

Do not treat the dashboard as an internal artifact. If the dashboard could not be generated, say why and give the exact command or blocker.
