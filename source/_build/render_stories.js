// Рендер сторис-анонсов: [id, путь, прозрачный фон?] из stories_auto.json
const { chromium } = require('playwright');
const path = require('path');
const jobs = require('./stories_auto.json');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 2000 } });
  await page.goto('file://' + path.join(__dirname, 'html', 'stories_auto.html'));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForLoadState('networkidle');
  for (const [id, out, transparent] of jobs) {
    const el = await page.$('#' + id); await el.scrollIntoViewIfNeeded(); await page.waitForTimeout(150);
    await el.screenshot(transparent ? { path: out, omitBackground: true } : { path: out, type: 'jpeg', quality: 92 });
  }
  await browser.close();
})();
