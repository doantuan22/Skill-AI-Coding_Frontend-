"""Read-only capability detector for browser execution contracts; standard library only."""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import urllib.request
from pathlib import Path


def command_version(command: str) -> dict[str, object]:
    location = shutil.which(command)
    if not location:
        return {"status": "NOT_AVAILABLE", "version": None, "confidence": "confirmed"}
    try:
        output = subprocess.run([command, "--version"], capture_output=True, text=True, timeout=3, check=False)
        version = (output.stdout or output.stderr).strip().splitlines()[0] if output.returncode == 0 else None
    except (OSError, subprocess.SubprocessError):
        version = None
    return {"status": "AVAILABLE" if version else "AVAILABLE_WITH_LIMITATIONS", "version": version, "confidence": "confirmed"}


def package_data(root: Path) -> dict[str, object]:
    path = root / "package.json"
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def has_dependency(data: dict[str, object], names: set[str]) -> bool:
    for field in ("dependencies", "devDependencies", "peerDependencies"):
        values = data.get(field, {})
        if isinstance(values, dict) and names.intersection(values):
            return True
    return False


def design_runtime(data: dict[str, object]) -> dict[str, object]:
    """Animation/graphics dependencies already present, mapped to technology-resolver ids (read-only)."""
    installed: set[str] = set()
    for field in ("dependencies", "devDependencies", "peerDependencies"):
        values = data.get(field, {})
        if isinstance(values, dict):
            installed.update(values)
    try:
        import knowledge_lib  # same directory; catalogs are the single source of package names
        entries, _ = knowledge_lib.load()
        catalog = {e["id"]: knowledge_lib._as_list(e.get("packages")) for e in entries.values() if e["kind"] == "technology"}
    except Exception:  # detector must never fail because of the knowledge base
        return {"packages": [], "technologies": [], "confidence": "unknown"}
    found = {tid: sorted(set(pkgs) & installed) for tid, pkgs in catalog.items() if set(pkgs) & installed}
    return {"packages": sorted({p for pkgs in found.values() for p in pkgs}), "technologies": sorted(found),
            "confidence": "confirmed"}


def framework(data: dict[str, object], root: Path) -> dict[str, str]:
    dependencies = set()
    for field in ("dependencies", "devDependencies"):
        values = data.get(field, {})
        if isinstance(values, dict):
            dependencies.update(values)
    signals = [
        ("Next.js", "next" in dependencies or (root / "next.config.js").exists() or (root / "next.config.mjs").exists()),
        ("Vite", "vite" in dependencies or (root / "vite.config.ts").exists() or (root / "vite.config.js").exists()),
        ("Angular", "@angular/core" in dependencies or (root / "angular.json").exists()),
        ("Vue", "vue" in dependencies),
        ("React", "react" in dependencies),
        ("Spring Boot", (root / "pom.xml").exists() or (root / "build.gradle").exists()),
        ("plain HTML", any(root.glob("*.html"))),
    ]
    for name, present in signals:
        if present:
            return {"value": name, "confidence": "confirmed"}
    return {"value": None, "confidence": "unknown"}


def running_url(url: str | None) -> dict[str, object]:
    if not url:
        return {"status": "UNKNOWN", "url": None, "confidence": "unknown"}
    try:
        with urllib.request.urlopen(url, timeout=2) as response:
            return {"status": "AVAILABLE", "url": url, "http_status": response.status, "confidence": "confirmed"}
    except Exception as exc:  # Network shape is platform-dependent; report, never mutate.
        return {"status": "NOT_AVAILABLE", "url": url, "reason": type(exc).__name__, "confidence": "confirmed"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only execution capability detector")
    parser.add_argument("project", nargs="?", default=".", help="project directory to inspect")
    parser.add_argument("--url", help="optional known application URL to probe read-only")
    args = parser.parse_args()
    root = Path(args.project).resolve()
    package = package_data(root)
    scripts = package.get("scripts", {}) if isinstance(package.get("scripts", {}), dict) else {}
    locks = [("pnpm", "pnpm-lock.yaml"), ("yarn", "yarn.lock"), ("npm", "package-lock.json"), ("bun", "bun.lockb")]
    manager = next(((name, filename) for name, filename in locks if (root / filename).exists()), (None, None))
    playwright = has_dependency(package, {"@playwright/test", "playwright", "playwright-core"})
    axe_playwright = has_dependency(package, {"@axe-core/playwright"})
    axe_core = has_dependency(package, {"axe-core"})
    compatible = has_dependency(package, {"puppeteer", "selenium-webdriver", "webdriverio", "cypress"})
    configs = [path.name for path in root.glob("playwright.config.*")]
    browser_commands = [name for name in ("chrome", "google-chrome", "chromium", "chromium-browser", "msedge") if shutil.which(name)]
    report = {
        "detector": {"mode": "read_only", "project": str(root)},
        "runtime": {"node": command_version("node"), "python": command_version("python")},
        "package_manager": {"detected": manager[0], "lockfile": manager[1], "command": manager[0],
                            "confidence": "confirmed" if manager[0] else "unknown"},
        "project": {"package_json": (root / "package.json").is_file(), "framework": framework(package, root),
                    "dev_command": scripts.get("dev") or scripts.get("start"), "build_command": scripts.get("build"),
                    "test_command": scripts.get("test")},
        "playwright": {"package_present": {"status": "AVAILABLE" if playwright else "NOT_AVAILABLE", "confidence": "confirmed"},
                       "config_present": {"status": "AVAILABLE" if configs else "NOT_AVAILABLE", "files": configs, "confidence": "confirmed"},
                       "browser_ready": {"status": "UNKNOWN", "confidence": "unknown"}},
        "browser": {"status": "AVAILABLE" if browser_commands else "UNKNOWN", "commands": browser_commands,
                    "headless": {"status": "UNKNOWN", "confidence": "unknown"}, "confidence": "confirmed" if browser_commands else "unknown"},
        "compatible_automation": {"status": "AVAILABLE" if compatible else "NOT_AVAILABLE", "confidence": "confirmed"},
        "accessibility": {"axe_playwright": {"status": "AVAILABLE" if axe_playwright else "NOT_AVAILABLE", "confidence": "confirmed"},
                          "axe_core": {"status": "AVAILABLE" if axe_core else "NOT_AVAILABLE", "confidence": "confirmed"},
                          "strategy": "axe-playwright" if axe_playwright else "axe-core-injection" if axe_core else "manual-fallback"},
        "design_runtime": design_runtime(package),
        "application": {"known_url": args.url, "already_running": running_url(args.url)},
        "limitations": ["No packages installed, configuration modified, browser downloaded, or process started."],
    }
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
