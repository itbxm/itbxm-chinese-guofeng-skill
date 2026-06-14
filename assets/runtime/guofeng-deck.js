(() => {
  const deck = document.querySelector("[data-guofeng-deck]");
  if (!deck) return;

  const slides = Array.from(deck.querySelectorAll(".slide"));
  if (!slides.length) return;

  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const state = {
    index: 0,
    overviewOpen: false,
    wheelAmount: 0,
    wheelTimer: 0,
    touchStartX: 0,
    touchStartY: 0,
  };

  const progressFill = document.querySelector("[data-deck-progress-fill]");
  const progressText = document.querySelector("[data-deck-progress-text]");
  const prevButton = document.querySelector("[data-deck-prev]");
  const nextButton = document.querySelector("[data-deck-next]");
  const overviewButton = document.querySelector("[data-deck-overview]");
  const overview = document.querySelector("[data-deck-overview-panel]");
  const overviewGrid = overview?.querySelector("[data-deck-overview-grid]");

  document.body.classList.add("guofeng-deck-ready");
  if (!prefersReducedMotion) {
    document.body.classList.add("guofeng-motion-ready");
  }

  slides.forEach((slide, index) => {
    slide.dataset.slideIndex = String(index);
    slide.setAttribute("tabindex", "-1");
  });

  function clamp(index) {
    return Math.max(0, Math.min(slides.length - 1, index));
  }

  function updateUi(index) {
    state.index = clamp(index);
    slides.forEach((slide, slideIndex) => {
      slide.classList.toggle("is-active", slideIndex === state.index);
      slide.setAttribute("aria-hidden", slideIndex === state.index ? "false" : "true");
    });

    const current = state.index + 1;
    const total = slides.length;
    if (progressFill) progressFill.style.width = `${(current / total) * 100}%`;
    if (progressText) progressText.textContent = `${String(current).padStart(2, "0")} / ${String(total).padStart(2, "0")}`;
    if (prevButton) prevButton.disabled = state.index === 0;
    if (nextButton) nextButton.disabled = state.index === slides.length - 1;

    overviewGrid?.querySelectorAll("[data-overview-jump]").forEach((button) => {
      button.classList.toggle("is-current", Number(button.dataset.overviewJump) === state.index);
    });
  }

  function goTo(index, focusSlide = false) {
    const next = clamp(index);
    const slide = slides[next];
    deck.scrollTo({
      left: slide.offsetLeft,
      behavior: prefersReducedMotion ? "auto" : "smooth",
    });
    updateUi(next);
    if (focusSlide) slide.focus({ preventScroll: true });
  }

  function detectCurrentSlide() {
    const deckLeft = deck.scrollLeft;
    let closest = 0;
    let smallestDistance = Number.POSITIVE_INFINITY;
    slides.forEach((slide, index) => {
      const distance = Math.abs(slide.offsetLeft - deckLeft);
      if (distance < smallestDistance) {
        closest = index;
        smallestDistance = distance;
      }
    });
    updateUi(closest);
  }

  function buildOverview() {
    if (!overviewGrid || overviewGrid.children.length) return;
    slides.forEach((slide, index) => {
      const title = slide.querySelector(".title, .section-title, h1, h2")?.textContent?.trim() || `Slide ${index + 1}`;
      const kicker = slide.querySelector(".kicker, .guofeng-kicker")?.textContent?.trim() || "Guofeng";
      const button = document.createElement("button");
      button.type = "button";
      button.className = "deck-overview-card";
      button.dataset.overviewJump = String(index);
      button.innerHTML = `<span>${String(index + 1).padStart(2, "0")}</span><strong>${escapeHtml(title)}</strong><em>${escapeHtml(kicker)}</em>`;
      button.addEventListener("click", () => {
        closeOverview();
        goTo(index, true);
      });
      overviewGrid.append(button);
    });
  }

  function escapeHtml(value) {
    return value.replace(/[&<>"']/g, (char) => ({
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#039;",
    }[char]));
  }

  function openOverview() {
    if (!overview) return;
    buildOverview();
    state.overviewOpen = true;
    overview.hidden = false;
    document.body.classList.add("guofeng-overview-open");
    updateUi(state.index);
    overview.querySelector("[data-deck-overview-close]")?.focus({ preventScroll: true });
  }

  function closeOverview() {
    if (!overview) return;
    state.overviewOpen = false;
    overview.hidden = true;
    document.body.classList.remove("guofeng-overview-open");
    overviewButton?.focus({ preventScroll: true });
  }

  function toggleOverview() {
    if (state.overviewOpen) closeOverview();
    else openOverview();
  }

  prevButton?.addEventListener("click", () => goTo(state.index - 1, true));
  nextButton?.addEventListener("click", () => goTo(state.index + 1, true));
  overviewButton?.addEventListener("click", toggleOverview);
  overview?.querySelector("[data-deck-overview-close]")?.addEventListener("click", closeOverview);

  deck.addEventListener("scroll", () => {
    window.requestAnimationFrame(detectCurrentSlide);
  }, { passive: true });

  window.addEventListener("keydown", (event) => {
    const tagName = document.activeElement?.tagName;
    if (tagName === "INPUT" || tagName === "TEXTAREA" || tagName === "SELECT") return;

    if (event.key === "Escape") {
      event.preventDefault();
      toggleOverview();
      return;
    }

    if (state.overviewOpen) return;

    if (event.key === "ArrowRight" || event.key === "PageDown") {
      event.preventDefault();
      goTo(state.index + 1, true);
    } else if (event.key === "ArrowLeft" || event.key === "PageUp") {
      event.preventDefault();
      goTo(state.index - 1, true);
    } else if (event.key === "Home") {
      event.preventDefault();
      goTo(0, true);
    } else if (event.key === "End") {
      event.preventDefault();
      goTo(slides.length - 1, true);
    }
  });

  window.addEventListener("wheel", (event) => {
    if (state.overviewOpen || window.innerWidth <= 760) return;
    state.wheelAmount += event.deltaX + event.deltaY;
    window.clearTimeout(state.wheelTimer);
    state.wheelTimer = window.setTimeout(() => {
      state.wheelAmount = 0;
    }, 160);

    if (Math.abs(state.wheelAmount) > 70) {
      event.preventDefault();
      goTo(state.index + (state.wheelAmount > 0 ? 1 : -1), true);
      state.wheelAmount = 0;
    }
  }, { passive: false });

  window.addEventListener("touchstart", (event) => {
    const touch = event.touches[0];
    state.touchStartX = touch.clientX;
    state.touchStartY = touch.clientY;
  }, { passive: true });

  window.addEventListener("touchend", (event) => {
    if (state.overviewOpen || window.innerWidth <= 760) return;
    const touch = event.changedTouches[0];
    const dx = touch.clientX - state.touchStartX;
    const dy = touch.clientY - state.touchStartY;
    if (Math.abs(dx) > 58 && Math.abs(dx) > Math.abs(dy) * 1.2) {
      goTo(state.index + (dx < 0 ? 1 : -1), true);
    }
  }, { passive: true });

  updateUi(0);
})();
