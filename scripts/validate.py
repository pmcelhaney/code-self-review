"""Check this small, plain-scalar skill package without external dependencies."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/prepare-code-self-review/SKILL.md"
text = SKILL.read_text()
assert text.startswith("---\n"), "Missing YAML frontmatter"
front, body = text[4:].split("\n---\n", 1)
fields = dict(line.split(": ", 1) for line in front.splitlines())
assert set(fields) == {"name", "description"}, "Unexpected frontmatter"
name = fields["name"]
assert re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name)
assert len(name) <= 64 and name == SKILL.parent.name
assert 1 <= len(fields["description"]) <= 1024
assert len(text.splitlines()) < 500
for safeguard in (
    "grants no blanket permission", "share private information",
    "comment-only review", "Never approve your own PR",
    "Read existing self-review comments first", "Read back the published review",
    "If only preparation or drafting is authorized", "exact current path",
    "Distinguish passed, failed, and not run",
):
    assert safeguard in body, f"Missing safeguard: {safeguard}"

for doc in ROOT.rglob("*.md"):
    if ".git" in doc.parts:
        continue
    for link in re.findall(r"\]\(([^)]+)\)", doc.read_text()):
        if "://" not in link and not link.startswith("#"):
            target = (doc.parent / link.split("#", 1)[0]).resolve()
            assert target.is_relative_to(ROOT) and target.exists(), (doc, link)

example = (ROOT / "examples/review.md").read_text()
patch = example.split("```diff\n", 1)[1].split("```", 1)[0]
old, new = [], []
for line in patch.splitlines():
    if line.startswith(("diff ", "---", "+++", "@@")):
        continue
    if line.startswith((" ", "-")):
        old.append(line[1:])
    if line.startswith((" ", "+")):
        new.append(line[1:])
assert len(old) == 3 and len(new) == 12, "Incorrect diff hunk counts"
assert "method ===" in new[2] and "response.status" in new[6]
assert "src/catalog.ts:3" in example and "src/catalog.ts:7" in example
assert "fictional" in example and "Not run" in example
assert "skills@1.7.4 add pmcelhaney/code-self-review --skill prepare-code-self-review" in (ROOT / "README.md").read_text()
assert (ROOT / "LICENSE").read_text().startswith("MIT License\n")
print("PASS: frontmatter, layout, local links, example anchors, permission safeguards")
