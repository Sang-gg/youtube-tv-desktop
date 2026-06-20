(function () {
  'use strict';
  // ---- Gia lap navigator ----
  const define = (obj, prop, value) => {
    try {
      Object.defineProperty(obj, prop, { get: () => value, configurable: true });
    } catch (e) {}
  };
  define(navigator, 'userAgent', __UA__);
  define(navigator, 'platform', 'Linux armv8l');
  define(navigator, 'vendor', 'Samsung Electronics');
  define(navigator, 'maxTouchPoints', 0);
  define(navigator, 'userAgentData', {
    brands: [{ brand: 'Tizen', version: '6.5' }],
    mobile: false,
    platform: 'Tizen',
  });

  // ---- Gia lap window.tizen ----
  if (!window.tizen) {
    window.tizen = {
      application: {
        getCurrentApplication: () => ({
          appInfo: { id: 'org.youtube.tv', version: '1.0.0' },
          exit: () => {},
          hide: () => {},
        }),
      },
      tvinputdevice: {
        registerKey: () => {},
        unregisterKey: () => {},
        getSupportedKeys: () => [],
      },
      systeminfo: { getCapability: () => null },
    };
  }

  // ---- Gia lap window.webapis ----
  if (!window.webapis) {
    window.webapis = {
      avplay: {
        open: () => {},
        play: () => {},
        pause: () => {},
        stop: () => {},
        close: () => {},
        getState: () => 'IDLE',
        setListener: () => {},
      },
      productinfo: {
        getVersion: () => '6.5',
        getModelCode: () => 'YTTV-DESKTOP',
        getFirmware: () => '1.0.0',
        isUdPanelSupported: () => true,
        is8KPanelSupported: () => __IS8K__,
      },
    };
  }

  // ---- Gia lap do phan giai TV ----
  define(window.screen, 'width', __WIDTH__);
  define(window.screen, 'height', __HEIGHT__);
  define(window.screen, 'availWidth', __WIDTH__);
  define(window.screen, 'availHeight', __HEIGHT__);
})();
