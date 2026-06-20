#!/usr/bin/env python3
import argparse
import html
import json
import subprocess
from pathlib import Path

DEFAULT_VIEWPORTS = [
    {"name": "phone", "width": 390, "height": 844},
    {"name": "tablet", "width": 768, "height": 1024},
    {"name": "laptop", "width": 1440, "height": 900},
]


def fmt(value):
    if value is None or value == "":
        return "--"
    if isinstance(value, float):
        return f"{value:.1f}"
    return str(value)


def esc(value):
    return html.escape(fmt(value), quote=True)


def row(cells, attrs=""):
    return f"<tr{attrs}>" + "".join(cells) + "</tr>"


def td(value, classes="px-4 py-3"):
    return f'<td class="{classes}">{esc(value)}</td>'


def parse_viewport(value):
    try:
        name, size = value.split(":", 1)
        width, height = size.lower().split("x", 1)
        return {"name": name.strip(), "width": int(width), "height": int(height)}
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "Use viewport format name:WIDTHxHEIGHT, for example phone:390x844"
        ) from exc


def viewport_label(viewport):
    return f"{viewport['name']} ({viewport['width']}x{viewport['height']})"


def git_root(start):
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=start,
            check=True,
            capture_output=True,
            text=True,
        )
        return Path(result.stdout.strip())
    except (subprocess.CalledProcessError, FileNotFoundError):
        return start


def ensure_gitignore(root):
    gitignore = root / ".gitignore"
    pattern = ".ui-ux-score-loop/"
    lines = []

    if gitignore.exists():
        lines = gitignore.read_text(encoding="utf-8").splitlines()

    if pattern not in lines:
        with gitignore.open("a", encoding="utf-8") as file:
            if lines:
                file.write("\n")
            file.write(f"{pattern}\n")


def seed_state(flow, viewports):
    return {
        "flow": flow,
        "user_goal": "",
        "concerns": [],
        "viewports": viewports,
        "target_score": 85,
        "completion": "Reach a flow score of 85/100.",
        "minimum_critical_view_score": 75,
        "status": "Baseline",
        "iterations": [
            {
                "iteration": 0,
                "changes": "Baseline captured.",
                "flow_score": None,
                "delta": None,
                "decision": "Continue",
                "why": "Evidence exists before changes.",
            }
        ],
        "views": [
            {
                "page": "Page",
                "view": "View",
                "view_number": "001",
                "viewport": viewport["name"],
                "iteration": 0,
                "screenshot": f"screenshots/iteration-000/{viewport['name']}/001-view.png",
                "score": None,
                "delta": None,
                "lowest_principle": "Clarity",
                "note": "What this view makes easier or harder for the user.",
            }
            for viewport in viewports
        ],
        "rubric_scores": [
            {
                "page": "Page",
                "view": "View",
                "view_number": "001",
                "viewport": viewports[0]["name"],
                "iteration": 0,
                "principle": "Clarity",
                "previous": None,
                "score": None,
                "delta": None,
                "evidence": "",
                "note": "",
            }
        ],
        "next_improvement": {
            "target": "",
            "expected_delta": "",
            "why": "",
        },
    }


def latest(values, key):
    present = [item for item in values if item.get(key) not in (None, "")]
    if not present:
        return None
    return present[-1].get(key)


def render(template, state):
    iterations = state.get("iterations", [])
    views = state.get("views", [])
    rubric_scores = state.get("rubric_scores", [])
    latest_flow = latest(iterations, "flow_score")
    latest_delta = latest(iterations, "delta")
    lowest_view = min(
        [view for view in views if isinstance(view.get("score"), (int, float))],
        key=lambda view: view["score"],
        default={},
    )

    iteration_rows = "\n".join(
        row(
            [
                td(item.get("iteration"), "px-4 py-3 font-medium tabular-nums"),
                td(item.get("changes")),
                td(item.get("flow_score"), "px-4 py-3 text-right font-semibold tabular-nums"),
                td(item.get("delta"), "px-4 py-3 text-right tabular-nums"),
                td(item.get("decision")),
                td(item.get("why"), "px-4 py-3 text-neutral-600"),
            ]
        )
        for item in iterations
    )

    view_rows = "\n".join(
        row(
            [
                td(item.get("page")),
                td(item.get("view_number")),
                td(item.get("view")),
                td(item.get("viewport")),
                td(item.get("iteration"), "px-4 py-3 tabular-nums"),
                td(item.get("screenshot"), "px-4 py-3 text-neutral-600"),
                td(item.get("score"), "px-4 py-3 text-right font-semibold tabular-nums"),
                td(item.get("delta"), "px-4 py-3 text-right tabular-nums"),
                td(item.get("lowest_principle")),
                td(item.get("note"), "px-4 py-3 text-neutral-600"),
            ],
            f' data-viewport-row="{esc(item.get("viewport"))}"',
        )
        for item in views
    )

    rubric_rows = "\n".join(
        row(
            [
                td(
                    f"{item.get('page', '')} / {item.get('view', '')} / {item.get('viewport', '')}"
                ),
                td(item.get("principle")),
                td(item.get("previous"), "px-4 py-3 text-right tabular-nums"),
                td(item.get("score"), "px-4 py-3 text-right tabular-nums"),
                td(item.get("delta"), "px-4 py-3 text-right tabular-nums"),
            ],
            f' data-viewport-row="{esc(item.get("viewport"))}"',
        )
        for item in rubric_scores
    )

    concerns = state.get("concerns") or []
    concern_text = ", ".join(concerns) if isinstance(concerns, list) else str(concerns)
    viewports = state.get("viewports") or DEFAULT_VIEWPORTS
    viewport_text = ", ".join(viewport_label(viewport) for viewport in viewports)
    viewport_buttons = "\n".join(
        [
            '<button class="rounded-full border border-neutral-950 bg-neutral-950 px-3 py-1 text-sm text-white" data-viewport-filter="all">All</button>'
        ]
        + [
            (
                f'<button class="rounded-full border border-neutral-200 bg-white px-3 py-1 text-sm text-neutral-700" '
                f'data-viewport-filter="{esc(viewport["name"])}">{esc(viewport_label(viewport))}</button>'
            )
            for viewport in viewports
        ]
    )
    next_improvement = state.get("next_improvement", {})

    replacements = {
        "{{FLOW_NAME}}": esc(state.get("flow")),
        "{{TARGET_SCORE}}": esc(state.get("target_score")),
        "{{COMPLETION}}": esc(state.get("completion")),
        "{{FLOW_SCORE}}": esc(latest_flow),
        "{{FLOW_DELTA}}": esc(latest_delta),
        "{{LOWEST_PAGE}}": esc(lowest_view.get("page")),
        "{{LOWEST_VIEW}}": esc(lowest_view.get("view")),
        "{{NEXT_TARGET}}": esc(next_improvement.get("target")),
        "{{USER_GOAL}}": esc(state.get("user_goal")),
        "{{CONCERNS}}": esc(concern_text),
        "{{VIEWPORTS}}": esc(viewport_text),
        "{{VIEWPORT_BUTTONS}}": viewport_buttons,
        "{{STATUS}}": esc(state.get("status")),
        "{{ITERATION_ROWS}}": iteration_rows,
        "{{VIEW_ROWS}}": view_rows,
        "{{RUBRIC_ROWS}}": rubric_rows,
        "{{NEXT_WHY}}": esc(next_improvement.get("why")),
        "{{EXPECTED_DELTA}}": esc(next_improvement.get("expected_delta")),
    }

    for key, value in replacements.items():
        template = template.replace(key, value)
    return template


def main():
    parser = argparse.ArgumentParser(
        description="Create or refresh a UI/UX Score Loop dashboard workspace."
    )
    parser.add_argument("--output", default=".ui-ux-score-loop/dashboard.html")
    parser.add_argument("--flow", default="Flow name")
    parser.add_argument(
        "--viewport",
        action="append",
        type=parse_viewport,
        help="Custom viewport as name:WIDTHxHEIGHT. Can be repeated.",
    )
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parents[1]
    template_path = skill_root / "assets" / "dashboard.html"
    output = Path(args.output).expanduser().resolve()
    workspace = output.parent
    ensure_gitignore(git_root(Path.cwd()))
    data_dir = workspace / "data"
    screenshots_dir = workspace / "screenshots"

    workspace.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(exist_ok=True)
    screenshots_dir.mkdir(exist_ok=True)
    viewports = args.viewport or DEFAULT_VIEWPORTS
    for viewport in viewports:
        (screenshots_dir / "iteration-000" / viewport["name"]).mkdir(
            parents=True,
            exist_ok=True,
        )

    state_path = data_dir / "state.json"
    if state_path.exists():
        state = json.loads(state_path.read_text(encoding="utf-8"))
    else:
        state = seed_state(args.flow, viewports)
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")

    ratings = data_dir / "ratings.md"
    if not ratings.exists():
        ratings.write_text(
            f"""# UI/UX Score Loop Notes

Flow: {state.get("flow", args.flow)}

Use `state.json` for structured scores. Use this file for short human notes,
open questions, approval needs, and rationale that should not clutter the
dashboard tables.
""",
            encoding="utf-8",
        )

    dashboard = render(template_path.read_text(encoding="utf-8"), state)
    output.write_text(dashboard, encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
