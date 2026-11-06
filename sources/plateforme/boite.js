const puppeteer = require("/Users/robinarbona/dev/beta/outils/blocs/node_modules/puppeteer-core");
const D = __dirname; const wait = ms => new Promise(r => setTimeout(r, ms));
// étape (0 = dialogue d'accueil) → catégorie à ouvrir
const VISITES = [[6, "Scène"], [6, "Sprites"], [3, "Sprites"]].sort((a, b) => a[0] - b[0]);
(async () => {
  const b = await puppeteer.launch({ executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", headless: "new" });
  const p = await b.newPage(); await p.setViewport({ width: 1500, height: 1100 });
  await p.goto("http://localhost:8767/tuto-local.html", { waitUntil: "networkidle2", timeout: 120000 });
  await wait(35000);
  const f = p.frames().find(x => x.url().includes("arcade.makecode.com"));
  let etape = 0;
  const suivant = () => f.evaluate(() => { const btn = [...document.querySelectorAll("button, .ui.button, [role=button]")].find(x => /Suivant|^Ok$/i.test((x.textContent || "").trim()) && x.offsetParent); if (btn) btn.click(); return !!btn; });
  for (const [cible, cat] of VISITES) {
    while (etape < cible) { await suivant(); etape++; await wait(2500); }
    const r = await f.evaluate((cat) => { const c = [...document.querySelectorAll("*")].filter(x => x.children.length === 0 && x.textContent.trim() === cat && x.offsetParent).pop(); if (!c) return null; const b = c.getBoundingClientRect(); return [b.x + b.width / 2, b.y + b.height / 2]; }, cat);
    if (r) await p.mouse.click(r[0], r[1]); else console.log("pas trouvé", cat);
    await wait(2500);
    await p.screenshot({ path: `${D}/b${cible}-${cat.slice(0, 4)}.png` });
    await p.mouse.click(1100, 600); await wait(800);
  }
  await b.close();
})();
