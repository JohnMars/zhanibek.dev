/* Site-wide chrome: theme toggle, search, header active state, tweaks bridge.
   Vanilla JS — no framework needed for these utilities. */

(function() {
  // ---------- THEME ----------
  const THEME_KEY = "zm.theme";
  function applyTheme(t) {
    if (t === "system" || !t) {
      document.documentElement.removeAttribute("data-theme");
    } else {
      document.documentElement.setAttribute("data-theme", t);
    }
  }
  function currentTheme() {
    return localStorage.getItem(THEME_KEY) || "system";
  }
  function nextTheme(t) {
    return t === "light" ? "dark" : t === "dark" ? "system" : "light";
  }
  function setThemeBtnLabel(btn) {
    const t = currentTheme();
    const label = t === "light" ? "☀" : t === "dark" ? "☾" : "◐";
    btn.textContent = label;
    btn.setAttribute("title", `theme: ${t} (click to cycle)`);
  }
  applyTheme(currentTheme());

  document.addEventListener("DOMContentLoaded", () => {
    const btn = document.querySelector("[data-theme-toggle]");
    if (btn) {
      setThemeBtnLabel(btn);
      btn.addEventListener("click", () => {
        const t = nextTheme(currentTheme());
        localStorage.setItem(THEME_KEY, t);
        applyTheme(t);
        setThemeBtnLabel(btn);
      });
    }

    // ---------- ACTIVE NAV ----------
    const path = location.pathname.split("/").pop() || "index.html";
    document.querySelectorAll("nav.primary a").forEach(a => {
      const href = a.getAttribute("href");
      if (href === path || (path === "" && href === "index.html")) {
        a.setAttribute("aria-current", "page");
      }
    });

    // ---------- DENSITY ----------
    const d = localStorage.getItem("zm.density") || "comfy";
    document.documentElement.setAttribute("data-density", d);

    // ---------- READ-TIME HIDE ----------
    const showReadTime = localStorage.getItem("zm.readtime") !== "false";
    document.documentElement.setAttribute("data-hide-readtime", String(!showReadTime));

    // ---------- SEARCH ----------
    const overlay = document.querySelector("[data-search-overlay]");
    const input   = document.querySelector("[data-search-input]");
    const results = document.querySelector("[data-search-results]");
    const openBtn = document.querySelector("[data-search-open]");

    function buildIndex() {
      const items = [];
      (window.SITE?.articles || []).forEach(a => {
        items.push({
          kind: "article",
          title: a.title,
          excerpt: a.excerpt,
          href: `article.html?slug=${a.slug}`
        });
      });
      (window.SITE?.talks || []).forEach(t => {
        items.push({
          kind: "talk",
          title: t.title,
          excerpt: `${t.venue}, ${t.city}`,
          href: `talk.html?slug=${t.slug}`
        });
      });
      [
        { kind: "page", title: "Resume", excerpt: "Experience, talks, recognition", href: "resume.html" },
        { kind: "page", title: "Now",     excerpt: "What I'm working on this season",     href: "now.html" },
        { kind: "page", title: "Articles",excerpt: "All writing",                          href: "articles.html" },
        { kind: "page", title: "Talks",   excerpt: "Public speaking",                      href: "talks.html" }
      ].forEach(p => items.push(p));
      return items;
    }
    const idx = buildIndex();
    let activeIdx = 0;

    function render(query) {
      if (!results) return;
      const q = query.trim().toLowerCase();
      let list = idx;
      if (q) {
        list = idx.filter(i =>
          i.title.toLowerCase().includes(q) ||
          (i.excerpt || "").toLowerCase().includes(q) ||
          i.kind.includes(q)
        );
      }
      if (list.length === 0) {
        results.innerHTML = `<div class="search-empty">no results for "${q}"</div>`;
        return;
      }
      results.innerHTML = list.slice(0, 12).map((r, i) => `
        <a class="search-result ${i===activeIdx?'active':''}" href="${r.href}" data-idx="${i}">
          <span class="kind">${r.kind}</span>
          <span class="title">${r.title}</span>
        </a>
      `).join("");
    }

    function openSearch() {
      if (!overlay) return;
      overlay.setAttribute("data-open", "true");
      activeIdx = 0;
      render("");
      setTimeout(() => input?.focus(), 30);
    }
    function closeSearch() {
      if (!overlay) return;
      overlay.setAttribute("data-open", "false");
      if (input) input.value = "";
    }
    openBtn?.addEventListener("click", openSearch);
    overlay?.addEventListener("click", e => { if (e.target === overlay) closeSearch(); });
    input?.addEventListener("input", e => { activeIdx = 0; render(e.target.value); });
    input?.addEventListener("keydown", e => {
      const links = results.querySelectorAll(".search-result");
      if (e.key === "ArrowDown") {
        e.preventDefault();
        activeIdx = Math.min(activeIdx + 1, links.length - 1);
        render(input.value);
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        activeIdx = Math.max(activeIdx - 1, 0);
        render(input.value);
      } else if (e.key === "Enter") {
        const a = results.querySelector(`.search-result[data-idx="${activeIdx}"]`);
        if (a) location.href = a.getAttribute("href");
      } else if (e.key === "Escape") {
        closeSearch();
      }
    });
    document.addEventListener("keydown", e => {
      if ((e.key === "k" || e.key === "K") && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        openSearch();
      } else if (e.key === "/" && document.activeElement?.tagName !== "INPUT") {
        e.preventDefault();
        openSearch();
      } else if (e.key === "Escape" && overlay?.getAttribute("data-open") === "true") {
        closeSearch();
      }
    });

    // ---------- READING PROGRESS ----------
    const bar = document.querySelector(".progress");
    if (bar) {
      const onScroll = () => {
        const article = document.querySelector("article.prose");
        if (!article) { bar.style.width = "0%"; return; }
        const rect = article.getBoundingClientRect();
        const total = rect.height - window.innerHeight;
        const scrolled = -rect.top;
        const pct = Math.max(0, Math.min(1, scrolled / total));
        bar.style.width = (pct * 100) + "%";
      };
      window.addEventListener("scroll", onScroll, { passive: true });
      onScroll();
    }
  });

  // expose for tweaks
  window.ZM = {
    setDensity(d)   { localStorage.setItem("zm.density", d); document.documentElement.setAttribute("data-density", d); },
    setReadtime(v)  { localStorage.setItem("zm.readtime", String(!!v)); document.documentElement.setAttribute("data-hide-readtime", String(!v)); },
    setListStyle(v) { localStorage.setItem("zm.liststyle", v); const el = document.querySelector(".post-list"); if (el) { el.classList.remove("cards","table-list"); if (v === "cards") el.classList.add("cards"); else if (v === "table") el.classList.add("table-list"); } },
    setTheme(t)     { localStorage.setItem(THEME_KEY, t); applyTheme(t); const b = document.querySelector("[data-theme-toggle]"); if (b) setThemeBtnLabel(b); },
    getDensity()    { return localStorage.getItem("zm.density")  || "comfy"; },
    getReadtime()   { return localStorage.getItem("zm.readtime") !== "false"; },
    getListStyle()  { return localStorage.getItem("zm.liststyle")|| "list"; },
    getTheme()      { return currentTheme(); }
  };
})();
