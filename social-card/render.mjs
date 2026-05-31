import { chromium } from "playwright";
import path from "node:path";
import fs from "node:fs";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const htmlPath = path.join(__dirname, "index.html");
const exportsDir = path.join(__dirname, "exports");

if (!fs.existsSync(exportsDir)) {
  fs.mkdirSync(exportsDir, { recursive: true });
}

console.log(`Loading ${htmlPath}...`);
const browser = await chromium.launch({
  args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader"],
});
const page = await browser.newPage();
await page.goto("file://" + htmlPath, { waitUntil: "networkidle" });

// Wait at least 1500ms to ensure WebGL/animations are rendered and stable
console.log("Waiting for animations and fonts to load...");
await page.waitForTimeout(1500);

const sections = await page.$$("section.poster");
console.log(`Found ${sections.length} posters to export.`);

for (const s of sections) {
  const id = await s.evaluate(el => el.id || el.className.split(" ").join("-"));
  const outputPath = path.join(exportsDir, `${id}.png`);
  console.log(`Exporting ${id} to ${outputPath}...`);
  await s.screenshot({ path: outputPath });
}

await browser.close();
console.log("Export complete!");
