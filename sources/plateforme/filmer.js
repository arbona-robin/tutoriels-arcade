// Filme le simulateur (version pilote automatique) et lit les blocs de la version normale.
const fs = require("fs");
const puppeteer = require("/Users/robinarbona/dev/beta/outils/blocs/node_modules/puppeteer-core");
const D = __dirname; const wait = ms => new Promise(r => setTimeout(r, ms));
const mode = process.argv[2]; // "film" ou "blocs"
(async () => {
  const b = await puppeteer.launch({ executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", headless: "new" });
  const p = await b.newPage(); await p.setViewport({ width: 1500, height: 1000 });
  p.on("console", m => { const t = m.text(); if (/import|error TS/i.test(t)) console.log(t.slice(0, 200)); });
  await p.goto("http://localhost:8767/projet-local.html" + (mode === "film" ? "?demo" : ""), { waitUntil: "networkidle2", timeout: 120000 });
  if (mode === "blocs") {
    await wait(30000);
    const f0 = p.frames().find(x => x.url().includes("arcade.makecode.com") && !x.url().includes("simulator"));
    await f0.evaluate(() => [...document.querySelectorAll("[title]")].find(x => x.getAttribute("title") === "Convertir le code en Blocs").click());
    await wait(8000);
    const f = p.frames().find(x => x.url().includes("arcade.makecode.com") && !x.url().includes("simulator"));
    const txt = await f.evaluate(() => [...document.querySelectorAll("g.blocklyDraggable")].map(g => [...g.querySelectorAll("text")].filter(t => t.closest("g.blocklyDraggable") === g).map(t => t.textContent).join(" ")).filter(s => s.trim()));
    console.log(txt.join("\n"));
    await p.screenshot({ path: D + "/projet-blocs.png" });
    await b.close(); return;
  }
  await wait(12000);
  // agrandir le simulateur : bouton plein écran de l'éditeur
  const ed = p.frames().find(x => x.url().includes("arcade.makecode.com") && !/simulator/.test(x.url()));
  await ed.evaluate(() => { const r = document.querySelector(".fullscreen-button, [title*=plein], [aria-label*=plein], [aria-label*=Plein]"); if (r) r.click(); });
  await wait(3000);
  await p.screenshot({ path: D + "/plein.png" });
  // position du canevas dans la page
  const rect = async () => {
    const sims = p.frames().filter(x => /simulator/.test(x.url()));
    for (const sim of sims) {
      const el = await sim.frameElement(); if (!el) continue;
      const box = await el.boundingBox(); if (!box || box.width < 50) continue;
      const c = await sim.$("canvas"); if (!c) continue;
      const cb = await c.boundingBox(); if (cb && cb.width > 50) return cb;
    }
    return null;
  };
  let clip = null; for (let i = 0; i < 20 && !clip; i++) { clip = await rect(); if (!clip) await wait(500); }
  console.log("clip", JSON.stringify(clip));
  fs.mkdirSync(D + "/film", { recursive: true });
  // relancer le jeu pour filmer depuis le début
  await ed.evaluate(() => { const r = document.querySelector(".restart-button, [title*=Redémarrer], [aria-label*=Redémarrer], [aria-label*=Relancer]"); if (r) r.click(); });
  const t0 = Date.now(); const temps = []; let n = 0;
  while (Date.now() - t0 < 22000 && n < 500) {
    await p.screenshot({ path: `${D}/film/f${String(n).padStart(4, "0")}.png`, clip });
    temps.push(Date.now() - t0); n++;
  }
  fs.writeFileSync(D + "/film/temps.json", JSON.stringify(temps));
  console.log("images", temps.length, "durée", temps[temps.length - 1]);
  await b.close();
})();
