const { test, expect } = require("@playwright/test");
const { assertRenderedLayout, loginAsStaff } = require("./helpers");

test("operations pages require staff permissions", async ({ page }, testInfo) => {
  await page.goto("/ops/");
  await expect(page).toHaveURL(/\/ops\/login\/\?next=\/ops\/$/);
  await expect(page.getByRole("heading", { name: "Staff login" })).toBeVisible();
  await expect(page.locator("body")).not.toContainText("Django administration");
  await assertRenderedLayout(page);
  await page.screenshot({ path: testInfo.outputPath("ops-login-full.png"), fullPage: true });

  await page.getByLabel("Username").fill("qa-member");
  await page.getByLabel("Password").fill("qa-browser-password");
  await page.getByRole("button", { name: "Log in" }).click();
  await expect(page).toHaveURL(/\/ops\/login\/\?next=\/ops\/$/);
  await expect(page.locator("body")).toContainText("does not have access to Fora operations");
});

test("dashboard and project list render responsively", async ({ page }, testInfo) => {
  await loginAsStaff(page);
  await expect(page.getByRole("heading", { name: "Business overview." })).toBeVisible();
  const navigationName = page.viewportSize().width >= 768 ? "Primary navigation" : "Mobile navigation";
  const navigation = page.getByRole("navigation", { name: navigationName, includeHidden: true });
  await expect(navigation).toContainText("Dashboard");
  await expect(navigation).toContainText("Leads");
  await expect(navigation).toContainText("Projects");
  await assertRenderedLayout(page);
  await page.screenshot({ path: testInfo.outputPath("ops-dashboard-full.png"), fullPage: true });

  await page.goto("/ops/projects/");
  await expect(page.getByRole("heading", { name: "Projects" })).toBeVisible();
  await assertRenderedLayout(page);
  await page.screenshot({ path: testInfo.outputPath("ops-projects-full.png"), fullPage: true });
});

test("lead workspace supports qualification and activity", async ({ page }, testInfo) => {
  await loginAsStaff(page);
  await page.goto("/ops/leads/?q=QA+Qualification+Lead");
  await expect(page.getByRole("heading", { name: "Leads" })).toBeVisible();
  await page.getByRole("link", { name: "Open →" }).click();
  await expect(page.getByRole("heading", { name: "QA Qualification Lead" })).toBeVisible();
  await assertRenderedLayout(page);

  await expect(page.getByText("0–39 Low fit")).toBeVisible();
  await page.getByLabel("Status").selectOption("qualified");
  await page.getByLabel("Score").fill("80");
  await page.getByLabel("Notes").fill("Qualified through rendered browser QA.");
  await page.getByRole("button", { name: "Save Lead" }).click();
  await expect(page.getByText("Lead details updated.")).toBeVisible();

  const activityNote = `Confirmed ${testInfo.project.name} scope and next steps.`;
  await page.getByLabel("Type").selectOption("call");
  await page.getByLabel("Note", { exact: true }).fill(activityNote);
  await page.getByRole("button", { name: "Add Activity" }).click();
  await expect(page.getByText(activityNote)).toBeVisible();
  await page.screenshot({ path: testInfo.outputPath("lead-workspace-full.png"), fullPage: true });
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

  const projectNote = `Browser activity from ${testInfo.project.name}.`;
  await page.getByLabel("Note", { exact: true }).fill(projectNote);
  await page.getByRole("button", { name: "Add Project Note" }).click();
  await expect(page.getByText(projectNote)).toBeVisible();

  const taskTitle = `Browser-created ${testInfo.project.name} task`;
  await page.getByLabel("Title").fill(taskTitle);
  await page.getByRole("button", { name: "Add Task" }).click();
  await expect(page.getByText(taskTitle, { exact: true })).toBeVisible();

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
  await expect(page).toHaveURL(/\/ops\/projects\/\d+\/$/);
  await expect(page.getByRole("heading", { name: "QA Won Lead" })).toBeVisible();
  await expect(page.getByText(/created successfully/)).toBeVisible();
  await expect(page.getByRole("heading", { name: "Project activity" })).toBeVisible();
  await expect(page.getByText(/Project created from lead/)).toBeVisible();
});
