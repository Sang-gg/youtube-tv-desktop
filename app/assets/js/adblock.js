(function () {
  'use strict';
  // B. Cosmetic filtering: tiem CSS an quang cao.
  const style = document.createElement('style');
  style.textContent = '__CSS__';
  (document.head || document.documentElement).appendChild(style);

  const SELECTORS = __SELECTORS__;

  // C. JavaScript filtering: xoa phan tu quang cao + skip overlay.
  const clean = () => {
    SELECTORS.forEach((sel) => {
      document.querySelectorAll(sel).forEach((el) => el.remove());
    });
    // Tu dong bam nut skip neu co.
    const skip = document.querySelector(
      '.ytp-ad-skip-button, .ytp-ad-skip-button-modern'
    );
    if (skip) skip.click();
    // Tua qua quang cao video neu dang phat.
    const player = document.querySelector('video');
    if (player && document.querySelector('.ad-showing, .ytp-ad-player-overlay')) {
      try {
        player.currentTime = player.duration;
      } catch (e) {}
    }
  };
  const observer = new MutationObserver(clean);
  observer.observe(document.documentElement, { childList: true, subtree: true });
  clean();
})();
