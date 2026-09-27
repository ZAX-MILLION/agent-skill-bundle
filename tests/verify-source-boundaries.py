#!/usr/bin/env python3
"""Offline supply-chain and strict-discovery boundaries for the reviewed bundle.

No network, installation, subprocess invocation, credential access, or host changes.
"""
import json
import pathlib
import sys

repo = pathlib.Path(__file__).resolve().parents[1]
categories = (
    "design", "security", "process", "multiplayer", "wordpress",
    "marketing", "qa", "operations", "coding", "research",
    "productivity", "automation", "creative",
)
skills = sorted(
    p for category in categories
    for p in (repo / category).glob("*/SKILL.md")
)
assert len(skills) == 174, f"reviewed baseline changed: {len(skills)} != 174"
names = [p.parent.name for p in skills]
assert len(names) == len(set(names)), "duplicate native skill names across categories"

# The two deliberately exposed native descriptions are the entire bootstrap.
bootstrap = {"i-have-adhd", "skill-retrieval-routing"}
assert bootstrap <= set(names)
assert len(bootstrap) == 2 and len(skills) - len(bootstrap) == 172

third = json.loads((repo / "registry/vendor-third-wave.json").read_text())
ecc = json.loads((repo / "registry/vendor-ecc.json").read_text())
externals = json.loads((repo / "registry/external-capabilities.json").read_text())
by_repo = {e["source"]: e for e in third["source_revisions"]}
assert len(by_repo) == 7
assert len(third["pinned_git_blob_sha"]) == 100

official = sorted((repo / "automation").glob("n8n-*-official/SKILL.md"))
official += list((repo / "automation").glob("using-n8n-skills-official/SKILL.md"))
assert len(official) == 14, f"expected all 14 official n8n skills, got {len(official)}"
for entry in official:
    assert (entry.parent / "LICENSE.txt").is_file(), entry
assert by_repo["n8n-io/skills"]["license"] == "Apache-2.0"
assert not by_repo["n8n-io/skills"]["runtime_bundled"]

superpowers = {
    "brainstorming", "diagnosing-superpowers", "dispatching-parallel-agents",
    "executing-plans", "finishing-a-development-branch", "receiving-code-review",
    "requesting-code-review", "subagent-driven-development", "systematic-debugging",
    "test-driven-development", "using-git-worktrees", "using-superpowers",
    "verification-before-completion", "writing-plans", "writing-skills",
}
assert all((repo / "process" / name / "SKILL.md").is_file() for name in superpowers)
assert (repo / "process/diagnosing-superpowers/LICENSE.txt").is_file()
assert by_repo["obra/superpowers"]["license"] == "MIT"

assert ecc["source"] == "affaan-m/ECC" and ecc["upstream_license"] == "MIT"
assert len(ecc["skill_pins"]) == 8
for local in ecc["skill_pins"]:
    path = repo / local
    assert path.is_file() and (path.parent / "LICENSE.txt").is_file(), local

# The bundle-authored adapters are guides, not partial upstream runtime copies.
routers = (
    "process/paul", "automation/n8n-instance",
    "creative/openmontage", "creative/shuohao-skills",
)
for relative in routers:
    directory = repo / relative
    assert sorted(p.name for p in directory.iterdir()) == ["SKILL.md"], relative
    assert "Original" in (directory / "SKILL.md").read_text(), relative

external = {e["repository"]: e for e in externals["external_sources"]}
for name in (
    "ChristopherKahler/paul", "calesthio/OpenMontage",
    "eternityspring/shuohao-skills", "pixel-agents-hq/pixel-agents",
    "czlonkowski/n8n-mcp", "affaan-m/ECC",
):
    entry = external[name]
    assert entry["installation_in_bundle"] is False, name
    assert entry["credentials_in_bundle"] is False, name
assert external["eternityspring/shuohao-skills"]["skills_copied"] == 0
assert external["affaan-m/ECC"]["selected_portable_skill_bodies"] == 8
assert external["n8n-io/skills"]["access_granted"] is False

# The installer only permits the two roots when --flat --on-demand is selected.
installer = (repo / "install.sh").read_text()
assert "productivity/i-have-adhd|research/skill-retrieval-routing" in installer
assert 'if [ "$ON_DEMAND" -eq 1 ] && [ "$count" -ne 2 ]' in installer
assert '--prune-managed' in installer
print(
    "PASS: 174 unique skills, 2 native bootstraps, 14 official n8n, "
    "15 Superpowers, 8 selected ECC, 4 local guides, "
    "7 source pins, and external runtime/credential boundaries"
)
