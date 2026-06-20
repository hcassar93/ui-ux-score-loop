---
name: ui-ux-score-loop
description: Browser-based UI/UX improvement loop for one specified product flow. Use when the user asks to inspect, score, improve, or iteratively test a flow such as signup, login, password reset, checkout, create/edit/delete/share, onboarding, or another key UI path using a selected real browser, screenshots, responsive breakpoints, light/dark modes, 0-100 UX rubric scores, and a dashboard state file.
---

# UI/UX Score Loop

Improve exactly one user flow by using browser evidence and 0-100 scores as the loop signal.

## Start Prompt

When the user invokes this skill, run this loop unless they ask only for advice:

```text
Run UI/UX Score Loop on [FLOW] at [URL] with one completion criterion: reach [TARGET]/100 flow score, improve by [PERCENT]%, or run [N] iterations. Use a real browser. Start at the supplied URL exactly; do not jump to a deeper route unless the user supplied it. Explore the flow as fully as a real user would from that entry point, splitting necessary steps, alternate states, modals, popovers, waiting/loading, errors, and recovery paths into separate analysis views. Act as a human proxy, not an agent: prefer visible navigation over guessed routes, assume imperfect memory and possible mistakes, value clear progress while waiting, and judge only what the UI explains without console logs or technical knowledge. For auth flows, include visible password reset/recovery as part of the audit unless the user excludes it. If a browser/tool is specified, use it unless it cannot faithfully run the flow; otherwise prefer an integrated browser such as the Codex in-app/browser panel or the IDE integrated browser, then fall back to Playwright MCP or another external browser when needed. Unless viewports are supplied, test phone 390x844, tablet 768x1024, and laptop 1440x900. Actively look for a readily apparent light/dark toggle; if present, always collect both light and dark modes automatically. If no toggle/support is apparent, use the default mode. Create or refresh `.ui-ux-score-loop/dashboard.html` before scoring, then complete the flow once without editing as iteration 0, break it into pages and views, and screenshot every view at every breakpoint and mode. Score each view/breakpoint/mode 0-100 against the UI/UX principles, update the dashboard after each iteration, improve the lowest user-impactful safe score with manageable brand-consistent changes, rerun from the same entry point, rescore, record deltas, and repeat until the criterion is met, progress stalls, or approval is needed. Do not finish without clearly giving the user the dashboard path and browser used.
```

If the flow, URL, or completion criterion is missing, ask only for the missing input.

## Workflow

1. Confirm the flow, URL, concerns, off-limits areas, one completion criterion, any custom viewports, any browser/tool preference, and whether light/dark mode is specified.
2. If custom viewports are not supplied, use phone 390x844, tablet 768x1024, and laptop 1440x900.
3. Actively look for a readily apparent light/dark toggle in the app. If present, always test both light and dark automatically. If support is specified by the user, test the specified modes. If no toggle/support is apparent, use one `default` mode.
4. Select the browser/tool. Prefer the user's requested browser if it can exercise the flow. If no preference is supplied, prefer an integrated browser. Use an external browser only when the integrated browser is unavailable, cannot set the needed viewport/mode, cannot capture screenshots, lacks required session/auth state, or cannot reach the target.
5. Run the dashboard helper immediately so `.ui-ux-score-loop/dashboard.html`, `data/`, `screenshots/`, and the gitignore entry exist before evidence is captured.
6. Start at the supplied URL exactly for iteration 0. If the URL is `/`, begin at `/`; if it is `/login`, begin at `/login`. Do not replace the user's entry point with a convenient deeper route.
7. Explore the flow as fully as possible from that start, following the path a human is likely to take. Prefer visible links, buttons, and navigation over guessed routes or internal knowledge. Break the flow into pages and views, including entry screens, route transitions, forms, validation states, modals, popovers, drawers, empty, loading, error, success, and post-completion states.
8. Treat obvious alternate or recovery paths that serve the same user goal as analysis views. For auth flows, include visible forgot-password/reset-password states unless the user excludes them.
9. Audit as a human proxy. Assume the user may not know exact credentials, may mistype, may need reassurance while waiting, may not understand technical errors, and may abandon if progress, next steps, or recovery options are unclear.
10. Screenshot every view at each breakpoint/mode.
11. Score each view/breakpoint/mode from 0-100 against the principles below.
12. Update and regenerate the dashboard with browser, mode, breakpoint, view, page, flow, and principle averages.
13. Improve the lowest user-impactful, safely changeable principle/view/breakpoint/mode score with manageable related changes that clearly target the score.
14. Rerun the same full flow from the same entry point, capture new screenshots for affected views, breakpoints, and modes, rescore, record deltas, and keep the iteration only if it improves the target without creating a worse problem elsewhere.

Stop when the completion criterion is met, two passes stall, or the next best change needs approval.

## Scoring

Before scoring or choosing an improvement target, read `references/ui-ux-principles.md` for compact principle guidance distilled from the user's preferred UI/UX playbook. Do not load or add the source book.

Use the full 0-100 range:

- 0-39: harmful or confusing.
- 40-59: weak; usable only with effort.
- 60-74: adequate, with clear friction.
- 75-89: strong, clear, low-friction.
- 90-100: excellent and hard to improve.

Score each view against: visual hierarchy, proximity, clarity, alignment, contrast, simplicity, whitespace, layout, balance and harmony, consistency, visual cues, depth and texture, color theory, typography, and interaction cost.

Always explain scores through serving the user: does this help the user accomplish their real goal with confidence, speed, and dignity? Penalize agent-only affordances: hidden routes, assumed knowledge, silent waiting, console-only errors, raw technical messages, unclear recovery, or states that are only understandable because the agent can infer what happened.

## Guardrails

Do not overhaul the UI. Preserve brand, voice, information architecture, and working behavior. Do not add decorative AI slop, generic gradients, random cards, unnecessary animation, or novelty that does not help the flow. Ask before changing navigation, pricing, auth, destructive actions, business logic, or product strategy.

## Browser Selection

Accept optional browser guidance such as:

- `Browser: Codex in-app browser`
- `Browser: VS Code integrated browser`
- `Browser: Playwright MCP`
- `Browser: Chrome with my logged-in session`
- `Browser: prefer integrated`

Choose the browser that best preserves the real user experience and required state. Prefer integrated browser tooling for local app flows because it keeps screenshots and interactions close to the workspace. Use Playwright MCP or another external browser when it is better for viewport automation, repeatable screenshots, auth/session access, cross-browser behavior, or when integrated tooling is unavailable. Record the preference, selected browser, and reason in `.ui-ux-score-loop/data/state.json`.

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
python3 scripts/create_dashboard.py --flow "Signup" --viewport phone:390x844 --viewport desktop:1728x1117 --mode light --mode dark --browser "Codex in-app browser"
```

Use `assets/dashboard.html` as a template asset; do not paste it into chat unless the user asks.

Do not hand-edit `dashboard.html`. Update `data/state.json` and `data/ratings.md`, then rerun the script.

The dashboard must be information dense, not a written report. Keep the top minimal: flow name, breakpoint dropdown, light/dark mode dropdown, and small text buttons for Expand all and Collapse all. Do not put status chips, next-target boxes, explanatory copy, or summary cards above the table. The main view must be one comparison matrix with iterations as columns and an obvious hierarchy: collapsible flow context rows, page band rows, then indented view groups. Flow context, page rows, and view rows must work like an accordion so the user can collapse noisy detail. Each page band should show that page's average for each iteration. Each view header row should show that view's score, delta, weakest principle, and screenshot thumbnail for each iteration; do not create a separate screenshot row. Screenshot thumbnails must remain visible when a view group is collapsed, sit on a contrasting evidence frame, and open a large modal preview. View detail rows should contain notes and rubric ratings. End each breakpoint/mode block with a flow average row.

## Final Answer Contract

Always deliver the dashboard explicitly. The final answer must include:

- The path to `.ui-ux-score-loop/dashboard.html`.
- The path to `.ui-ux-score-loop/data/state.json`.
- The screenshot root path.
- The browser/tool used and why.
- The completion status and current flow score or best available score.
- The next target if the loop is not complete.

Do not treat the dashboard as an internal artifact. If the dashboard could not be generated, say why and give the exact command or blocker.
