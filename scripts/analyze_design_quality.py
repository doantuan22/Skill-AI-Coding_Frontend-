"""Static (and optional runtime-probe) evidence collector for design quality evals E65-E80.

Read-only and standard-library only. It scans a project's HTML/CSS/JS-family sources for motion, effect,
interaction and consistency signals, optionally merges runner motion probes from manifest.json files, and
reports heuristic statuses: PASS, WARN, FAIL, NEEDS_REVIEW (human/agent judgment required) or
NEEDS_RUNTIME (evidence requires a browser capture). It never claims a visual judgment it cannot make.

Usage:
    python scripts/analyze_design_quality.py <project> [--manifest .evidence/<session>/manifest.json]
                                             [--visual-intensity 3] [--format json|md]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SOURCE_SUFFIXES = {".html", ".htm", ".css", ".scss", ".sass", ".less", ".js", ".mjs", ".cjs", ".jsx", ".ts",
                   ".tsx", ".vue", ".svelte", ".astro"}
SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".next", ".nuxt", ".output", ".evidence", "coverage", ".svelte-kit"}
EFFECT_BUDGET = {1: 2, 2: 3, 3: 5, 4: 8, 5: 12}
LAYOUT_PROPS = r"(?:width|height|top|left|right|bottom|margin(?:-[a-z]+)?|padding(?:-[a-z]+)?|font-size)"
LIBRARIES = {
    "gsap": r"from\s+['\"]gsap|require\(['\"]gsap", "motion": r"from\s+['\"](?:framer-motion|motion(?:/react)?)['\"]",
    "three": r"from\s+['\"]three['\"]|require\(['\"]three['\"]", "lottie": r"lottie", "rive": r"@rive-app",
    "animejs": r"animejs|from\s+['\"]anime", "aos": r"\baos\b|data-aos", "scroll-hijack-lib": r"locomotive-scroll|fullpage\.js|fullpage-js",
}


def _ms(value: str) -> float | None:
    match = re.fullmatch(r"([\d.]+)(ms|s)", value.strip())
    if not match:
        return None
    number = float(match.group(1))
    return number if match.group(2) == "ms" else number * 1000


def collect(project: Path) -> tuple[dict, int]:
    texts: list[tuple[str, str]] = []
    for path in sorted(project.rglob("*")):
        if path.is_file() and path.suffix.lower() in SOURCE_SUFFIXES and not (SKIP_DIRS & set(path.relative_to(project).parts)):
            try:
                texts.append((path.suffix.lower(), path.read_text(encoding="utf-8", errors="ignore")))
            except OSError:
                continue
    blob = "\n".join(t for _, t in texts)
    style_blob = "\n".join(t for s, t in texts if s in {".css", ".scss", ".sass", ".less", ".html", ".htm", ".vue", ".svelte", ".astro", ".jsx", ".tsx"})
    markup = "\n".join(t for s, t in texts if s in {".html", ".htm", ".vue", ".svelte", ".astro", ".jsx", ".tsx"})
    s: dict[str, object] = {}
    decls = re.findall(r"(?:transition|animation)(?:-duration)?\s*:\s*([^;{}]+)", style_blob, re.I)
    durations = sorted({d for decl in decls for d in (_ms(tok) for tok in re.findall(r"[\d.]+m?s\b", decl)) if d is not None and d > 0})
    easings = sorted({e.lower().replace(" ", "") for decl in decls for e in re.findall(
        r"cubic-bezier\([^)]*\)|linear\([^)]*\)|steps\([^)]*\)|ease-in-out|ease-in|ease-out|\bease\b|\blinear\b", decl, re.I)})
    keyframes = re.findall(r"@keyframes\s+[\w-]+\s*\{((?:[^{}]*\{[^{}]*\})*[^{}]*)\}", style_blob)
    s["transition_declarations"] = len(re.findall(r"\btransition(?:-property)?\s*:", style_blob, re.I))
    s["transition_all"] = len(re.findall(r"transition(?:-property)?\s*:\s*all\b", style_blob, re.I))
    s["distinct_durations_ms"] = durations
    s["distinct_easings"] = easings
    s["keyframes"] = len(keyframes)
    s["infinite_animations"] = len(re.findall(r"animation[^;{}]*\binfinite\b", style_blob, re.I)) + len(re.findall(r"iterations\s*:\s*Infinity|repeat\s*:\s*-1", blob))
    s["animated_layout_properties"] = sorted({m.lower() for kf in keyframes for m in re.findall(rf"\b({LAYOUT_PROPS})\s*:", kf, re.I)}
                                             | {m.lower() for m in re.findall(rf"transition(?:-property)?\s*:[^;{{}}]*\b({LAYOUT_PROPS})\b", style_blob, re.I)})
    s["animated_filters"] = sum(1 for kf in keyframes if re.search(r"\b(?:filter|backdrop-filter)\s*:", kf))
    s["reduced_motion_queries"] = len(re.findall(r"prefers-reduced-motion", blob, re.I)) + len(re.findall(r"useReducedMotion|reducedMotion", blob))
    s["scroll_listeners"] = len(re.findall(r"addEventListener\(\s*['\"]scroll['\"]", blob)) + len(re.findall(r"\bonscroll\s*=|\.scroll\(\s*function", blob))
    s["passive_scroll_listeners"] = len(re.findall(r"addEventListener\(\s*['\"]scroll['\"][^)]*passive\s*:\s*true", blob))
    s["wheel_prevent_default"] = len(re.findall(r"['\"](?:wheel|mousewheel|touchmove)['\"][\s\S]{0,200}?preventDefault", blob))
    s["intersection_observers"] = len(re.findall(r"IntersectionObserver", blob))
    s["request_animation_frame"] = len(re.findall(r"requestAnimationFrame", blob))
    s["scroll_driven_css"] = len(re.findall(r"animation-timeline|view-timeline|scroll-timeline", style_blob))
    s["view_transitions"] = len(re.findall(r"startViewTransition|view-transition-name|@view-transition", blob))
    s["layout_animation_apis"] = len(re.findall(r"\blayoutId\b|\blayout\s*=\s*\{?true|\.animate\(\s*\[|getBoundingClientRect\(\)[\s\S]{0,300}?\.animate\(", blob))
    s["will_change"] = len(re.findall(r"will-change\s*:", style_blob))
    s["entrance_attributes"] = len(re.findall(r"data-(?:aos|animate|reveal|scroll)\b|class=\"[^\"]*\b(?:reveal|animate-on-scroll|fade-in)\b", markup))
    s["parallax_signals"] = len(re.findall(r"parallax|background-attachment\s*:\s*fixed", blob, re.I))
    s["scroll_snap_mandatory"] = len(re.findall(r"scroll-snap-type\s*:[^;]*mandatory", style_blob))
    # effects (feature-query conditions such as "@supports (backdrop-filter: blur())" are not usages)
    effect_blob = re.sub(r"@supports[^{]*", "@supports ", style_blob)
    s["backdrop_filters"] = len(re.findall(r"backdrop-filter\s*:\s*(?!none)", effect_blob))
    s["blur_filters"] = len(re.findall(r"(?<!backdrop-)filter\s*:[^;]*blur\(", effect_blob))
    shadows = re.findall(r"box-shadow\s*:\s*([^;{}]+)", style_blob)
    s["distinct_shadows"] = len({x.strip() for x in shadows if x.strip() != "none"})
    s["large_shadows"] = sum(1 for x in shadows if any(float(v) >= 40 for v in re.findall(r"(\d+(?:\.\d+)?)px", x)[2:3]))
    s["gradients"] = len(re.findall(r"(?:linear|radial|conic)-gradient\(", style_blob))
    s["blend_modes"] = len(re.findall(r"mix-blend-mode\s*:\s*(?!normal)", style_blob))
    s["canvas_or_webgl"] = len(re.findall(r"<canvas|getContext\(\s*['\"](?:webgl2?|2d)['\"]", blob))
    s["supports_fallbacks"] = len(re.findall(r"@supports", style_blob))
    s["reduced_transparency"] = len(re.findall(r"prefers-reduced-transparency|prefers-contrast", style_blob))
    # interaction
    s["hover_rules"] = len(re.findall(r":hover", style_blob))
    s["focus_visible_rules"] = len(re.findall(r":focus-visible", style_blob))
    s["focus_rules"] = len(re.findall(r":focus(?![-\w])", style_blob))
    s["active_rules"] = len(re.findall(r":active", style_blob))
    s["hover_media"] = len(re.findall(r"\(\s*hover\s*:\s*hover\s*\)|\(\s*pointer\s*:\s*(?:fine|coarse)\s*\)", style_blob))
    s["keyboard_handlers"] = len(re.findall(r"['\"]key(?:down|up)['\"]|onKeyDown|@keydown", blob))
    s["interactive_elements"] = len(re.findall(r"<(?:button|a\s|input|select|textarea)|role=['\"](?:button|tab|menuitem)['\"]", markup))
    s["custom_cursor_none"] = len(re.findall(r"cursor\s*:\s*none", style_blob))
    s["outline_none"] = len(re.findall(r"outline\s*:\s*(?:none|0)\b", style_blob))
    s["aria_live"] = len(re.findall(r"aria-live|role=['\"](?:status|alert)['\"]", markup))
    # layout / consistency / detail
    s["media_queries"] = len(re.findall(r"@media", style_blob))
    s["container_queries"] = len(re.findall(r"@container", style_blob))
    s["fluid_type"] = len(re.findall(r"clamp\(", style_blob))
    s["grid_layouts"] = len(re.findall(r"display\s*:\s*grid", style_blob))
    s["grid_template_areas"] = len(re.findall(r"grid-template-areas", style_blob))
    s["three_equal_columns"] = len(re.findall(r"grid-template-columns\s*:\s*repeat\(\s*3\s*,\s*1fr\s*\)", style_blob))
    s["sections"] = len(re.findall(r"<section\b", markup))
    s["distinct_radii"] = len({x.strip() for x in re.findall(r"border-radius\s*:\s*([^;{}]+)", style_blob)})
    s["distinct_font_sizes"] = len({x.strip() for x in re.findall(r"font-size\s*:\s*([^;{}]+)", style_blob)})
    s["font_families"] = sorted({x.split(",")[0].strip().strip("'\"").lower() for x in re.findall(r"font-family\s*:\s*([^;{}]+)", style_blob)
                                 if not x.strip().startswith("var(") and x.split(",")[0].strip().strip("'\"").lower() not in {"inherit", "system-ui", "sans-serif", "serif", "monospace"}})
    s["css_custom_properties"] = len(re.findall(r"--[\w-]+\s*:", style_blob))
    detail = {
        "focus_visible": s["focus_visible_rules"] > 0,
        "tabular_numerals": bool(re.search(r"tabular-nums", style_blob)),
        "text_wrap_balance": bool(re.search(r"text-wrap\s*:\s*(?:balance|pretty)", style_blob)),
        "aspect_ratio": bool(re.search(r"aspect-ratio", style_blob)),
        "disabled_styles": bool(re.search(r":disabled|\[aria-disabled", style_blob)),
        "busy_or_loading_states": bool(re.search(r"aria-busy|skeleton|is-loading|data-loading", blob)),
        "reduced_motion": s["reduced_motion_queries"] > 0,
        "feature_fallbacks": s["supports_fallbacks"] > 0,
    }
    s["detail_signals"] = detail
    s["libraries"] = sorted(name for name, pattern in LIBRARIES.items() if re.search(pattern, blob))
    return s, len(texts)


def runtime_summary(manifests: list[Path]) -> dict | None:
    probes = []
    for manifest in manifests:
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        for capture in data.get("captures", []):
            probe = capture.get("motion_probe")
            if isinstance(probe, dict) and "animations" in probe:
                probes.append({"viewport": capture.get("viewport"), "reduced_motion": capture.get("reduced_motion"), **probe})
    if not probes:
        return None
    def pick(pred):
        return [p for p in probes if pred(p)]
    normal = pick(lambda p: p.get("reduced_motion") != "reduce")
    reduced = pick(lambda p: p.get("reduced_motion") == "reduce")
    return {
        "captures_with_probe": len(probes),
        "max_running_animations": max(p["animations"]["total"] for p in probes),
        "max_infinite_animations": max((p["animations"]["infinite"] for p in normal), default=0),
        "reduced_motion_infinite_animations": max((p["animations"]["infinite"] for p in reduced), default=None),
        "max_cls": max(p.get("cumulative_layout_shift", 0) for p in probes),
        "max_backdrop_filter_elements": max(p["effects"]["backdrop_filter"] for p in probes),
        "desktop_animations": max((p["animations"]["total"] for p in normal if p.get("viewport") in {"desktop", "desktop_wide"}), default=None),
        "mobile_animations": max((p["animations"]["total"] for p in normal if p.get("viewport") == "mobile"), default=None),
        "mobile_backdrop_filter": max((p["effects"]["backdrop_filter"] for p in normal if p.get("viewport") == "mobile"), default=None),
    }


def result(status: str, *reasons: str) -> dict:
    return {"status": status, "reasons": [r for r in reasons if r]}


def evaluate(s: dict, rt: dict | None, visual_intensity: int) -> dict:
    has_motion = s["transition_declarations"] + s["keyframes"] > 0
    e: dict[str, dict] = {}
    # E65 Motion Presence
    if not has_motion:
        e["E65"] = result("WARN", "no transitions or keyframes: controls have no motion feedback (valid only if intentionally static)")
    elif s["entrance_attributes"] > 12:
        e["E65"] = result("WARN", f"{s['entrance_attributes']} elements marked for entrance animation; presence may exceed purpose")
    else:
        e["E65"] = result("PASS", f"{s['transition_declarations']} transitions, {s['keyframes']} keyframes")
    # E66 Motion Consistency
    nd, ne = len(s["distinct_durations_ms"]), len(s["distinct_easings"])
    status = "PASS" if nd <= 6 and ne <= 4 and not s["transition_all"] else "FAIL" if nd > 9 or ne > 6 else "WARN"
    e["E66"] = result(status, f"{nd} distinct durations, {ne} distinct easings",
                      f"{s['transition_all']} 'transition: all' declarations" if s["transition_all"] else "")
    # E67 Motion Performance
    risk, why = 0, []
    unthrottled = s["scroll_listeners"] - s["passive_scroll_listeners"]
    if s["scroll_listeners"] and not (s["intersection_observers"] or s["request_animation_frame"]):
        risk += 2; why.append(f"{s['scroll_listeners']} scroll listener(s) without rAF/IntersectionObserver")
    elif unthrottled > 0:
        risk += 1; why.append(f"{unthrottled} non-passive scroll listener(s)")
    if s["animated_layout_properties"]:
        risk += 2; why.append(f"animates layout properties: {', '.join(s['animated_layout_properties'])}")
    if s["animated_filters"]:
        risk += 2; why.append(f"{s['animated_filters']} keyframes animate filter/backdrop-filter")
    if s["infinite_animations"] > 2:
        risk += 1; why.append(f"{s['infinite_animations']} infinite animations")
    if s["will_change"] > 10:
        risk += 1; why.append(f"{s['will_change']} will-change declarations")
    if rt and rt["max_cls"] > 0.1:
        risk += 3; why.append(f"runtime CLS {rt['max_cls']}")
    e["E67"] = result("PASS" if risk == 0 else "WARN" if risk <= 2 else "FAIL", *why or ["no static performance risk signals"])
    # E68 Reduced Motion Support
    if not has_motion:
        e["E68"] = result("PASS", "no motion to reduce")
    elif not s["reduced_motion_queries"]:
        e["E68"] = result("FAIL", "motion present but no prefers-reduced-motion handling")
    elif rt and rt["reduced_motion_infinite_animations"]:
        e["E68"] = result("WARN", f"{rt['reduced_motion_infinite_animations']} infinite animations still running under reduced motion")
    else:
        e["E68"] = result("PASS" if rt else "NEEDS_RUNTIME", f"{s['reduced_motion_queries']} reduced-motion handlers",
                          "" if rt else "capture with options.reduced_motion='reduce' to verify behavior")
    # E69 Interaction Feedback
    if s["interactive_elements"] and not (s["focus_visible_rules"] or s["focus_rules"]):
        e["E69"] = result("FAIL", "interactive elements without any focus styling")
    elif s["outline_none"] and not s["focus_visible_rules"]:
        e["E69"] = result("FAIL", "outline removed without a focus-visible replacement")
    elif not s["active_rules"] and s["interactive_elements"]:
        e["E69"] = result("WARN", "no :active/pressed feedback styles")
    else:
        e["E69"] = result("PASS", f"hover {s['hover_rules']}, focus-visible {s['focus_visible_rules']}, active {s['active_rules']}")
    # E70 Transition Continuity
    cont = s["view_transitions"] + s["layout_animation_apis"]
    e["E70"] = result("NEEDS_REVIEW", f"{cont} continuity mechanisms (view transitions / layout animations) found",
                      "judge against the motion plan: do list→detail, card→modal and navigation keep object identity?")
    # E71 Visual Effect Quality
    notes = []
    if s["backdrop_filters"] and not s["supports_fallbacks"]:
        notes.append("backdrop-filter without @supports fallback")
    if (s["backdrop_filters"] or s["blend_modes"]) and not s["reduced_transparency"]:
        notes.append("translucent effects without prefers-reduced-transparency/contrast handling")
    e["E71"] = result("WARN" if notes else "NEEDS_REVIEW", *notes, "inspect captures for banding, contrast over effects and purpose")
    # E72 Effect Overuse
    points = (4 if s["backdrop_filters"] else 0) + (4 if s["backdrop_filters"] > 3 else 0) + (2 if s["blur_filters"] else 0) \
        + (2 if s["large_shadows"] else 0) + (1 if s["gradients"] else 0) + (1 if s["gradients"] > 8 else 0) \
        + (1 if s["blend_modes"] else 0) + (4 if s["canvas_or_webgl"] else 0) + (2 if s["infinite_animations"] > 2 else 0)
    budget = EFFECT_BUDGET[visual_intensity]
    status = "PASS" if points <= budget else "WARN" if points <= budget * 1.5 else "FAIL"
    e["E72"] = result(status, f"estimated effect points {points} vs budget {budget} at visual intensity {visual_intensity}")
    # E73 Layout Sophistication
    responsive = s["media_queries"] + s["container_queries"] + s["fluid_type"]
    e["E73"] = result("WARN" if not responsive else "NEEDS_REVIEW",
                      "no media/container queries or fluid type" if not responsive else f"{s['grid_layouts']} grids, {s['grid_template_areas']} template areas, {s['container_queries']} container queries, {s['fluid_type']} clamp()",
                      "judge hierarchy, rhythm and pattern fit on captures")
    # E74 Pattern Consistency
    drift = [f"{s['distinct_radii']} distinct radii" if s["distinct_radii"] > 6 else "",
             f"{s['distinct_shadows']} distinct shadows" if s["distinct_shadows"] > 5 else "",
             f"{s['distinct_font_sizes']} distinct font sizes" if s["distinct_font_sizes"] > 12 else ""]
    drift = [d for d in drift if d]
    e["E74"] = result("PASS" if not drift else "WARN" if len(drift) == 1 else "FAIL", *drift or ["token-like value counts within range"])
    # E75 Design Style Coherence
    fams = s["font_families"]
    e["E75"] = result("WARN" if len(fams) > 3 else "NEEDS_REVIEW", f"font families: {', '.join(fams) or 'system/variables only'}",
                      "compare rendered result with CAPABILITY-PLAN style, recipe and signature")
    # E76 Premium Detail Density
    present = sum(s["detail_signals"].values())
    e["E76"] = result("PASS" if present >= 6 else "WARN" if present >= 4 else "FAIL",
                      f"{present}/8 detail signals: " + ", ".join(k for k, v in s["detail_signals"].items() if v))
    # E77 Scroll Experience
    if s["wheel_prevent_default"] or "scroll-hijack-lib" in s["libraries"]:
        e["E77"] = result("FAIL", "scroll hijacking signal (wheel/touch preventDefault or full-page scroll library)")
    elif s["parallax_signals"] > 2 or s["scroll_snap_mandatory"]:
        e["E77"] = result("WARN", f"{s['parallax_signals']} parallax signals, {s['scroll_snap_mandatory']} mandatory scroll-snap")
    else:
        e["E77"] = result("NEEDS_REVIEW", "no hijack signals; judge pacing and narrative on a scroll-through")
    # E78 Responsive Motion
    if rt and rt["desktop_animations"] is not None and rt["mobile_animations"] is not None:
        ok = rt["mobile_animations"] <= rt["desktop_animations"]
        e["E78"] = result("PASS" if ok else "WARN", f"running animations desktop {rt['desktop_animations']} vs mobile {rt['mobile_animations']}",
                          "" if ok else "mobile runs more motion than desktop; expected equal or reduced")
    else:
        e["E78"] = result("NEEDS_RUNTIME" if has_motion else "PASS",
                          f"{s['hover_media']} hover/pointer media queries" if has_motion else "no motion",
                          "capture desktop and mobile with options.motion_probe to compare" if has_motion else "")
    # E79 Interaction Discoverability
    if s["hover_rules"] and not (s["focus_visible_rules"] or s["focus_rules"]):
        e["E79"] = result("FAIL", "hover-only affordances: no focus equivalents")
    elif s["custom_cursor_none"]:
        e["E79"] = result("WARN", "native cursor hidden (cursor: none)")
    else:
        e["E79"] = result("NEEDS_REVIEW", f"{s['keyboard_handlers']} keyboard handlers; verify gestures/shortcuts have visible cues")
    # E80 Composition Quality
    e["E80"] = result("WARN" if s["three_equal_columns"] >= 2 else "NEEDS_REVIEW",
                      f"{s['three_equal_columns']} three-equal-column grids across {s['sections']} sections" if s["three_equal_columns"] >= 2 else f"{s['sections']} sections",
                      "check for GENERIC_TEMPLATE_COMPOSITION and HOMOGENIZED_DESIGN against the plan")
    return e


def render_md(report: dict) -> str:
    lines = ["# Design quality evidence", "", f"Project: `{report['project']}` — files scanned: {report['files_scanned']}",
             f"Runtime probes: {'yes' if report['runtime'] else 'none (static evidence only)'}", "", "| Eval | Status | Evidence |", "|---|---|---|"]
    for eid, item in report["evals"].items():
        lines.append(f"| {eid} | {item['status']} | {'; '.join(item['reasons'])} |")
    lines += ["", "Limitations:"] + [f"- {x}" for x in report["limitations"]]
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # Windows consoles default to a legacy code page
    ap = argparse.ArgumentParser(description="Collect design quality evidence (read-only)")
    ap.add_argument("project")
    ap.add_argument("--manifest", action="append", default=[])
    ap.add_argument("--visual-intensity", type=int, default=3, choices=range(1, 6))
    ap.add_argument("--format", choices=("json", "md"), default="json")
    args = ap.parse_args(argv)
    project = Path(args.project).resolve()
    if not project.is_dir():
        print(json.dumps({"status": "INVALID_INPUT", "error": "project directory not found"})); return 3
    signals, count = collect(project)
    runtime = runtime_summary([Path(m) for m in args.manifest])
    report = {
        "schema_version": 1, "project": str(project), "files_scanned": count, "visual_intensity": args.visual_intensity,
        "signals": signals, "runtime": runtime, "evals": evaluate(signals, runtime, args.visual_intensity),
        "limitations": [
            "Static heuristics over source text; frameworks that generate CSS at runtime may be under-counted.",
            "NEEDS_REVIEW requires agent/human judgment against CAPABILITY-PLAN and captures.",
            "NEEDS_RUNTIME requires runner captures with options.motion_probe (and reduced_motion) — no browser is installed by this tool.",
        ],
    }
    print(render_md(report) if args.format == "md" else json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
