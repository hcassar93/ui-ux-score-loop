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
```

If viewports are not specified, the loop tests phone `390x844`, tablet `768x1024`, and laptop `1440x900`. You can also specify custom viewports:

```text
Viewports: phone 390x844, desktop 1728x1117.
```

## Prompt-Only Version

Copy this into any agent:

```text
Evaluate one specified key flow in a real browser. Require one completion criterion: target flow score, percent improvement, or max iterations. Unless viewports are specified, test phone 390x844, tablet 768x1024, and laptop 1440x900. Break the flow into pages and views, screenshot and score every view/viewport 0-100 as iteration 0 against visual hierarchy, proximity, clarity, alignment, contrast, simplicity, whitespace, layout, balance, consistency, cues, depth, color, typography, and interaction cost. Keep a dashboard with viewport-switchable iteration screenshots, view/page/flow averages, score deltas, notes, and the next target. Improve the lowest user-impactful safe score with manageable brand-consistent changes, rerun, rescore, and repeat until the criterion is met, progress stalls, or approval is needed. Do not overhaul the UI; serve the user.
```

Use it like this:

```text
Run UI/UX Score Loop on [FLOW] at [URL].

Completion: choose one: reach [TARGET]/100 flow score, improve by [PERCENT]%, or run [N] iterations.
Viewports: optional. Defaults to phone 390x844, tablet 768x1024, and laptop 1440x900.

Use a real browser. Complete the flow once without editing at each viewport, then break it into pages and views, including modals, popovers, drawers, empty states, loading states, error states, and success states. This first pass is iteration 0. Screenshot every view at each viewport.

Create a dashboard. Score every view/viewport from 0-100 against these principles: visual hierarchy, proximity, clarity, alignment, contrast, simplicity, whitespace, layout, balance and harmony, consistency, visual cues, depth and texture, color theory, typography, and interaction cost. View score is the average of its principle scores. Page score is the average of its views and viewports. Flow score is the average of its pages.

The scores are the loop signal. Improve the lowest-scoring principle/view pair that is user-impactful, safe to change, and likely to improve the flow. Each iteration may include multiple related changes, but keep them manageable, clearly connected to the target score, and easy to review. Do not overhaul the UI.

Rerun the same flow after each iteration, capture a new screenshot for every affected view, rescore, update the dashboard, and record the delta. Keep the iteration only if it improves the target score without creating a worse problem elsewhere. Repeat until the completion criterion is met, progress stalls, or the next change needs approval.

Serve the user. Reduce confusion, hesitation, rework, anxiety, waiting, and avoidable choice. Preserve the product's brand, voice, information architecture, and working behavior. Do not add decorative AI slop, generic gradients, random cards, unnecessary animation, or novelty that does not help the flow. Ask before changing navigation, pricing, auth, destructive actions, business logic, or product strategy.
```

Example:

```text
Run UI/UX Score Loop on signup at http://localhost:3000.
Concerns: mobile clarity, form errors, trust, and reducing hesitation before submit.
Completion: reach a flow score of 85/100.
Viewports: phone 390x844, tablet 768x1024, laptop 1440x900.
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

## Dashboard

The dashboard is the loop state. It must show screenshot and rating progress over time, not only a before/after comparison.

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
      tablet/
      laptop/
    iteration-001/
```

Keep it simple:

```markdown
# UI/UX Score Loop Dashboard

Flow:
User goal:
Concerns:
Target:
Completion:
Status:

## Iterations
| Iteration | Changes | Flow Score | Delta | Decision |
| ---: | --- | ---: | ---: | --- |
| 0 | Baseline |  |  |  |

## Views
| Page | View | Viewport | Iteration | Screenshot | Score | Delta | Lowest Principle | User-Serving Note |
| --- | --- | --- | ---: | --- | ---: | ---: | --- | --- |

## Principle Scores
| Page | View | Iteration | Principle | Score | Previous | Delta |
| --- | --- | ---: | --- | ---: | ---: | ---: |
```

The skill version includes a minimal Tailwind dashboard template and a helper. The agent should edit `data/state.json`, keep short rationale in `data/ratings.md`, and regenerate the dashboard:

```bash
python3 scripts/create_dashboard.py --flow "Signup"
```

Custom dashboard viewports:

```bash
python3 scripts/create_dashboard.py --flow "Signup" --viewport phone:390x844 --viewport desktop:1728x1117
```

## Maintainer Submission

Title:

```text
The UI/UX score loop
```

Prompt:

```text
Evaluate one specified key flow in a real browser. Require one completion criterion: target flow score, percent improvement, or max iterations. Unless viewports are specified, test phone 390x844, tablet 768x1024, and laptop 1440x900. Break the flow into pages and views, screenshot and score every view/viewport 0-100 as iteration 0 against visual hierarchy, proximity, clarity, alignment, contrast, simplicity, whitespace, layout, balance, consistency, cues, depth, color, typography, and interaction cost. Keep a dashboard with viewport-switchable iteration screenshots, view/page/flow averages, score deltas, notes, and the next target. Improve the lowest user-impactful safe score with manageable brand-consistent changes, rerun, rescore, and repeat until the criterion is met, progress stalls, or approval is needed. Do not overhaul the UI; serve the user.
```

Source link after publishing:

```text
https://github.com/hcassar93/ui-ux-score-loop
```
