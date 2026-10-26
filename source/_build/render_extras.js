// Рендер аватара, обложек хайлайтов и шаблонов сторис: node render_extras.js
const { chromium } = require('playwright');
const path = require('path');
const items = require('./extras.json');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 2000 } });
  await page.goto('file://' + path.join(__dirname, 'html', 'extras.html'));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForLoadState('networkidle');
  for (const [id, out] of items) {
    const el = await page.$('#' + id); await el.scrollIntoViewIfNeeded(); await page.waitForTimeout(250);
    await el.screenshot({ path: out, type: 'jpeg', quality: 92 });
  }
  await browser.close();
  console.log('ok', items.length);
})();
