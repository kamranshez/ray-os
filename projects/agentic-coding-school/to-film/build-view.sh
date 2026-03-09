#!/bin/bash
# Generates an HTML dashboard from all to-film markdown files.
# Usage: cd to-film && ./build-view.sh && open view.html

OUTPUT="view.html"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

cat > "$SCRIPT_DIR/$OUTPUT" << 'HEADER'
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Agentic Coding School — To Film</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #0d1117; color: #c9d1d9; padding: 24px; }
  h1 { color: #f0f6fc; margin-bottom: 8px; font-size: 24px; }
  .subtitle { color: #8b949e; margin-bottom: 24px; font-size: 14px; }
  .stats { display: flex; gap: 16px; margin-bottom: 24px; flex-wrap: wrap; }
  .stat { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px 16px; }
  .stat-num { font-size: 28px; font-weight: 700; color: #f0f6fc; }
  .stat-label { font-size: 12px; color: #8b949e; text-transform: uppercase; letter-spacing: 0.5px; }
  .class-section { margin-bottom: 32px; }
  .class-header { display: flex; align-items: center; gap: 10px; margin-bottom: 12px; cursor: pointer; }
  .class-header h2 { font-size: 18px; color: #f0f6fc; }
  .class-badge { font-size: 12px; background: #30363d; color: #8b949e; padding: 2px 8px; border-radius: 12px; }
  .chapter-group { margin-bottom: 16px; margin-left: 8px; }
  .chapter-name { font-size: 13px; font-weight: 600; color: #8b949e; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; padding-left: 8px; border-left: 3px solid #30363d; }
  .video-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 8px; }
  .card { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px 16px; transition: border-color 0.15s; }
  .card:hover { border-color: #58a6ff; }
  .card-title { font-size: 14px; font-weight: 600; color: #f0f6fc; margin-bottom: 6px; }
  .card-meta { display: flex; gap: 8px; flex-wrap: wrap; }
  .tag { font-size: 11px; padding: 2px 8px; border-radius: 12px; }
  .tag-duration { background: #1f2937; color: #93c5fd; }
  .tag-batch { background: #1c2333; color: #a78bfa; }
  .tag-order { background: #1a2332; color: #6ee7b7; }
  .card-body { font-size: 12px; color: #8b949e; margin-top: 8px; line-height: 1.5; max-height: 60px; overflow: hidden; }
  .card.expanded .card-body { max-height: none; }
  .card-toggle { font-size: 11px; color: #58a6ff; cursor: pointer; margin-top: 4px; border: none; background: none; padding: 0; }
  .class-claude-code .chapter-name { border-left-color: #58a6ff; }
  .class-techniques .chapter-name { border-left-color: #f97316; }
  .class-context-engineering .chapter-name { border-left-color: #a78bfa; }
  .class-business .chapter-name { border-left-color: #34d399; }
  .class-workflows .chapter-name { border-left-color: #fbbf24; }
  .color-claude-code { color: #58a6ff; }
  .color-techniques { color: #f97316; }
  .color-context-engineering { color: #a78bfa; }
  .color-business { color: #34d399; }
  .color-workflows { color: #fbbf24; }
  .filter-bar { display: flex; gap: 8px; margin-bottom: 20px; flex-wrap: wrap; }
  .filter-btn { font-size: 12px; padding: 6px 14px; border-radius: 20px; border: 1px solid #30363d; background: #161b22; color: #c9d1d9; cursor: pointer; transition: all 0.15s; }
  .filter-btn:hover, .filter-btn.active { background: #30363d; border-color: #58a6ff; color: #f0f6fc; }
</style>
</head>
<body>
<h1>Agentic Coding School — To Film</h1>
<p class="subtitle">Auto-generated from to-film/*.md files</p>
<div class="stats" id="stats"></div>
<div class="filter-bar" id="filters"></div>
<div id="content"></div>
<script>
const data =
HEADER

# Build JSON data from all markdown files
echo -n "[" >> "$SCRIPT_DIR/$OUTPUT"
FIRST=true

for class_dir in "$SCRIPT_DIR"/*/; do
  [ ! -d "$class_dir" ] && continue
  class_name=$(basename "$class_dir")
  [ "$class_name" = "." ] && continue

  for f in "$class_dir"*.md; do
    [ ! -f "$f" ] && continue

    # Parse frontmatter
    duration=""
    batch=""
    order=""
    batch_name=""
    chapter=""
    title=""
    body=""

    in_frontmatter=false
    frontmatter_done=false
    body_lines=""

    while IFS= read -r line; do
      if [ "$frontmatter_done" = false ]; then
        if [ "$line" = "---" ]; then
          if [ "$in_frontmatter" = true ]; then
            frontmatter_done=true
          else
            in_frontmatter=true
          fi
          continue
        fi
        if [ "$in_frontmatter" = true ]; then
          key=$(echo "$line" | sed 's/:.*//' | xargs)
          val=$(echo "$line" | sed 's/^[^:]*: *//' | sed 's/^"//;s/"$//')
          case "$key" in
            duration) duration="$val" ;;
            batch) batch="$val" ;;
            order) order="$val" ;;
            batch_name) batch_name="$val" ;;
            chapter) chapter="$val" ;;
          esac
        fi
      else
        # First non-empty line after frontmatter = title
        if [ -z "$title" ]; then
          cleaned=$(echo "$line" | sed 's/^#* *//')
          if [ -n "$cleaned" ]; then
            title="$cleaned"
          fi
        else
          body_lines="$body_lines$line "
        fi
      fi
    done < "$f"

    # Clean body for JSON (escape quotes, remove newlines)
    body_clean=$(echo "$body_lines" | sed 's/"/\\"/g' | tr '\n' ' ' | sed 's/  */ /g' | head -c 300)

    if [ "$FIRST" = true ]; then
      FIRST=false
    else
      echo -n "," >> "$SCRIPT_DIR/$OUTPUT"
    fi

    cat >> "$SCRIPT_DIR/$OUTPUT" << ENTRY
{"class":"$class_name","chapter":"$chapter","title":"$(echo "$title" | sed 's/"/\\"/g')","duration":"$duration","batch":"$batch","order":"$order","batchName":"$batch_name","body":"$body_clean","file":"$(basename "$f")"}
ENTRY

  done
done

cat >> "$SCRIPT_DIR/$OUTPUT" << 'FOOTER'
];

const classLabels = {
  'claude-code': 'Master Claude Code',
  'techniques': 'Bonus Techniques',
  'context-engineering': 'Context Engineering',
  'business': 'Claude Code for Business',
  'workflows': 'Workflows & Applications'
};

const classOrder = ['claude-code', 'techniques', 'context-engineering', 'business', 'workflows'];

// Stats
const totalVideos = data.length;
const classes = [...new Set(data.map(d => d.class))];
const chapters = [...new Set(data.map(d => d.chapter))];
document.getElementById('stats').innerHTML = `
  <div class="stat"><div class="stat-num">${totalVideos}</div><div class="stat-label">Videos to Film</div></div>
  <div class="stat"><div class="stat-num">${classes.length}</div><div class="stat-label">Classes</div></div>
  <div class="stat"><div class="stat-num">${chapters.length}</div><div class="stat-label">Chapters</div></div>
`;

// Filters
let activeFilter = 'all';
const filtersEl = document.getElementById('filters');
filtersEl.innerHTML = `<button class="filter-btn active" data-filter="all">All</button>` +
  classOrder.filter(c => data.some(d => d.class === c)).map(c =>
    `<button class="filter-btn" data-filter="${c}">${classLabels[c] || c}</button>`
  ).join('');

filtersEl.addEventListener('click', e => {
  if (!e.target.matches('.filter-btn')) return;
  activeFilter = e.target.dataset.filter;
  filtersEl.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  e.target.classList.add('active');
  render();
});

function render() {
  const filtered = activeFilter === 'all' ? data : data.filter(d => d.class === activeFilter);
  const grouped = {};
  filtered.forEach(d => {
    if (!grouped[d.class]) grouped[d.class] = {};
    if (!grouped[d.class][d.chapter]) grouped[d.class][d.chapter] = [];
    grouped[d.class][d.chapter].push(d);
  });

  // Sort videos within chapters by batch then order
  Object.values(grouped).forEach(chapters => {
    Object.values(chapters).forEach(videos => {
      videos.sort((a, b) => (Number(a.batch) - Number(b.batch)) || (Number(a.order) - Number(b.order)));
    });
  });

  let html = '';
  classOrder.forEach(cls => {
    if (!grouped[cls]) return;
    const chapterMap = grouped[cls];
    const count = Object.values(chapterMap).reduce((s, v) => s + v.length, 0);

    html += `<div class="class-section class-${cls}">`;
    html += `<div class="class-header"><h2 class="color-${cls}">${classLabels[cls] || cls}</h2><span class="class-badge">${count} videos</span></div>`;

    Object.keys(chapterMap).sort().forEach(chapter => {
      const videos = chapterMap[chapter];
      html += `<div class="chapter-group">`;
      html += `<div class="chapter-name">${chapter || 'Uncategorized'}</div>`;
      html += `<div class="video-grid">`;
      videos.forEach(v => {
        html += `<div class="card" onclick="this.classList.toggle('expanded')">`;
        html += `<div class="card-title">${v.title}</div>`;
        html += `<div class="card-meta">`;
        if (v.duration) html += `<span class="tag tag-duration">${v.duration}</span>`;
        if (v.batch) html += `<span class="tag tag-batch">Batch ${v.batch}</span>`;
        if (v.order) html += `<span class="tag tag-order">#${v.order}</span>`;
        html += `</div>`;
        if (v.body && v.body.trim()) {
          html += `<div class="card-body">${v.body}</div>`;
          html += `<button class="card-toggle">more</button>`;
        }
        html += `</div>`;
      });
      html += `</div></div>`;
    });
    html += `</div>`;
  });

  document.getElementById('content').innerHTML = html;
}
render();
</script>
</body>
</html>
FOOTER

echo "Built $SCRIPT_DIR/$OUTPUT ($(wc -l < "$SCRIPT_DIR/$OUTPUT") lines)"
