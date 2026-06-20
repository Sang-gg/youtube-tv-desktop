// ==UserScript==
// @name Vi du UserScript
// @version 1.0
// @description Script mau hien thi cach su dung GM API.
// @author YouTube TV Desktop
// @match *://*.youtube.com/*
// @exclude https://www.youtube.com/live_chat*
// @run-at document-idle
// ==/UserScript==

(function () {
  'use strict';
  GM_log('UserScript mau da chay tren ' + location.href);

  // Vi du GM_addStyle: lam dam tieu de.
  GM_addStyle('h1, h2 { font-weight: 700 !important; }');

  // Vi du GM_getValue / GM_setValue: dem so lan chay.
  const count = (GM_getValue('run_count', 0) || 0) + 1;
  GM_setValue('run_count', count);
  GM_log('So lan chay: ' + count);
})();
