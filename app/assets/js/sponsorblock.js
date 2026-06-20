(function () {
  'use strict';
  const CATS = __CATS__;
  let segments = [];
  let currentId = null;

  const extractId = () => {
    const m = location.href.match(/[?&]v=([\w-]{11})/);
    return m ? m[1] : null;
  };

  const loadSegments = (id) => {
    const url =
      'https://sponsor.ajay.app/api/skipSegments?videoID=' +
      id +
      '&categories=' +
      encodeURIComponent(JSON.stringify(CATS));
    fetch(url)
      .then((r) => (r.ok ? r.json() : []))
      .then((data) => {
        segments = Array.isArray(data) ? data : [];
      })
      .catch(() => {
        segments = [];
      });
  };

  setInterval(() => {
    const id = extractId();
    if (id && id !== currentId) {
      currentId = id;
      loadSegments(id);
    }
    const video = document.querySelector('video');
    if (!video || !segments.length) return;
    const t = video.currentTime;
    for (const seg of segments) {
      const start = seg.segment[0];
      const end = seg.segment[1];
      if (t >= start && t < end - 0.3) {
        video.currentTime = end;
        break;
      }
    }
  }, 500);
})();
