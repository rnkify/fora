const { expect } = require("@playwright/test");

async function assertRenderedLayout(page) {
  const findings = await page.evaluate(() => {
    const viewportWidth = document.documentElement.clientWidth;
    const overflow = [];
    const narrowText = [];
    const ignored = new Set(["SCRIPT", "STYLE", "OPTION"]);

    for (const element of document.querySelectorAll("body *")) {
      if (ignored.has(element.tagName)) continue;
      const style = getComputedStyle(element);
      if (style.display === "none" || style.visibility === "hidden") continue;
      const rect = element.getBoundingClientRect();
      if (!rect.width || !rect.height) continue;

      if (rect.left < -1 || rect.right > viewportWidth + 1) {
        let ancestor = element.parentElement;
        let allowsScroll = false;
        while (ancestor && ancestor !== document.body) {
          const node = ancestor;
          const overflowX = getComputedStyle(node).overflowX;
          if (overflowX === "auto" || overflowX === "scroll") {
            allowsScroll = true;
            break;
          }
          ancestor = ancestor.parentElement;
        }
        if (!allowsScroll) {
          overflow.push({
            tag: element.tagName,
            className: String(element.className).slice(0, 100),
            left: Math.round(rect.left),
            right: Math.round(rect.right),
          });
        }
      }

      if (
        ["P", "H1", "H2", "H3", "LI"].includes(element.tagName) &&
        element.innerText.trim().length > 35 &&
        rect.width < 110
      ) {
        narrowText.push({
          text: element.innerText.trim().slice(0, 90),
          width: Math.round(rect.width),
        });
      }
    }

    return {
      documentWidth: document.documentElement.scrollWidth,
      viewportWidth,
      overflow: overflow.slice(0, 10),
      narrowText: narrowText.slice(0, 10),
    };
  });

  expect(findings.documentWidth, JSON.stringify(findings)).toBeLessThanOrEqual(
    findings.viewportWidth + 1
  );
  expect(findings.overflow, JSON.stringify(findings)).toEqual([]);
  expect(findings.narrowText, JSON.stringify(findings)).toEqual([]);
}

async function loginAsStaff(page) {
  await page.goto("/admin/login/?next=/ops/");
  await page.getByLabel("Username").fill("qa-staff");
  await page.getByLabel("Password").fill("qa-browser-password");
  await page.getByRole("button", { name: "Log in" }).click();
  await expect(page).toHaveURL(/\/ops\/$/);
}

async function revealPage(page) {
  const revealItems = page.locator("[data-reveal]");
  for (let index = 0; index < (await revealItems.count()); index += 1) {
    const item = revealItems.nth(index);
    await item.scrollIntoViewIfNeeded();
    await expect(item).toHaveClass(/is-visible/);
  }
  await page.evaluate(() => window.scrollTo(0, 0));
}

module.exports = { assertRenderedLayout, loginAsStaff, revealPage };
