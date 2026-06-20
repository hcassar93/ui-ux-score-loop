#!/usr/bin/env python3
import argparse
import html
import json
import re
import subprocess
from pathlib import Path

DEFAULT_VIEWPORTS = [
    {"name": "phone", "width": 390, "height": 844},
    {"name": "tablet", "width": 768, "height": 1024},
    {"name": "laptop", "width": 1440, "height": 900},
]
DEFAULT_COLOR_MODES = ["light", "dark"]
DEFAULT_BROWSER = "Prefer integrated browser; use external browser only if needed."
DEFAULT_IMPROVEMENT_INTENSITY = "grouped"
DEFAULT_VIEW_GRANULARITY = "standard"
DEFAULT_INTERACTIVE_MODE = "auto"
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


def parse_browser(value):
    browser = value.strip()
    if not browser:
        raise argparse.ArgumentTypeError("Browser preference cannot be empty.")
    return browser


def parse_improvement_intensity(value):
    intensity = value.strip().lower()
    allowed = {"focused", "grouped", "broad"}
    if intensity not in allowed:
        raise argparse.ArgumentTypeError(
            "Improvement intensity must be one of: focused, grouped, broad."
        )
    return intensity


def parse_view_granularity(value):
    granularity = value.strip().lower()
    allowed = {"essential", "standard", "exhaustive"}
    if granularity not in allowed:
        raise argparse.ArgumentTypeError(
            "View granularity must be one of: essential, standard, exhaustive."
        )
    return granularity


def parse_interactive_mode(value):
    mode = value.strip().lower()
    allowed = {"auto", "interactive", "direct"}
    if mode not in allowed:
        raise argparse.ArgumentTypeError(
            "Interactive mode must be one of: auto, interactive, direct."
        )
    return mode


def parse_flow_id(value):
    flow_id = slug(value)
    if not flow_id:
        raise argparse.ArgumentTypeError("Flow id cannot be empty.")
    return flow_id


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


def seed_state(
    flow,
    flow_id,
    viewports,
    modes,
    browser,
    improvement_intensity,
    view_granularity,
    interactive_mode,
):
    return {
        "flow": flow,
        "flow_id": flow_id,
        "user_goal": "",
        "concerns": [],
        "improvement_intensity": improvement_intensity,
        "view_granularity": view_granularity,
        "interactive_mode": interactive_mode,
        "browser": {
            "preference": browser,
            "selected": "",
            "reason": "",
        },
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
    state.setdefault("improvement_intensity", DEFAULT_IMPROVEMENT_INTENSITY)
    state.setdefault("view_granularity", DEFAULT_VIEW_GRANULARITY)
    state.setdefault("interactive_mode", DEFAULT_INTERACTIVE_MODE)
    state.setdefault("flow_id", slug(state.get("flow") or "flow"))

    browser = state.get("browser")
    if not browser:
        state["browser"] = {
            "preference": DEFAULT_BROWSER,
            "selected": "",
            "reason": "",
        }
    elif isinstance(browser, str):
        state["browser"] = {
            "preference": browser,
            "selected": "",
            "reason": "",
        }

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


def browser_label(state):
    browser = state.get("browser") or {}
    if isinstance(browser, str):
        return browser
    return browser.get("selected") or browser.get("preference") or DEFAULT_BROWSER


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


def slug(value):
    value = str(value or "").lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "item"


def page_id(viewport, mode, page):
    return slug(f"{viewport}-{mode}-{page}")


def view_id(viewport, mode, page, view_number, view_name):
    return slug(f"{viewport}-{mode}-{page}-{view_number}-{view_name}")


def row_attrs(viewport, mode, kind, page=None, view=None):
    attrs = data_attrs(viewport, mode)
    attrs += f' data-row-kind="{esc(kind)}"'
    if page:
        attrs += f' data-page-id="{esc(page)}"'
    if view:
        attrs += f' data-view-id="{esc(view)}"'
    return attrs


def context_row_attrs(kind, context):
    return (
        f' data-context-row="{esc(context)}"'
        f' data-row-kind="{esc(kind)}"'
        f' data-context-id="{esc(context)}"'
    )


def sticky_label(title, meta="", classes="", marker=""):
    title_class = "text-white" if "text-white" in classes else "text-neutral-950"
    meta_class = "text-neutral-300" if "text-white" in classes else "text-neutral-500"
    bg_class = "" if "bg-" in classes else "bg-white"
    marker_html = (
        f'<span class="mr-2 inline-block h-2.5 w-2.5 rounded-sm {marker}"></span>'
        if marker
        else ""
    )
    return (
        f'<th class="sticky left-0 z-10 border-b border-r border-neutral-200 {bg_class} '
        f'px-3 py-2 text-left align-top {classes}">'
        f'<div class="font-semibold {title_class}">{marker_html}{esc(title)}</div>'
        f'<div class="mt-0.5 text-[11px] font-normal {meta_class}">{esc(meta)}</div>'
        f"</th>"
    )


def disclosure_label(title, meta, target_type, target_id, classes="", marker=""):
    title_class = "text-white" if "text-white" in classes else "text-neutral-950"
    meta_class = "text-neutral-300" if "text-white" in classes else "text-neutral-500"
    bg_class = "" if "bg-" in classes else "bg-white"
    marker_html = (
        f'<span class="mr-2 inline-block h-2.5 w-2.5 rounded-sm {marker}"></span>'
        if marker
        else ""
    )
    target_attr = {
        "context": "data-toggle-context",
        "page": "data-toggle-page",
        "view": "data-toggle-view",
    }[target_type]
    return (
        f'<th class="sticky left-0 z-10 border-b border-r border-neutral-200 {bg_class} '
        f'px-3 py-2 text-left align-top {classes}">'
        f'<div class="flex items-start gap-2">'
        f'<button type="button" class="mt-0.5 inline-flex h-4 w-4 items-center justify-center '
        f'rounded border border-current text-[10px] leading-none" aria-expanded="true" '
        f'{target_attr}="{esc(target_id)}">-</button>'
        f'<div><div class="font-semibold {title_class}">{marker_html}{esc(title)}</div>'
        f'<div class="mt-0.5 text-[11px] font-normal {meta_class}">{esc(meta)}</div></div>'
        f"</div></th>"
    )


def screenshot_cell(item, compact=False):
    path = item.get("screenshot") if item else None
    if not path:
        return '<span class="text-neutral-400">--</span>'
    safe_path = esc(path)
    frame_size = "h-28 w-44" if compact else "h-36 w-56"
    path_class = "sr-only" if compact else "mt-1 block max-w-56 truncate text-[10px] text-neutral-400"
    onerror = (
        "this.style.display='none';"
        "const label=this.parentElement.nextElementSibling;"
        "label.textContent='Missing screenshot';"
        "label.classList.remove('sr-only','hidden');"
        "label.classList.add('mt-1','block','text-[10px]','text-neutral-400');"
    )
    return (
        f'<button type="button" class="block text-left" data-screenshot-src="{safe_path}" '
        f'aria-label="Open screenshot {safe_path}">'
        f'<span class="screenshot-frame flex {frame_size} items-center justify-center rounded-md '
        f'border border-neutral-400 p-2 shadow-inner">'
        f'<img src="{safe_path}" alt="{safe_path}" '
        f'onerror="{esc(onerror)}" '
        f'class="max-h-full max-w-full rounded-sm bg-white object-contain shadow-sm ring-2 ring-neutral-500/40" />'
        f"</span>"
        f'<span class="{path_class}">{safe_path}</span>'
        f"</button>"
    )


def iteration_value_cells(iteration_numbers, value_for_number, classes):
    return [
        td(value_for_number(number), classes)
        for number in iteration_numbers
    ]


def average_cells(iteration_numbers, values_for_number, classes):
    return [
        raw_td(
            score_pill(average(values_for_number(number))),
            classes,
        )
        for number in iteration_numbers
    ]


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
    iteration_by_number = {
        item.get("iteration", 0): item for item in iterations if isinstance(item, dict)
    }

    viewports = state.get("viewports") or DEFAULT_VIEWPORTS
    modes = state.get("color_modes") or DEFAULT_COLOR_MODES
    viewport_options = "\n".join(
        [
            '<option value="all">All breakpoints</option>'
        ]
        + [
            (
                f'<option value="{esc(viewport["name"])}">{esc(viewport_label(viewport))}</option>'
            )
            for viewport in viewports
        ]
    )
    mode_options = "\n".join(
        [
            '<option value="all">All modes</option>'
        ]
        + [
            (
                f'<option value="{esc(mode)}">{esc(mode)}</option>'
            )
            for mode in modes
        ]
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
    context_id = "flow-context"
    for label, key in (("Changes", "changes"), ("Decision", "decision"), ("Why", "why")):
        label_cell = (
            disclosure_label(
                label,
                "Flow / iteration context",
                "context",
                context_id,
                "bg-neutral-50",
                "bg-neutral-400",
            )
            if key == "changes"
            else sticky_label(
                label,
                "Flow / iteration context",
                "bg-neutral-50",
                "bg-neutral-400",
            )
        )
        matrix_rows.append(
            row(
                [
                    label_cell,
                    *iteration_value_cells(
                        iteration_numbers,
                        lambda number, key=key: (iteration_by_number.get(number) or {}).get(key),
                        "border-b border-r border-neutral-200 bg-neutral-50 px-3 py-2 align-top text-neutral-700",
                    ),
                ],
                context_row_attrs(
                    "context" if key == "changes" else "context-detail",
                    context_id,
                ),
            )
        )

    visible_combinations = [
        (viewport["name"], mode)
        for viewport in viewports
        for mode in modes
        if any(
            item.get("viewport") == viewport["name"] and item.get("mode") == mode
            for item in views
        )
    ]

    for viewport, mode in visible_combinations:
        pages = sorted(
            {
                key[0]
                for key in grouped_views
                if key[3] == viewport and key[4] == mode
            }
        )
        for page in pages:
            current_page_id = page_id(viewport, mode, page)
            page_keys = [
                key
                for key in sorted(grouped_views)
                if key[0] == page and key[3] == viewport and key[4] == mode
            ]
            page_items = [
                item
                for key in page_keys
                for item in grouped_views[key].values()
            ]
            matrix_rows.append(
                row(
                    [
                        disclosure_label(
                            f"Page: {page}",
                            f"Flow > {page} / {viewport} / {mode}",
                            "page",
                            current_page_id,
                            "bg-neutral-900 text-white",
                            "bg-white",
                        ),
                        *average_cells(
                            iteration_numbers,
                            lambda number, page_items=page_items: (
                                numeric(item.get("score"))
                                for item in page_items
                                if item.get("iteration", 0) == number
                            ),
                            "border-b border-r border-neutral-700 bg-neutral-900 px-3 py-2 align-top",
                        ),
                    ],
                    row_attrs(viewport, mode, "page", page=current_page_id),
                )
            )

            for key in page_keys:
                page, view_number, view_name, viewport, mode = key
                current_page_id = page_id(viewport, mode, page)
                current_view_id = view_id(viewport, mode, page, view_number, view_name)
                by_iteration = grouped_views[key]
                meta = f"Flow > {page} > {view_name} / {viewport} / {mode}"
                principle_map = grouped_rubric.get(key, {})
                ordered_principles = [
                    principle for principle in PRINCIPLES if principle in principle_map
                ] + sorted(
                    principle for principle in principle_map if principle not in PRINCIPLES
                )

                matrix_rows.append(
                    row(
                        [
                            disclosure_label(
                                f"{view_number} {view_name}",
                                meta,
                                "view",
                                current_view_id,
                                "bg-neutral-900 pl-6 text-white",
                                "bg-white",
                            ),
                            *[
                                raw_td(
                                    (
                                        f'<div class="flex flex-col gap-2">'
                                        f'<div>'
                                        f'{score_pill(numeric((by_iteration.get(number) or {}).get("score")))}'
                                        f'<span class="ml-2 text-[11px] text-neutral-400">'
                                        f'{esc(delta_text((by_iteration.get(number) or {}).get("delta")))}</span>'
                                        f'<div class="mt-1 text-[11px] text-neutral-300">'
                                        f'{esc((by_iteration.get(number) or {}).get("lowest_principle"))}</div>'
                                        f'</div>'
                                        f'{screenshot_cell(by_iteration.get(number), compact=True)}'
                                        f'</div>'
                                    ),
                                    "border-b border-r border-neutral-700 bg-neutral-900 px-3 py-2 align-top",
                                )
                                for number in iteration_numbers
                            ],
                        ],
                        row_attrs(
                            viewport,
                            mode,
                            "view",
                            page=current_page_id,
                            view=current_view_id,
                        ),
                    )
                )
                matrix_rows.append(
                    row(
                        [
                            sticky_label("Notes", "View rationale", "pl-10"),
                            *[
                                td(
                                    (by_iteration.get(number) or {}).get("note"),
                                    "border-b border-r border-neutral-200 px-3 py-2 align-top text-neutral-700",
                                )
                                for number in iteration_numbers
                            ],
                        ],
                        row_attrs(
                            viewport,
                            mode,
                            "detail",
                            page=current_page_id,
                            view=current_view_id,
                        ),
                    )
                )

                for principle in ordered_principles:
                    scores_by_iteration = principle_map[principle]
                    matrix_rows.append(
                        row(
                            [
                                sticky_label(principle, "Rubric", "pl-14 font-normal"),
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
                            row_attrs(
                                viewport,
                                mode,
                                "detail",
                                page=current_page_id,
                                view=current_view_id,
                            ),
                        )
                    )

        combo_items = [
            item
            for item in views
            if item.get("viewport") == viewport and item.get("mode") == mode
        ]
        matrix_rows.append(
            row(
                [
                    sticky_label(
                        "Flow avg",
                        f"Flow / {viewport} / {mode}",
                        "bg-black text-white",
                        "bg-white",
                    ),
                    *average_cells(
                        iteration_numbers,
                        lambda number, combo_items=combo_items: (
                            numeric(item.get("score"))
                            for item in combo_items
                            if item.get("iteration", 0) == number
                        ),
                        "border-b border-r border-neutral-700 bg-black px-3 py-2 align-top",
                    ),
                ],
                row_attrs(viewport, mode, "flow"),
            )
        )

    matrix_rows = "\n".join(matrix_rows)

    replacements = {
        "{{FLOW_NAME}}": esc(state.get("flow")),
        "{{VIEWPORT_OPTIONS}}": viewport_options,
        "{{MODE_OPTIONS}}": mode_options,
        "{{MATRIX_HEADER}}": matrix_header,
        "{{MATRIX_ROWS}}": matrix_rows,
    }

    for key, value in replacements.items():
        template = template.replace(key, value)
    return template


def main():
    parser = argparse.ArgumentParser(
        description="Create or refresh a UI/UX Score Loop dashboard workspace."
    )
    parser.add_argument(
        "--output",
        default=None,
        help=(
            "Dashboard path. Defaults to "
            ".ui-ux-score-loop/flows/{flow-id}/dashboard.html."
        ),
    )
    parser.add_argument("--flow", default="Flow name")
    parser.add_argument(
        "--flow-id",
        default=None,
        type=parse_flow_id,
        help="Stable folder id for this flow. Defaults to a slug of --flow.",
    )
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
    parser.add_argument(
        "--browser",
        default=DEFAULT_BROWSER,
        type=parse_browser,
        help="Browser preference or selected browser/tool for this loop.",
    )
    parser.add_argument(
        "--improvement-intensity",
        default=None,
        type=parse_improvement_intensity,
        choices=("focused", "grouped", "broad"),
        help="How aggressively to improve each view per iteration.",
    )
    parser.add_argument(
        "--view-granularity",
        default=None,
        type=parse_view_granularity,
        choices=("essential", "standard", "exhaustive"),
        help="How aggressively to split the flow into views/states.",
    )
    parser.add_argument(
        "--interactive-mode",
        default=None,
        type=parse_interactive_mode,
        choices=("auto", "interactive", "direct"),
        help="How to handle preflight configuration questions.",
    )
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parents[1]
    template_path = skill_root / "assets" / "dashboard.html"
    flow_id = args.flow_id or slug(args.flow)
    output_path = args.output or f".ui-ux-score-loop/flows/{flow_id}/dashboard.html"
    output = Path(output_path).expanduser().resolve()
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
        state["flow_id"] = state.get("flow_id") or flow_id
        if args.improvement_intensity:
            state["improvement_intensity"] = args.improvement_intensity
        if args.view_granularity:
            state["view_granularity"] = args.view_granularity
        if args.interactive_mode:
            state["interactive_mode"] = args.interactive_mode
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    else:
        state = seed_state(
            args.flow,
            flow_id,
            viewports,
            modes,
            args.browser,
            args.improvement_intensity or DEFAULT_IMPROVEMENT_INTENSITY,
            args.view_granularity or DEFAULT_VIEW_GRANULARITY,
            args.interactive_mode or DEFAULT_INTERACTIVE_MODE,
        )
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
