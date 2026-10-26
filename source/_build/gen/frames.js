// Покадровый рендер рилса: node frames.js page.html outdir fps nA nB
// Кадры 0..nA-1 — ведущий (кадры клипа Seedance из outdir/host/), затем nB кадров демо и финала.
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [page_, out, fps, nA, nB] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto('file://' + path.resolve(page_));
  await page.evaluate(() => document.fonts.ready);
  let k = 0;
  for (let i = 0; i < +nA; i++, k++) {
    const src = 'file://' + path.resolve(out, 'host', String(i + 1).padStart(5, '0') + '.jpg');
    await page.evaluate(async ([s, t]) => { await window.setFrame(s); window.renderHost(t, true); }, [src, i / +fps]);
    await page.screenshot({ path: path.join(out, 'f', String(k).padStart(5, '0') + '.jpg'), type: 'jpeg', quality: 92 });
  }
  for (let i = 0; i < +nB; i++, k++) {
    await page.evaluate(t => { window.renderHost(0, false); window.render(t); }, i / +fps);
    await page.screenshot({ path: path.join(out, 'f', String(k).padStart(5, '0') + '.jpg'), type: 'jpeg', quality: 92 });
  }
  await browser.close();
  console.log('frames', k);
})();
