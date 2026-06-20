import { createServer } from "node:http";
import { readFile, writeFile, appendFile, mkdir } from "node:fs/promises";
import { existsSync } from "node:fs";
import { extname, join, normalize } from "node:path";
import { fileURLToPath } from "node:url";

const root = fileURLToPath(new URL(".", import.meta.url));
const publicDir = join(root, "public");
const dataDir = join(root, "data");
const cardsPath = join(dataDir, "cards.json");
const eventsPath = join(dataDir, "events.jsonl");
const draftsPath = join(dataDir, "drafts.json");
const sentRepliesPath = join(dataDir, "sent-replies.json");
const port = Number(process.env.PORT || 4177);

const mimeTypes = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".svg": "image/svg+xml",
};

await mkdir(dataDir, { recursive: true });

async function readJson(path, fallback) {
  if (!existsSync(path)) return fallback;
  return JSON.parse(await readFile(path, "utf8"));
}

async function writeCards(cards) {
  await writeFile(cardsPath, `${JSON.stringify(cards, null, 2)}\n`);
}

async function writeDrafts(drafts) {
  await writeFile(draftsPath, `${JSON.stringify(drafts, null, 2)}\n`);
}

async function logEvent(event) {
  await appendFile(eventsPath, `${JSON.stringify({ at: new Date().toISOString(), ...event })}\n`);
}

function send(res, status, body, type = "application/json; charset=utf-8") {
  res.writeHead(status, { "content-type": type });
  res.end(typeof body === "string" || Buffer.isBuffer(body) ? body : JSON.stringify(body));
}

async function readBody(req) {
  let body = "";
  for await (const chunk of req) body += chunk;
  return body ? JSON.parse(body) : {};
}

function inferCommand(command) {
  const text = command.toLowerCase();
  if (/\b(archive|done|clear|handled)\b/.test(text)) return "archive";
  if (/\b(reply|draft|respond)\b/.test(text)) return "draft";
  if (/\b(wait|later|follow up|follow-up)\b/.test(text)) return "waiting";
  if (/\b(skip|ignore|newsletter|fyi)\b/.test(text)) return "skip";
  if (/\b(task|todo|issue|fix|add)\b/.test(text)) return "task";
  return "note";
}

function nextStatus(action) {
  if (action === "archive" || action === "skip") return "cleared";
  if (action === "waiting" || action === "task" || action === "draft") return "queued";
  return "reviewing";
}

function isIgnoredSource(card) {
  const haystack = [
    card.senderEmail,
    card.senderName,
    card.subject,
    ...(card.tags || []),
  ].filter(Boolean).join(" ").toLowerCase();

  return /\b(newsletter|substack)\b/.test(haystack) || haystack.includes("@substack.com");
}

async function getState() {
  const cards = await readJson(cardsPath, []);
  const drafts = await readJson(draftsPath, []);
  const sentReplies = await readJson(sentRepliesPath, []);
  const active = cards.filter((card) => card.status !== "cleared" && !isIgnoredSource(card)).length;
  const queued = cards.filter((card) => card.status === "queued").length;
  const cleared = cards.filter((card) => card.status === "cleared").length;
  const ignored = cards.filter(isIgnoredSource).length;
  return {
    cards,
    drafts,
    sentReplies,
    stats: {
      total: cards.length,
      active,
      queued,
      drafts: drafts.length,
      sentReplies: sentReplies.length,
      cleared,
      ignored,
    },
    source: {
      provider: "gmail",
      scope: "in:inbox -in:spam -in:trash newer_than:30d",
      syncedAt: new Date().toISOString(),
    },
  };
}

async function handleApi(req, res, path) {
  if (req.method === "GET" && path === "/api/state") {
    return send(res, 200, await getState());
  }

  const commandMatch = path.match(/^\/api\/cards\/([^/]+)\/command$/);
  if (req.method === "POST" && commandMatch) {
    const { command } = await readBody(req);
    if (!command || typeof command !== "string") {
      return send(res, 400, { error: "Command text is required." });
    }

    const cards = await readJson(cardsPath, []);
    const id = decodeURIComponent(commandMatch[1]);
    const card = cards.find((item) => item.id === id);
    if (!card) return send(res, 404, { error: "Card not found." });

    const action = inferCommand(command);
    const entry = { at: new Date().toISOString(), command, action };
    card.conversation = [...(card.conversation || []), entry];
    card.status = nextStatus(action);
    card.updatedAt = entry.at;
    card.proposedAction = action === "note" ? card.proposedAction : action;
    await writeCards(cards);
    await logEvent({ type: "command", cardId: id, command, action, status: card.status });
    return send(res, 200, { card, action });
  }

  const draftMatch = path.match(/^\/api\/cards\/([^/]+)\/draft$/);
  if (req.method === "POST" && draftMatch) {
    const { reply = "", codexTask = "", source = "composer" } = await readBody(req);
    if (typeof reply !== "string" || typeof codexTask !== "string") {
      return send(res, 400, { error: "Reply and Codex task must be text." });
    }

    const trimmedReply = reply.trim();
    const trimmedTask = codexTask.trim();
    if (!trimmedReply && !trimmedTask) {
      return send(res, 400, { error: "Add a reply draft or Codex task first." });
    }

    const cards = await readJson(cardsPath, []);
    const drafts = await readJson(draftsPath, []);
    const id = decodeURIComponent(draftMatch[1]);
    const card = cards.find((item) => item.id === id);
    if (!card) return send(res, 404, { error: "Card not found." });

    const at = new Date().toISOString();
    const existing = drafts.find((item) => item.cardId === id && item.status === "draft");
    const draft = {
      id: existing?.id || `draft-${id}-${Date.now()}`,
      cardId: id,
      status: "draft",
      source,
      reply: trimmedReply,
      codexTask: trimmedTask,
      senderName: card.senderName,
      senderEmail: card.senderEmail,
      subject: card.subject,
      summary: card.summary,
      nextAction: card.nextAction,
      fullEmail: card.fullEmail,
      replySuggestions: card.replySuggestions || [],
      createdAt: existing?.createdAt || at,
      updatedAt: at,
    };

    if (existing) {
      Object.assign(existing, draft);
    } else {
      drafts.push(draft);
    }

    const entry = {
      at,
      action: "draft",
      command: [
        trimmedReply && `Saved reply draft: ${trimmedReply}`,
        trimmedTask && `Codex task: ${trimmedTask}`,
      ].filter(Boolean).join("\n\n"),
      draftId: draft.id,
    };
    card.conversation = [...(card.conversation || []), entry];
    card.status = "queued";
    card.proposedAction = "draft";
    card.updatedAt = at;

    await writeCards(cards);
    await writeDrafts(drafts);
    await logEvent({ type: "draft", cardId: id, draftId: draft.id, source, hasReply: Boolean(trimmedReply), hasCodexTask: Boolean(trimmedTask) });
    return send(res, 200, { card, draft });
  }

  const statusMatch = path.match(/^\/api\/cards\/([^/]+)\/status$/);
  if (req.method === "POST" && statusMatch) {
    const { status } = await readBody(req);
    const allowed = new Set(["new", "reviewing", "queued", "cleared"]);
    if (!allowed.has(status)) return send(res, 400, { error: "Unsupported status." });

    const cards = await readJson(cardsPath, []);
    const id = decodeURIComponent(statusMatch[1]);
    const card = cards.find((item) => item.id === id);
    if (!card) return send(res, 404, { error: "Card not found." });

    card.status = status;
    card.updatedAt = new Date().toISOString();
    await writeCards(cards);
    await logEvent({ type: "status", cardId: id, status });
    return send(res, 200, { card });
  }

  return send(res, 404, { error: "Not found." });
}

async function handleStatic(req, res, path) {
  const requestPath = path === "/" ? "/index.html" : path;
  const normalized = normalize(requestPath).replace(/^(\.\.[/\\])+/, "");
  const filePath = join(publicDir, normalized);
  if (!filePath.startsWith(publicDir)) return send(res, 403, "Forbidden", "text/plain");

  try {
    const body = await readFile(filePath);
    send(res, 200, body, mimeTypes[extname(filePath)] || "application/octet-stream");
  } catch {
    send(res, 404, "Not found", "text/plain; charset=utf-8");
  }
}

const server = createServer(async (req, res) => {
  try {
    const url = new URL(req.url, `http://${req.headers.host}`);
    if (url.pathname.startsWith("/api/")) {
      await handleApi(req, res, url.pathname);
    } else {
      await handleStatic(req, res, url.pathname);
    }
  } catch (error) {
    send(res, 500, { error: error.message });
  }
});

server.listen(port, () => {
  console.log(`Inbox Sweep running at http://localhost:${port}`);
});
