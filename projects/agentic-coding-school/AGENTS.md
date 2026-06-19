# agentic-coding-school

Source content for Ray's Agentic Coding School (https://www.agenticcoding.school). Video scripts, ideas, research, and promotion material. The live site is backed by a database that the **Agentic Coding School MCP** reads and writes (`mcp__claude_ai_Agentic_Coding_School__*`).

## Folder layout

Folders encode **placement**; stage is encoded by `status` (see below), not by which folder a file sits in.

- `classes/<class-slug>/<NN-chapter>/<NN-slug>.md` — the canonical, chaptered home for each video script. This is the target structure. `classes/<class-slug>/_drafts/` holds scripts whose class is known but chapter isn't yet.
- `to-film/<staging-class>/...` — scripted staging. Scripts are drained out of `to-film/` into `classes/`, one class at a time. Once a class is migrated, its scripts live under `classes/` only.
- `ideas/` — the classless idea inbox: raw seeds and research, no class assigned yet.
- `research/`, `vsl/` — supporting material, not class scripts.

## Content lifecycle: `status`

Every non-filmed script carries a `status` frontmatter field marking its stage in the pipeline. Use [[content-pipeline]] (Dataview views) as the filter dashboard across all folders.

```
status: "idea"       seed / stub / one-liner — no real script yet (all of ideas/, plus stub scripts elsewhere)
status: "scripted"   a real drafted script, planned to film, not yet recorded
status: "filmed"     recorded/published — signalled by the presence of video_id
```

`video_id` present ⇒ `filmed`; filmed files don't need `status` re-touched, their stage is implied by the join key. Classification rule used when stamping `status` (deterministic, idempotent):

1. has `video_id` → `filmed`.
2. else under `ideas/` → `idea` (seeds by definition).
3. else if the body is a **stub** (≤3 non-frontmatter lines, OR 0 `## ` headings and <10 body lines, OR a single "go through / placeholder" pointer line) → `idea`.
4. else → `scripted`.

A `status: "idea"` file is the upstream of a script; promote it to `scripted` once a real draft exists, and to `filmed` (via `video_id`) once recorded.

## The link between a script and its video: `video_id`

Every class script links to its live database video by a `video_id` in the frontmatter. The ID is the short code at the end of a video's public URL: `https://www.agenticcoding.school/v/<video_id>` (e.g. `7kCW7mhA`).

<important if="you are creating or editing a class script, or stamping a script with its video">

- `video_id` is the FIRST field in the frontmatter.
- Get it from the MCP: `get_video(classSlug, videoTitle)` returns a `url`; the `video_id` is the last path segment of that URL.
- A script with no matching database video (idea/placeholder not yet added) simply has no `video_id`. Do not invent one.
- `video_id` is the join key. The folder a file sits in is just where it is *authored*; the database is the source of truth for where the video actually appears.
</important>

## Videos with multiple placements (cross-listing)

A single video can appear in more than one class/chapter. The database models this as one **video** plus many **placements** (`list_video_placements` returns them, each with `isPrimary` and `orderIndex`). `list_videos` only returns each chapter's PRIMARY videos, so a borrowed (secondary) video will NOT show up there. Always check `list_video_placements` before assuming a video isn't in a class.

We mirror this with the **canonical-file model**: one markdown file per video, no duplicates.

<important if="a video appears in multiple classes/chapters (has 2+ placements)">

- The canonical `.md` file lives in the video's **primary** class folder only.
- It does NOT get a second copy in the borrowing class's folder. The borrowing class's membership is reconstructed from the `placements` field (e.g. an Obsidian Dataview query: list where `placements` contains that class).
- Record the placements in frontmatter so the cross-listing is visible locally and greppable.
- If a script currently sits in a class folder where it is only a SECONDARY placement (because its primary class hasn't been migrated yet), leave it for now but flag it; it relocates to its primary class folder when that class is migrated.
</important>

## Frontmatter schema

Single-placement script (most scripts):

```yaml
---
video_id: "7kCW7mhA"
duration: "8-12 min"
batch: 1
order: 1
batch_name: "Setup"
class: "loopy-ai"
chapter: "Intro"
aliases: [intro]
---
```

Multi-placement script (cross-listed). Add `primary_class` and a `placements` list; `class` stays the canonical/primary class:

```yaml
---
video_id: "5VMOl8yu"
primary_class: "codex"
class: "codex"
chapter: "Codex App"
placements:
  - { class: "codex",    chapter: "Codex App",   primary: true,  order: 37 }
  - { class: "loopy-ai", chapter: "The Toolbox", primary: false, order: 8 }
aliases: [goal]
---
```

`class` = the class folder the file currently lives in (its authoring location). `primary_class` = the canonical/primary class from the database. For most files these are equal. When they differ, the file is **borrowed**: it is physically staged in a class where it is only a secondary placement, and it should relocate to its `primary_class` folder once that class is migrated. That divergence is the relocation signal, no separate flag needed.

The `placements` list mirrors the database; the database stays the source of truth. When in doubt, re-read it with `list_video_placements` rather than trusting stale frontmatter.

## Vault conventions (inherited from repo root)

These apply to every script here:

- No H1 title (Obsidian uses the filename / `aliases`).
- kebab-case all file and folder names.
- No em dashes or en dashes in script prose. Commas, periods, or a rewrite instead.
- Internal links are `[[alias]]` wikilinks; image embeds are filename-only `![[name.png]]` (images live in the vault-root `images/` folder).

See the class-scriptwriter skill for voice/structure when writing a new script.
