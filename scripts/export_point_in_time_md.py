#!/usr/bin/env python3
"""
Export system prompt JSON configs to a point-in-time Markdown snapshot and archive it as a numbered release.

Reads all JSON files from system-prompts/json and writes a timestamped
directory under exports/, generating one Markdown file per config following the
general markdown model-card template used in this repo.

Usage:
  python3 scripts/export_point_in_time_md.py
  python3 scripts/export_point_in_time_md.py --out-dir exports/20250101-120000
  python3 scripts/export_point_in_time_md.py --archive-format zip

Notes:
- Handles both JSON schemas observed in this repo (lowercase-with-hyphens and
  Title Case with spaces) by normalizing keys.
- Missing values are rendered as "Not provided".
 - Produces an archive (tar.gz by default) and assigns an auto-incremented
   release number stored in exports/releases.json.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
import tarfile
import zipfile
from pathlib import Path
from typing import Any, Dict, Optional


REPO_ROOT = Path(__file__).resolve().parents[1]
JSON_DIR = REPO_ROOT / "system-prompts" / "json"
EXPORTS_DIR = REPO_ROOT / "exports"
RELEASES_INDEX = EXPORTS_DIR / "releases.json"


def as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        v = value.strip().lower()
        return v in {"true", "yes", "y", "1", "✅"}
    return False


def normalize_keys(d: Dict[str, Any]) -> Dict[str, Any]:
    """Return a dict with additional normalized keys for easy lookup.

    We keep original keys and also add lowercased, hyphenated variants so that
    fields can be accessed across different JSON forks.
    """
    out = dict(d)
    for k, v in list(d.items()):
        norm = k.strip().lower()
        norm = norm.replace(" ", "-")
        out.setdefault(norm, v)
    return out


def get_first(d: Dict[str, Any], *keys: str, default: Optional[str] = None) -> Any:
    for k in keys:
        if k in d and d[k] not in (None, ""):
            return d[k]
    return default


def md_escape(text: str) -> str:
    if text is None:
        return ""
    # Keep formatting simple; preserve markdown where present.
    return text


def bool_emoji(val: Any) -> str:
    return "✅" if as_bool(val) else "❌"


def to_slug(name: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9\-\s_]", "", name or "")
    slug = slug.strip().lower().replace(" ", "-")
    slug = slug.replace("_", "-")
    slug = re.sub(r"-+", "-", slug)
    return slug or "unnamed"


def render_markdown(data: Dict[str, Any], json_filename: str) -> str:
    d = normalize_keys(data)

    agent_name = get_first(d, "agent_name", "agentname", default="Unnamed Agent")
    one_line = get_first(d, "one-line-summary", "one-line", "one-line-summary", default="Not provided")
    created = get_first(d, "creation-date", "creation_date", default="Not provided")
    description = get_first(d, "description", "Description", default=None)
    system_prompt = get_first(d, "systemprompt", "system-prompt", default="Not provided")
    chatgpt_url = get_first(d, "chatgptlink", "chatgpt-access-url", default=None)
    n8n_link = get_first(d, "n8n-link", default=None)

    # Capability booleans (aggregated across schemas)
    caps = {
        "Single turn": get_first(d, "is-single-turn", "single-turn-(workflow-type)", default=False),
        "Structured output": get_first(d, "structured-output-generation", "structured-output-(workflow-type)", default=False),
        "Image generation": get_first(d, "image-generation", "image-generation-(workflow-type)", default=False),
        "External tooling required": get_first(d, "external-tooling-(required)", default=False),
        "RAG required": get_first(d, "rag-(required)", default=False),
        "Vision required": get_first(d, "vision-(req)", default=False),
        "Speech-to-speech": get_first(d, "spech-to-speech", "speech-to-speech", default=False),
        "Video input required": get_first(d, "video-input-(required)", default=False),
        "Audio required": get_first(d, "audio-(required)", default=False),
        "TTS required": get_first(d, "tts-(required)", default=False),
        "File input required": get_first(d, "file-input-(req)", default=False),
        "Test entry": get_first(d, "test-entry", default=False),
        "Better as tool": get_first(d, "better-as-tool", default=False),
        "Is agent": get_first(d, "is-agent", "is-agent?", default=False),
        "Local LLM friendly": get_first(d, "local-llm-friendly?", default=False),
        "Deep research": get_first(d, "deep-research", default=False),
        "Update/iteration expected": get_first(d, "update/iteration", "update-iteration", default=False),
    }

    # Interaction style booleans
    interaction = {
        "Character (type)": get_first(d, "character-(type)", default=False),
        "Roleplay (behavior)": get_first(d, "roleplay-(behavior)", default=False),
        "Voice-first": get_first(d, "voice-first", default=False),
        "Writing assistant": get_first(d, "writing-assistant", default=False),
        "Data utility (category)": get_first(d, "data-utility-(category)", "data-utility", default=False),
        "Conversational": get_first(d, "conversational", default=False),
        "Instructional": get_first(d, "instructional", default=False),
        "Autonomous": get_first(d, "autonomous", default=False),
    }

    # Notes/secondary fields
    use_case = get_first(d, "use-case-outline", default=None)
    iter_notes = get_first(d, "iteration-notes", default=None)
    pii_notes = get_first(d, "pii-notes", default=None)
    cost_est = get_first(d, "cost-estimates", default=None)
    loc_notes = get_first(d, "localtisation-notes", "localisation-notes", default=None)
    guardrails = get_first(d, "guardrails-notes", default=None)
    mcp_used = get_first(d, "mcps-used", default=None)
    api_notes = get_first(d, "api-notes", default=None)
    mcp_notes = get_first(d, "mcp-notes", default=None)
    local_llm_notes = get_first(d, "local-llm-notes", default=None)
    llm_selection_notes = get_first(d, "llm-selection-notes", default=None)

    # Build Markdown
    lines = []
    lines.append(f"# {agent_name}")
    lines.append("")
    if system_prompt and system_prompt != "Not provided":
        lines.append(md_escape(system_prompt))
        lines.append("")
    lines.append("---")
    lines.append("")

    # Identity
    lines.append("## 🏷️ Identity")
    lines.append("")
    lines.append(f"- **Agent Name:** {agent_name}  ")
    lines.append(f"- **One-line Summary:** {one_line or 'Not provided'}  ")
    lines.append(f"- **Creation Date (ISO8601):** {created or 'Not provided'}  ")
    if description:
        lines.append("- **Description:**  ")
        lines.append(f"  {md_escape(description)}")
    else:
        lines.append("- **Description:** Not provided")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Access & Links
    lines.append("## 🔗 Access & Links")
    lines.append("")
    if chatgpt_url:
        lines.append(f"- **ChatGPT Access URL:** [View on ChatGPT]({chatgpt_url})  ")
    else:
        lines.append("- **ChatGPT Access URL:** Not provided  ")
    lines.append(f"- **n8n Link:** {('*Not provided*' if not n8n_link else n8n_link)}  ")
    # Keep repo-relative link like other docs
    lines.append(f"- **GitHub JSON Source:** [system-prompts/json/{json_filename}](system-prompts/json/{json_filename})")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Capabilities table
    lines.append("## 🛠️ Capabilities")
    lines.append("")
    lines.append("| Capability | Status |")
    lines.append("|-----------|--------|")
    for label, val in caps.items():
        lines.append(f"| {label} | {bool_emoji(val)} |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Interaction style
    lines.append("## 🧠 Interaction Style")
    lines.append("")
    lines.append("- **System Prompt:** (See above)")
    for label, val in interaction.items():
        lines.append(f"- **{label}:** {'✅' if as_bool(val) else '❌'}  ")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Use case outline
    lines.append("## 📊 Use Case Outline")
    lines.append("")
    lines.append(md_escape(use_case) if use_case else "Not provided")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Product thinking & iteration
    lines.append("## 📥 Product Thinking & Iteration Notes")
    lines.append("")
    lines.append(f"- **Iteration notes:** {md_escape(iter_notes) if iter_notes else 'Not provided'}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Governance & Ops
    lines.append("## 🛡️ Governance & Ops")
    lines.append("")
    lines.append(f"- **PII Notes:** {md_escape(pii_notes) if pii_notes else 'Not provided'}")
    lines.append(f"- **Cost Estimates:** {md_escape(cost_est) if cost_est else 'Not provided'}")
    lines.append(f"- **Localisation Notes:** {md_escape(loc_notes) if loc_notes else 'Not provided'}")
    lines.append(f"- **Guardrails Notes:** {md_escape(guardrails) if guardrails else 'Not provided'}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Model selection & local notes
    lines.append("## 📦 Model Selection & Local Notes")
    lines.append("")
    lines.append(f"- **Local LLM notes:** {md_escape(local_llm_notes) if local_llm_notes else 'Not provided'}")
    lines.append(f"- **LLM selection notes:** {md_escape(llm_selection_notes) if llm_selection_notes else 'Not provided'}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Tooling & MCP
    lines.append("## 🔌 Tooling & MCP")
    lines.append("")
    lines.append(f"- **MCPs used:** {md_escape(mcp_used) if mcp_used else '*None specified*'}  ")
    lines.append(f"- **API notes:** {md_escape(api_notes) if api_notes else '*Not applicable*'}  ")
    lines.append(f"- **MCP notes:** {md_escape(mcp_notes) if mcp_notes else '*Not applicable*'}")
    lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Export point-in-time Markdown snapshot from JSON configs and package as a release")
    parser.add_argument("--out-dir", type=str, help="Output directory under exports/ (optional)")
    parser.add_argument(
        "--archive-format",
        type=str,
        choices=["tar.gz", "zip"],
        default="tar.gz",
        help="Archive format for the release (default: tar.gz)",
    )
    parser.add_argument(
        "--release-number",
        type=int,
        default=None,
        help="Override auto-incremented release number (advanced)",
    )
    args = parser.parse_args()

    if not JSON_DIR.exists():
        print(f"ERROR: JSON directory not found: {JSON_DIR}")
        return 1

    if args.out_dir:
        out_dir = Path(args.out_dir)
        if not out_dir.is_absolute():
            out_dir = EXPORTS_DIR / out_dir
    else:
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        out_dir = EXPORTS_DIR / ts

    out_dir.mkdir(parents=True, exist_ok=True)

    json_files = sorted(JSON_DIR.glob("*.json"))
    if not json_files:
        print("No JSON files found to export.")
        return 0

    count = 0
    for jf in json_files:
        try:
            with open(jf, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"WARN: Skipping {jf.name}: {e}")
            continue

        # Determine filename
        d = normalize_keys(data)
        name = get_first(d, "agent_name", "agentname", default=None)
        if isinstance(name, str) and name.strip():
            base = to_slug(name)
        else:
            base = jf.stem
        md_path = out_dir / f"{base}.md"

        content = render_markdown(data, jf.name)
        try:
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(content)
            count += 1
        except Exception as e:
            print(f"ERROR: Failed writing {md_path.name}: {e}")
            continue

    # Determine release number
    releases = {"releases": []}
    if RELEASES_INDEX.exists():
        try:
            with open(RELEASES_INDEX, "r", encoding="utf-8") as f:
                releases = json.load(f) or {"releases": []}
        except Exception:
            releases = {"releases": []}

    existing_numbers = [r.get("number", 0) for r in releases.get("releases", [])]
    next_number = (max(existing_numbers) if existing_numbers else 0) + 1
    if args.release_number is not None:
        next_number = int(args.release_number)

    # Create archive
    timestamp = out_dir.name
    base_name = f"release-{next_number}_{timestamp}"
    archive_path: Path
    if args.archive_format == "tar.gz":
        archive_path = EXPORTS_DIR / f"{base_name}.tar.gz"
        # Avoid overwrite: append suffix if exists
        suffix = 1
        while archive_path.exists():
            archive_path = EXPORTS_DIR / f"{base_name}({suffix}).tar.gz"
            suffix += 1
        with tarfile.open(archive_path, "w:gz") as tar:
            tar.add(out_dir, arcname=timestamp)
    else:
        archive_path = EXPORTS_DIR / f"{base_name}.zip"
        suffix = 1
        while archive_path.exists():
            archive_path = EXPORTS_DIR / f"{base_name}({suffix}).zip"
            suffix += 1
        with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for p in out_dir.rglob("*"):
                if p.is_file():
                    zf.write(p, arcname=str(Path(timestamp) / p.relative_to(out_dir)))

    # Write release marker inside the folder
    try:
        with open(out_dir / "RELEASE.txt", "w", encoding="utf-8") as f:
            f.write(
                f"Release: {next_number}\n"
                f"Timestamp: {timestamp}\n"
                f"Files: {count}\n"
                f"Archive: {archive_path.name}\n"
                f"Format: {args.archive_format}\n"
            )
    except Exception:
        pass

    # Update releases index
    entry = {
        "number": next_number,
        "timestamp": timestamp,
        "dir": str(out_dir.relative_to(REPO_ROOT)),
        "count": count,
        "archive": str(archive_path.relative_to(REPO_ROOT)),
        "format": args.archive_format,
        "created_at": datetime.now().isoformat(),
    }
    releases.setdefault("releases", []).append(entry)
    RELEASES_INDEX.parent.mkdir(parents=True, exist_ok=True)
    with open(RELEASES_INDEX, "w", encoding="utf-8") as f:
        json.dump(releases, f, indent=2)

    print(
        f"Exported {count} markdown files to {out_dir.relative_to(REPO_ROOT)} | "
        f"Release #{next_number} -> {archive_path.relative_to(REPO_ROOT)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
