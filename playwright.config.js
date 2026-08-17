const { defineConfig } = require("@playwright/test");

const managedChromium =
  process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE ||
  "/home/rnk4i/.cache/ms-playwright/chromium-1234/chrome-linux64/chrome";

module.exports = defineConfig({
  testDir: "./tests/browser",
  outputDir: "test-results",
  fullyParallel: false,
  workers: 1,
  retries: 0,
  reporter: [["list"], ["html", { outputFolder: "playwright-report", open: "never" }]],
  use: {
    baseURL: "http://127.0.0.1:8765",
    browserName: "chromium",
    headless: true,
    launchOptions: { executablePath: managedChromium },
    screenshot: "only-on-failure",
    trace: "retain-on-failure",
  },
  webServer: {
    command:
      ".venv/bin/python manage.py migrate --noinput --settings=config.settings.browser " +
      "&& .venv/bin/python tests/browser/seed_qa.py " +
      "&& .venv/bin/python manage.py runserver 127.0.0.1:8765 --noreload --insecure --settings=config.settings.browser",
    url: "http://127.0.0.1:8765/health/",
    reuseExistingServer: false,
    timeout: 120000,
  },
  projects: [
    { name: "desktop", use: { viewport: { width: 1440, height: 900 } } },
    { name: "tablet", use: { viewport: { width: 768, height: 1024 } } },
    { name: "mobile", use: { viewport: { width: 390, height: 844 } } },
  ],
});
