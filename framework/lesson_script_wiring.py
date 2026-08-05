"""Helper to wire teacher scripts into existing stage generators.

Each stage generator (generate-stage1.py, generate-stage2.py, etc.)
has its own set of template strings (TEMPLATE = \"\"\"...\"\"\") and
its own build_* functions. Rather than edit each one individually, this
module provides a single function that:

  1. Reads the generator source file
  2. Finds every `TEMPLATE = \"\"\"...\"\"\"` block
  3. Inserts `{teacher_script}` before the closing `\"\"\"` if not present
  4. Reports which templates were updated

This is intentionally conservative — it only modifies the source text
of the generator, never invokes it. Run the generator manually (or via
`just gen-lessons`) after wiring to regenerate the lesson MDs.

Usage:
    python -c "from framework.lesson_script_wiring import wire_generator; \
                wire_generator('scripts/generate-stage1.py')"
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Regex to find a triple-quoted string assignment to a variable
# ending in _TEMPLATE
_TEMPLATE_RE = re.compile(
    r'^(?P<var>[A-Z_][A-Z0-9_]*_TEMPLATE\s*=\s*)"""(?P<body>.*?)"""',
    re.DOTALL | re.MULTILINE,
)

# Pattern to find the closing of a lesson MD: the "Practice at home" line
# is always the last content line before the closing """. We insert
# the script after that line.
_PRACTICE_LINE_RE = re.compile(
    r'(?P<line>\*Practice at home:.*?\n)(?P<rest>\s*""")',
    re.DOTALL,
)


def wire_generator(generator_path: str | Path) -> list[str]:
    """Add {teacher_script} placeholder to every *_TEMPLATE in the file.

    Returns the list of template variable names that were updated.
    Already-updated templates are skipped.
    """
    path = Path(generator_path)
    if not path.exists():
        raise FileNotFoundError(f"Generator not found: {path}")
    text = path.read_text(encoding="utf-8")
    updated: list[str] = []
    out = []

    # Scan with line-level regex
    last = 0
    new_text = []
    for m in _TEMPLATE_RE.finditer(text):
        var = m.group("var").split("=")[0].strip()
        body = m.group("body")
        # Skip if already has teacher_script placeholder
        if "{teacher_script}" in body:
            new_text.append(text[last:m.end()])
            last = m.end()
            continue
        # Insert {teacher_script} before the closing """ — after the
        # last content line of the body
        new_body = body.rstrip() + "\n\n{teacher_script}\n"
        new_text.append(text[last:m.start()])
        new_text.append(m.group("var") + '"""' + new_body + '"""')
        last = m.end()
        updated.append(var)
    new_text.append(text[last:])
    if updated:
        path.write_text("".join(new_text), encoding="utf-8")
    return updated


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m framework.lesson_script_wiring <generator.py> [...]")
        sys.exit(1)
    for g in sys.argv[1:]:
        try:
            updated = wire_generator(g)
            print(f"  {g}: updated {len(updated)} templates: {', '.join(updated)}")
        except FileNotFoundError as e:
            print(f"  {g}: ERROR {e}")
