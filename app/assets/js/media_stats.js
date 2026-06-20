(function () {
  'use strict';
  const detectCodec = (mime) => {
    if (!mime) return 'unknown';
    if (/av01/i.test(mime)) return 'AV1';
    if (/vp9|vp09/i.test(mime)) return 'VP9';
    if (/avc1|h264/i.test(mime)) return 'H264';
    return mime;
  };
  const collect = () => {
    const stats = {
      codec: 'unknown',
      resolution: '',
      droppedFrames: 0,
      totalFrames: 0,
      network: '',
    };
    const player = document.querySelector('#movie_player, .html5-video-player');
    const video = document.querySelector('video');
    try {
      if (player && player.getStatsForNerds) {
        const s = player.getStatsForNerds();
        stats.codec = detectCodec(s.codecs || s.video_codec);
        stats.resolution = s.resolution || '';
        stats.network = s.bandwidth_kbps ? s.bandwidth_kbps + ' kbps' : '';
      }
    } catch (e) {}
    if (video) {
      if (!stats.resolution) {
        stats.resolution = video.videoWidth + 'x' + video.videoHeight;
      }
      try {
        const q = video.getVideoPlaybackQuality();
        stats.droppedFrames = q.droppedVideoFrames;
        stats.totalFrames = q.totalVideoFrames;
      } catch (e) {}
    }
    window.__yttvMediaStats = stats;
  };
  setInterval(collect, 1000);
  collect();
})();
