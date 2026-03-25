"""
Thumbnail Backfill Lab — Streamlit app for managing bulk thumbnail A/B tests.

Tracks generation status, shortlisting, uploads, and results across all videos.
All state persisted in data.json.
"""

import streamlit as st
import json
from pathlib import Path
from datetime import datetime, timedelta

APP_DIR = Path(__file__).resolve().parent
DATA_FILE = APP_DIR / "data.json"
OUTPUT_DIR = (APP_DIR.parent / "output").resolve()

st.set_page_config(
    page_title="Thumbnail Backfill Lab",
    page_icon="🧪",
    layout="wide",
)

# --- Data ---

def load_data():
    return json.loads(DATA_FILE.read_text())

def save_data(data):
    DATA_FILE.write_text(json.dumps(data, indent=2))

def get_thumbnails(video_id):
    """Get all thumbnails for a video."""
    video_dir = OUTPUT_DIR / video_id
    if not video_dir.exists():
        return []
    return sorted([p.name for p in video_dir.glob("*.png")])

def status_emoji(status):
    return {
        "not_generated": "⬜",
        "generated": "🟡",
        "shortlisted": "🟢",
        "uploaded": "🔵",
        "results_in": "✅",
    }.get(status, "❓")

def status_label(status):
    return {
        "not_generated": "Not Generated",
        "generated": "Generated",
        "shortlisted": "Shortlisted",
        "uploaded": "Uploaded",
        "results_in": "Results In",
    }.get(status, status)

# --- Sidebar ---

data = load_data()
videos = data["videos"]
config = data["config"]

with st.sidebar:
    st.title("Backfill Lab")
    page = st.radio("", ["Dashboard", "Review", "Results"], label_visibility="collapsed")

    st.divider()

    # Stats
    total = len(videos)
    generated = sum(1 for v in videos.values() if v["status"] != "not_generated")
    shortlisted = sum(1 for v in videos.values() if v["status"] in ("shortlisted", "uploaded", "results_in"))
    uploaded = sum(1 for v in videos.values() if v["status"] in ("uploaded", "results_in") and v.get("uploaded_thumbs"))
    results_done = sum(1 for v in videos.values() if v["status"] == "results_in")

    st.caption("Progress")
    st.progress(generated / total if total else 0)
    st.markdown(f"**{generated}**/{total} generated")
    st.markdown(f"**{shortlisted}**/{total} shortlisted")
    st.markdown(f"**{uploaded}**/{total} uploaded")
    st.markdown(f"**{results_done}**/{total} results in")

# --- Dashboard ---

if page == "Dashboard":
    st.header("Thumbnail Backfill Dashboard")
    st.caption(f"{total} videos · {config['variants_per_video']} variants x {config['images_per_variant']} each = {config['variants_per_video'] * config['images_per_variant']} thumbnails per video")

    # Sort by views descending
    sorted_videos = sorted(videos.items(), key=lambda x: x[1]["views"], reverse=True)

    # Status filter
    filter_status = st.selectbox("Filter by status", ["All", "Not Generated", "Generated", "Shortlisted", "Uploaded", "Results In"])

    cols = st.columns(3)
    for i, (vid, info) in enumerate(sorted_videos):
        if filter_status != "All" and status_label(info["status"]) != filter_status:
            continue

        col = cols[i % 3]
        with col:
            emoji = status_emoji(info["status"])
            shortlist_count = len(info.get("shortlisted", []))
            upload_count = len(info.get("uploaded_thumbs", []))

            # Due date line for uploaded videos
            due_line = ""
            if info["status"] == "uploaded" and info.get("results_due"):
                try:
                    days_left = (datetime.strptime(info["results_due"], "%Y-%m-%d") - datetime.now()).days
                    due_color = "#ef4444" if days_left <= 0 else "#eab308" if days_left <= 2 else "#888"
                    due_text = "DUE NOW" if days_left <= 0 else f"{days_left}d left"
                    due_line = f'<div style="font-size:0.7rem;color:{due_color};margin-top:2px;">⏰ Check results: {due_text}</div>'
                except ValueError:
                    pass

            st.markdown(f"""
            <div style="background:#1a1a2e;border-radius:12px;padding:16px;margin-bottom:12px;border-left:4px solid {'#e8590c' if info['status'] == 'not_generated' else '#22c55e' if info['status'] in ('shortlisted','uploaded','results_in') else '#eab308'};">
                <div style="font-size:0.75rem;color:#888;">{info['video_number']} · {info['views']:,} views</div>
                <div style="font-size:0.95rem;font-weight:600;margin:4px 0;">{info['title'][:50]}{'...' if len(info['title']) > 50 else ''}</div>
                <div style="font-size:0.8rem;color:#aaa;">{emoji} {status_label(info['status'])} · {shortlist_count}/{config['max_shortlist']} picked{f' · {upload_count} uploaded' if upload_count else ''}</div>
                <div style="font-size:0.7rem;color:#666;margin-top:4px;">{info['topic']}</div>
                {due_line}
            </div>
            """, unsafe_allow_html=True)

    # Quick actions
    st.divider()
    st.subheader("Quick Actions")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Export shortlisted filenames", use_container_width=True):
            export = {}
            for vid, info in videos.items():
                if info.get("shortlisted"):
                    export[vid] = {
                        "title": info["title"],
                        "video_number": info["video_number"],
                        "shortlisted": info["shortlisted"],
                    }
            if export:
                st.code(json.dumps(export, indent=2), language="json")
            else:
                st.warning("No videos shortlisted yet.")

    with col2:
        if st.button("Export upload checklist", use_container_width=True):
            lines = []
            for vid, info in sorted_videos:
                if info["status"] == "shortlisted":
                    lines.append(f"- [ ] {info['video_number']}: {info['title'][:40]}... ({len(info['shortlisted'])} thumbnails)")
            if lines:
                st.code("\n".join(lines))
            else:
                st.info("No videos ready to upload.")


# --- Review ---

elif page == "Review":
    st.header("Review & Shortlist Thumbnails")

    # Video selector — only generated+
    available = {vid: info for vid, info in videos.items() if info["status"] != "not_generated"}

    if not available:
        st.warning("No thumbnails generated yet. Run the generation pipeline first.")
        st.stop()

    # Sort by views
    sorted_available = sorted(available.items(), key=lambda x: x[1]["views"], reverse=True)
    options = [f"{info['video_number']} — {info['title'][:50]} ({info['views']:,} views)" for _, info in sorted_available]
    video_ids = [vid for vid, _ in sorted_available]

    selected_idx = st.selectbox("Select video", range(len(options)), format_func=lambda i: options[i])
    selected_vid = video_ids[selected_idx]
    selected_info = videos[selected_vid]

    st.caption(f"Topic: {selected_info['topic']} · Status: {status_emoji(selected_info['status'])} {status_label(selected_info['status'])}")

    thumbnails = get_thumbnails(selected_vid)

    if not thumbnails:
        st.warning(f"No thumbnails found in `output/{selected_vid}/`")
        st.stop()

    # Current shortlist
    current_shortlist = set(selected_info.get("shortlisted", []))
    max_picks = config["max_shortlist"]

    st.markdown(f"**Shortlisted: {len(current_shortlist)}/{max_picks}** — Click thumbnails to toggle selection")

    # Group by variant (strip -a.png / -b.png suffix)
    variants = {}
    for t in thumbnails:
        if t == "picker.html":
            continue
        base = t.rsplit("-", 1)[0] if t.endswith(("-a.png", "-b.png")) else t.replace(".png", "")
        variants.setdefault(base, []).append(t)

    changed = False

    for variant_name, variant_files in variants.items():
        cols = st.columns(len(variant_files) + 1)

        # Variant label
        with cols[0]:
            st.markdown(f"**{variant_name}**")

        for j, fname in enumerate(variant_files):
            with cols[j + 1]:
                img_path = OUTPUT_DIR / selected_vid / fname
                is_selected = fname in current_shortlist

                # Show image
                st.image(str(img_path), use_container_width=True)

                # Toggle button
                if is_selected:
                    if st.button(f"★ Selected", key=f"sel_{fname}", type="primary", use_container_width=True):
                        current_shortlist.discard(fname)
                        changed = True
                else:
                    can_select = len(current_shortlist) < max_picks
                    if st.button(f"Select", key=f"sel_{fname}", disabled=not can_select, use_container_width=True):
                        current_shortlist.add(fname)
                        changed = True

                st.caption(fname)

        st.divider()

    # Save shortlist
    if changed or st.button("Save shortlist", type="primary", use_container_width=True):
        videos[selected_vid]["shortlisted"] = list(current_shortlist)
        if len(current_shortlist) > 0:
            videos[selected_vid]["status"] = "shortlisted"
        elif videos[selected_vid]["status"] == "shortlisted":
            videos[selected_vid]["status"] = "generated"
        data["videos"] = videos
        save_data(data)
        st.success(f"Saved {len(current_shortlist)} shortlisted thumbnails for {selected_info['video_number']}")
        st.rerun()

    # Mark individual thumbnails as uploaded
    if selected_info["status"] in ("shortlisted", "uploaded") and current_shortlist:
        st.divider()
        st.subheader("Mark uploaded to YouTube Studio")

        # Show upload date and check-back reminder if already uploaded
        if selected_info.get("uploaded_date"):
            upload_date = selected_info["uploaded_date"]
            due_date = selected_info.get("results_due", "?")
            try:
                days_left = (datetime.strptime(due_date, "%Y-%m-%d") - datetime.now()).days
                if days_left > 0:
                    st.info(f"Uploaded on **{upload_date}** — check results in **{days_left} days** ({due_date})")
                else:
                    st.warning(f"Uploaded on **{upload_date}** — results are **due now!** ({due_date})")
            except ValueError:
                st.info(f"Uploaded on **{upload_date}**")

        st.caption("Select which shortlisted thumbnails you've uploaded:")

        already_uploaded = set(selected_info.get("uploaded_thumbs", []))
        new_uploaded = set()

        upload_cols = st.columns(min(len(current_shortlist), 5))
        for j, fname in enumerate(sorted(current_shortlist)):
            with upload_cols[j % len(upload_cols)]:
                img_path = OUTPUT_DIR / selected_vid / fname
                if img_path.exists():
                    st.image(str(img_path), use_container_width=True)
                is_up = st.checkbox(
                    "Uploaded",
                    key=f"up_{fname}",
                    value=fname in already_uploaded,
                )
                if is_up:
                    new_uploaded.add(fname)
                st.caption(fname)

        if st.button("Save upload status", type="primary", use_container_width=True):
            today = datetime.now().strftime("%Y-%m-%d")
            due = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
            videos[selected_vid]["uploaded_thumbs"] = list(new_uploaded)
            if new_uploaded:
                videos[selected_vid]["status"] = "uploaded"
                if not videos[selected_vid].get("uploaded_date"):
                    videos[selected_vid]["uploaded_date"] = today
                    videos[selected_vid]["results_due"] = due
            elif selected_info["status"] == "uploaded":
                # All unchecked — revert to shortlisted
                videos[selected_vid]["status"] = "shortlisted"
                videos[selected_vid]["uploaded_date"] = None
                videos[selected_vid]["results_due"] = None
            data["videos"] = videos
            save_data(data)
            count = len(new_uploaded)
            st.success(f"Saved — {count}/{len(current_shortlist)} thumbnails marked as uploaded.")
            st.rerun()


# --- Results ---

elif page == "Results":
    st.header("A/B Test Results")

    # Show videos awaiting results
    uploaded = {vid: info for vid, info in videos.items() if info["status"] == "uploaded"}
    results_in = {vid: info for vid, info in videos.items() if info["status"] == "results_in"}

    if uploaded:
        st.subheader("Awaiting Results")
        for vid, info in sorted(uploaded.items(), key=lambda x: x[1].get("results_due", "")):
            due = info.get("results_due", "?")
            days_left = "?"
            if due and due != "?":
                try:
                    days_left = (datetime.strptime(due, "%Y-%m-%d") - datetime.now()).days
                    days_left = f"{days_left} days" if days_left > 0 else "DUE NOW"
                except ValueError:
                    pass

            with st.expander(f"🔵 {info['video_number']} — {info['title'][:50]} · Due: {due} ({days_left})"):
                uploaded_thumbs = info.get("uploaded_thumbs", info["shortlisted"])
                not_uploaded = [f for f in info["shortlisted"] if f not in uploaded_thumbs]
                st.caption(f"Uploaded: {info.get('uploaded_date', '?')} · {len(uploaded_thumbs)}/{len(info['shortlisted'])} thumbnails uploaded")

                # Show uploaded thumbnails
                if uploaded_thumbs:
                    cols = st.columns(len(uploaded_thumbs))
                    for j, fname in enumerate(uploaded_thumbs):
                        with cols[j]:
                            img_path = OUTPUT_DIR / vid / fname
                            if img_path.exists():
                                st.image(str(img_path), use_container_width=True)
                            st.caption(fname)

                # Show non-uploaded shortlisted (dimmed)
                if not_uploaded:
                    st.caption(f"Not uploaded: {', '.join(not_uploaded)}")

                # Record results — only for uploaded thumbnails
                st.markdown("**Record results:**")
                result_data = {}
                for fname in uploaded_thumbs:
                    col1, col2, col3 = st.columns([3, 2, 1])
                    with col1:
                        st.text(fname)
                    with col2:
                        wt = st.number_input(
                            "Watch-time %",
                            min_value=0.0, max_value=100.0, step=0.1,
                            key=f"wt_{vid}_{fname}",
                            value=info.get("results", {}).get(fname, {}).get("watch_time_share", 0.0),
                        )
                        result_data[fname] = {"watch_time_share": wt}
                    with col3:
                        is_winner = st.checkbox(
                            "Winner",
                            key=f"win_{vid}_{fname}",
                            value=info.get("results", {}).get(fname, {}).get("winner", False),
                        )
                        result_data[fname]["winner"] = is_winner

                if st.button(f"Save results for {info['video_number']}", key=f"save_results_{vid}"):
                    videos[vid]["results"] = result_data
                    videos[vid]["status"] = "results_in"
                    data["videos"] = videos
                    save_data(data)
                    st.success(f"Results saved for {info['video_number']}!")
                    st.rerun()

    else:
        st.info("No videos awaiting results. Upload shortlisted thumbnails first.")

    # Show completed results
    if results_in:
        st.divider()
        st.subheader("Completed Results")

        for vid, info in sorted(results_in.items(), key=lambda x: x[1]["video_number"]):
            with st.expander(f"✅ {info['video_number']} — {info['title'][:50]}"):
                # Show thumbnails with results
                if info["shortlisted"]:
                    cols = st.columns(len(info["shortlisted"]))
                    for j, fname in enumerate(info["shortlisted"]):
                        with cols[j]:
                            img_path = OUTPUT_DIR / vid / fname
                            if img_path.exists():
                                st.image(str(img_path), use_container_width=True)

                            result = info.get("results", {}).get(fname, {})
                            wt = result.get("watch_time_share", 0)
                            is_winner = result.get("winner", False)

                            if is_winner:
                                st.markdown(f"**🏆 {wt}%**")
                            else:
                                st.markdown(f"{wt}%")
                            st.caption(fname)

        # Summary table
        st.divider()
        st.subheader("Winners Summary")
        rows = []
        for vid, info in results_in.items():
            for fname, result in info.get("results", {}).items():
                if result.get("winner"):
                    rows.append({
                        "Video": f"{info['video_number']} — {info['title'][:40]}",
                        "Winner": fname,
                        "Watch-time %": result["watch_time_share"],
                    })
        if rows:
            st.table(rows)
