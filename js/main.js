(function () {
  "use strict";

  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".main-nav");

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", nav.classList.contains("open") ? "true" : "false");
    });

    document.addEventListener("click", function (e) {
      if (!nav.contains(e.target) && !toggle.contains(e.target)) {
        nav.classList.remove("open");
      }
    });
  }

  var langSwitch = document.querySelector(".lang-switch");
  var langBtn = langSwitch && langSwitch.querySelector(".lang-btn");
  if (langSwitch && langBtn) {
    langBtn.addEventListener("click", function (e) {
      e.stopPropagation();
      var open = langSwitch.classList.toggle("open");
      langBtn.setAttribute("aria-expanded", open ? "true" : "false");
    });
    document.addEventListener("click", function (e) {
      if (!langSwitch.contains(e.target)) {
        langSwitch.classList.remove("open");
        langBtn.setAttribute("aria-expanded", "false");
      }
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") {
        langSwitch.classList.remove("open");
        langBtn.setAttribute("aria-expanded", "false");
      }
    });
  }

  var yearEl = document.getElementById("year");
  if (yearEl) {
    yearEl.textContent = new Date().getFullYear();
  }

  /* ---------- 通用入场动画系统 ----------
     给任意元素加 .reveal / .reveal-left / .reveal-right / .reveal-zoom
     进入视口时加 .visible 触发过渡；用 --d 变量错峰（如 style="--d:.1s"）
     标题逐行入场：.hl-line > span 由父级 .visible 触发 */
  var revealSel = ".reveal, .reveal-left, .reveal-right, .reveal-zoom";
  var revealEls = document.querySelectorAll(revealSel);

  function revealNow(items) {
    items.forEach(function (el) {
      el.classList.add("visible");
    });
  }

  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("visible");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );
    revealEls.forEach(function (el) {
      io.observe(el);
    });
  } else {
    revealNow(revealEls);
  }

  /* header 滚动后加 scrolled 态 */
  var header = document.querySelector(".site-header");
  if (header) {
    var onHeaderScroll = function () {
      header.classList.toggle("scrolled", window.pageYOffset > 40);
    };
    window.addEventListener("scroll", onHeaderScroll, { passive: true });
    onHeaderScroll();
  }

  /* 平滑滚动到站内锚点 */
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener("click", function (e) {
      var id = a.getAttribute("href");
      if (id.length < 2) return;
      var target = document.querySelector(id);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    });
  });

  /* ---------- 首页 hero 入场与视差 ---------- */
  var hero = document.querySelector(".hero");
  var pEls = document.querySelectorAll(".hero .hero-copy > *");
  var hwEl = document.querySelector(".hero-watermark");

  if (hero && "IntersectionObserver" in window) {
    var heroVisible = false;
    var settled = false;
    var ioHero = new IntersectionObserver(function (entries) {
      heroVisible = entries[0].isIntersecting;
    }, { threshold: 0 });
    ioHero.observe(hero);

    var ticking = false;
    var onScroll = function () {
      if (!heroVisible || !settled) return;
      ticking = false;
      var y = window.pageYOffset;
      if (y > 900) return;
      pEls.forEach(function (el) {
        el.style.transform = "translateY(" + y * 0.14 + "px)";
      });
      if (hwEl) hwEl.style.transform = "translateY(calc(-50% + " + y * 0.05 + "px))";
    };

    window.addEventListener(
      "scroll",
      function () {
        if (!ticking) {
          ticking = true;
          requestAnimationFrame(onScroll);
        }
      },
      { passive: true }
    );

    setTimeout(function () {
      settled = true;
    }, 2600);
  }

  /* ---------- 表单模拟提交 ---------- */
  var forms = document.querySelectorAll("form[data-success]");
  forms.forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var success = document.getElementById(form.getAttribute("data-success"));
      if (success) {
        success.style.display = "block";
        form.reset();
      }
    });
  });

  /* ---------- 相册 tab ---------- */
  var tabs = document.querySelectorAll(".gallery-tab");
  tabs.forEach(function (tab) {
    tab.addEventListener("click", function () {
      var target = tab.getAttribute("data-pane");
      var group = tab.closest(".gallery");
      if (!group) return;
      group.querySelectorAll(".gallery-tab").forEach(function (t) {
        t.classList.toggle("active", t === tab);
      });
      group.querySelectorAll(".gallery-pane").forEach(function (p) {
        p.classList.toggle("active", p.getAttribute("data-pane") === target);
      });
    });
  });
})();