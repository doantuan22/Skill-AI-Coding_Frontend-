import re
with open('tests/test_codex_adapter.py', 'r', encoding='utf-8') as f:
    text = f.read()

replacement = """import importlib.util
        spec1 = importlib.util.spec_from_file_location("export", str(ROOT / ".codex-plugin" / "export.py"))
        export = importlib.util.module_from_spec(spec1)
        spec1.loader.exec_module(export)
        
        spec2 = importlib.util.spec_from_file_location("verify", str(ROOT / ".codex-plugin" / "verify.py"))
        verify = importlib.util.module_from_spec(spec2)
        if (ROOT / ".codex-plugin" / "verify.py").exists():
            spec2.loader.exec_module(verify)"""

text = re.sub(r'import importlib\.util; spec = .*?exec_module.*?\n', replacement + '\n', text)
with open('tests/test_codex_adapter.py', 'w', encoding='utf-8') as f:
    f.write(text)
