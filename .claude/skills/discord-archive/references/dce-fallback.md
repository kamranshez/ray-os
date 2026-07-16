# DiscordChatExporter — the fallback

[DiscordChatExporter](https://github.com/Tyrrrz/DiscordChatExporter) (DCE) is a
mature, well-maintained CLI that does the same job as our custom archiver. It's
the right thing to reach for if:

- The custom script breaks on a Discord API change and you need the archive
  now.
- You want HTML output instead of JSON (DCE renders messages as a styled web
  page, very readable in a browser).
- You want attachments downloaded inline (DCE handles signed URL expiry).
- You don't want to manage a session profile — DCE just takes the token.

## What DCE doesn't do that ours does

- DCE only sends `Authorization` + a fixed UA. No `cf_clearance`, no
  `x-super-properties`, no `x-installation-id`. If Cloudflare bot-check is
  active on the API, DCE will fail before our script does.
- DCE doesn't support arbitrary per-channel concurrency limits without a
  config file. Our archiver paces inter-channel sleeps as a primary control.

## Install (macOS arm64)

Already done on this machine, but for reproducibility:

```bash
mkdir -p ~/tools/discordchatexporter && cd ~/tools/discordchatexporter
curl -fL --retry 5 --retry-delay 3 -A "Mozilla/5.0" \
  -o dce.zip \
  "https://github.com/Tyrrrz/DiscordChatExporter/releases/latest/download/DiscordChatExporter.Cli.osx-arm64.zip"
# (the URL pattern works for any latest release; check API for exact version
#  if /latest/download/ stops working)
unzip -o -q dce.zip && rm dce.zip
chmod +x DiscordChatExporter.Cli
xattr -dr com.apple.quarantine .   # strip Gatekeeper quarantine
mkdir -p ~/bin && ln -sf ~/tools/discordchatexporter/DiscordChatExporter.Cli ~/bin/dce
~/bin/dce --version
```

The download is ~10 MB. We've sanity-checked the strings in `Core.dll` — only
URL references are Discord CDN + standard embed providers (YouTube, Spotify,
Twitch, twemoji/jsdelivr fonts, cdnjs highlight.js styles). No exfil endpoints.

## Use DCE

```bash
TOKEN='<paste with `read -rs DISCORD_TOKEN && export DISCORD_TOKEN`>'

# List servers (auth check)
dce guilds -t "$TOKEN"

# List channels in one server
dce channels -t "$TOKEN" -g <guild_id>

# Export a single channel (JSON)
dce export -t "$TOKEN" -c <channel_id> -f Json -o ~/Downloads/channel.json --media false

# Export every channel in a guild, HTML format with media
dce exportguild -t "$TOKEN" -g <guild_id> -f HtmlDark -o ~/Downloads/guild-archive/ --media true
```

Formats: `Json`, `HtmlDark`, `HtmlLight`, `PlainText`, `Csv`.
Useful flags: `--media true` (download attachments), `--reuse-media` (dedupe
the downloads), `--include-threads All` (forums + threads).

## When to switch from custom → DCE mid-archive

If the custom archiver starts failing partway through a run (captcha, 403 on
an endpoint that used to work, or repeated 429s), don't fight it — switch to
DCE for the remaining channels. The output formats differ (DCE's JSON has a
slightly different shape) so you'd want to keep DCE outputs in a separate
subdirectory.
