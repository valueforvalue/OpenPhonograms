"""Per-page Spelling Aid sidebar for decodable readers (issues #20, #22).

Each page of a reader's story is wrapped in:

  <div class="reader-page">
    <div class="reader-text">…</div>
    <div class="reader-sidebar">…</div>
  </div>

The sidebar lists phonograms (with example words from the story) and
rules (with the rule name) that appear on that page. Format mirrors
the existing 001-fred-the-frog reference.
"""
import re
import sys
from pathlib import Path

# Allow standalone import during generator development
sys.path.insert(0, str(Path(__file__).resolve().parent))
from phonograms import PG_STAGE  # noqa: E402
from rules import RULES, words_using_phonogram, rules_for_words  # noqa: E402


# Words that should NOT be detected as rule examples (function words etc.)
_STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "must", "shall", "can", "to", "of", "in",
    "for", "on", "with", "at", "by", "from", "as", "into", "through",
    "and", "or", "but", "if", "then", "than", "so", "that", "this",
    "these", "those", "i", "you", "he", "she", "it", "we", "they",
    "me", "him", "her", "us", "them", "my", "your", "his", "its",
    "our", "their", "what", "which", "who", "whom", "whose", "where",
    "when", "why", "how", "no", "not", "yes",
}


def _page_words(text: str) -> list[str]:
    """Extract lowercase words from text, drop stopwords."""
    words = re.findall(r"[a-zA-Z']+", text)
    return [w.lower() for w in words if w.lower() not in _STOPWORDS]


def _phonograms_in_text(text: str) -> list[str]:
    """Return phonograms that appear in text, ordered by teaching sequence (PG_STAGE then alpha).

    Uses a simple substring check: a word contains a phonogram if the
    phonogram substring appears anywhere in the word. This is
    deliberately a heuristic (some words have multiple PGs); we
    return all matches sorted by stage/alpha for consistent output.
    """
    words = _page_words(text)
    word_set = set(words)
    found = set()
    for word in word_set:
        for pg in PG_STAGE.keys():
            if pg in word:
                found.add(pg)
    # Sort by stage, then alphabetically
    return sorted(found, key=lambda p: (PG_STAGE[p], p))


def build_sidebar(text: str, new_phonogram: str | None = None) -> str:
    """Build a Spelling Aid sidebar for a page of reader text.

    Args:
        text: The story text for this page.
        new_phonogram: Optional phonogram highlighted as the lesson's
            new teaching focus (appears in bold at top of sidebar).

    Returns:
        HTML string for the <div class="reader-sidebar">…</div> block.
    """
    # Find phonograms and rules used on this page
    pgs = _phonograms_in_text(text)
    rules = rules_for_words(_page_words(text))

    lines = ['<div class="reader-sidebar">', '', '### Spelling Aid', '']

    # Highlight new phonogram if specified
    if new_phonogram and new_phonogram in pgs:
        lines.append(f"**New:** {new_phonogram}")
        lines.append("")
        # Show 2-3 example words from the page
        examples = words_using_phonogram(new_phonogram, _page_words(text))
        if examples:
            lines.append(f"**Sounds:** {', '.join(examples)}")
            lines.append("")
        # Move new PG to front of list
        pgs = [new_phonogram] + [p for p in pgs if p != new_phonogram]

    # Other phonograms on the page
    other_pgs = [p for p in pgs if p != new_phonogram]
    if other_pgs:
        # Show up to 5 others
        display = other_pgs[:5]
        lines.append(f"**Phonograms on this page:** {', '.join(display)}")
        lines.append("")

    # Rules used on this page
    if rules:
        lines.append("**Rules in this story:**")
        lines.append("")
        for num in rules[:3]:  # Limit to 3 rules for compact display
            lines.append(f"**Rule {num}:** {RULES[num]['name']}")
            lines.append("")

    lines.append('</div>')
    return "\n".join(lines)


def split_into_pages(text: str, sentences_per_page: int = 3) -> list[str]:
    """Split story text into pages of ~N sentences each.

    Used by the reader generator to break a flat story into per-page
    blocks, each of which gets its own Spelling Aid sidebar.
    """
    # Split on sentence-end punctuation followed by space/newline
    # but preserve abbreviations like "Mr." and "e.g."
    # Simple approach: split on '. ' or '! ' or '? ' boundaries
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    pages = []
    for i in range(0, len(sentences), sentences_per_page):
        page = " ".join(sentences[i:i + sentences_per_page]).strip()
        if page:
            pages.append(page)
    return pages
