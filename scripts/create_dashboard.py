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
DEFAULT_COLOR_MODES = ["light", "dark"]
PRINCIPLES = [
    "Visual hierarchy",
    "Proximity",
    "Clarity",
    "Alignment",
    "Contrast",
    "Simplicity",
    "Whitespace",
    "Layout",
    "Balance and harmony",
    "Consistency",
    "Visual cues",
    "Depth and texture",
    "Color theory",
    "Typography",
    "Interaction cost",
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


def raw_td(value, classes="px-3 py-2"):
    return f'<td class="{classes}">{value}</td>'


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


def parse_mode(value):
    mode = value.strip().lower()
    if not mode:
        raise argparse.ArgumentTypeError("Mode cannot be empty.")
    return mode


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


def seed_state(flow, viewports, modes):
    return {
        "flow": flow,
        "user_goal": "",
        "concerns": [],
        "viewports": viewports,
        "color_modes": modes,
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
                "mode": mode,
                "iteration": 0,
                "screenshot": f"screenshots/iteration-000/{viewport['name']}/{mode}/001-view.png",
                "score": None,
                "delta": None,
                "lowest_principle": "Clarity",
                "note": "What this view makes easier or harder for the user.",
            }
            for viewport in viewports
            for mode in modes
        ],
        "rubric_scores": [
            {
                "page": "Page",
                "view": "View",
                "view_number": "001",
                "viewport": viewports[0]["name"],
                "mode": modes[0],
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


def normalize_state(state):
    modes = state.get("color_modes")
    if not modes:
        modes = sorted(
            {
                item.get("mode")
                for collection in ("views", "rubric_scores")
                for item in state.get(collection, [])
                if item.get("mode")
            }
        )
        state["color_modes"] = modes or ["default"]

    for collection in ("views", "rubric_scores"):
        for item in state.get(collection, []):
            item.setdefault("mode", state["color_modes"][0])

    return state


def numeric(value):
    return value if isinstance(value, (int, float)) else None


def average(values):
    present = [value for value in values if isinstance(value, (int, float))]
    if not present:
        return None
    return round(sum(present) / len(present), 1)


def latest(values, key):
    present = [item for item in values if item.get(key) not in (None, "")]
    if not present:
        return None
    return present[-1].get(key)


def score_classes(score):
    if not isinstance(score, (int, float)):
        return "bg-neutral-100 text-neutral-500"
    if score >= 90:
        return "bg-emerald-100 text-emerald-800"
    if score >= 75:
        return "bg-lime-100 text-lime-800"
    if score >= 60:
        return "bg-amber-100 text-amber-800"
    return "bg-red-100 text-red-800"


def score_pill(score):
    return (
        f'<span class="inline-flex min-w-10 justify-center rounded px-2 py-0.5 '
        f'text-xs font-semibold tabular-nums {score_classes(score)}">{esc(score)}</span>'
    )


def delta_text(value):
    if not isinstance(value, (int, float)):
        return ""
    prefix = "+" if value > 0 else ""
    return f"{prefix}{value:g}"


def view_key(item):
    return (
        item.get("page") or "Page",
        item.get("view_number") or "999",
        item.get("view") or "View",
        item.get("viewport") or "",
        item.get("mode") or "",
    )


def data_attrs(viewport, mode):
    return f' data-viewport-row="{esc(viewport)}" data-mode-row="{esc(mode)}"'


def sticky_label(title, meta="", classes=""):
    title_class = "text-white" if "text-white" in classes else "text-neutral-950"
    meta_class = "text-neutral-300" if "text-white" in classes else "text-neutral-500"
    bg_class = "" if "bg-" in classes else "bg-white"
    return (
        f'<th class="sticky left-0 z-10 border-b border-r border-neutral-200 {bg_class} '
        f'px-3 py-2 text-left align-top {classes}">'
        f'<div class="font-semibold {title_class}">{esc(title)}</div>'
        f'<div class="mt-0.5 text-[11px] font-normal {meta_class}">{esc(meta)}</div>'
        f"</th>"
    )


def screenshot_cell(item):
    path = item.get("screenshot") if item else None
    if not path:
        return '<span class="text-neutral-400">--</span>'
    safe_path = esc(path)
    return (
        f'<a href="{safe_path}" target="_blank" class="block">'
        f'<img src="{safe_path}" alt="{safe_path}" '
        f'onerror="this.style.display=\'none\';this.nextElementSibling.textContent=\'Missing screenshot\';" '
        f'class="h-36 w-56 rounded border border-neutral-200 bg-neutral-50 object-contain" />'
        f'<span class="mt-1 block max-w-56 truncate text-[10px] text-neutral-400">{safe_path}</span>'
        f"</a>"
    )


def render(template, state):
    iterations = state.get("iterations", [])
    views = state.get("views", [])
    rubric_scores = state.get("rubric_scores", [])
    iteration_numbers = sorted(
        {
            item.get("iteration", 0)
            for collection in (iterations, views, rubric_scores)
            for item in collection
            if isinstance(item.get("iteration", 0), int)
        }
    ) or [0]
    latest_flow = latest(iterations, "flow_score")
    latest_delta = latest(iterations, "delta")
    lowest_view = min(
        [view for view in views if isinstance(view.get("score"), (int, float))],
        key=lambda view: view["score"],
        default={},
    )
    iteration_by_number = {
        item.get("iteration", 0): item for item in iterations if isinstance(item, dict)
    }

    concerns = state.get("concerns") or []
    concern_text = ", ".join(concerns) if isinstance(concerns, list) else str(concerns)
    viewports = state.get("viewports") or DEFAULT_VIEWPORTS
    viewport_text = ", ".join(viewport_label(viewport) for viewport in viewports)
    modes = state.get("color_modes") or DEFAULT_COLOR_MODES
    mode_text = ", ".join(modes)
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
    mode_buttons = "\n".join(
        [
            '<button class="rounded-full border border-neutral-950 bg-neutral-950 px-3 py-1 text-sm text-white" data-mode-filter="all">All</button>'
        ]
        + [
            (
                f'<button class="rounded-full border border-neutral-200 bg-white px-3 py-1 text-sm text-neutral-700" '
                f'data-mode-filter="{esc(mode)}">{esc(mode)}</button>'
            )
            for mode in modes
        ]
    )
    next_improvement = state.get("next_improvement", {})
    summary_chips = "\n".join(
        (
            f'<span class="rounded border border-neutral-200 bg-white px-2.5 py-1">'
            f'<span class="text-neutral-500">{label}</span> '
            f'<span class="font-semibold tabular-nums">{esc(value)}</span>'
            f"</span>"
        )
        for label, value in (
            ("Score", latest_flow),
            ("Delta", delta_text(latest_delta) or "--"),
            ("Target", state.get("target_score")),
            ("Status", state.get("status")),
            ("Views", len({view_key(item) for item in views})),
            ("Iterations", len(iteration_numbers)),
        )
    )
    matrix_header = "\n".join(
        (
            '<th class="min-w-64 border-b border-r border-neutral-200 px-3 py-2 align-top">'
            f'<div class="font-semibold text-neutral-950">Iteration {esc(number)}</div>'
            f'<div class="mt-0.5 text-[11px] font-normal normal-case text-neutral-500">'
            f'{esc((iteration_by_number.get(number) or {}).get("decision"))}</div>'
            "</th>"
        )
        for number in iteration_numbers
    )

    grouped_views = {}
    for item in views:
        grouped_views.setdefault(view_key(item), {})[item.get("iteration", 0)] = item

    grouped_rubric = {}
    for item in rubric_scores:
        key = view_key(item)
        principle = item.get("principle") or "Rubric"
        grouped_rubric.setdefault(key, {}).setdefault(principle, {})[
            item.get("iteration", 0)
        ] = item

    matrix_rows = []
    for label, key in (("Changes", "changes"), ("Decision", "decision"), ("Why", "why")):
        matrix_rows.append(
            row(
                [
                    sticky_label(label, "Iteration context", "bg-neutral-50"),
                    *[
                        td(
                            (iteration_by_number.get(number) or {}).get(key),
                            "border-b border-r border-neutral-200 px-3 py-2 align-top text-neutral-700",
                        )
                        for number in iteration_numbers
                    ],
                ]
            )
        )

    for key in sorted(grouped_views):
        page, view_number, view_name, viewport, mode = key
        attrs = data_attrs(viewport, mode)
        by_iteration = grouped_views[key]
        meta = f"{page} / {viewport} / {mode}"
        matrix_rows.append(
            row(
                [
                    sticky_label(f"{view_number} {view_name}", meta, "bg-neutral-50"),
                    *[
                        raw_td(
                            (
                                f'{score_pill(numeric((by_iteration.get(number) or {}).get("score")))}'
                                f'<span class="ml-2 text-[11px] text-neutral-500">'
                                f'{esc(delta_text((by_iteration.get(number) or {}).get("delta")))}</span>'
                                f'<div class="mt-1 text-[11px] text-neutral-500">'
                                f'{esc((by_iteration.get(number) or {}).get("lowest_principle"))}</div>'
                            ),
                            "border-b border-r border-neutral-200 px-3 py-2 align-top",
                        )
                        for number in iteration_numbers
                    ],
                ],
                attrs,
            )
        )
        matrix_rows.append(
            row(
                [
                    sticky_label("Screenshot", meta),
                    *[
                        raw_td(
                            screenshot_cell(by_iteration.get(number)),
                            "border-b border-r border-neutral-200 px-3 py-2 align-top",
                        )
                        for number in iteration_numbers
                    ],
                ],
                attrs,
            )
        )
        matrix_rows.append(
            row(
                [
                    sticky_label("Notes", meta),
                    *[
                        td(
                            (by_iteration.get(number) or {}).get("note"),
                            "border-b border-r border-neutral-200 px-3 py-2 align-top text-neutral-700",
                        )
                        for number in iteration_numbers
                    ],
                ],
                attrs,
            )
        )

        principle_map = grouped_rubric.get(key, {})
        ordered_principles = [
            principle for principle in PRINCIPLES if principle in principle_map
        ] + sorted(
            principle for principle in principle_map if principle not in PRINCIPLES
        )
        for principle in ordered_principles:
            scores_by_iteration = principle_map[principle]
            matrix_rows.append(
                row(
                    [
                        sticky_label(principle, "Rubric", "font-normal"),
                        *[
                            raw_td(
                                (
                                    f'{score_pill(numeric((scores_by_iteration.get(number) or {}).get("score")))}'
                                    f'<span class="ml-2 text-[11px] text-neutral-500">'
                                    f'{esc(delta_text((scores_by_iteration.get(number) or {}).get("delta")))}</span>'
                                    f'<div class="mt-1 text-[11px] text-neutral-500">'
                                    f'{esc((scores_by_iteration.get(number) or {}).get("note"))}</div>'
                                ),
                                "border-b border-r border-neutral-200 px-3 py-1.5 align-top",
                            )
                            for number in iteration_numbers
                        ],
                    ],
                    attrs,
                )
            )

    matrix_rows = "\n".join(matrix_rows)

    average_rows = []
    for viewport in [item["name"] for item in viewports]:
        for mode in modes:
            matching = [
                item
                for item in views
                if item.get("viewport") == viewport and item.get("mode") == mode
            ]
            if not matching:
                continue
            for page in sorted({item.get("page") or "Page" for item in matching}):
                page_items = [item for item in matching if (item.get("page") or "Page") == page]
                average_rows.append(
                    row(
                        [
                            sticky_label(f"Page avg: {page}", f"{viewport} / {mode}", "bg-neutral-950 text-white"),
                            *[
                                raw_td(
                                    score_pill(
                                        average(
                                            numeric(item.get("score"))
                                            for item in page_items
                                            if item.get("iteration", 0) == number
                                        )
                                    ),
                                    "border-b border-r border-neutral-700 px-3 py-2 align-top",
                                )
                                for number in iteration_numbers
                            ],
                        ],
                        data_attrs(viewport, mode),
                    )
                )
            average_rows.append(
                row(
                    [
                        sticky_label("Flow avg", f"{viewport} / {mode}", "bg-neutral-950 text-white"),
                        *[
                            raw_td(
                                score_pill(
                                    average(
                                        numeric(item.get("score"))
                                        for item in matching
                                        if item.get("iteration", 0) == number
                                    )
                                ),
                                "border-b border-r border-neutral-700 px-3 py-2 align-top",
                            )
                            for number in iteration_numbers
                        ],
                    ],
                    data_attrs(viewport, mode),
                )
            )

    average_rows = "\n".join(average_rows)

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
        "{{COLOR_MODES}}": esc(mode_text),
        "{{VIEWPORT_BUTTONS}}": viewport_buttons,
        "{{MODE_BUTTONS}}": mode_buttons,
        "{{SUMMARY_CHIPS}}": summary_chips,
        "{{MATRIX_HEADER}}": matrix_header,
        "{{MATRIX_ROWS}}": matrix_rows,
        "{{AVERAGE_ROWS}}": average_rows,
        "{{STATUS}}": esc(state.get("status")),
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
    parser.add_argument(
        "--mode",
        action="append",
        type=parse_mode,
        help="Color mode to test, such as light, dark, or default. Can be repeated.",
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
    modes = args.mode or DEFAULT_COLOR_MODES
    for viewport in viewports:
        for mode in modes:
            (screenshots_dir / "iteration-000" / viewport["name"] / mode).mkdir(
                parents=True,
                exist_ok=True,
            )

    state_path = data_dir / "state.json"
    if state_path.exists():
        state = normalize_state(json.loads(state_path.read_text(encoding="utf-8")))
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    else:
        state = seed_state(args.flow, viewports, modes)
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
