// DAOS landing — interaksi kecil, jujur:
// 1. tombol salin perintah (clipboard, dengan umpan balik "Tersalin");
// 2. cek kompatibilitas ABO — logika yang sama dengan is_kompatibel()
//    di src/uas.c (AB terima semua; A terima A/O; B terima B/O;
//    O hanya terima O). Tidak ada data palsu di sini.
(function () {
  "use strict";

  // ── Tombol salin ────────────────────────────────────────────────────
  document.querySelectorAll("[data-copy]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var text = btn.getAttribute("data-copy");
      var done = function () {
        var label = btn.textContent;
        btn.textContent = "Tersalin";
        btn.disabled = true;
        window.setTimeout(function () {
          btn.textContent = label;
          btn.disabled = false;
        }, 1600);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done, function () {
          fallbackCopy(text);
          done();
        });
      } else {
        fallbackCopy(text);
        done();
      }
    });
  });

  function fallbackCopy(text) {
    var ta = document.createElement("textarea");
    ta.value = text;
    ta.setAttribute("readonly", "");
    ta.style.position = "absolute";
    ta.style.left = "-9999px";
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand("copy"); } catch (e) { /* abaikan */ }
    document.body.removeChild(ta);
  }

  // ── Cek ABO ─────────────────────────────────────────────────────────
  var pasien = document.getElementById("abo-pasien");
  var kantong = document.getElementById("abo-kantong");
  var result = document.getElementById("abo-result");
  if (!pasien || !kantong || !result) return;

  function kompatibel(golPasien, golKantong) {
    if (golPasien === "AB") return true;
    if (golPasien === "A") return golKantong === "A" || golKantong === "O";
    if (golPasien === "B") return golKantong === "B" || golKantong === "O";
    if (golPasien === "O") return golKantong === "O";
    return false;
  }

  function render() {
    var p = pasien.value;
    var k = kantong.value;
    if (kompatibel(p, k)) {
      result.textContent =
        "Kompatibel — kantong gol " + k + " bisa dialokasikan ke pasien gol " + p + ".";
      result.className = "abo-result ok";
    } else {
      result.textContent =
        "Tidak kompatibel — pasien gol " + p + " tidak bisa menerima kantong gol " + k +
        " (aturan ABO). Alokasi akan [GAGAL].";
      result.className = "abo-result no";
    }
  }

  pasien.addEventListener("change", render);
  kantong.addEventListener("change", render);
  render();
})();
