/* ============================================================
   ui.js — 极简交互层（约 4KB，无依赖）
   只做 CSS 做不到的部分：切换、焦点管理、键盘导航。
   设计原则：渐进增强 —— 没有 JS 时页面仍可用。
   ============================================================ */
(function () {
  "use strict";

  /* ---------- 标签页 ---------- */
  function initTabs(root) {
    var tabs = root.querySelectorAll('[role="tab"]');
    if (!tabs.length) return;

    function select(tab) {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.setAttribute("aria-selected", on ? "true" : "false");
        t.tabIndex = on ? 0 : -1;
        var panel = document.getElementById(t.getAttribute("aria-controls"));
        if (panel) panel.hidden = !on;
      });
      tab.focus();
    }

    tabs.forEach(function (tab, i) {
      tab.addEventListener("click", function () { select(tab); });
      tab.addEventListener("keydown", function (e) {
        var next = null;
        if (e.key === "ArrowRight") next = tabs[(i + 1) % tabs.length];
        else if (e.key === "ArrowLeft") next = tabs[(i - 1 + tabs.length) % tabs.length];
        else if (e.key === "Home") next = tabs[0];
        else if (e.key === "End") next = tabs[tabs.length - 1];
        if (next) { e.preventDefault(); select(next); }
      });
    });

    // 初始只留一个选中
    var initial = root.querySelector('[aria-selected="true"]') || tabs[0];
    select(initial);
  }

  /* ---------- 对话框 ---------- */
  // data-dialog-open="id" 打开；[data-dialog-close] 关闭
  function initDialogs() {
    document.addEventListener("click", function (e) {
      var opener = e.target.closest("[data-dialog-open]");
      if (opener) {
        var dlg = document.getElementById(opener.getAttribute("data-dialog-open"));
        if (dlg && dlg.showModal) dlg.showModal();
        return;
      }
      var closer = e.target.closest("[data-dialog-close]");
      if (closer) {
        var d = closer.closest("dialog");
        if (d) d.close();
      }
    });

    // 点遮罩关闭（点 dialog 元素本身 = 点在 backdrop 上）
    document.querySelectorAll("dialog").forEach(function (dlg) {
      dlg.addEventListener("click", function (e) {
        if (e.target === dlg && dlg.hasAttribute("data-backdrop-close")) dlg.close();
      });
    });
  }

  /* ---------- 下拉菜单 ---------- */
  function initMenus() {
    document.addEventListener("click", function (e) {
      var trigger = e.target.closest("[data-menu-toggle]");
      if (trigger) {
        var menu = document.getElementById(trigger.getAttribute("data-menu-toggle"));
        if (menu) {
          var willOpen = menu.hidden;
          closeAllMenus();
          menu.hidden = !willOpen;
          trigger.setAttribute("aria-expanded", willOpen ? "true" : "false");
          if (willOpen) {
            var first = menu.querySelector(".menu__item:not(:disabled)");
            if (first) first.focus();
          }
        }
        return;
      }
      if (!e.target.closest(".menu")) closeAllMenus();
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeAllMenus();
    });
  }

  function closeAllMenus() {
    document.querySelectorAll(".menu").forEach(function (m) { m.hidden = true; });
    document.querySelectorAll("[data-menu-toggle]").forEach(function (t) {
      t.setAttribute("aria-expanded", "false");
    });
  }

  /* ---------- 侧栏抽屉 ---------- */
  function initNavToggle() {
    document.addEventListener("click", function (e) {
      if (e.target.closest(".nav-toggle")) {
        document.body.classList.toggle("nav-open");
      } else if (document.body.classList.contains("nav-open") && !e.target.closest(".sidebar")) {
        document.body.classList.remove("nav-open");
      }
    });
  }

  /* ---------- 开关（role=switch 的替代实现） ---------- */
  // 原生 checkbox + CSS 已够用，这里只同步 aria-checked
  function initSwitches() {
    document.querySelectorAll('[role="switch"]').forEach(function (sw) {
      sw.addEventListener("click", function () {
        var on = sw.getAttribute("aria-checked") === "true";
        sw.setAttribute("aria-checked", on ? "false" : "true");
      });
      sw.addEventListener("keydown", function (e) {
        if (e.key === " " || e.key === "Enter") { e.preventDefault(); sw.click(); }
      });
    });
  }

  /* ---------- Toast ---------- */
  var toastRegion = null;
  function ensureToastRegion() {
    if (toastRegion) return toastRegion;
    toastRegion = document.createElement("div");
    toastRegion.className = "toast-region";
    toastRegion.setAttribute("role", "status");
    toastRegion.setAttribute("aria-live", "polite");
    document.body.appendChild(toastRegion);
    return toastRegion;
  }

  function toast(message, type, ms) {
    var region = ensureToastRegion();
    var el = document.createElement("div");
    el.className = "toast" + (type ? " toast--" + type : "");
    el.textContent = message;
    region.appendChild(el);
    setTimeout(function () {
      el.style.opacity = "0";
      el.style.transition = "opacity .2s";
      setTimeout(function () { el.remove(); }, 220);
    }, ms || 3200);
  }

  /* ---------- 命令面板 ---------- */
  function initCommand() {
    document.querySelectorAll("[data-command]").forEach(function (root) {
      var input = root.querySelector(".command__search input");
      var items = Array.prototype.slice.call(root.querySelectorAll(".command__item"));
      var empty = root.querySelector(".command__empty");
      if (!input) return;

      function filter() {
        var q = input.value.trim().toLowerCase();
        var shown = 0;
        items.forEach(function (it) {
          var hit = !q || it.textContent.toLowerCase().indexOf(q) !== -1;
          it.hidden = !hit;
          if (hit) shown++;
        });
        if (empty) empty.hidden = shown > 0;
        var first = items.filter(function (i) { return !i.hidden; })[0];
        items.forEach(function (i) { i.setAttribute("aria-selected", "false"); });
        if (first) first.setAttribute("aria-selected", "true");
      }

      input.addEventListener("input", filter);

      input.addEventListener("keydown", function (e) {
        var visible = items.filter(function (i) { return !i.hidden; });
        var idx = visible.findIndex(function (i) { return i.getAttribute("aria-selected") === "true"; });
        if (e.key === "ArrowDown") {
          e.preventDefault();
          var n = visible[(idx + 1) % visible.length];
          if (n) { visible.forEach(function (v) { v.setAttribute("aria-selected", "false"); }); n.setAttribute("aria-selected", "true"); n.scrollIntoView({ block: "nearest" }); }
        } else if (e.key === "ArrowUp") {
          e.preventDefault();
          var p = visible[(idx - 1 + visible.length) % visible.length];
          if (p) { visible.forEach(function (v) { v.setAttribute("aria-selected", "false"); }); p.setAttribute("aria-selected", "true"); p.scrollIntoView({ block: "nearest" }); }
        } else if (e.key === "Enter") {
          var cur = visible[idx];
          if (cur) cur.click();
        }
      });

      filter();
    });
  }

  /* ---------- 主题切换 ---------- */
  function initTheme() {
    var stored = null;
    try { stored = localStorage.getItem("theme"); } catch (e) {}
    if (stored) document.documentElement.setAttribute("data-theme", stored);

    document.addEventListener("click", function (e) {
      if (!e.target.closest("[data-theme-toggle]")) return;
      var cur = document.documentElement.getAttribute("data-theme");
      var next = cur === "dark" ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", next);
      try { localStorage.setItem("theme", next); } catch (err) {}
    });
  }

  /* ---------- 启动 ---------- */
  function boot() {
    document.querySelectorAll('[role="tablist"]').forEach(initTabs);
    initDialogs();
    initMenus();
    initNavToggle();
    initSwitches();
    initCommand();
    initTheme();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }

  window.UI = { toast: toast };
})();
