---
name: ui-ux-score-loop
description: Browser-based UI/UX improvement loop for one specified product flow. Use when the user asks to inspect, score, improve, or iteratively test a flow such as signup, login, password reset, checkout, create/edit/delete/share, onboarding, or another key UI path using a selected real browser, screenshots, responsive breakpoints, light/dark modes, 0-100 UX rubric scores, and a dashboard state file.
---

# UI/UX Score Loop

Improve exactly one user flow by using browser evidence and 0-100 scores as the loop signal.

## Start Prompt

When the user invokes this skill, run this loop unless they ask only for advice:

```text
Run UI/UX Score Loop on [FLOW] at [URL or app environment] with one completion criterion: reach [TARGET]/100 flow score, improve by [PERCENT]%, or run [N] iterations. Use a real browser. A flow name is a user goal, not a route: "login flow" does not mean start at `/login`. If the user supplies a URL, start at that exact URL. If the user asks you to start or find an environment but gives no URL, identify the app origin and start at its root `/`. Do not open a deeper route such as `/login`, `/signup`, or `/reset-password` unless the user explicitly supplied that route or the root redirects there. Explore the flow as fully as a real user would from the entry point, splitting necessary steps, alternate states, modals, popovers, waiting/loading, errors, and recovery paths into separate analysis views. Act as a human proxy, not an agent: prefer visible navigation over guessed routes, assume imperfect memory and possible mistakes, value clear progress while waiting, and judge only what the UI explains without console logs or technical knowledge. For auth flows, include visible password reset/recovery as part of the audit unless the user excludes it. If a browser/tool is specified, use it unless it cannot faithfully run the flow; otherwise prefer an integrated browser such as the Codex in-app/browser panel or the IDE integrated browser, then fall back to Playwright MCP or another external browser when needed. Unless viewports are supplied, test phone 390x844, tablet 768x1024, and laptop 1440x900. Discover theme support at the app level, not only on the entry page: check root/home, app shell after login when credentials exist, settings/profile/header controls, persisted theme keys, html classes/data attributes, CSS/framework dark-mode support, and browser color-scheme emulation. If light and dark can be activated reliably, always test both even when no toggle is visible on the login page; record how each mode was set. If no support is discoverable, use `default` mode. Improvement intensity defaults to `grouped` unless specified: `focused` changes one highest-leverage issue per view, `grouped` changes a few logically related issues per view, and `broad` changes all safe identified issues per view. Apply intensity per view, not once for the whole iteration; in each iteration, improve every view that has a safe useful improvement, while leaving views alone when nothing should change. Create or refresh `.ui-ux-score-loop/dashboard.html` before scoring, then complete the flow once without editing as iteration 0, break it into pages and views, and screenshot every view at every breakpoint and mode. Score each view/breakpoint/mode 0-100 against the UI/UX principles, update the dashboard after each iteration, improve the lowest user-impactful safe scores according to the intensity setting with brand-consistent changes, rerun from the same entry point, rescore, record deltas, and repeat until the criterion is met, progress stalls, or approval is needed. Do not finish without clearly giving the user the dashboard path and browser used.
```

If the flow or completion criterion is missing, ask only for the missing input. If the URL is missing but the user asks you to start or inspect an app/environment, first try to identify the app origin and use `/`; ask for a URL only if no app URL can be found.

## Workflow

1. Confirm the flow, URL or discoverable app environment, concerns, off-limits areas, one completion criterion, any custom viewports, any browser/tool preference, whether light/dark mode is specified, and the improvement intensity. If intensity is not specified, use `grouped`.
2. If custom viewports are not supplied, use phone 390x844, tablet 768x1024, and laptop 1440x900.
3. Discover theme support before finalizing modes. Check the root/home page, authenticated app shell when credentials are available, settings/profile/header controls, persisted theme keys, html classes/data attributes, CSS/framework dark-mode support, and browser `prefers-color-scheme` emulation. If light and dark can be activated reliably, test both automatically even if the login page itself has no visible toggle. If support is specified by the user, test the specified modes. If no support is discoverable, use one `default` mode. Record how each mode was set.
4. Select the browser/tool. Prefer the user's requested browser if it can exercise the flow. If no preference is supplied, prefer an integrated browser. Use an external browser only when the integrated browser is unavailable, cannot set the needed viewport/mode, cannot capture screenshots, lacks required session/auth state, or cannot reach the target.
5. Run the dashboard helper immediately so `.ui-ux-score-loop/dashboard.html`, `data/`, `screenshots/`, and the gitignore entry exist before evidence is captured.
6. Choose the entry point as a human would. A flow name is not a route. If the user supplies a URL, start at that exact URL for iteration 0. If the user asks you to start/find an app but supplies no URL, identify the app origin and start at `/`. For a login flow, begin at `/` and follow visible navigation or redirects into auth; do not start at `/login` unless the user explicitly supplied `/login` or `/` redirects there.
7. Explore the flow as fully as possible from that start, following the path a human is likely to take. Prefer visible links, buttons, and navigation over guessed routes or internal knowledge. Break the flow into pages and views, including entry screens, route transitions, forms, validation states, modals, popovers, drawers, empty, loading, error, success, and post-completion states.
8. Treat obvious alternate or recovery paths that serve the same user goal as analysis views. For auth flows, include visible forgot-password/reset-password states unless the user excludes them.
9. Audit as a human proxy. Assume the user may not know exact credentials, may mistype, may need reassurance while waiting, may not understand technical errors, and may abandon if progress, next steps, or recovery options are unclear.
10. Screenshot every view at each breakpoint/mode.
11. Score each view/breakpoint/mode from 0-100 against the principles below.
12. Update and regenerate the dashboard with browser, mode, breakpoint, view, page, flow, and principle averages.
13. Improve per view according to the intensity setting. `focused` means one highest-leverage safe change per view. `grouped` means a few logically related safe changes per view and is the default. `broad` means all identified safe improvements per view, while still avoiding rewrites, brand drift, and risky behavior changes. Do not spend an iteration on one change in one view unless only that view has a safe useful improvement or approval is needed elsewhere.
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
- `.ui-ux-score-loop/data/state.json`: structured source of truth for improvement intensity, iterations, view scores, rubric scores, and next target.
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
python3 scripts/create_dashboard.py --flow "Signup" --viewport phone:390x844 --viewport desktop:1728x1117 --mode light --mode dark --browser "Codex in-app browser" --improvement-intensity grouped
```

Improvement intensity options:

- `focused`: change one highest-leverage safe issue per view per iteration.
- `grouped`: change a few logically related safe issues per view per iteration. This is the default.
- `broad`: change all identified safe issues per view per iteration, while preserving brand, behavior, and reviewability.

Use `assets/dashboard.html` as a template asset; do not paste it into chat unless the user asks.

Do not hand-edit `dashboard.html`. Update `data/state.json` and `data/ratings.md`, then rerun the script.

The dashboard must be information dense, not a written report. Keep the top minimal: flow name, subtle Expand all / Collapse all text controls, breakpoint dropdown, and light/dark mode dropdown. Put the expand/collapse controls to the left of the dropdowns and style them as secondary text, not prominent buttons. Do not put status chips, next-target boxes, explanatory copy, or summary cards above the table. The main view must be one comparison matrix with iterations as columns and an obvious hierarchy: collapsible flow context rows, page band rows, then indented view groups. Flow context, page rows, and view rows must work like an accordion so the user can collapse noisy detail. Each page band should show that page's average for each iteration. Each view header row should show that view's score, delta, weakest principle, and screenshot thumbnail for each iteration; do not create a separate screenshot row. Screenshot thumbnails must remain visible when a view group is collapsed, sit on a contrasting evidence frame, and open a large modal preview. View detail rows should contain notes and rubric ratings. End each breakpoint/mode block with a flow average row.

## Final Answer Contract

Always deliver the dashboard explicitly. The final answer must include:

- The path to `.ui-ux-score-loop/dashboard.html`.
- The path to `.ui-ux-score-loop/data/state.json`.
- The screenshot root path.
- The browser/tool used and why.
- The completion status and current flow score or best available score.
- The next target if the loop is not complete.

Do not treat the dashboard as an internal artifact. If the dashboard could not be generated, say why and give the exact command or blocker.
