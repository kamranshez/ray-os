#!/usr/bin/env python3
"""Extract newsletter emails from a Google Takeout mbox file, filtered by sender."""

import argparse
import email
import email.policy
import mailbox
import re
import sys
from html import unescape
from pathlib import Path


def html_to_text(html: str) -> str:
    """Lightweight HTML-to-text conversion suitable for newsletter prose."""
    # Drop scripts/styles
    html = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", html, flags=re.DOTALL | re.IGNORECASE)
    # Treat block-level breaks as newlines
    html = re.sub(r"<\s*br\s*/?\s*>", "\n", html, flags=re.IGNORECASE)
    html = re.sub(r"</\s*(p|div|li|h[1-6]|tr|td|blockquote)\s*>", "\n\n", html, flags=re.IGNORECASE)
    html = re.sub(r"<\s*li[^>]*>", "- ", html, flags=re.IGNORECASE)
    # Strip remaining tags
    text = re.sub(r"<[^>]+>", "", html)
    text = unescape(text)
    # Collapse whitespace
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def get_body(msg) -> str:
    """Return the best plain-text body for an email message."""
    plain_parts = []
    html_parts = []
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            if part.is_multipart():
                continue
            try:
                payload = part.get_content()
            except Exception:
                try:
                    payload = part.get_payload(decode=True)
                    if isinstance(payload, bytes):
                        payload = payload.decode(part.get_content_charset() or "utf-8", errors="replace")
                except Exception:
                    payload = ""
            if ctype == "text/plain":
                plain_parts.append(payload)
            elif ctype == "text/html":
                html_parts.append(payload)
    else:
        try:
            payload = msg.get_content()
        except Exception:
            payload = msg.get_payload(decode=True)
            if isinstance(payload, bytes):
                payload = payload.decode(msg.get_content_charset() or "utf-8", errors="replace")
        ctype = msg.get_content_type()
        if ctype == "text/plain":
            plain_parts.append(payload)
        elif ctype == "text/html":
            html_parts.append(payload)

    if plain_parts:
        return "\n\n".join(p.strip() for p in plain_parts if p).strip()
    if html_parts:
        return html_to_text("\n\n".join(html_parts))
    return ""


def slugify(s: str, maxlen: int = 60) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()
    return s[:maxlen] or "untitled"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mbox", type=Path)
    parser.add_argument("outdir", type=Path)
    parser.add_argument("--filter", required=True,
                        help="Regex applied to From: header (case-insensitive), e.g. 'sender-name|newsletter-domain'")
    args = parser.parse_args()

    args.outdir.mkdir(parents=True, exist_ok=True)
    pattern = re.compile(args.filter, re.IGNORECASE)

    box = mailbox.mbox(str(args.mbox), factory=lambda f: email.message_from_binary_file(f, policy=email.policy.default))

    extracted = 0
    index_rows = []
    for i, msg in enumerate(box):
        from_hdr = str(msg.get("From", ""))
        if not pattern.search(from_hdr):
            continue
        subject = str(msg.get("Subject", "")).strip()
        date = str(msg.get("Date", "")).strip()
        body = get_body(msg)
        if not body.strip():
            continue

        slug = slugify(subject)
        fname = f"{extracted+1:02d}-{slug}.md"
        out_path = args.outdir / fname

        out_path.write_text(
            f"---\nfrom: {from_hdr}\nsubject: {subject}\ndate: {date}\n---\n\n{body}\n",
            encoding="utf-8",
        )
        index_rows.append((extracted + 1, subject, date, fname))
        extracted += 1

    index = ["# Example Email Index", ""]
    for n, subject, date, fname in index_rows:
        index.append(f"{n}. [{subject}]({fname}) — {date}")
    (args.outdir / "INDEX.md").write_text("\n".join(index) + "\n", encoding="utf-8")
    print(f"Wrote {extracted} emails to {args.outdir}")


if __name__ == "__main__":
    main()
