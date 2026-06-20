# UI/UX Score Loop

A browser-driven UI/UX improvement loop where numeric scores decide what the agent improves next.

UI/UX Score Loop turns one key product flow into a measurable feedback system. The agent uses a real browser, breaks the flow into pages and views, screenshots each view, scores it from 0-100 against UI/UX principles, improves the weakest user-impactful score, then reruns the same flow to verify the delta.

The goal is not a redesign. The goal is to serve the user with small, brand-consistent improvements that reduce confusion, friction, hesitation, and avoidable effort.

## Use It

You have two options:

- Install the skill and call it with a flow. This is best because it includes the dashboard template, state structure, screenshots folder, and helper script.
- Copy and paste the prompt-only version into any agent.

## Install The Skill

After publishing this repo to GitHub:

```bash
npx skills add hcassar93/ui-ux-score-loop -g
```

Then restart Codex so it picks up the new skill.

To try the skill prompt without installing:

```bash
npx skills use hcassar93/ui-ux-score-loop
```

Then call the skill with one flow, any extra concerns, and one completion criterion:

```text
Use $ui-ux-score-loop on the signup flow at http://localhost:3000.
Concerns: mobile clarity, form errors, trust, and reducing hesitation before submit.
Completion: reach a flow score of 85/100.
Browser: prefer integrated.
```

If viewports are not specified, the loop tests phone `390x844`, tablet `768x1024`, and laptop `1440x900`. You can also specify custom viewports:

```text
Viewports: phone 390x844, desktop 1728x1117.
```

If a light/dark toggle is readily apparent, test both modes automatically. Otherwise use the app's default mode unless modes are specified.

Start at the URL you provide. If you provide `/`, the loop begins at `/` and treats navigation into the flow as evidence. If you provide `/login`, it begins at `/login`. The agent should act as a human proxy, not use agent shortcuts.

Browser is optional. If omitted, prefer an integrated browser such as Codex in-app/browser panel or the IDE integrated browser. Use Playwright MCP, Chrome, or another external browser when that better preserves auth/session state, viewport control, screenshots, or access to the target.

## Prompt-Only Version

Copy this into any agent:

```text
Evaluate one specified key flow in a real browser. Require one completion criterion: target flow score, percent improvement, or max iterations. Start at the supplied URL exactly; do not jump to a deeper route unless the user supplied it. Explore the flow as a real user would, splitting necessary steps, alternate states, modals, popovers, waiting/loading, errors, and recovery paths into separate analysis views. Act as a human proxy, not an agent: prefer visible navigation over guessed routes, assume imperfect memory and possible mistakes, value clear progress while waiting, and judge only what the UI explains without console logs or technical knowledge. For auth flows, include visible password reset/recovery unless excluded. If a browser/tool is specified, use it unless it cannot faithfully run the flow; otherwise prefer an integrated browser, falling back to Playwright MCP or another external browser when needed. Unless viewports are specified, test phone 390x844, tablet 768x1024, and laptop 1440x900. Actively look for a readily apparent light/dark toggle; if present, always collect both light and dark modes automatically. If no toggle/support is apparent, use the default mode. Create a dashboard before scoring. Screenshot and score every view/breakpoint/mode 0-100 against visual hierarchy, proximity, clarity, alignment, contrast, simplicity, whitespace, layout, balance, consistency, cues, depth, color, typography, and interaction cost. Keep the dashboard updated with screenshots, averages, deltas, notes, and the next target. Improve the lowest user-impactful safe score with manageable brand-consistent changes, rerun from the same entry point, rescore, and repeat until the criterion is met, progress stalls, or approval is needed. Do not finish without giving the dashboard path and browser used. Do not overhaul the UI; serve the user.
```

Use it like this:

```text
Run UI/UX Score Loop on [FLOW] at [URL].

Completion: choose one: reach [TARGET]/100 flow score, improve by [PERCENT]%, or run [N] iterations.
Viewports: optional. Defaults to phone 390x844, tablet 768x1024, and laptop 1440x900.
Modes: optional. If a light/dark toggle is readily apparent, collect both automatically; otherwise use default.
Browser: optional. Prefer integrated browser by default; examples: Codex in-app browser, VS Code integrated browser, Playwright MCP, Chrome with logged-in session.

Use the selected real browser. Start at the supplied URL exactly. Complete the flow once without editing at each breakpoint/mode combination, then break it into pages and views as a human would experience them: entry screens, visible navigation, route transitions, forms, validation states, modals, popovers, drawers, empty states, loading states, error states, success states, and post-completion states. Treat obvious alternate or recovery paths that serve the same user goal as analysis views; for auth flows, include visible forgot-password/reset-password states unless excluded. This first pass is iteration 0. Screenshot every view at each breakpoint/mode.

Create a dashboard before scoring and explicitly deliver its path in the final answer. Score every view/breakpoint/mode from 0-100 against these principles: visual hierarchy, proximity, clarity, alignment, contrast, simplicity, whitespace, layout, balance and harmony, consistency, visual cues, depth and texture, color theory, typography, and interaction cost. View score is the average of its principle scores. Page score is the average of its views, breakpoints, and modes. Flow score is the average of its pages.

Score as a human proxy. Penalize hidden routes, assumed knowledge, silent waiting, console-only errors, raw technical messages, unclear recovery, or states that only make sense because the agent can infer what happened.

The scores are the loop signal. Improve the lowest-scoring principle/view pair that is user-impactful, safe to change, and likely to improve the flow. Each iteration may include multiple related changes, but keep them manageable, clearly connected to the target score, and easy to review. Do not overhaul the UI.

Rerun the same full flow from the same entry point after each iteration, capture a new screenshot for every affected view, rescore, update the dashboard, and record the delta. Keep the iteration only if it improves the target score without creating a worse problem elsewhere. Repeat until the completion criterion is met, progress stalls, or the next change needs approval.

Final answer must include the dashboard path, state file path, screenshot root, browser used, completion status, current score, and next target if unfinished.

Serve the user. Reduce confusion, hesitation, rework, anxiety, waiting, and avoidable choice. Preserve the product's brand, voice, information architecture, and working behavior. Do not add decorative AI slop, generic gradients, random cards, unnecessary animation, or novelty that does not help the flow. Ask before changing navigation, pricing, auth, destructive actions, business logic, or product strategy.
```

Example:

```text
Run UI/UX Score Loop on signup at http://localhost:3000.
Concerns: mobile clarity, form errors, trust, and reducing hesitation before submit.
Completion: reach a flow score of 85/100.
Viewports: phone 390x844, tablet 768x1024, laptop 1440x900.
Modes: light and dark.
Browser: Codex in-app browser.
```

## Rubric

Use the full 0-100 range. Small differences matter because the scores choose the next change.

| Score | Meaning |
| --- | --- |
| 0-39 | Harmful or confusing. |
| 40-59 | Weak; usable only with effort. |
| 60-74 | Adequate, with clear friction. |
| 75-89 | Strong, clear, and low-friction. |
| 90-100 | Excellent; effortless and hard to improve. |

Score each view against:

- Visual hierarchy
- Proximity
- Clarity
- Alignment
- Contrast
- Simplicity
- Whitespace
- Layout
- Balance and harmony
- Consistency
- Visual cues
- Depth and texture
- Color theory
- Typography
- Interaction cost

Every score should answer: does this help the user accomplish their real goal with confidence, speed, and dignity?

The installed skill also includes `references/ui-ux-principles.md`, a compact summary of the scoring principles. The source book is intentionally not included in this repo.

## Dashboard

The dashboard is the loop state. It must be dense enough to compare progress after several iterations, not a long report.

Generated loop state belongs in `.ui-ux-score-loop/`, which is ignored by git:

```text
.ui-ux-score-loop/
  dashboard.html
  data/
    state.json
    ratings.md
  screenshots/
    iteration-000/
      phone/
        light/
          001-login.png
          002-post-login-home.png
        dark/
          001-login.png
          002-post-login-home.png
      tablet/
      laptop/
    iteration-001/
```

Keep it simple:

```markdown
# UI/UX Score Loop Dashboard

Top: flow name, subtle Expand all / Collapse all text controls, breakpoint dropdown, and light/dark mode dropdown.

Main matrix:
- columns are iterations
- collapsible flow context rows show changes, decision, and why
- page band rows show page averages
- indented view groups sit under each page
- view header rows show score, delta, weakest principle, and screenshot
- view detail rows show notes and rubric ratings
- each breakpoint/mode block ends with a flow average
- flow context, page, and view groups can expand/collapse
- screenshot thumbnails open in a modal
- screenshot thumbnails sit on a contrasting evidence frame
```

The skill version includes a minimal Tailwind dashboard template and a helper. The agent must create or refresh the dashboard before scoring, edit `data/state.json`, keep short rationale in `data/ratings.md`, regenerate the dashboard, and give the dashboard path in its final answer:

```bash
python3 scripts/create_dashboard.py --flow "Signup"
```

The helper adds `.ui-ux-score-loop/` to the target repository's `.gitignore` before creating dashboard files.

Custom dashboard viewports:

```bash
python3 scripts/create_dashboard.py --flow "Signup" --viewport phone:390x844 --viewport desktop:1728x1117 --mode light --mode dark --browser "Codex in-app browser"
```

## Maintainer Submission

Title:

```text
The UI/UX score loop
```

Prompt:

```text
Evaluate one specified key flow in a real browser. Require one completion criterion: target flow score, percent improvement, or max iterations. Start at the supplied URL exactly; do not jump to a deeper route unless the user supplied it. Explore the flow as a real user would, splitting necessary steps, alternate states, modals, popovers, waiting/loading, errors, and recovery paths into separate analysis views. Act as a human proxy, not an agent: prefer visible navigation over guessed routes, assume imperfect memory and possible mistakes, value clear progress while waiting, and judge only what the UI explains without console logs or technical knowledge. For auth flows, include visible password reset/recovery unless excluded. If a browser/tool is specified, use it unless it cannot faithfully run the flow; otherwise prefer an integrated browser, falling back to Playwright MCP or another external browser when needed. Unless viewports are specified, test phone 390x844, tablet 768x1024, and laptop 1440x900. Actively look for a readily apparent light/dark toggle; if present, always collect both light and dark modes automatically. If no toggle/support is apparent, use the default mode. Create a dashboard before scoring. Screenshot and score every view/breakpoint/mode 0-100 against visual hierarchy, proximity, clarity, alignment, contrast, simplicity, whitespace, layout, balance, consistency, cues, depth, color, typography, and interaction cost. Keep the dashboard updated with screenshots, averages, deltas, notes, and the next target. Improve the lowest user-impactful safe score with manageable brand-consistent changes, rerun from the same entry point, rescore, and repeat until the criterion is met, progress stalls, or approval is needed. Do not finish without giving the dashboard path and browser used. Do not overhaul the UI; serve the user.
```

Source link after publishing:

```text
https://github.com/hcassar93/ui-ux-score-loop
```
