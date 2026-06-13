import { spawn } from "node:child_process";
import { readFile, writeFile } from "node:fs/promises";

const port = 4187;
const base = `http://localhost:${port}`;
const cardsUrl = new URL("../data/cards.json", import.meta.url);
const eventsUrl = new URL("../data/events.jsonl", import.meta.url);
const originalCards = await readFile(cardsUrl, "utf8");
const originalEvents = await readFile(eventsUrl, "utf8");
const server = spawn(process.execPath, ["server.mjs"], {
  cwd: new URL("..", import.meta.url),
  env: { ...process.env, PORT: String(port) },
  stdio: ["ignore", "pipe", "pipe"],
});

async function waitForServer() {
  const started = Date.now();
  while (Date.now() - started < 5000) {
    try {
      const response = await fetch(`${base}/api/state`);
      if (response.ok) return;
    } catch {
      await new Promise((resolve) => setTimeout(resolve, 100));
    }
  }
  throw new Error("Server did not start.");
}

async function json(path, options) {
  const response = await fetch(`${base}${path}`, {
    headers: { "content-type": "application/json" },
    ...options,
  });
  if (!response.ok) throw new Error(`${path} failed: ${await response.text()}`);
  return response.json();
}

try {
  await waitForServer();

  const state = await json("/api/state");
  if (state.source.provider !== "gmail") throw new Error("Expected Gmail source metadata.");
  if (state.cards.length < 8) throw new Error("Expected seeded inbox cards.");
  if (!state.cards.every((card) => card.summary && card.nextAction && card.preview)) {
    throw new Error("Every card needs summary, nextAction, and preview.");
  }

  const target = state.cards.find((card) => card.status !== "cleared");
  const result = await json(`/api/cards/${encodeURIComponent(target.id)}/command`, {
    method: "POST",
    body: JSON.stringify({ command: "Draft a reply and queue this locally" }),
  });
  if (result.action !== "draft") throw new Error("Command interpreter did not infer draft.");
  if (result.card.status !== "queued") throw new Error("Draft command should queue the card.");

  const html = await fetch(base).then((response) => response.text());
  if (!html.includes("Inbox Sweep")) throw new Error("HTML shell did not render.");

  const events = await readFile(new URL("../data/events.jsonl", import.meta.url), "utf8");
  if (!events.includes(target.id)) throw new Error("Filesystem event log was not updated.");

  console.log("Validation passed: Gmail snapshot loads, UI shell serves, commands update cards, and events persist.");
} finally {
  server.kill();
  await writeFile(cardsUrl, originalCards);
  await writeFile(eventsUrl, originalEvents);
}
