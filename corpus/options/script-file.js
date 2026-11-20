// The delivery note's lines, which script-file.html loads from this file and writes into the page
var note = { number: "DN-2026-0457", customer: "Acme Trading Ltd", parcels: 5, lines: [
  { item: "A4 copier paper, box of 5 reams", ordered: 12, sent: 12 },
  { item: "Toner cartridge, black", ordered: 4, sent: 3 },
  { item: "Archive boxes, pack of 10", ordered: 6, sent: 6 } ] };
function fillDeliveryNote() {
  document.getElementById("number").textContent = note.number;
  document.getElementById("intro").textContent = "For " + note.customer + ": " + note.lines.length + " lines, one toner cartridge to follow.";
  var body = document.getElementById("lines");
  for (var i = 0; i < note.lines.length; i++) {
    var l = note.lines[i], tr = document.createElement("tr");
    tr.innerHTML = "<td>" + l.item + "</td><td class='n'>" + l.ordered + "</td><td class='n'>" + l.sent + "</td>";
    body.appendChild(tr);
  }
  document.getElementById("parcels").textContent = note.parcels;
}
