const puppeteer = require("/Users/robinarbona/dev/beta/outils/blocs/node_modules/puppeteer-core");
const D = __dirname; const wait = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const b = await puppeteer.launch({ executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", headless: "new" });
  const p = await b.newPage(); await p.setViewport({ width: 1500, height: 950 });
  p.on("console", m => { const t = m.text(); if (/msg|error/i.test(t)) console.log(t.slice(0, 250)); });
  await p.goto("http://localhost:8767/tuto-local.html", { waitUntil: "networkidle2", timeout: 120000 });
  await wait(15000);

  await wait(20000);
  const f = p.frames().find(x => x.url().includes("arcade.makecode.com"));
  await p.screenshot({ path: `${D}/intro.png` }); if (process.argv[2] === "intro") { await b.close(); return; }
  for (let i = 0; i < 13; i++) {
    const h = await f.$(".tutorial-hint-button, button[aria-label*=ndice], button[title*=ndice]");
    if (h) { await h.click(); await wait(2500); }
    await p.screenshot({ path: `${D}/t${String(i).padStart(2, "0")}.png` });
    if (h) { await f.evaluate(() => { const x = document.querySelector(".tutorial-callout .close, .tutorial-hint .close, [aria-label=Fermer], [title=Fermer], .hint-close, .icon.close"); if (x) x.click(); else document.querySelector(".tutorial-hint-button")?.click(); }); await wait(800); }
    const ok = await f.evaluate(() => {
      const btn = [...document.querySelectorAll("button, .ui.button, [role=button]")].find(x => /Suivant|^Ok$|Terminé/i.test((x.textContent || x.getAttribute("aria-label") || "").trim()) && x.offsetParent);
      if (btn) { btn.click(); return (btn.getAttribute("aria-label") || btn.textContent).trim(); } return null;
    });
    console.log("étape", i, ok);
    await wait(2500);
  }
  await b.close();
})();
