const $ = (s, r = document) => r.querySelector(s);

const overlay = $("#search-overlay");
const input = $("#search-input");
const results = $("#search-results");
const sidebar = $("#sidebar");
const article = $("#article");
const kicker = $("#kicker");

let pack = null;

function openSearch() {
  overlay.classList.add("open");
  input.value = "";
  results.innerHTML = "";
  input.focus();
}
function closeSearch() {
  overlay.classList.remove("open");
}

$("#search-open")?.addEventListener("click", openSearch);
$("#search-open-mobile")?.addEventListener("click", openSearch);
$("#menu-toggle")?.addEventListener("click", () => sidebar.classList.toggle("open"));
overlay?.addEventListener("click", (e) => {
  if (e.target === overlay) closeSearch();
});

document.addEventListener("keydown", (e) => {
  if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
    e.preventDefault();
    openSearch();
  } else if (e.key === "/" && !["INPUT", "TEXTAREA"].includes(document.activeElement.tagName)) {
    e.preventDefault();
    openSearch();
  } else if (e.key === "Escape") {
    closeSearch();
    sidebar?.classList.remove("open");
  }
});

function slugFromPath() {
  const path = location.pathname.replace(/\/+$/, "") || "/";
  if (path === "/" || path === "/index.html") return "home";
  return path.replace(/^\//, "").replace(/\.html$/, "");
}

function setActive(slug) {
  document.querySelectorAll(".nav-link").forEach((a) => {
    a.classList.toggle("active", a.getAttribute("href") === `/${slug}` || (slug === "home" && a.getAttribute("href") === "/"));
  });
}

function render(slug) {
  if (!pack) return;
  const page = pack.pages[slug] || pack.pages.home;
  const meta = pack.meta[slug] || pack.meta.home;
  kicker.textContent = meta.kicker;
  article.innerHTML = page + pack.footer;
  document.title = `${meta.title} — 2026 AI Interview Handbook`;
  setActive(slug);
  sidebar?.classList.remove("open");
  window.scrollTo(0, 0);
}

function renderHits(q) {
  const query = q.trim().toLowerCase();
  if (query.length < 2) {
    results.innerHTML = '<div class="search-hit"><small>Type at least 2 characters</small></div>';
    return;
  }
  const hits = [];
  for (const item of pack.search) {
    const hay = `${item.title} ${item.group} ${item.text}`.toLowerCase();
    if (!hay.includes(query)) continue;
    const i = item.text.toLowerCase().indexOf(query);
    const start = Math.max(0, i - 60);
    const snippet = item.text.slice(start, start + 140).replace(/\s+/g, " ");
    hits.push({ ...item, snippet });
    if (hits.length >= 20) break;
  }
  if (!hits.length) {
    results.innerHTML = '<div class="search-hit"><small>No matches</small></div>';
    return;
  }
  results.innerHTML = hits
    .map(
      (h, i) =>
        `<a class="search-hit${i === 0 ? " active" : ""}" href="${h.href}"><strong>${h.title}</strong><small>${h.group} — ${h.snippet}</small></a>`
    )
    .join("");
}

input?.addEventListener("input", (e) => renderHits(e.target.value));
input?.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    const first = results.querySelector(".search-hit");
    if (first) {
      closeSearch();
      history.pushState({}, "", first.getAttribute("href"));
      render(slugFromPath());
    }
  }
});

document.addEventListener("click", (e) => {
  const a = e.target.closest("a");
  if (!a) return;
  const href = a.getAttribute("href");
  if (!href || href.startsWith("http") || href.startsWith("mailto:") || href.startsWith("#")) return;
  if (a.origin && a.origin !== location.origin) return;
  if (!pack) return;
  e.preventDefault();
  closeSearch();
  history.pushState({}, "", href);
  render(slugFromPath());
});

window.addEventListener("popstate", () => render(slugFromPath()));

async function loadPack() {
  const res = await fetch("/content.json.gz");
  if (!res.ok) throw new Error("content pack missing");
  let text;
  if ("DecompressionStream" in window) {
    const stream = res.body.pipeThrough(new DecompressionStream("gzip"));
    text = await new Response(stream).text();
  } else {
    const buf = await res.arrayBuffer();
    text = await inflateFallback(buf);
  }
  pack = JSON.parse(text);
}

async function inflateFallback(buf) {
  throw new Error("Please use a current browser (Chrome, Firefox, Safari 16.4+, Edge).");
}

loadPack()
  .then(() => render(slugFromPath()))
  .catch((err) => {
    console.warn(err);
    kicker.textContent = "2026 AI Interview Handbook";
  });
