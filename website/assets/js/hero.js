document.documentElement.classList.add('js');

document.querySelectorAll('[data-recovery-card]').forEach((card) => {
  const buttons = Array.from(card.querySelectorAll('[data-scenario-button]'));
  const templates = Array.from(card.querySelectorAll('[data-recovery-scenario]'));
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let sequence = 0;

  const selectButton = (scenario) => {
    buttons.forEach((button) => {
      button.setAttribute('aria-pressed', String(button.dataset.scenarioButton === String(scenario)));
    });
  };

  const renderScenario = (scenario, animate) => {
    const template = templates.find((item) => item.dataset.recoveryScenario === String(scenario));
    const content = card.querySelector('[data-recovery-content]');

    if (!template || !content) return [];

    content.replaceChildren(template.content.cloneNode(true));
    content.classList.toggle('is-animating', animate);
    selectButton(scenario);
    return Array.from(content.querySelectorAll('.recovery-line'));
  };

  // Reserve the tallest scenario's height so the card never jumps between scenarios.
  const lockHeight = () => {
    const content = card.querySelector('[data-recovery-content]');
    if (!content) return;
    const current = Array.from(content.childNodes);
    content.style.minHeight = '';
    let tallest = 0;
    templates.forEach((template) => {
      content.replaceChildren(template.content.cloneNode(true));
      tallest = Math.max(tallest, content.offsetHeight);
    });
    content.replaceChildren(...current);
    content.style.minHeight = `${tallest}px`;
  };

  lockHeight();
  let resizeTimer;
  window.addEventListener('resize', () => {
    window.clearTimeout(resizeTimer);
    resizeTimer = window.setTimeout(lockHeight, 150);
  });
  if (document.fonts) document.fonts.ready.then(lockHeight);

  const waitWhileVisible = (duration, currentSequence) => new Promise((resolve) => {
    let remaining = duration;
    let previous = performance.now();

    const tick = () => {
      if (currentSequence !== sequence) {
        resolve(false);
        return;
      }

      const now = performance.now();
      if (!document.hidden) remaining -= now - previous;
      previous = now;

      if (remaining <= 0) {
        resolve(true);
        return;
      }

      window.setTimeout(tick, Math.min(100, remaining));
    };

    window.setTimeout(tick, Math.min(100, remaining));
  });

  const animateScenario = async (scenario, currentSequence) => {
    const lines = renderScenario(scenario, true);

    for (let index = 0; index < lines.length; index += 1) {
      const shouldContinue = await waitWhileVisible(index === 0 ? 80 : 600, currentSequence);
      if (!shouldContinue) return false;
      lines[index].classList.add('is-visible');
    }

    return true;
  };

  const playOnce = async () => {
    const currentSequence = sequence;

    for (let scenario = 0; scenario < templates.length; scenario += 1) {
      const completed = await animateScenario(scenario, currentSequence);
      if (!completed || scenario === templates.length - 1) return;

      const shouldContinue = await waitWhileVisible(2500, currentSequence);
      if (!shouldContinue) return;
    }
  };

  buttons.forEach((button) => {
    button.addEventListener('click', () => {
      sequence += 1;
      const scenario = Number(button.dataset.scenarioButton);

      if (reducedMotion.matches) {
        renderScenario(scenario, false);
        return;
      }

      void animateScenario(scenario, sequence);
    });
  });

  if (reducedMotion.matches) {
    renderScenario(0, false);
  } else {
    void playOnce();
  }
});
