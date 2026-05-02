import fs from "node:fs/promises";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const outputDir = "/Users/ray/Desktop/ray-os/outputs/claude-code-vs-codex";
const outputPath = `${outputDir}/claude-code-vs-codex-feature-comparison.xlsx`;

const asOfDate = "2026-05-01";

const summaryRows = [
  ["Best fit", "Claude-native local and cross-surface coding workflows", "Parallel cloud/local agent work, worktrees, PRs, and automation"],
  ["Primary feel", "Terminal-first assistant that now spans IDE, desktop, web, and browser", "Agent command center for local CLI plus cloud task delegation"],
  ["Strongest differentiator", "MCP-heavy ecosystem, Unix-style CLI, CLAUDE.md, routines, and cross-device handoff", "Built-in worktrees, cloud sandboxes, subagents, Skills, and background work"],
  ["Pricing/access", "Claude Pro/Max; Team premium seats; API token billing available", "ChatGPT Plus/Pro/Business/Edu/Enterprise; token/credit-based Codex rates"],
];

const featureRows = [
  ["Core identity", "Agentic coding tool that reads codebases, edits files, runs commands, and integrates with development tools.", "OpenAI coding agent that can read, modify, run, review, and ship code locally or in cloud.", "Tie"],
  ["Main surfaces", "Terminal, VS Code, JetBrains, desktop app, web, browser/mobile handoff.", "Codex app, CLI, IDE extension, cloud/web, GitHub, Slack, Linear.", "Tie"],
  ["Local terminal workflow", "Very strong terminal-native workflow, including piping, scripting, logs, and CI-style prompts.", "Open-source CLI with terminal TUI, approvals, web search, image inputs, local code review, and subagents.", "Tie"],
  ["Cloud task execution", "Web/cloud sessions, routines, scheduled tasks, and remote control.", "Major product emphasis: isolated cloud sandboxes, background tasks, PR work, and parallel execution.", "Codex"],
  ["Parallel agents", "Supports multiple Claude Code agents and lead-agent coordination.", "Designed around multi-agent workflows with built-in worktrees and cloud environments.", "Codex"],
  ["Project instructions", "Uses CLAUDE.md, custom commands, hooks, and auto memory.", "Uses AGENTS.md, rules, hooks, Skills, and memories/Chronicle.", "Tie"],
  ["MCP and external tools", "MCP is central; examples include Google Drive, Jira, Slack, and custom tooling.", "Supports MCP and connectors; also tightly integrated with GitHub and OpenAI agent tooling.", "Claude Code"],
  ["GitHub automation", "GitHub Actions and GitLab CI/CD; @claude can work from issues/PRs.", "@codex on issues/PRs can spin up tasks and propose changes.", "Tie"],
  ["IDE experience", "VS Code and JetBrains support with diff review and context sharing.", "IDE extension can delegate cloud tasks and apply diffs locally.", "Tie"],
  ["Desktop app", "Standalone app for visual diffs, side-by-side sessions, recurring tasks, and cloud sessions.", "Codex app is positioned as a command center with worktrees, previews, terminal tabs, and agent activity.", "Tie"],
  ["Mobile/browser continuity", "Remote Control, web, iOS, and teleporting/handoff between surfaces.", "Cloud tasks can be monitored asynchronously; ChatGPT ecosystem access.", "Claude Code"],
  ["Scheduling and recurring work", "Routines, desktop scheduled tasks, and /loop in CLI.", "Automations and background work for routine tasks and monitoring.", "Tie"],
  ["Code review", "GitHub Code Review and CI/CD review workflows.", "Local code review by a separate agent plus GitHub review workflows.", "Tie"],
  ["Image/multimodal inputs", "Can use screenshots/design context depending on surface and integrations.", "CLI docs explicitly call out image inputs and image generation/editing.", "Codex"],
  ["Model ecosystem", "Claude models such as Sonnet and Opus, with Anthropic API, AWS Bedrock, and Google Vertex options.", "OpenAI frontier coding models including Codex-oriented GPT-5 family options in Codex CLI.", "Preference"],
  ["Pricing/access model", "Included with Claude paid plans; enterprise/API usage can be token-based and varies by usage.", "Included with ChatGPT paid plans; current Codex rate card is token/credit-based.", "Preference"],
  ["Recommended when", "You want a Claude-native, terminal-friendly assistant with broad MCP and workflow integration.", "You want parallel agent work, cloud sandboxes, PR/task delegation, and a stronger command-center feel.", "Preference"],
];

const sourceRows = [
  ["Claude Code overview", "https://code.claude.com/docs/en/overview", "Primary Anthropic documentation for surfaces, CLI, routines, MCP, hooks, agents, and integrations."],
  ["Claude Code GitHub Actions", "https://code.claude.com/docs/en/github-actions", "Primary Anthropic documentation for @claude issue/PR automation."],
  ["Claude pricing", "https://www.claude.com/pricing", "Claude plan access and subscription tiers."],
  ["Claude Code product page", "https://www.claude.com/product/claude-code", "Claude Code plan positioning and included usage."],
  ["Codex cloud docs", "https://developers.openai.com/codex/cloud", "Primary OpenAI documentation for Codex cloud tasks, sandboxes, and GitHub delegation."],
  ["Codex CLI docs", "https://developers.openai.com/codex/cli", "Primary OpenAI documentation for local CLI, approvals, subagents, image inputs, web search, and MCP."],
  ["Codex product page", "https://openai.com/codex/", "OpenAI product positioning for multi-agent workflows, worktrees, Skills, and background work."],
  ["Using Codex with ChatGPT plan", "https://help.openai.com/en/articles/11369540", "OpenAI Help Center article for current plan access."],
  ["Codex rate card", "https://help.openai.com/en/articles/20001106-codex-rate-card", "OpenAI Help Center article for current Codex credit/rate model."],
];

function setWidths(sheet, widths) {
  widths.forEach((width, index) => {
    sheet.getRangeByIndexes(0, index, 1, 1).format.columnWidthPx = width;
  });
}

function header(range, fill = "#B83280") {
  range.format = {
    fill,
    font: { bold: true, color: "#FFFFFF" },
    wrapText: true,
    horizontalAlignment: "center",
    verticalAlignment: "center",
  };
}

function body(range) {
  range.format = {
    wrapText: true,
    verticalAlignment: "top",
  };
}

await fs.mkdir(outputDir, { recursive: true });

const workbook = Workbook.create();

const summary = workbook.worksheets.add("Summary");
summary.showGridLines = false;
summary.getRange("A1:D1").values = [["Claude Code vs Codex Feature Comparison", "", "", ""]];
summary.getRange("A1:D1").merge();
summary.getRange("A1").format = {
  fill: "#8A1459",
  font: { bold: true, color: "#FFFFFF" },
  horizontalAlignment: "center",
  verticalAlignment: "center",
};
summary.getRange("A1").format.rowHeightPx = 38;
summary.getRange("A2:D2").values = [[`As of ${asOfDate}`, "", "", ""]];
summary.getRange("A2:D2").merge();
summary.getRange("A2").format = {
  fill: "#FCE7F3",
  font: { italic: true, color: "#8A1459" },
  horizontalAlignment: "center",
};
summary.getRange("A4:D4").values = [["Area", "Claude Code", "Codex", "Quick read"]];
header(summary.getRange("A4:D4"));
summary.getRange("A5:D8").values = summaryRows.map((row) => [...row, row[0] === "Best fit" ? "Different centers of gravity" : row[0] === "Pricing/access" ? "Check current plan limits" : "Mostly overlapping"]);
body(summary.getRange("A5:D8"));
summary.getRange("A10:D10").values = [["Bottom line", "", "", ""]];
summary.getRange("A10:D10").merge();
header(summary.getRange("A10:D10"), "#C02674");
summary.getRange("A11:D12").values = [
  ["Claude Code is strongest when you want a Claude-native, terminal-friendly assistant that travels across IDE, desktop, browser, mobile, MCP tools, and scheduled routines.", "", "", ""],
  ["Codex is strongest when you want a command-center style coding workflow with local CLI plus cloud sandboxes, parallel agents, worktrees, PR workflows, and background automation.", "", "", ""],
];
summary.getRange("A11:D11").merge();
summary.getRange("A12:D12").merge();
body(summary.getRange("A11:D12"));
summary.getRange("A11:D12").format.fill = "#FFF1F8";
summary.freezePanes.freezeRows(4);
setWidths(summary, [160, 330, 330, 180]);
summary.getRange("A5:D12").format.rowHeightPx = 48;

const matrix = workbook.worksheets.add("Feature Matrix");
matrix.showGridLines = false;
matrix.getRange("A1:E1").values = [["Feature", "Claude Code", "Codex", "Edge", "Notes"]];
header(matrix.getRange("A1:E1"));
matrix.getRangeByIndexes(1, 0, featureRows.length, 5).values = featureRows.map(([feature, claude, codex, edge]) => [
  feature,
  claude,
  codex,
  edge,
  edge === "Tie" ? "Both products cover this well; choose by ecosystem and workflow preference." : edge === "Preference" ? "Depends on existing model/vendor stack and team budget." : `${edge} has a clearer product emphasis here.`,
]);
body(matrix.getRange(`A2:E${featureRows.length + 1}`));
matrix.freezePanes.freezeRows(1);
setWidths(matrix, [185, 370, 370, 115, 270]);
matrix.getRange(`A2:E${featureRows.length + 1}`).format.rowHeightPx = 68;
matrix.getRange(`D2:D${featureRows.length + 1}`).format.horizontalAlignment = "center";
matrix.getRange(`D2:D${featureRows.length + 1}`).conditionalFormats.add("containsText", {
  text: "Claude Code",
  format: { fill: "#FCE7F3", font: { bold: true, color: "#9D174D" } },
});
matrix.getRange(`D2:D${featureRows.length + 1}`).conditionalFormats.add("containsText", {
  text: "Codex",
  format: { fill: "#FFE4E6", font: { bold: true, color: "#9F1239" } },
});
matrix.getRange(`D2:D${featureRows.length + 1}`).conditionalFormats.add("containsText", {
  text: "Tie",
  format: { fill: "#FDF2F8", font: { bold: true, color: "#831843" } },
});

const sources = workbook.worksheets.add("Sources and Notes");
sources.showGridLines = false;
sources.getRange("A1:C1").values = [["Source", "URL", "Used for"]];
header(sources.getRange("A1:C1"));
sources.getRangeByIndexes(1, 0, sourceRows.length, 3).values = sourceRows;
body(sources.getRange(`A2:C${sourceRows.length + 1}`));
sources.getRange(`B2:B${sourceRows.length + 1}`).format.font = { color: "#0563C1" };
sources.getRange(`A${sourceRows.length + 3}:C${sourceRows.length + 3}`).values = [["Notes", "", ""]];
sources.getRange(`A${sourceRows.length + 3}:C${sourceRows.length + 3}`).merge();
header(sources.getRange(`A${sourceRows.length + 3}:C${sourceRows.length + 3}`), "#DB2777");
sources.getRange(`A${sourceRows.length + 4}:C${sourceRows.length + 5}`).values = [
  ["This workbook summarizes online research performed on the date shown in the Summary tab. Product capabilities and pricing can change quickly.", "", ""],
  ["The Edge column reflects product positioning and documented emphasis, not a benchmarked performance test.", "", ""],
];
sources.getRange(`A${sourceRows.length + 4}:C${sourceRows.length + 4}`).merge();
sources.getRange(`A${sourceRows.length + 5}:C${sourceRows.length + 5}`).merge();
body(sources.getRange(`A${sourceRows.length + 4}:C${sourceRows.length + 5}`));
sources.freezePanes.freezeRows(1);
setWidths(sources, [210, 420, 520]);
sources.getRange(`A2:C${sourceRows.length + 5}`).format.rowHeightPx = 44;

for (const sheet of [summary, matrix, sources]) {
  const used = sheet.getUsedRange();
  used.format.font = { ...used.format.font, name: "Aptos" };
}

const summaryPreview = await workbook.render({
  sheetName: "Summary",
  autoCrop: "all",
  scale: 1,
  format: "png",
});
await fs.writeFile(`${outputDir}/summary-preview.png`, new Uint8Array(await summaryPreview.arrayBuffer()));

const matrixPreview = await workbook.render({
  sheetName: "Feature Matrix",
  autoCrop: "all",
  scale: 1,
  format: "png",
});
await fs.writeFile(`${outputDir}/matrix-preview.png`, new Uint8Array(await matrixPreview.arrayBuffer()));

const errors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 300 },
  summary: "final formula error scan",
});
console.log(errors.ndjson);

const check = await workbook.inspect({
  kind: "table",
  range: "Feature Matrix!A1:E8",
  include: "values",
  tableMaxRows: 8,
  tableMaxCols: 5,
});
console.log(check.ndjson);

const xlsx = await SpreadsheetFile.exportXlsx(workbook);
await xlsx.save(outputPath);
console.log(outputPath);
