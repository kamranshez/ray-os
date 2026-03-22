"""
Thumbnail Lab — Streamlit UI for YouTube thumbnail generation workflow.

Browse generated thumbnails, leave feedback, regenerate with comments,
and compare against competitor references.
"""

import streamlit as st
import json
import os
import subprocess
import glob
from pathlib import Path
from datetime import datetime

SKILL_DIR = Path(__file__).parent
OUTPUT_DIR = SKILL_DIR / "output"
RESEARCH_DIR = SKILL_DIR / "research" / "competitor-thumbnails"
FEEDBACK_FILE = SKILL_DIR / "feedback.json"

st.set_page_config(
    page_title="Thumbnail Lab",
    page_icon="🎨",
    layout="wide",
)

# --- Helpers ---

def load_feedback():
    if FEEDBACK_FILE.exists():
        return json.loads(FEEDBACK_FILE.read_text())
    return {}

def save_feedback(data):
    FEEDBACK_FILE.write_text(json.dumps(data, indent=2))

def get_all_thumbnails():
    """Find all generated thumbnails across batch dirs."""
    thumbnails = []
    for png in sorted(OUTPUT_DIR.rglob("*.png")):
        rel = png.relative_to(OUTPUT_DIR)
        batch = str(rel.parent)
        thumbnails.append({
            "path": str(png),
            "batch": batch,
            "name": png.name,
            "id": str(rel),
        })
    return thumbnails

def get_competitors():
    """Load competitor thumbnails."""
    comps = []
    for jpg in sorted(RESEARCH_DIR.glob("*.jpg")):
        comps.append({
            "path": str(jpg),
            "id": jpg.stem,
            "name": jpg.name,
        })
    return comps

COMPETITOR_META = {
    "Ii99RU3mOJM": {"title": "Claude can now show you", "channel": "Claude", "views": "456.1k"},
    "F4zSxfBe5R0": {"title": "Claude Code 2.0 Has Arrived", "channel": "Simon Scrapes", "views": "156.5k"},
    "EOPJwMAjUxk": {"title": "I Fed an AI My Real Codebase...", "channel": "Alex Ziskind", "views": "118.5k"},
    "4Cb_l2LJAW8": {"title": "Claude Code + Karpathy's Autoresearch", "channel": "Nick Saraev", "views": "110.8k"},
    "UhRGHr7pgnU": {"title": "My Opencode Workflow", "channel": "DevOps Toolbox", "views": "108.3k"},
    "qKU-e0x2EmE": {"title": "Stop Fixing Your Claude Skills", "channel": "Nick Saraev", "views": "97.5k"},
    "QUHrntlfPo4": {"title": "Claude Code is Expensive", "channel": "Better Stack", "views": "81.9k"},
    "japT66frdhM": {"title": "One Simple System Gave All My AI Tools a Memory", "channel": "Nate B Jones", "views": "77.9k"},
    "wQ0duoTeAAU": {"title": "Build Self-Improving Claude Code Skills", "channel": "Simon Scrapes", "views": "61.9k"},
    "ShTxTquBDxY": {"title": "Claude Code 2.0 MASSIVE Upgrade!", "channel": "WorldofAI", "views": "56.4k"},
    "vou38sa3IFY": {"title": "The NEW Claude Visualizer", "channel": "Leonardo Grigorio", "views": "55.8k"},
    "Rgb-Kx-kkaA": {"title": "Claude Code, Paperclip & AI Agent Companies", "channel": "Chase AI", "views": "36.9k"},
    "LqN_ItMqovA": {"title": "I Didn't Know This Was Possible", "channel": "AI LABS", "views": "23.3k"},
    "AURa5oPVvaE": {"title": "Anthropic's Engineers Hit the Same Wall", "channel": "Solo Swift Crafter", "views": "15.0k"},
    "nve6PtFJeo4": {"title": "Claude is taking over...", "channel": "Prompt Engineering", "views": "15.0k"},
}

# --- State ---

if "regenerating" not in st.session_state:
    st.session_state.regenerating = set()

feedback = load_feedback()

# --- Sidebar ---

with st.sidebar:
    st.title("Thumbnail Lab")
    page = st.radio("", ["Generated", "Competitors", "Regenerate"], label_visibility="collapsed")

    st.divider()
    st.caption("Quick stats")
    thumbnails = get_all_thumbnails()
    st.metric("Generated", len(thumbnails))
    st.metric("With feedback", len([t for t in thumbnails if t["id"] in feedback]))

    favorites = [t for t in thumbnails if feedback.get(t["id"], {}).get("favorite")]
    st.metric("Favorites", len(favorites))

# --- Pages ---

if page == "Generated":
    st.header("Generated Thumbnails")
    st.caption("Click a thumbnail to expand. Leave feedback to regenerate with improvements.")

    # Group by batch
    batches = {}
    for t in thumbnails:
        batches.setdefault(t["batch"], []).append(t)

    for batch_name, batch_thumbs in batches.items():
        with st.expander(f"📁 {batch_name} ({len(batch_thumbs)} thumbnails)", expanded=True):
            cols = st.columns(min(len(batch_thumbs), 3))
            for i, thumb in enumerate(batch_thumbs):
                col = cols[i % 3]
                with col:
                    st.image(thumb["path"], use_container_width=True)

                    fb = feedback.get(thumb["id"], {})

                    # Favorite toggle
                    is_fav = fb.get("favorite", False)
                    if st.checkbox("⭐ Favorite", value=is_fav, key=f"fav_{thumb['id']}"):
                        fb["favorite"] = True
                    else:
                        fb["favorite"] = False

                    # Rating
                    rating = fb.get("rating", 3)
                    new_rating = st.slider(
                        "Rating", 1, 5, rating,
                        key=f"rate_{thumb['id']}",
                        help="1 = bad, 5 = great"
                    )
                    fb["rating"] = new_rating

                    # Comment
                    comment = fb.get("comment", "")
                    new_comment = st.text_area(
                        "Feedback",
                        value=comment,
                        placeholder="e.g. 'make text bigger', 'more shocked expression', 'try yellow bg'...",
                        key=f"comment_{thumb['id']}",
                        height=80,
                    )
                    fb["comment"] = new_comment

                    # Reference selector
                    competitors = get_competitors()
                    comp_options = ["(keep current)"] + [
                        f"{c['id']} — {COMPETITOR_META.get(c['id'], {}).get('channel', '?')}"
                        for c in competitors
                    ]
                    ref_idx = st.selectbox(
                        "Style reference",
                        options=comp_options,
                        key=f"ref_{thumb['id']}",
                        help="Pick a competitor thumbnail to use as the style reference for regeneration"
                    )
                    if ref_idx != "(keep current)":
                        fb["reference"] = ref_idx.split(" — ")[0]

                    feedback[thumb["id"]] = fb

    # Save all feedback
    if st.button("💾 Save all feedback", type="primary", use_container_width=True):
        save_feedback(feedback)
        st.success("Feedback saved!")

elif page == "Competitors":
    st.header("Competitor Thumbnails")
    st.caption("Your audience's most-watched videos, ranked by views.")

    competitors = get_competitors()
    # Sort by views
    def view_sort(c):
        meta = COMPETITOR_META.get(c["id"], {})
        v = meta.get("views", "0")
        return float(v.replace("k", "").replace("M", "000"))

    competitors.sort(key=view_sort, reverse=True)

    cols = st.columns(3)
    for i, comp in enumerate(competitors):
        meta = COMPETITOR_META.get(comp["id"], {})
        col = cols[i % 3]
        with col:
            st.image(comp["path"], use_container_width=True)
            st.markdown(f"**{meta.get('title', comp['id'])}**")
            st.caption(f"{meta.get('channel', '?')} · {meta.get('views', '?')} views")

elif page == "Regenerate":
    st.header("Regenerate from Feedback")
    st.caption("Thumbnails with comments will be regenerated using your feedback as prompt guidance.")

    feedback = load_feedback()
    actionable = {k: v for k, v in feedback.items() if v.get("comment", "").strip()}

    if not actionable:
        st.info("No thumbnails have feedback comments yet. Go to 'Generated' and add comments to thumbnails you want to improve.")
    else:
        st.write(f"**{len(actionable)} thumbnail(s)** have feedback ready for regeneration:")

        for thumb_id, fb in actionable.items():
            thumb_path = OUTPUT_DIR / thumb_id
            col1, col2 = st.columns([1, 2])
            with col1:
                if thumb_path.exists():
                    st.image(str(thumb_path), use_container_width=True)
                else:
                    st.warning(f"Image not found: {thumb_id}")
            with col2:
                st.markdown(f"**{thumb_id}**")
                st.write(f"Rating: {'⭐' * fb.get('rating', 3)}")
                st.write(f"Feedback: _{fb['comment']}_")
                if fb.get("reference"):
                    st.write(f"Reference: `{fb['reference']}`")
                st.write(f"Favorite: {'Yes' if fb.get('favorite') else 'No'}")

        st.divider()

        # Build regeneration commands
        st.subheader("Regeneration Commands")
        st.caption("Copy these commands to run in Claude Code, or click 'Generate instructions.md' to save them.")

        instructions = []
        for thumb_id, fb in actionable.items():
            ref = fb.get("reference", "")
            ref_path = f"-r research/competitor-thumbnails/{ref}.jpg" if ref else ""
            out_dir = f"output/regen-{datetime.now().strftime('%Y%m%d-%H%M')}"

            instruction = {
                "original": thumb_id,
                "feedback": fb["comment"],
                "reference": ref,
                "output_dir": out_dir,
            }
            instructions.append(instruction)

            st.code(
                f"# Regenerate {thumb_id}\n"
                f"# Feedback: {fb['comment']}\n"
                f"npx ts-node scripts/generate.ts \"<incorporate feedback: {fb['comment']}>\" "
                f"-n 3 -o {out_dir} {ref_path}",
                language="bash"
            )

        if st.button("📝 Save as instructions.md", use_container_width=True):
            md = "# Regeneration Instructions\n\n"
            md += f"Generated: {datetime.now().isoformat()}\n\n"
            for inst in instructions:
                md += f"## {inst['original']}\n"
                md += f"- **Feedback**: {inst['feedback']}\n"
                md += f"- **Reference**: {inst['reference'] or '(none)'}\n"
                md += f"- **Output**: {inst['output_dir']}\n\n"

            inst_path = SKILL_DIR / "instructions.md"
            inst_path.write_text(md)
            st.success(f"Saved to {inst_path}")

# Auto-save feedback on any interaction
save_feedback(feedback)
