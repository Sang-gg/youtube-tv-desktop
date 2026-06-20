(function () {
  'use strict';
  // G. API Compatibility Layer (Tampermonkey-like).
  // Cac quyen duoc cap tu Python: __ALLOW_CLIPBOARD__, __ALLOW_FETCH__.
  const STORE_PREFIX = '__GM__:';

  window.GM_log = function (msg) {
    try {
      console.log('[GM_log] ' + msg);
    } catch (e) {}
  };

  window.GM_addStyle = function (css) {
    const style = document.createElement('style');
    style.textContent = css;
    (document.head || document.documentElement).appendChild(style);
    return style;
  };

  window.GM_getValue = function (key, defaultValue) {
    try {
      const raw = localStorage.getItem(STORE_PREFIX + key);
      return raw === null ? defaultValue : JSON.parse(raw);
    } catch (e) {
      return defaultValue;
    }
  };

  window.GM_setValue = function (key, value) {
    try {
      localStorage.setItem(STORE_PREFIX + key, JSON.stringify(value));
    } catch (e) {}
  };
})();
