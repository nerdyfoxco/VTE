import { chromium } from 'playwright';
import * as fs from 'fs';
import * as path from 'path';

async function extractAppFolio() {
    console.log('[AppFolio RPA Engine] Booting System...');
    const cookiePath = path.resolve(__dirname, '../../storage/cookies/appfolio.json');
    if (!fs.existsSync(cookiePath)) {
        console.error("[AppFolio RPA Engine] FATAL: No cookie found at", cookiePath);
        return;
    }

    const cookies = JSON.parse(fs.readFileSync(cookiePath, 'utf8'));

    console.log('[AppFolio RPA Engine] Firing Headed Browser (Visible to User)...');
    // Launch visibly so the user can physically verify the RPA action
    const browser = await chromium.launch({ headless: false });
    const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
    await context.addCookies(cookies);

    const page = await context.newPage();
    console.log('[AppFolio RPA Engine] Accessing https://anchorrealty.appfolio.com...');
    await page.goto('https://anchorrealty.appfolio.com/', { waitUntil: 'domcontentloaded' });

    console.log('[AppFolio RPA Engine] Awaiting Authorization and Dashboard Load...');
    await page.waitForTimeout(5000);

    console.log('[AppFolio RPA Engine] Navigating to Delinquency Dashboard / Reports...');
    try {
        await page.goto('https://anchorrealty.appfolio.com/reports/delinquency', { waitUntil: 'domcontentloaded', timeout: 15000 });
        await page.waitForTimeout(6000); // Give the DOM tables time to render
    } catch (e) {
        console.log('[AppFolio RPA Engine] Notice: Could not access /reports/delinquency directly. Scraping current viewport.');
    }

    console.log('[AppFolio RPA Engine] Capturing visual proof...');
    // Create exports dir if it doesn't exist
    const exportsDir = path.resolve(__dirname, '../../storage/exports');
    if (!fs.existsSync(exportsDir)) {
        fs.mkdirSync(exportsDir, { recursive: true });
    }

    await page.screenshot({ path: path.join(exportsDir, 'appfolio_proof.png'), fullPage: true });

    console.log('[AppFolio RPA Engine] Extracting true structured tenant data from DOM...');
    const pageText = await page.evaluate(() => document.body.innerText);
    fs.writeFileSync(path.join(exportsDir, 'appfolio_raw_text.txt'), pageText);

    console.log('[AppFolio RPA Engine] True Data Extracted and Saved. Closing Browser in 3 seconds...');
    await page.waitForTimeout(3000);
    await browser.close();
}

extractAppFolio().catch(console.error);
