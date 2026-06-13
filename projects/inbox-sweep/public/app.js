let state = { cards: [], stats: {} };
let activeId = null;
let showAll = false;

const cardList = document.querySelector("#card-list");
const activeCard = document.querySelector("#active-card");
const showAllButton = document.querySelector("#show-all");

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "content-type": "application/json" },
    ...options,
  });
  if (!response.ok) throw new Error(await response.text());
  return response.json();
}

function visibleCards() {
  return state.cards.filter((card) => showAll || card.status !== "cleared");
}

function formatDate(value) {
  return new Intl.DateTimeFormat(undefined, { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" }).format(new Date(value));
}

function setCounts() {
  document.querySelector("#active-count").textContent = state.stats.active ?? 0;
  document.querySelector("#queued-count").textContent = state.stats.queued ?? 0;
  document.querySelector("#cleared-count").textContent = state.stats.cleared ?? 0;
}

function renderList() {
  const cards = visibleCards();
  if (!cards.some((card) => card.id === activeId)) activeId = cards[0]?.id ?? state.cards[0]?.id ?? null;

  cardList.replaceChildren(
    ...cards.map((card) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = `list-item${card.id === activeId ? " is-active" : ""}`;
      button.addEventListener("click", () => {
        activeId = card.id;
        render();
      });

      const subject = document.createElement("span");
      subject.className = "list-subject";
      subject.textContent = card.subject;

      const meta = document.createElement("span");
      meta.className = "list-meta";
      meta.innerHTML = `<span>${card.senderName}</span><span class="status ${card.status}">${card.status}</span>`;

      button.append(subject, meta);
      return button;
    }),
  );
}

function panel(title, body, className = "") {
  const node = document.createElement("section");
  node.className = `panel ${className}`.trim();
  const heading = document.createElement("h3");
  heading.textContent = title;
  const content = document.createElement("p");
  content.textContent = body;
  node.append(heading, content);
  return node;
}

function renderCard() {
  const card = state.cards.find((item) => item.id === activeId);
  activeCard.replaceChildren();

  if (!card) {
    activeCard.className = "message-card empty";
    activeCard.textContent = "Inbox cleared.";
    return;
  }

  activeCard.className = "message-card";

  const head = document.createElement("div");
  head.className = "card-head";
  const titleWrap = document.createElement("div");
  const sender = document.createElement("p");
  sender.className = "sender";
  sender.textContent = `${card.senderName} <${card.senderEmail}>`;
  const title = document.createElement("h2");
  title.textContent = card.subject;
  titleWrap.append(sender, title);
  const date = document.createElement("span");
  date.className = "date";
  date.textContent = formatDate(card.receivedAt);
  head.append(titleWrap, date);

  const grid = document.createElement("div");
  grid.className = "summary-grid";
  grid.append(
    panel("About", card.summary),
    panel("Next action", card.nextAction),
    panel("Draft seed", card.draftSeed, "draft"),
  );

  const preview = document.createElement("section");
  preview.className = "body-preview";
  preview.textContent = card.preview;

  const actions = document.createElement("section");
  actions.className = "actions";
  const quickActions = document.createElement("div");
  quickActions.className = "quick-actions";
  [
    "Done and archive locally",
    "Draft a reply",
    "Wait for later",
    "Make this a task",
    "Skip as FYI",
  ].forEach((label) => {
    const button = document.createElement("button");
    button.type = "button";
    button.dataset.command = label;
    button.textContent = label;
    button.addEventListener("click", () => submitCommand(label));
    quickActions.append(button);
  });

  const talk = document.createElement("form");
  talk.className = "talk";
  talk.addEventListener("submit", (event) => {
    event.preventDefault();
    const textarea = talk.querySelector("textarea");
    submitCommand(textarea.value);
    textarea.value = "";
  });
  const textarea = document.createElement("textarea");
  textarea.name = "command";
  textarea.placeholder = "Tell Codex what to do with this email";
  const apply = document.createElement("button");
  apply.type = "submit";
  apply.textContent = "Apply";
  talk.append(textarea, apply);

  const history = document.createElement("div");
  history.className = "history";
  (card.conversation || []).slice(-4).forEach((entry) => {
    const item = document.createElement("div");
    item.className = "history-item";
    item.textContent = `${entry.action}: ${entry.command}`;
    history.append(item);
  });

  actions.append(quickActions, talk, history);
  activeCard.append(head, grid, preview, actions);
}

async function submitCommand(command) {
  if (!activeId || !command.trim()) return;
  await api(`/api/cards/${encodeURIComponent(activeId)}/command`, {
    method: "POST",
    body: JSON.stringify({ command: command.trim() }),
  });
  await load();
  const cards = visibleCards();
  const index = cards.findIndex((card) => card.id === activeId);
  if (state.cards.find((card) => card.id === activeId)?.status === "cleared") {
    activeId = cards[index + 1]?.id || cards[index - 1]?.id || cards[0]?.id || null;
  }
  render();
}

function render() {
  setCounts();
  renderList();
  renderCard();
}

async function load() {
  state = await api("/api/state");
}

showAllButton.addEventListener("click", () => {
  showAll = !showAll;
  showAllButton.textContent = showAll ? "Open" : "All";
  render();
});

document.addEventListener("keydown", (event) => {
  const tag = document.activeElement?.tagName;
  if (tag === "TEXTAREA" || tag === "INPUT") return;
  const cards = visibleCards();
  const index = cards.findIndex((card) => card.id === activeId);
  if (event.key === "j" || event.key === "ArrowDown") activeId = cards[Math.min(index + 1, cards.length - 1)]?.id || activeId;
  if (event.key === "k" || event.key === "ArrowUp") activeId = cards[Math.max(index - 1, 0)]?.id || activeId;
  render();
});

await load();
render();
