# Bootstrap 5 in wkhtmltopdf 0.12.6.1: what prints

Odoo 16 to 20 print their reports with wkhtmltopdf 0.12.6.1, and their report templates use Bootstrap 5.
This folder measures, one feature per page, which Bootstrap 5 features print the way a browser shows them, and which do not.

**The matrix: [results/RESULTS.md](results/RESULTS.md).** Each verdict links a picture of the page: Chrome on the left, wkhtmltopdf on the right, each difference marked.

## How it is measured

- **Pages.** [`features/`](features): one Bootstrap 5 feature per page, doing the job it does in a report (address columns, invoice lines, totals, a status badge), plus a control page in plain CSS.
- **Stylesheets.** Every page is printed six times:
  - Bootstrap 5.1.3 alone (Odoo 16 and 17) and Bootstrap 5.3.3 alone (Odoo 18, 19 and 20), as Odoo's source tree ships them (the same files as Bootstrap's own release);
  - the report CSS that Odoo 17, 18, 19 and 20 compile for PDFs, fetched from each version's official Docker image, inside Odoo's PDF page structure.
- **wkhtmltopdf.** The binary inside Odoo's official Docker image (0.12.6.1, with patched Qt; the same file in all four versions), with the arguments Odoo passes for its default A4 paper format (`--dpi 90 --zoom 1.0667 --disable-local-file-access --javascript-delay 1000`). Only the top and bottom margins differ: these pages have no header or footer to make room for.
- **Reference.** Headless Chrome, printing at the scale wkhtmltopdf prints a CSS pixel with those arguments (measured on every run), so the same CSS gives the same page.
- **Judge.** `marqius-wkhtmltopdf compare` sets wkhtmltopdf's PDF against Chrome's and gives each page a verdict:
  - *same*;
  - *appearance only*: the same words, laid out or drawn differently;
  - *content differs*: words missing, added or out of their place.

  It names each difference and marks it on both PDFs. compare does not compare the roundness of corners: on the two corner pages, the corner radius each program computed decides.
- **Why.** Each page also reads a few computed styles in both programs. For example, Bootstrap 5.3's body line height comes out as `normal` in wkhtmltopdf and `24px` in Chrome.

> compare is part of marqius-wkhtmltopdf, which Simple AI LLC makes and which publishes this suite. The program measured here is the original wkhtmltopdf.

## Keeping the comparison fair

- **The control page comes out the same.** A plain-CSS invoice block, with no Bootstrap, prints the same in both programs, so a difference on any other page comes from the CSS it tests.
- **Same fonts.** Odoo's image carries the URW font clones, which wkhtmltopdf picks for Helvetica and Times, while Chrome picks the Liberation fonts. The URW clones are hidden, so both programs print with the same fonts.
- **One feature per page.**
  - The Bootstrap-alone pages set the body font, size, line height and colour in plain CSS, as Odoo's report CSS does. Bootstrap sets them through `var()`, which the body-text page shows on its own.
  - Odoo's PDF body carries `.container`, whose width comes from a media query that never matches in wkhtmltopdf. Both programs print it at full width, and the container page shows the difference.
  - Invoice tables have fixed column widths.
- **Nothing fetched while printing.** Pages and their files are served from the machine itself.

## Run it yourself

With Docker and curl (about 15 GB of disk for Odoo's images):

```bash
sh bootstrap5-matrix/run.sh
```

Or fork this repository and run **Actions > Bootstrap 5 matrix > Run workflow**. Every filed matrix links the run that made it ([results/run.txt](results/run.txt)) and carries a GitHub attestation.

## Licence

The pages in `features/` are public domain (CC0 1.0), and the harness is MIT, like the rest of this repository.
