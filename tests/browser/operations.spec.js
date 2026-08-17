const { test, expect } = require("@playwright/test");
const { assertRenderedLayout, loginAsStaff } = require("./helpers");

test("operations pages require staff permissions", async ({ page }) => {
  await page.goto("/ops/");
  await expect(page).toHaveURL(/\/admin\/login\/\?next=\/ops\/$/);

  await page.getByLabel("Username").fill("qa-member");
  await page.getByLabel("Password").fill("qa-browser-password");
  await page.getByRole("button", { name: "Log in" }).click();
  await expect(page).toHaveURL(/\/admin\/login\/\?next=\/ops\/$/);
  await expect(page.locator("body")).toContainText("staff account");
});

test("dashboard and project list render responsively", async ({ page }, testInfo) => {
  await loginAsStaff(page);
  await expect(page.getByRole("heading", { name: "Business overview." })).toBeVisible();
  await assertRenderedLayout(page);
  await page.screenshot({ path: testInfo.outputPath("ops-dashboard-full.png"), fullPage: true });

  await page.goto("/ops/projects/");
  await expect(page.getByRole("heading", { name: "Projects" })).toBeVisible();
  await assertRenderedLayout(page);
  await page.screenshot({ path: testInfo.outputPath("ops-projects-full.png"), fullPage: true });
});

test("project search, state filters, and pagination work", async ({ page }) => {
  await loginAsStaff(page);
  await page.goto("/ops/projects/?state=all");
  await expect(page.getByText(/Page 1 of 2/)).toBeVisible();
  await page.getByRole("link", { name: "Next" }).click();
  await expect(page).toHaveURL(/page=2/);

  await page.getByLabel("Search").fill("QA Primary Client");
  await page.getByRole("button", { name: "Filter projects" }).click();
  await expect(page.getByText("QA Primary Client")).toBeVisible();
  await expect(page.getByText("QA Pagination Client 00")).toHaveCount(0);

  await page.goto("/ops/projects/?state=delivered");
  await expect(page.locator("tbody")).toContainText("Delivered");
  await page.goto("/ops/projects/?state=archived");
  await expect(page.getByText("No projects found")).toBeVisible();
});

test("project workspace supports project and task updates", async ({ page }, testInfo) => {
  await loginAsStaff(page);
  await page.goto("/ops/projects/?q=QA+Primary+Client&state=all");
  await page.getByRole("link", { name: "Workspace" }).click();
  await expect(page.getByRole("heading", { name: "QA Primary Client" })).toBeVisible();
  await assertRenderedLayout(page);

  await page.getByLabel("Notes").fill("Updated through rendered browser QA.");
  await page.getByRole("button", { name: "Save Project" }).click();
  await expect(page.getByText("Project details updated.")).toBeVisible();

  const taskTitle = `Browser-created ${testInfo.project.name} task`;
  await page.getByLabel("Title").fill(taskTitle);
  await page.getByRole("button", { name: "Add Task" }).click();
  await expect(page.getByText(taskTitle)).toBeVisible();

  const task = page.locator("article.fora-ops-row").filter({ hasText: taskTitle });
  await task.locator("select[name=status]").selectOption("done");
  await task.getByRole("button", { name: "Update" }).click();
  await expect(page.getByText("Task status updated.")).toBeVisible();
  await expect(page.locator("article.fora-ops-row").filter({ hasText: taskTitle })).toContainText("Done");
  await page.screenshot({ path: testInfo.outputPath("project-workspace-full.png"), fullPage: true });
});

test("won lead can be converted to one project", async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== "desktop", "The state-changing workflow runs once.");
  await loginAsStaff(page);
  const card = page.locator("article.fora-ops-row").filter({ hasText: "QA Won Lead" });
  await expect(card).toBeVisible();
  await card.getByRole("button", { name: /Start project/i }).click();
  await expect(page.getByText(/created successfully/)).toBeVisible();
  const readyPanel = page
    .getByRole("heading", { name: "Won leads ready to start" })
    .locator(
      "xpath=(ancestor::div[contains(concat(' ', normalize-space(@class), ' '), ' fora-ops-panel ')])[1]"
    );
  await expect(readyPanel).toContainText("No won leads are waiting to enter delivery.");
  await page.goto("/ops/projects/?q=QA+Won+Lead&state=all");
  await expect(page.getByText("QA Won Lead")).toBeVisible();
});
