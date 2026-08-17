const { test, expect } = require("@playwright/test");
const { assertRenderedLayout, revealPage } = require("./helpers");

const publicPages = [
  ["home", "/"],
  ["services", "/services/"],
  ["service-ai-systems", "/services/ai-systems/"],
  ["service-conversion-copy", "/services/conversion-copy/"],
  ["service-content-systems", "/services/content-systems/"],
  ["service-ai-automation", "/services/ai-automation/"],
  ["pricing", "/pricing/"],
  ["process", "/process/"],
  ["work", "/work/"],
  ["about", "/about/"],
  ["faq", "/faq/"],
  ["contact", "/contact/"],
  ["start", "/start/"],
  ["privacy", "/privacy/"],
  ["terms", "/terms/"],
];

for (const [name, path] of publicPages) {
  test(`${name} renders without layout defects`, async ({ page }, testInfo) => {
    const response = await page.goto(path);
    expect(response.status()).toBe(200);
    await expect(page.locator("main")).toBeVisible();
    await assertRenderedLayout(page);

    if (["home", "services", "pricing", "process", "contact", "start"].includes(name)) {
      await revealPage(page);
      await page.screenshot({
        path: testInfo.outputPath(`${name}-full.png`),
        fullPage: true,
      });
    }
  });
}

test("sitemap, robots, and custom 404 render", async ({ page }) => {
  let response = await page.goto("/sitemap.xml");
  expect(response.status()).toBe(200);
  await expect(page.locator("body")).toContainText("/pricing/");

  response = await page.goto("/robots.txt");
  expect(response.status()).toBe(200);
  await expect(page.locator("body")).toContainText("Disallow: /ops/");

  response = await page.goto("/browser-qa-missing-page/");
  expect(response.status()).toBe(404);
  await expect(page.getByRole("heading", { name: "This page could not be found." })).toBeVisible();
  await assertRenderedLayout(page);
});

test("homepage sections and pricing geometry are intentional", async ({ page }, testInfo) => {
  await page.goto("/");
  const sections = page.locator("main > section");
  await expect(sections).toHaveCount(7);

  for (let index = 0; index < 7; index += 1) {
    const section = sections.nth(index);
    await section.scrollIntoViewIfNeeded();
    if ((await section.getAttribute("data-reveal")) !== null) {
      await expect(section).toHaveClass(/is-visible/);
    }
    await expect(section).toBeVisible();
    const box = await section.boundingBox();
    expect(box.width).toBeGreaterThan(300);
    expect(box.height).toBeGreaterThan(100);
    await section.screenshot({ path: testInfo.outputPath(`homepage-section-${index + 1}.png`) });
  }

  const cards = page.locator(".fora-pricing-card");
  await expect(cards).toHaveCount(4);
  const growth = cards.filter({ hasText: "Growth" });
  const description = growth.locator(".fora-pricing-card-description");
  const badge = growth.getByText("Recommended", { exact: true });
  const descriptionBox = await description.boundingBox();
  const cardBox = await growth.boundingBox();
  const badgeBox = await badge.boundingBox();

  expect(descriptionBox.width).toBeGreaterThan(cardBox.width * 0.7);
  expect(descriptionBox.height).toBeLessThan(180);
  expect(badgeBox.x + badgeBox.width).toBeLessThanOrEqual(cardBox.x + cardBox.width);

  const ctaTops = await cards.locator(".fora-button").evaluateAll((buttons) =>
    buttons.map((button) => Math.round(button.getBoundingClientRect().top))
  );
  if (page.viewportSize().width >= 1051) {
    expect(Math.max(...ctaTops) - Math.min(...ctaTops)).toBeLessThanOrEqual(2);
  }

  await growth.screenshot({ path: testInfo.outputPath("growth-card.png") });
});

test("desktop navigation, service CTA, and pricing CTA route correctly", async ({ page }) => {
  test.skip(page.viewportSize().width < 768, "Desktop navigation is hidden at this viewport.");
  await page.goto("/");
  await page.getByRole("navigation", { name: "Primary navigation" }).getByText("Services").click();
  await expect(page).toHaveURL(/\/services\/$/);

  await page.locator("main .fora-grid-2 article").first().getByRole("link").click();
  await expect(page).toHaveURL(/\/services\/ai-systems\/$/);
  await page.locator("main").getByRole("link", { name: "Start a Project" }).first().click();
  await expect(page).toHaveURL(/\/start\/\?service=ai_systems$/);
  await expect(page.locator("select[name=service_interest_id]")).toHaveValue("ai_systems");

  await page.goto("/pricing/");
  await page.locator(".fora-pricing-card").filter({ hasText: "Growth" }).getByRole("link").click();
  await expect(page).toHaveURL(/\/start\/\?plan=growth$/);
  await expect(page.locator("select[name=plan_interest_id]")).toHaveValue("growth");
});

test("mobile navigation opens and routes", async ({ page }) => {
  test.skip(page.viewportSize().width >= 768, "Mobile navigation is hidden at this viewport.");
  await page.goto("/");
  const menu = page.locator(".fora-mobile-menu");
  await menu.locator("summary").click();
  await expect(menu).toHaveAttribute("open", "");
  await menu.getByRole("link", { name: "Pricing" }).click();
  await expect(page).toHaveURL(/\/pricing\/$/);
});

test("FAQ controls are keyboard operable", async ({ page }) => {
  await page.goto("/faq/");
  const first = page.locator("main details").first();
  const summary = first.locator("summary");
  await summary.focus();
  await expect(summary).toBeFocused();
  await page.keyboard.press("Enter");
  await expect(first).toHaveAttribute("open", "");
});

test("process sequence wraps only between connected units", async ({ page }) => {
  await page.goto("/process/");
  const sequence = page.locator(".fora-process-sequence");
  await expect(sequence).toBeVisible();
  await expect(sequence.locator(".fora-process-sequence-unit")).toHaveCount(4);
  const units = await sequence.locator(".fora-process-sequence-unit").evaluateAll((elements) =>
    elements.map((element) => ({
      whiteSpace: getComputedStyle(element).whiteSpace,
      arrow: element.querySelector(".fora-process-sequence-arrow")?.textContent.trim(),
      step: element.querySelector(".fora-process-sequence-step")?.textContent.trim(),
    }))
  );
  expect(units.every((unit) => unit.whiteSpace === "nowrap" && unit.arrow === "→" && unit.step)).toBe(true);
});

test("contact form validates and reaches success state", async ({ page }) => {
  await page.goto("/contact/");
  await page.getByLabel("Email").fill("not-an-email");
  await page.getByRole("button", { name: "Send Message" }).click();
  await expect(page.locator("body")).toContainText("Enter a valid email address");
  await expect(page.getByLabel("Email")).toHaveAttribute("aria-invalid", "true");
  await expect(page.locator("#id_email_error")).toHaveAttribute("role", "alert");

  await page.getByLabel("Name").fill("Browser QA Contact");
  await page.getByLabel("Email").fill("browser-contact@qa.example");
  await page.getByLabel("Message").fill("Rendered contact form verification.");
  await page.getByRole("button", { name: "Send Message" }).click();
  await expect(page).toHaveURL(/\/contact\/\?submitted=1$/);
  await expect(page.getByText("Your message has been submitted.")).toBeVisible();
});

test("submission success cannot be spoofed by query string", async ({ page }) => {
  await page.goto("/start/?submitted=1");
  await expect(page.getByRole("button", { name: "Submit Project" })).toBeVisible();
  await expect(page.getByText("Your project inquiry has been submitted.")).toHaveCount(0);
});

test("project inquiry validates, preserves preselection, and succeeds", async ({ page }) => {
  await page.goto("/start/?service=ai_systems&plan=growth");
  await expect(page.locator("select[name=service_interest_id]")).toHaveValue("ai_systems");
  await expect(page.locator("select[name=plan_interest_id]")).toHaveValue("growth");
  await page.getByLabel("Email").fill("invalid");
  await page.getByRole("button", { name: "Submit Project" }).click();
  await expect(page.locator("body")).toContainText("Enter a valid email address");

  await page.getByLabel("Name").fill("Browser QA Project");
  await page.getByLabel("Email").fill("browser-project@qa.example");
  await page.getByLabel("Company").fill("Browser QA Company");
  await page.getByLabel("What are you trying to improve?").fill("Verify the complete rendered inquiry flow.");
  await page.getByRole("button", { name: "Submit Project" }).click();
  await expect(page).toHaveURL(/\/start\/\?submitted=1$/);
  await expect(page.getByText("Your project inquiry has been submitted.")).toBeVisible();
});

test("reduced motion disables reveal transitions", async ({ page }) => {
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.goto("/");
  await expect(page.locator("html")).toHaveClass(/reduced-motion/);
  const transition = await page.locator("[data-reveal]").first().evaluate((element) =>
    getComputedStyle(element).transitionDuration
  );
  expect(Number.parseFloat(transition)).toBeLessThanOrEqual(0.00001);
});

test("key public pages remain sound at extended release widths", async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== "desktop", "Extended widths run once.");
  const widths = [320, 375, 430, 1024, 1280, 1920];
  const paths = ["/", "/services/", "/pricing/", "/process/", "/contact/", "/start/"];
  for (const width of widths) {
    await page.setViewportSize({ width, height: width < 700 ? 844 : 1000 });
    for (const path of paths) {
      const response = await page.goto(path);
      expect(response.status()).toBe(200);
      await assertRenderedLayout(page);
    }
    await page.goto("/");
    await revealPage(page);
    await page.screenshot({ path: testInfo.outputPath(`home-${width}.png`), fullPage: true });
  }
});
