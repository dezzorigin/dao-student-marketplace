import { test, expect } from "@playwright/test";

// Landing dao-student-marketplace adalah etalase program CLI C: yang diuji
// adalah konten + interaksi halamannya (papan triase, kartu kantong,
// cek ABO, tombol salin, navigasi). Program CLI-nya sendiri diuji di job
// build-test CI (make test) — bukan di browser.

test("landing tampil: papan triase, kantong contoh, sesi demo", async ({ page }) => {
  await page.goto("/");
  await expect(page).toHaveTitle(/DAOS/i);
  await expect(page.locator("text=Budi Santoso").first()).toBeVisible();
  await expect(page.locator("text=DAOS - SISTEM ALOKASI KANTONG DARAH").first()).toBeVisible();
  await expect(page.locator("text=D001").first()).toBeVisible();
  await expect(page.locator("text=Kantong D001 dialokasikan ke Pasien P002").first()).toBeVisible();
  // kejujuran isi: bukan marketplace
  await expect(page.locator("text=bukan").first()).toBeVisible();
});

test("cek ABO: AB terima O, O tolak A", async ({ page }) => {
  await page.goto("/");
  // default: pasien AB + kantong O = kompatibel
  await expect(page.locator("#abo-result")).toContainText("Kompatibel");
  await page.locator("#abo-pasien").selectOption("O");
  await page.locator("#abo-kantong").selectOption("A");
  await expect(page.locator("#abo-result")).toContainText("Tidak kompatibel");
  await expect(page.locator("#abo-result")).toContainText("[GAGAL]");
  // O + O = kompatibel lagi
  await page.locator("#abo-kantong").selectOption("O");
  await expect(page.locator("#abo-result")).toContainText("Kompatibel");
});

test("tombol salin perintah build menyalin 'make'", async ({ page }) => {
  await page.goto("/");
  await page.context().grantPermissions(["clipboard-read", "clipboard-write"]);
  await page.getByRole("button", { name: "Salin perintah make" }).click();
  const clip = await page.evaluate(() => navigator.clipboard.readText());
  expect(clip).toBe("make");
  await expect(page.getByRole("button", { name: "Tersalin" }).first()).toBeVisible();
});

test("mobile 390px: tanpa scroll horizontal", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("/");
  const overflow = await page.evaluate(
    () => document.documentElement.scrollWidth - document.documentElement.clientWidth,
  );
  expect(overflow).toBe(0);
});

test("og-image + favicon termuat (bukan 404)", async ({ page }) => {
  const og = await page.request.get("/og-image.png");
  expect(og.status()).toBe(200);
  expect(og.headers()["content-type"] ?? "").toMatch(/image\//);
  const fav = await page.request.get("/favicon.svg");
  expect(fav.status()).toBe(200);
});
