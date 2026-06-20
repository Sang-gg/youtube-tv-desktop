(function () {
  'use strict';
  const ENDPOINTS = __ENDPOINTS__;
  const matches = (u) => ENDPOINTS.some((e) => (u || '').indexOf(e) !== -1);
  const report = (src, u) => {
    try {
      console.info('[YTTV_API]' + src + '|' + u);
    } catch (e) {}
  };

  // Hook fetch.
  const origFetch = window.fetch;
  window.fetch = function (input, init) {
    const url = typeof input === 'string' ? input : input && input.url;
    if (matches(url)) report('fetch', url);
    return origFetch.apply(this, arguments);
  };

  // Hook XMLHttpRequest.
  const origOpen = XMLHttpRequest.prototype.open;
  XMLHttpRequest.prototype.open = function (method, url) {
    if (matches(url)) report('xhr', url);
    return origOpen.apply(this, arguments);
  };
})();
