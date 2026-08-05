"""Inject teacher_script keyword into every TEMPLATE.format() call in a generator.

For each call to *_TEMPLATE.format(...) in a generator, appends
    teacher_script=format_phonogram_script(pg, sounds)  (or appropriate)
based on the template variable name.

This is a heuristic — the assistant may pick a wrong script function
for unusual builders. But the script function names map cleanly to
template names:
  *_PHONOGRAM_TEMPLATE*       -> format_phonogram_script(pg, sounds)
  *_RULE_TEMPLATE*            -> format_rule_script(num, name, statement)
  *_SPELLING_ANALYSIS_TEMPLATE* -> format_spelling_script(word, sentence)
  others                      -> no script (templates don't have {teacher_script})

Run after framework.lesson_script_wiring.wire_generator(). Then manually
edit any complex builders the heuristic missed.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

_FORMAT_CALL_RE = re.compile(
    r'(?P<name>[A-Z_][A-Z0-9_]*_TEMPLATE)\.format\(\s*\n'
    r'(?P<args>(?:[ \t]*(?:\w+\s*=\s*[^,\n]+|[\w\.\"\'\(\) ]+),?\s*\n)+)'
    r'\s*\)',
    re.MULTILINE,
)


def _pick_script_fn(template_var: str) -> str | None:
    """Return the helper function name + kwargs to use for this template."""
    if "PHONOGRAM_INTRO" in template_var or "MULTI_PG" in template_var:
        return "format_phonogram_script(pg=pg, sounds=sounds)"
    if "RULE" in template_var and "RULE_TEMPLATE" in template_var:
        return "format_rule_script(num=rule_num, name=rule_name, statement=rule_statement)"
    if "SPELLING_ANALYSIS" in template_var:
        return "format_spelling_script(word=word, sentence=sentence)"
    return None


def inject(generator_path: str | Path) -> list[str]:
    """Add teacher_script=... to each *.format() call. Returns templates updated."""
    path = Path(generator_path)
    if not path.exists():
        raise FileNotFoundError(path)
    text = path.read_text(encoding="utf-8")
    updated = []
    out = []
    last = 0

    # Find every TEMPLATE.format(...) call
    pattern = re.compile(
        r'(?P<call>[A-Z_][A-Z0-9_]*_TEMPLATE\.format\()'
        r'(?P<args>.*?)'
        r'(?P<close>\))',
        re.DOTALL,
    )
    new_text = []
    pos = 0
    for m in pattern.finditer(text):
        var_name = m.group("call").split(".")[0]
        script_fn = _pick_script_fn(var_name)
        if not script_fn:
            continue
        # Find the matching close paren (use balanced match in the args)
        args_text = m.group("args")
        close_idx = m.end()
        if "teacher_script" in args_text:
            continue  # already injected
        # Insert teacher_script=... as the last kwarg before the close paren.
        # Strip trailing whitespace+comma from args
        args_stripped = args_text.rstrip().rstrip(",").rstrip()
        new_args = args_stripped + f",\n        teacher_script={script_fn},\n    "
        new_text.append(text[pos:m.start()])
        new_text.append(m.group("call") + new_args + ")")
        pos = close_idx
        updated.append(var_name)
    new_text.append(text[pos:])
    if updated:
        path.write_text("".join(new_text), encoding="utf-8")
    return updated


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m framework.inject_teacher_script <generator.py> [...]")
        sys.exit(1)
    for g in sys.argv[1:]:
        try:
            updated = inject(g)
            print(f"  {g}: injected {len(updated)}: {', '.join(updated)}")
        except FileNotFoundError as e:
            print(f"  {g}: ERROR {e}")
