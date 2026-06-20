let state = { cards: [], stats: {} };
let activeId = null;
let showAll = false;
let searchQuery = "";
let statusFilter = "open";
let actionFilter = "all";

const cardList = document.querySelector("#card-list");
const activeCard = document.querySelector("#active-card");
const showAllButton = document.querySelector("#show-all");
const cardSearch = document.querySelector("#card-search");
const statusFilters = document.querySelector("#status-filters");
const actionFilters = document.querySelector("#action-filters");

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "content-type": "application/json" },
    ...options,
  });
  if (!response.ok) throw new Error(await response.text());
  return response.json();
}

function visibleCards() {
  const query = searchQuery.trim().toLowerCase();
  return state.cards.filter((card) => {
    if (!showAll && (card.status === "cleared" || isIgnoredSource(card))) return false;
    if (statusFilter !== "all" && statusFilter !== "open" && card.status !== statusFilter) return false;
    if (statusFilter === "open" && (card.status === "cleared" || isIgnoredSource(card))) return false;
    if (actionFilter !== "all" && card.proposedAction !== actionFilter) return false;
    if (!query) return true;

    return [card.subject, card.senderName, card.senderEmail, card.summary, card.nextAction]
      .filter(Boolean)
      .some((value) => value.toLowerCase().includes(query));
  });
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

function formatDate(value) {
  return new Intl.DateTimeFormat(undefined, { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" }).format(new Date(value));
}

function setCounts() {
  document.querySelector("#active-count").textContent = state.stats.active ?? 0;
  document.querySelector("#queued-count").textContent = state.stats.queued ?? 0;
  document.querySelector("#cleared-count").textContent = state.stats.cleared ?? 0;
}

function countBy(key, cards = state.cards) {
  return cards.reduce((counts, card) => {
    const value = key(card);
    counts[value] = (counts[value] || 0) + 1;
    return counts;
  }, {});
}

function makeChip(label, count, active, onClick) {
  const button = document.createElement("button");
  button.type = "button";
  button.className = `filter-chip${active ? " is-active" : ""}`;
  button.textContent = `${label} ${count}`;
  button.addEventListener("click", onClick);
  return button;
}

function renderFilters() {
  const statusCounts = countBy((card) => card.status);
  const openCount = state.cards.filter((card) => card.status !== "cleared" && !isIgnoredSource(card)).length;
  const countableCards = state.cards.filter((card) => showAll || (card.status !== "cleared" && !isIgnoredSource(card)));
  const actionCounts = countBy((card) => card.proposedAction || "note", countableCards);

  statusFilters.replaceChildren(
    makeChip("Open", openCount, statusFilter === "open", () => {
      statusFilter = "open";
      showAll = false;
      showAllButton.textContent = "All";
      render();
    }),
    makeChip("New", statusCounts.new || 0, statusFilter === "new", () => {
      statusFilter = "new";
      render();
    }),
    makeChip("Queued", statusCounts.queued || 0, statusFilter === "queued", () => {
      statusFilter = "queued";
      showAll = true;
      showAllButton.textContent = "Open";
      render();
    }),
    makeChip("Cleared", statusCounts.cleared || 0, statusFilter === "cleared", () => {
      statusFilter = "cleared";
      showAll = true;
      showAllButton.textContent = "Open";
      render();
    }),
    makeChip("All", state.cards.length, statusFilter === "all", () => {
      statusFilter = "all";
      showAll = true;
      showAllButton.textContent = "Open";
      render();
    }),
  );

  const actions = ["all", ...Object.keys(actionCounts).sort()];
  actionFilters.replaceChildren(
    ...actions.map((action) => makeChip(
      action === "all" ? "Any" : action,
      action === "all" ? visibleCards().length : actionCounts[action],
      actionFilter === action,
      () => {
        actionFilter = action;
        render();
      },
    )),
  );
}

function renderList() {
  const cards = visibleCards();
  if (!cards.some((card) => card.id === activeId)) activeId = cards[0]?.id ?? null;

  if (!cards.length) {
    const empty = document.createElement("div");
    empty.className = "list-empty";
    empty.textContent = "No cards match these filters.";
    cardList.replaceChildren(empty);
    return;
  }

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
      meta.textContent = card.senderName;

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

function renderMetaPill(text, className = "") {
  const pill = document.createElement("span");
  pill.className = `meta-pill ${className}`.trim();
  pill.textContent = text;
  return pill;
}

function renderEmailReader(card) {
  const node = document.createElement("section");
  node.className = "email-reader";

  const header = document.createElement("div");
  header.className = "reader-head";
  const title = document.createElement("h3");
  title.textContent = "Full email";
  header.append(title);

  const content = document.createElement("pre");
  content.className = "reader-body";
  content.textContent = card.fullEmail || "This card only has a preview right now. Ask Codex to fetch the full thread if you want the complete message here.";
  node.append(header, content);

  return node;
}

function renderTopSummary(card) {
  const node = document.createElement("section");
  node.className = "top-summary";

  const title = document.createElement("h3");
  title.textContent = "Summary so far";

  const summary = document.createElement("p");
  summary.textContent = card.summary;

  const details = document.createElement("div");
  details.className = "summary-strip";
  [
    ["From", `${card.senderName} <${card.senderEmail}>`],
    ["Received", formatDate(card.receivedAt)],
    ["Best next move", card.nextAction],
  ].forEach(([label, value]) => {
    const item = document.createElement("div");
    const itemLabel = document.createElement("span");
    itemLabel.textContent = label;
    const itemValue = document.createElement("strong");
    itemValue.textContent = value;
    item.append(itemLabel, itemValue);
    details.append(item);
  });

  node.append(title, summary, details);
  return node;
}

function draftIntoReplyBox(value) {
  const textarea = document.querySelector(".reply-box");
  if (!textarea) return;
  textarea.value = value;
  autosizeTextarea(textarea);
  textarea.focus();
}

function autosizeTextarea(textarea) {
  textarea.style.height = "auto";
  textarea.style.height = `${textarea.scrollHeight + 2}px`;
}

function wireAutosize(textarea) {
  textarea.addEventListener("input", () => autosizeTextarea(textarea));
  requestAnimationFrame(() => autosizeTextarea(textarea));
}

function cleanupDraftText(value) {
  const text = value
    .replace(/\r\n?/g, "\n")
    .split("\n")
    .map((line) => line.replace(/[ \t]+$/g, ""))
    .join("\n")
    .replace(/\n{3,}/g, "\n\n")
    .trim();

  if (!text) return "";

  const lines = text.split("\n");
  if (/^hi [^,\n]+$/i.test(lines[0])) {
    lines[0] = `${lines[0]},`;
  }

  let cleaned = lines.join("\n").trim();
  if (!/\b(best|thanks|thank you|cheers|regards),?\s*\n+\s*ray\s*$/i.test(cleaned)) {
    cleaned = `${cleaned}\n\nBest,\n\nRay`;
  }

  return cleaned;
}

function latestDraftFor(cardId) {
  return (state.drafts || [])
    .filter((draft) => draft.cardId === cardId && ["draft", "gmail_draft", "sent"].includes(draft.status))
    .sort((a, b) => new Date(b.updatedAt) - new Date(a.updatedAt))[0];
}

function renderReplySuggestions(card) {
  const node = document.createElement("section");
  node.className = "reply-suggestions";

  const heading = document.createElement("div");
  heading.className = "suggestion-head";
  const title = document.createElement("h3");
  title.textContent = "Reply suggestions";
  const count = document.createElement("span");
  const suggestions = card.replySuggestions || [];
  count.textContent = `${suggestions.length} drafts`;
  heading.append(title, count);

  const list = document.createElement("div");
  list.className = "suggestion-list";

  if (!suggestions.length) {
    const empty = document.createElement("p");
    empty.className = "suggestion-empty";
    empty.textContent = "No suggestions yet.";
    list.append(empty);
  } else {
    suggestions.forEach((suggestion) => {
      const item = document.createElement("article");
      item.className = "suggestion-card";

      const label = document.createElement("h4");
      label.textContent = suggestion.label;

      const edit = document.createElement("textarea");
      edit.className = "suggestion-edit";
      edit.value = suggestion.body;
      edit.setAttribute("aria-label", `Edit ${suggestion.label} reply`);
      wireAutosize(edit);

      const draft = document.createElement("button");
      draft.type = "button";
      draft.className = "draft-reply";
      draft.textContent = "Clean up into reply box";
      draft.addEventListener("click", () => {
        draftIntoReplyBox(cleanupDraftText(edit.value || suggestion.body));
      });

      item.append(label, edit, draft);
      list.append(item);
    });
  }

  node.append(heading, list);
  return node;
}

function renderComposer(card) {
  const savedDraft = latestDraftFor(card.id);
  const actions = document.createElement("form");
  actions.className = "actions";
  actions.addEventListener("submit", (event) => {
    event.preventDefault();
    const reply = actions.querySelector(".reply-box").value.trim();
    const meta = actions.querySelector(".meta-box").value.trim();
    saveDraft({ reply, codexTask: meta });
  });

  const replyLabel = document.createElement("label");
  replyLabel.className = "composer-field";
  const replyTitle = document.createElement("span");
  replyTitle.textContent = "Reply box";
  const replyBox = document.createElement("textarea");
  replyBox.className = "reply-box";
  replyBox.placeholder = "Drafted replies from above land here. You can edit before applying.";
  replyBox.value = savedDraft?.reply || "";
  wireAutosize(replyBox);
  replyLabel.append(replyTitle, replyBox);

  const taskDetails = document.createElement("details");
  taskDetails.className = "task-drawer";
  if (savedDraft?.codexTask) taskDetails.open = true;
  const taskSummary = document.createElement("summary");
  taskSummary.textContent = "Add Codex task";
  const metaLabel = document.createElement("label");
  metaLabel.className = "composer-field task-field";
  const metaTitle = document.createElement("span");
  metaTitle.textContent = "Optional task";
  const metaBox = document.createElement("textarea");
  metaBox.className = "meta-box";
  metaBox.placeholder = "Optional: tell Codex to archive later, make a task, wait, or do anything beyond saving the reply draft.";
  metaBox.value = savedDraft?.codexTask || "";
  wireAutosize(metaBox);
  metaLabel.append(metaTitle, metaBox);
  taskDetails.append(taskSummary, metaLabel);

  const saveNote = document.createElement("p");
  saveNote.className = "save-note";
  saveNote.textContent = savedDraft?.status === "sent"
    ? `Sent in Gmail ${formatDate(savedDraft.sentAt || savedDraft.updatedAt)} and recorded for future reply learning.`
    : savedDraft?.status === "gmail_draft"
    ? `Pushed to Gmail as a draft ${formatDate(savedDraft.pushedToGmailAt || savedDraft.updatedAt)}. Edit and apply again to save a new local version.`
    : savedDraft
      ? `Saved locally ${formatDate(savedDraft.updatedAt)}. Edit and apply again to update this draft.`
    : "Apply saves a local draft for later sending and keeps this card queued.";

  const apply = document.createElement("button");
  apply.type = "submit";
  apply.className = "apply-button";
  apply.textContent = "Apply";

  const history = document.createElement("div");
  history.className = "history";
  (card.conversation || []).slice(-4).forEach((entry) => {
    const item = document.createElement("div");
    item.className = "history-item";
    item.textContent = `${entry.action}: ${entry.command}`;
    history.append(item);
  });

  actions.append(replyLabel, taskDetails, saveNote, apply, history);
  return actions;
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

  const topSummary = renderTopSummary(card);
  const emailReader = renderEmailReader(card);

  const replySuggestions = renderReplySuggestions(card);

  activeCard.append(head, topSummary, emailReader, replySuggestions, renderComposer(card));
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

async function saveDraft({ reply, codexTask }) {
  if (!activeId || (!reply.trim() && !codexTask.trim())) return;
  await api(`/api/cards/${encodeURIComponent(activeId)}/draft`, {
    method: "POST",
    body: JSON.stringify({ reply: reply.trim(), codexTask: codexTask.trim(), source: "composer" }),
  });
  await load();
  render();
}

function render() {
  setCounts();
  renderFilters();
  renderList();
  renderCard();
}

async function load() {
  state = await api("/api/state");
}

showAllButton.addEventListener("click", () => {
  showAll = !showAll;
  if (!showAll && (statusFilter === "all" || statusFilter === "cleared")) statusFilter = "open";
  showAllButton.textContent = showAll ? "Open" : "All";
  render();
});

cardSearch.addEventListener("input", (event) => {
  searchQuery = event.target.value;
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
