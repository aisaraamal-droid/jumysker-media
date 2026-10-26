// Рендер слайдов каруселей в JPEG 1080x1350: node render.js [p01 p02 ...]
const { chromium } = require('playwright');
const path = require('path');
const jobs = require('./jobs.json');
(async () => {
  const only = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  for (const job of jobs) {
    if (only.length && !only.some(id => job.html.endsWith(id + '.html'))) continue;
    await page.goto('file://' + job.html);
    await page.evaluate(() => document.fonts.ready);
    await page.waitForLoadState('networkidle');
    const slides = await page.$$('.slide');
    const overflow = await page.$$eval('.slide', els => els.map(el => {
      const b = el.querySelector('.body'), r = b.getBoundingClientRect();
      const rs = [...b.children].map(c => c.getBoundingClientRect());
      return Math.max(0, Math.round(Math.max(...rs.map(x => x.bottom)) - r.bottom), Math.round(r.top - Math.min(...rs.map(x => x.top))));
    }));
    for (let i = 0; i < slides.length; i++) {
      await slides[i].screenshot({ path: path.join(job.out, `slide-${String(i + 1).padStart(2, '0')}.jpg`), type: 'jpeg', quality: 92 });
      if (overflow[i] > 0) console.log('ПЕРЕПОЛНЕНИЕ', path.basename(job.html), 'слайд', i + 1, overflow[i] + 'px');
    }
    console.log('ok', path.basename(job.html), slides.length);
  }
  await browser.close();
})();
