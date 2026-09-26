"""Runtime Capability Detector: Read-only detection of package manager, build/dev/test commands, and Playwright readiness.

Strictly read-only: never installs packages, never downloads browsers, never fabricates missing commands.
"""
from __future__ import annotations

from typing import Any

from uiux.engine.repo_intelligence.scanner import RepositorySnapshot

PLAYWRIGHT_PKGS = ("playwright", "@playwright/test", "playwright-core")


def detect_runtime_capabilities(snapshot: RepositorySnapshot) -> dict[str, Any]:
    files = snapshot.file_set
    pkg = snapshot.package_json if isinstance(snapshot.package_json, dict) else {}
    scripts = pkg.get("scripts", {}) if isinstance(pkg.get("scripts"), dict) else {}
    deps = snapshot.get_dependencies()

    # 1. Detect Package Manager from lockfiles or manifests
    pm: str | None = None
    if "pnpm-lock.yaml" in files:
        pm = "pnpm"
    elif "yarn.lock" in files:
        pm = "yarn"
    elif "bun.lockb" in files or "bun.lock" in files:
        pm = "bun"
    elif "package-lock.json" in files or pkg:
        pm = "npm"
    elif "pom.xml" in files:
        pm = "maven"
    elif "build.gradle" in files or "build.gradle.kts" in files:
        pm = "gradle"

    # 2. Extract commands strictly from declared configuration
    dev_cmd: str | None = None
    build_cmd: str | None = None
    test_cmd: str | None = None
    lint_cmd: str | None = None
    typecheck_cmd: str | None = None
    install_cmd: str | None = None
    commands_source: str | None = None

    if scripts:
        commands_source = "package.json scripts"
        prefix = f"{pm} run " if pm in ("npm", "bun") else f"{pm} " if pm else "npm run "

        if "dev" in scripts:
            dev_cmd = f"{prefix}dev"
        elif "start" in scripts:
            dev_cmd = f"{prefix}start"

        if "build" in scripts:
            build_cmd = f"{prefix}build"

        if "test" in scripts:
            test_cmd = f"{pm} test" if pm in ("npm", "pnpm", "yarn") else "npm test"

        if "lint" in scripts:
            lint_cmd = f"{prefix}lint"

        if "typecheck" in scripts or "check" in scripts:
            key = "typecheck" if "typecheck" in scripts else "check"
            typecheck_cmd = f"{prefix}{key}"

        if pm:
            install_cmd = f"{pm} install"
    elif pm == "maven":
        commands_source = "pom.xml"
        install_cmd = "mvn install"
        build_cmd = "mvn package"
        dev_cmd = "./mvnw spring-boot:run" if "mvnw" in files else "mvn spring-boot:run"
        test_cmd = "mvn test"
    elif pm == "gradle":
        commands_source = "build.gradle"
        install_cmd = "./gradlew build" if "gradlew" in files else "gradle build"
        build_cmd = "./gradlew assemble" if "gradlew" in files else "gradle assemble"
        dev_cmd = "./gradlew bootRun" if "gradlew" in files else "gradle bootRun"
        test_cmd = "./gradlew test" if "gradlew" in files else "gradle test"
    elif "Makefile" in files:
        makefile_text = snapshot.read_text("Makefile", max_chars=10_000)
        commands_source = "Makefile"
        if "dev:" in makefile_text:
            dev_cmd = "make dev"
        if "build:" in makefile_text:
            build_cmd = "make build"
        if "test:" in makefile_text:
            test_cmd = "make test"

    # 3. Detect Playwright availability without executing or modifying anything
    playwright_available = False
    has_pw_dep = any(pkg_name in deps for pkg_name in PLAYWRIGHT_PKGS)
    has_pw_config = any("playwright.config." in f for f in files)

    if has_pw_dep or has_pw_config:
        playwright_available = True
        browser_validation = "playwright"
    else:
        browser_validation = "manual" if snapshot.ui_files else "none"

    # 4. Confidence
    if commands_source and (dev_cmd or build_cmd):
        confidence = 0.95
    elif pm:
        confidence = 0.70
    else:
        confidence = 0.0

    return {
        "package_manager": pm,
        "install_command": install_cmd,
        "dev_command": dev_cmd,
        "build_command": build_cmd,
        "test_command": test_cmd,
        "lint_command": lint_cmd,
        "typecheck_command": typecheck_cmd,
        "browser_validation": browser_validation,
        "playwright_available": playwright_available,
        "commands_source": commands_source,
        "confidence": confidence,
    }
