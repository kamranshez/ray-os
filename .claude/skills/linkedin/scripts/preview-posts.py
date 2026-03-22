#!/usr/bin/env python3
"""
Generate an HTML preview of LinkedIn post variations.

Usage:
    python preview-posts.py posts.json [--output preview.html] [--open]

Input JSON format:
{
    "posts": [
        {
            "number": 1,
            "triggers": "Productive Discomfort + Aspiration",
            "body": "The full post text..."
        },
        ...
    ]
}

Or simply pass a flat array of post objects.
"""

import argparse
import html
import json
import os
import subprocess
import sys

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "post-preview.html")


def build_post_card(post: dict, index: int) -> str:
    number = post.get("number", index + 1)
    triggers = html.escape(post.get("triggers", ""))
    body = post.get("body", "")

    # Convert post body to HTML: preserve line breaks, escape HTML
    body_escaped = html.escape(body)
    # Double newlines become paragraph breaks, single newlines become <br>
    body_html = body_escaped.replace("\n\n", '</p><p class="post-paragraph">').replace(
        "\n", "<br>"
    )
    body_html = f'<p class="post-paragraph">{body_html}</p>'

    # The raw text for clipboard (no HTML)
    body_for_clipboard = body.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")

    return f"""
    <div class="post-card" id="post-{number}">
        <div class="post-header">
            <div class="post-label">
                <span class="post-number">Post {number}</span>
                <span class="post-triggers">{triggers}</span>
            </div>
            <button class="copy-btn" onclick="copyPost(this, `{body_for_clipboard}`)">
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                    <rect x="5" y="5" width="9" height="9" rx="1.5" stroke="currentColor" stroke-width="1.5"/>
                    <path d="M3 10V3C3 2.44772 3.44772 2 4 2H11" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                </svg>
                Copy
            </button>
        </div>

        <div class="linkedin-post">
            <div class="post-author">
                <div class="avatar">RA</div>
                <div class="author-info">
                    <div class="author-name">Ray Amjad</div>
                    <div class="author-headline">Building with AI &middot; YouTube @RAmjad</div>
                    <div class="post-time">Just now &middot; <svg width="12" height="12" viewBox="0 0 16 16" fill="currentColor"><path d="M8 1a7 7 0 107 7 7 7 0 00-7-7zM3 8a5 5 0 014.54-4.98C5.6 3.56 4 6.73 4 8s1.6 4.44 3.54 4.98A5 5 0 013 8zm6.64 4.81A8.93 8.93 0 0010 8a8.93 8.93 0 00-.36-4.81A5 5 0 0113 8a5 5 0 01-3.36 4.81zM8 12.5A8.43 8.43 0 016 8a8.43 8.43 0 012-4.5A8.43 8.43 0 0110 8a8.43 8.43 0 01-2 4.5z"/></svg></div>
                </div>
            </div>
            <div class="post-body">{body_html}</div>
            <div class="post-actions">
                <div class="action-btn">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M14 9V5a3 3 0 00-6 0v1m0 0H6a2 2 0 00-2 2v1a2 2 0 002 2h2m0-5v5m10-1v6a2 2 0 01-2 2H8a2 2 0 01-2-2v-6m12 0h-4m4 0a2 2 0 002-2v-1a2 2 0 00-2-2h-2m-4 5V6"/></svg>
                    Like
                </div>
                <div class="action-btn">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>
                    Comment
                </div>
                <div class="action-btn">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M4 12v7a2 2 0 002 2h12a2 2 0 002-2v-7M16 6l-4-4-4 4M12 2v13"/></svg>
                    Repost
                </div>
                <div class="action-btn">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"/></svg>
                    Send
                </div>
            </div>
        </div>
    </div>"""


def generate_html(posts: list[dict]) -> str:
    cards = "\n".join(build_post_card(p, i) for i, p in enumerate(posts))

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>LinkedIn Post Variations</title>
<style>
    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}

    body {{
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
        background: #f3f2ef;
        color: #000000e6;
        padding: 24px;
        min-height: 100vh;
    }}

    .page-header {{
        max-width: 560px;
        margin: 0 auto 24px;
        text-align: center;
    }}

    .page-header h1 {{
        font-size: 20px;
        font-weight: 600;
        color: #000000e6;
        margin-bottom: 4px;
    }}

    .page-header p {{
        font-size: 14px;
        color: #00000099;
    }}

    .post-card {{
        max-width: 560px;
        margin: 0 auto 20px;
    }}

    .post-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
        padding: 0 4px;
    }}

    .post-label {{
        display: flex;
        align-items: center;
        gap: 10px;
    }}

    .post-number {{
        font-size: 13px;
        font-weight: 700;
        color: #0a66c2;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}

    .post-triggers {{
        font-size: 12px;
        color: #00000099;
        background: #e8e8e8;
        padding: 2px 8px;
        border-radius: 12px;
    }}

    .copy-btn {{
        display: flex;
        align-items: center;
        gap: 6px;
        padding: 6px 14px;
        border: 1.5px solid #0a66c2;
        background: white;
        color: #0a66c2;
        font-size: 13px;
        font-weight: 600;
        border-radius: 20px;
        cursor: pointer;
        transition: all 0.15s;
    }}

    .copy-btn:hover {{
        background: #0a66c20d;
    }}

    .copy-btn.copied {{
        background: #057642;
        border-color: #057642;
        color: white;
    }}

    .linkedin-post {{
        background: white;
        border-radius: 8px;
        border: 1px solid #e0dfdc;
        overflow: hidden;
    }}

    .post-author {{
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 16px 16px 0;
    }}

    .avatar {{
        width: 48px;
        height: 48px;
        border-radius: 50%;
        background: linear-gradient(135deg, #0a66c2, #004182);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 16px;
        flex-shrink: 0;
    }}

    .author-info {{
        flex: 1;
    }}

    .author-name {{
        font-size: 14px;
        font-weight: 600;
        color: #000000e6;
        line-height: 1.3;
    }}

    .author-headline {{
        font-size: 12px;
        color: #00000099;
        line-height: 1.3;
    }}

    .post-time {{
        font-size: 12px;
        color: #00000099;
        display: flex;
        align-items: center;
        gap: 4px;
        line-height: 1.3;
    }}

    .post-body {{
        padding: 12px 16px 16px;
        font-size: 14px;
        line-height: 1.5;
        color: #000000e6;
    }}

    .post-body .post-paragraph {{
        margin-bottom: 8px;
    }}

    .post-body .post-paragraph:last-child {{
        margin-bottom: 0;
    }}

    .post-actions {{
        display: flex;
        justify-content: space-around;
        padding: 4px 8px;
        border-top: 1px solid #e0dfdc;
    }}

    .action-btn {{
        display: flex;
        align-items: center;
        gap: 6px;
        padding: 12px 8px;
        font-size: 13px;
        color: #00000099;
        font-weight: 600;
        cursor: default;
        border-radius: 4px;
        user-select: none;
    }}

    @media (max-width: 600px) {{
        body {{
            padding: 12px;
        }}
        .post-card {{
            margin-bottom: 16px;
        }}
    }}
</style>
</head>
<body>

<div class="page-header">
    <h1>LinkedIn Post Variations</h1>
    <p>{len(posts)} variations &middot; each uses different emotional triggers</p>
</div>

{cards}

<script>
function copyPost(btn, text) {{
    navigator.clipboard.writeText(text).then(() => {{
        btn.classList.add('copied');
        btn.innerHTML = `
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <path d="M3 8.5L6.5 12L13 4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Copied!
        `;
        setTimeout(() => {{
            btn.classList.remove('copied');
            btn.innerHTML = `
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                    <rect x="5" y="5" width="9" height="9" rx="1.5" stroke="currentColor" stroke-width="1.5"/>
                    <path d="M3 10V3C3 2.44772 3.44772 2 4 2H11" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                </svg>
                Copy
            `;
        }}, 2000);
    }});
}}
</script>

</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(description="Generate LinkedIn post preview HTML")
    parser.add_argument("input", help="Path to JSON file with posts")
    parser.add_argument("--output", "-o", default="/tmp/linkedin-preview.html", help="Output HTML path")
    parser.add_argument("--open", action="store_true", help="Open in browser after generating")
    args = parser.parse_args()

    with open(args.input) as f:
        data = json.load(f)

    posts = data.get("posts", data) if isinstance(data, dict) else data

    html_content = generate_html(posts)

    with open(args.output, "w") as f:
        f.write(html_content)

    print(f"Preview written to {args.output}")

    if args.open:
        subprocess.run(["open", args.output])


if __name__ == "__main__":
    main()
