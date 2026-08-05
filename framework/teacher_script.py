"""Teacher script injection for lesson files (issue #4).

The framework/templates/teacher-script-*.md files contain scripted
teacher dialogue (say-this, do-that). This module loads them and provides
formatters that wrap the rendered script in a collapsible <details>
block — teachers can skip it if they prefer the plan-only view.

Public API:
    format_phonogram_script(pg, sounds)        -> str (HTML block)
    format_rule_script(num, name, statement)   -> str (HTML block)
    format_spelling_script(word, sentence)     -> str (HTML block)

Each formatter returns a Markdown-fenced <details> block that:
  - Has a visible summary "📖 Teacher Script (click to expand)"
  - Contains the formatted script from the template
  - Sits at the END of the lesson, after all other content
"""

import re
from pathlib import Path

TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"


def _read_template(name: str) -> str:
    """Read a teacher script template from framework/templates/."""
    path = TEMPLATES_DIR / f"teacher-script-{name}.md"
    return path.read_text(encoding="utf-8")


def _strip_frontmatter(text: str) -> str:
    """Drop the leading '## Teacher Script' heading if present.

    The templates have a redundant H2 heading at the top. When we embed
    them inside a <details> block the heading is replaced by <summary>,
    so we drop the H2 to avoid duplication.
    """
    lines = text.splitlines()
    if lines and lines[0].lstrip().startswith("## "):
        lines = lines[1:]
    return "\n".join(lines).strip()


def _wrap_collapsible(body: str, label: str) -> str:
    """Wrap a Markdown block in a collapsible <details> element.

    The CSS in framework/assets/main.css renders <details><summary>
    as a clickable card. Inside, the original Markdown is preserved so
    pdftotext + WeasyPrint can render it.
    """
    summary = f"📖 {label} (click to expand)"
    return (
        f'\n<details class="teacher-script">\n'
        f'<summary>{summary}</summary>\n\n'
        f'{body}\n\n'
        f'</details>\n'
    )


def format_phonogram_script(pg: str, sounds: str, rule_script: str = "") -> str:
    """Render the phonogram teacher script for a phonogram introduction.

    Args:
        pg:          The phonogram (e.g. 'sh', 'a', 'ough')
        sounds:      Its sounds in IPA notation (e.g. '/sh/')
        rule_script: Optional pre-rendered rule script to insert (the
                     template has a {rule_script} placeholder for this).

    Returns:
        HTML <details> block with the formatted script.
    """
    template = _read_template("phonogram")
    body = _strip_frontmatter(template)
    body = body.format(pg=pg, sounds=sounds, rule_script=rule_script)
    return _wrap_collapsible(body, f"Phonogram {pg} — Teacher Script")


def format_rule_script(num: str, name: str, statement: str | None = None) -> str:
    """Render the rule teacher script for a rule introduction.

    Args:
        num:       Rule number (e.g. '1', '12', '31')
        name:      Rule name (e.g. 'C softens to /s/ before E, I, Y')
        statement: Optional restatement; falls back to name if None.

    Returns:
        HTML <details> block.
    """
    template = _read_template("rule")
    body = _strip_frontmatter(template)
    if statement is None:
        statement = name
    body = body.format(num=num, name=name, statement=statement)
    return _wrap_collapsible(body, f"Rule {num} — Teacher Script")


def format_spelling_script(word: str, sentence: str) -> str:
    """Render the Spelling Analysis teacher script for one word.

    Args:
        word:    The spelling-analysis word (e.g. 'cent')
        sentence: A sentence using the word (e.g. 'A cent is a coin.')

    Returns:
        HTML <details> block.
    """
    template = _read_template("spelling")
    body = _strip_frontmatter(template)
    body = body.format(word=word, sentence=sentence)
    return _wrap_collapsible(body, f"Spelling '{word}' — Teacher Script")
