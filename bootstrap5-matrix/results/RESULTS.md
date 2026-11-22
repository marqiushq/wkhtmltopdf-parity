# Bootstrap 5 in wkhtmltopdf 0.12.6.1, page by page

Each page uses one Bootstrap 5 feature as an Odoo report would. wkhtmltopdf prints it as Odoo calls it; Chrome prints it as the reference, at the scale wkhtmltopdf prints a CSS pixel (0.8533), so the same CSS gives the same page. `marqius-wkhtmltopdf compare` sets wkhtmltopdf's PDF against Chrome's: ✓ same; ✗ appearance (the same words, laid out or drawn differently) or ✗ content (words missing, added or changed), with the kinds of difference it found. – : not in that Bootstrap. Each verdict links compare's picture: Chrome left, wkhtmltopdf right, each difference marked. compare does not compare the roundness of corners: on the two corner pages, the corner radius each program computed decides.

Programs: wkhtmltopdf 0.12.6.1 (with patched qt); Google Chrome 158.0.8127.36; marqius-wkhtmltopdf 0.12.13; pdfinfo version 24.02.0.

| Feature | Bootstrap 5.1.3 alone | Bootstrap 5.3.3 alone | Odoo 17 report CSS | Odoo 18 report CSS | Odoo 19 report CSS | Odoo 20 report CSS |
|---|---|---|---|---|---|---|
| **Control** | | | | | | |
| Control: the same invoice block in plain CSS, no Bootstrap | [✓ same](pictures/bootstrap-5.1.3/00-control.png) | [✓ same](pictures/bootstrap-5.3.3/00-control.png) | [✓ same](pictures/odoo-17.0/00-control.png) | [✓ same](pictures/odoo-18.0/00-control.png) | [✓ same](pictures/odoo-19.0/00-control.png) | [✓ same](pictures/odoo-20.0/00-control.png) |
| **Text** | | | | | | |
| Body text: Bootstrap's font, size, line height and colour | [✗ appearance: moved, reflow, font](pictures/bootstrap-5.1.3/01-body-text.png) | [✗ appearance: moved, reflow, font](pictures/bootstrap-5.3.3/01-body-text.png) | [✗ appearance: moved](pictures/odoo-17.0/01-body-text.png) | [✓ same](pictures/odoo-18.0/01-body-text.png) | [✓ same](pictures/odoo-19.0/01-body-text.png) | [✓ same](pictures/odoo-20.0/01-body-text.png) |
| Headings h1 to h4 | [✗ appearance: moved, size](pictures/bootstrap-5.1.3/02-headings.png) | [✗ appearance: moved, size](pictures/bootstrap-5.3.3/02-headings.png) | [✓ same](pictures/odoo-17.0/02-headings.png) | [✓ same](pictures/odoo-18.0/02-headings.png) | [✗ appearance: colour](pictures/odoo-19.0/02-headings.png) | [✗ appearance: colour](pictures/odoo-20.0/02-headings.png) |
| .lead, &lt;small&gt; and &lt;mark&gt; | [✗ appearance: spacing](pictures/bootstrap-5.1.3/03-lead-small-mark.png) | [✗ appearance: spacing, colour](pictures/bootstrap-5.3.3/03-lead-small-mark.png) | [✗ appearance: moved](pictures/odoo-17.0/03-lead-small-mark.png) | [✗ appearance: moved, colour](pictures/odoo-18.0/03-lead-small-mark.png) | [✗ appearance: moved, colour](pictures/odoo-19.0/03-lead-small-mark.png) | [✗ appearance: moved, colour](pictures/odoo-20.0/03-lead-small-mark.png) |
| Display headings: .display-4 | [✗ appearance: moved, size](pictures/bootstrap-5.1.3/04-display.png) | [✗ appearance: moved, size](pictures/bootstrap-5.3.3/04-display.png) | [✗ appearance: moved, size](pictures/odoo-17.0/04-display.png) | [✓ same](pictures/odoo-18.0/04-display.png) | [✓ same](pictures/odoo-19.0/04-display.png) | [✓ same](pictures/odoo-20.0/04-display.png) |
| Font size utilities: .fs-1, .fs-4, .fs-6 | [✗ appearance: moved, size](pictures/bootstrap-5.1.3/05-font-size.png) | [✗ appearance: moved, size](pictures/bootstrap-5.3.3/05-font-size.png) | [✗ appearance: moved, size](pictures/odoo-17.0/05-font-size.png) | [✓ same](pictures/odoo-18.0/05-font-size.png) | [✓ same](pictures/odoo-19.0/05-font-size.png) | [✓ same](pictures/odoo-20.0/05-font-size.png) |
| Weight and style: .fw-bold, .fw-light, .fst-italic | [✓ same](pictures/bootstrap-5.1.3/06-font-weight-style.png) | [✓ same](pictures/bootstrap-5.3.3/06-font-weight-style.png) | [✗ appearance: moved](pictures/odoo-17.0/06-font-weight-style.png) | [✗ appearance: moved](pictures/odoo-18.0/06-font-weight-style.png) | [✗ appearance: moved](pictures/odoo-19.0/06-font-weight-style.png) | [✗ appearance: moved](pictures/odoo-20.0/06-font-weight-style.png) |
| Case and lines: .text-uppercase, .text-decoration-* | [✓ same](pictures/bootstrap-5.1.3/07-text-transform.png) | [✓ same](pictures/bootstrap-5.3.3/07-text-transform.png) | [✓ same](pictures/odoo-17.0/07-text-transform.png) | [✓ same](pictures/odoo-18.0/07-text-transform.png) | [✓ same](pictures/odoo-19.0/07-text-transform.png) | [✓ same](pictures/odoo-20.0/07-text-transform.png) |
| Monospace: .font-monospace | [✗ appearance: moved, font](pictures/bootstrap-5.1.3/08-font-monospace.png) | [✗ appearance: moved, font](pictures/bootstrap-5.3.3/08-font-monospace.png) | [✗ appearance: moved, font](pictures/odoo-17.0/08-font-monospace.png) | [✗ appearance: moved, font](pictures/odoo-18.0/08-font-monospace.png) | [✗ appearance: moved, font](pictures/odoo-19.0/08-font-monospace.png) | [✗ appearance: moved, font](pictures/odoo-20.0/08-font-monospace.png) |
| Line height: .lh-1, .lh-lg | [✓ same](pictures/bootstrap-5.1.3/09-line-height.png) | [✓ same](pictures/bootstrap-5.3.3/09-line-height.png) | [✓ same](pictures/odoo-17.0/09-line-height.png) | [✓ same](pictures/odoo-18.0/09-line-height.png) | [✓ same](pictures/odoo-19.0/09-line-height.png) | [✓ same](pictures/odoo-20.0/09-line-height.png) |
| Alignment: .text-end, .text-center | [✓ same](pictures/bootstrap-5.1.3/10-text-align.png) | [✓ same](pictures/bootstrap-5.3.3/10-text-align.png) | [✓ same](pictures/odoo-17.0/10-text-align.png) | [✓ same](pictures/odoo-18.0/10-text-align.png) | [✓ same](pictures/odoo-19.0/10-text-align.png) | [✓ same](pictures/odoo-20.0/10-text-align.png) |
| Wrapping: .text-nowrap, .text-truncate, .text-break | [✗ content: text](pictures/bootstrap-5.1.3/11-text-wrap.png) | [✗ content: text](pictures/bootstrap-5.3.3/11-text-wrap.png) | [✗ content: moved, text](pictures/odoo-17.0/11-text-wrap.png) | [✗ content: text](pictures/odoo-18.0/11-text-wrap.png) | [✗ content: text](pictures/odoo-19.0/11-text-wrap.png) | [✗ content: text](pictures/odoo-20.0/11-text-wrap.png) |
| **Colour** | | | | | | |
| Text colours: .text-primary, -success, -danger, -warning, -info, -secondary | [✗ appearance: colour, moved](pictures/bootstrap-5.1.3/12-text-colours.png) | [✗ appearance: colour, moved](pictures/bootstrap-5.3.3/12-text-colours.png) | [✓ same](pictures/odoo-17.0/12-text-colours.png) | [✓ same](pictures/odoo-18.0/12-text-colours.png) | [✓ same](pictures/odoo-19.0/12-text-colours.png) | [✓ same](pictures/odoo-20.0/12-text-colours.png) |
| Quiet text: .text-muted (and .text-body-secondary in 5.3) | [✓ same](pictures/bootstrap-5.1.3/13-text-muted.png) | [✓ same](pictures/bootstrap-5.3.3/13-text-muted.png) | [✓ same](pictures/odoo-17.0/13-text-muted.png) | [✓ same](pictures/odoo-18.0/13-text-muted.png) | [✓ same](pictures/odoo-19.0/13-text-muted.png) | [✓ same](pictures/odoo-20.0/13-text-muted.png) |
| Backgrounds: .bg-light, .bg-primary, .bg-warning | [✗ appearance: drawing](pictures/bootstrap-5.1.3/14-bg-colours.png) | [✗ appearance: drawing](pictures/bootstrap-5.3.3/14-bg-colours.png) | [✗ appearance: moved](pictures/odoo-17.0/14-bg-colours.png) | [✓ same](pictures/odoo-18.0/14-bg-colours.png) | [✓ same](pictures/odoo-19.0/14-bg-colours.png) | [✓ same](pictures/odoo-20.0/14-bg-colours.png) |
| Text and background together: .text-bg-success (5.2 and later) | – | [✗ appearance: drawing](pictures/bootstrap-5.3.3/15-text-bg.png) | – | [✗ appearance: drawing](pictures/odoo-18.0/15-text-bg.png) | [✗ appearance: drawing](pictures/odoo-19.0/15-text-bg.png) | [✗ appearance: drawing](pictures/odoo-20.0/15-text-bg.png) |
| Background opacity and gradient: .bg-opacity-25, .bg-gradient | [✗ appearance: drawing](pictures/bootstrap-5.1.3/16-bg-opacity.png) | [✗ appearance: drawing](pictures/bootstrap-5.3.3/16-bg-opacity.png) | [✗ appearance: moved](pictures/odoo-17.0/16-bg-opacity.png) | [✗ appearance: drawing](pictures/odoo-18.0/16-bg-opacity.png) | [✗ appearance: drawing](pictures/odoo-19.0/16-bg-opacity.png) | [✗ appearance: drawing](pictures/odoo-20.0/16-bg-opacity.png) |
| Links | [✓ same](pictures/bootstrap-5.1.3/17-links.png) | [✗ appearance: colour](pictures/bootstrap-5.3.3/17-links.png) | [✓ same](pictures/odoo-17.0/17-links.png) | [✗ appearance: colour](pictures/odoo-18.0/17-links.png) | [✗ appearance: colour](pictures/odoo-19.0/17-links.png) | [✗ appearance: colour](pictures/odoo-20.0/17-links.png) |
| **Grid** | | | | | | |
| Two columns: .row &gt; .col-6 (no gutter, .g-0) | [✗ content: missing, moved, added](pictures/bootstrap-5.1.3/20-grid-col-6.png) | [✗ content: missing, moved, added](pictures/bootstrap-5.3.3/20-grid-col-6.png) | [✗ appearance: moved](pictures/odoo-17.0/20-grid-col-6.png) | [✓ same](pictures/odoo-18.0/20-grid-col-6.png) | [✓ same](pictures/odoo-19.0/20-grid-col-6.png) | [✓ same](pictures/odoo-20.0/20-grid-col-6.png) |
| Three columns: .row &gt; .col-4 (no gutter) | [✗ content: moved, missing, added](pictures/bootstrap-5.1.3/21-grid-col-4.png) | [✗ content: moved, missing, added](pictures/bootstrap-5.3.3/21-grid-col-4.png) | [✗ appearance: moved](pictures/odoo-17.0/21-grid-col-4.png) | [✓ same](pictures/odoo-18.0/21-grid-col-4.png) | [✓ same](pictures/odoo-19.0/21-grid-col-4.png) | [✓ same](pictures/odoo-20.0/21-grid-col-4.png) |
| Columns sized by content: .col-auto and .col (no gutter) | [✗ appearance: reflow](pictures/bootstrap-5.1.3/22-grid-col-auto.png) | [✗ appearance: reflow](pictures/bootstrap-5.3.3/22-grid-col-auto.png) | [✗ content: text, added, moved](pictures/odoo-17.0/22-grid-col-auto.png) | [✓ same](pictures/odoo-18.0/22-grid-col-auto.png) | [✓ same](pictures/odoo-19.0/22-grid-col-auto.png) | [✓ same](pictures/odoo-20.0/22-grid-col-auto.png) |
| Gutter between columns: .row &gt; .col-6 with the default gutter | [✗ content: missing, moved, added](pictures/bootstrap-5.1.3/23-grid-gutter.png) | [✗ content: missing, moved, added](pictures/bootstrap-5.3.3/23-grid-gutter.png) | [✗ appearance: moved](pictures/odoo-17.0/23-grid-gutter.png) | [✗ appearance: moved](pictures/odoo-18.0/23-grid-gutter.png) | [✗ appearance: moved](pictures/odoo-19.0/23-grid-gutter.png) | [✗ appearance: moved](pictures/odoo-20.0/23-grid-gutter.png) |
| Wrapping: three .col-6 in one row (no gutter) | [✗ content: moved, missing, added](pictures/bootstrap-5.1.3/24-grid-wrap.png) | [✗ content: moved, missing, added](pictures/bootstrap-5.3.3/24-grid-wrap.png) | [✗ content: moved, added, missing](pictures/odoo-17.0/24-grid-wrap.png) | [✗ content: moved, added, missing](pictures/odoo-18.0/24-grid-wrap.png) | [✗ content: moved, added, missing](pictures/odoo-19.0/24-grid-wrap.png) | [✗ content: moved, added, missing](pictures/odoo-20.0/24-grid-wrap.png) |
| Offset: .col-5.offset-7, the customer address on the right (no gutter) | [✓ same](pictures/bootstrap-5.1.3/25-grid-offset.png) | [✓ same](pictures/bootstrap-5.3.3/25-grid-offset.png) | [✗ appearance: moved](pictures/odoo-17.0/25-grid-offset.png) | [✓ same](pictures/odoo-18.0/25-grid-offset.png) | [✓ same](pictures/odoo-19.0/25-grid-offset.png) | [✓ same](pictures/odoo-20.0/25-grid-offset.png) |
| Columns pushed apart: .col-5 + .col-5.ms-auto (no gutter) | [✗ content: missing, moved, added](pictures/bootstrap-5.1.3/26-grid-ms-auto.png) | [✗ content: missing, moved, added](pictures/bootstrap-5.3.3/26-grid-ms-auto.png) | [✗ content: moved, text, number](pictures/odoo-17.0/26-grid-ms-auto.png) | [✗ content: moved, text, missing](pictures/odoo-18.0/26-grid-ms-auto.png) | [✗ content: moved, text, missing](pictures/odoo-19.0/26-grid-ms-auto.png) | [✗ content: moved, text, missing](pictures/odoo-20.0/26-grid-ms-auto.png) |
| Order: .order-last (no gutter) | [✗ content: moved, missing, added](pictures/bootstrap-5.1.3/27-grid-order.png) | [✗ content: moved, missing, added](pictures/bootstrap-5.3.3/27-grid-order.png) | [✗ appearance: moved](pictures/odoo-17.0/27-grid-order.png) | [✗ appearance: moved](pictures/odoo-18.0/27-grid-order.png) | [✗ appearance: moved](pictures/odoo-19.0/27-grid-order.png) | [✗ appearance: moved](pictures/odoo-20.0/27-grid-order.png) |
| Breakpoint columns: .col-md-6 (no gutter) | [✗ content: missing, moved, added](pictures/bootstrap-5.1.3/28-grid-md.png) | [✗ content: missing, moved, added](pictures/bootstrap-5.3.3/28-grid-md.png) | [✗ content: moved, text, missing](pictures/odoo-17.0/28-grid-md.png) | [✗ content: moved, text, size](pictures/odoo-18.0/28-grid-md.png) | [✗ content: moved, text, size](pictures/odoo-19.0/28-grid-md.png) | [✗ content: moved, text, size](pictures/odoo-20.0/28-grid-md.png) |
| Breakpoint columns: .col-lg-6 (no gutter) | [✓ same](pictures/bootstrap-5.1.3/29-grid-lg.png) | [✓ same](pictures/bootstrap-5.3.3/29-grid-lg.png) | [✗ content: moved, added, text](pictures/odoo-17.0/29-grid-lg.png) | [✗ content: moved, added, text](pictures/odoo-18.0/29-grid-lg.png) | [✗ content: moved, added, text](pictures/odoo-19.0/29-grid-lg.png) | [✗ content: moved, added, text](pictures/odoo-20.0/29-grid-lg.png) |
| Row columns: .row-cols-2 (no gutter) | [✗ appearance: moved](pictures/bootstrap-5.1.3/30-grid-row-cols.png) | [✗ appearance: moved](pictures/bootstrap-5.3.3/30-grid-row-cols.png) | [✗ content: moved, text, added](pictures/odoo-17.0/30-grid-row-cols.png) | [✓ same](pictures/odoo-18.0/30-grid-row-cols.png) | [✓ same](pictures/odoo-19.0/30-grid-row-cols.png) | [✓ same](pictures/odoo-20.0/30-grid-row-cols.png) |
| Nested rows (no gutter) | [✗ content: moved, missing, added](pictures/bootstrap-5.1.3/31-grid-nested.png) | [✗ content: moved, missing, added](pictures/bootstrap-5.3.3/31-grid-nested.png) | [✗ appearance: moved](pictures/odoo-17.0/31-grid-nested.png) | [✓ same](pictures/odoo-18.0/31-grid-nested.png) | [✓ same](pictures/odoo-19.0/31-grid-nested.png) | [✓ same](pictures/odoo-20.0/31-grid-nested.png) |
| Container padding: .container | [✗ appearance: moved](pictures/bootstrap-5.1.3/32-container.png) | [✗ appearance: moved](pictures/bootstrap-5.3.3/32-container.png) | [✗ appearance: moved](pictures/odoo-17.0/32-container.png) | [✗ appearance: moved](pictures/odoo-18.0/32-container.png) | [✗ appearance: moved](pictures/odoo-19.0/32-container.png) | [✗ appearance: moved](pictures/odoo-20.0/32-container.png) |
| **Flex** | | | | | | |
| Flex row, ends apart: .d-flex .justify-content-between | [✗ appearance: moved](pictures/bootstrap-5.1.3/40-flex-between.png) | [✗ appearance: moved](pictures/bootstrap-5.3.3/40-flex-between.png) | [✗ appearance: reflow](pictures/odoo-17.0/40-flex-between.png) | [✓ same](pictures/odoo-18.0/40-flex-between.png) | [✓ same](pictures/odoo-19.0/40-flex-between.png) | [✓ same](pictures/odoo-20.0/40-flex-between.png) |
| Flex row, at the end: .d-flex .justify-content-end | [✗ appearance: moved](pictures/bootstrap-5.1.3/41-flex-end.png) | [✗ appearance: moved](pictures/bootstrap-5.3.3/41-flex-end.png) | [✓ same](pictures/odoo-17.0/41-flex-end.png) | [✓ same](pictures/odoo-18.0/41-flex-end.png) | [✓ same](pictures/odoo-19.0/41-flex-end.png) | [✓ same](pictures/odoo-20.0/41-flex-end.png) |
| Flex row, centred: .d-flex .justify-content-center | [✗ appearance: moved](pictures/bootstrap-5.1.3/42-flex-center.png) | [✗ appearance: moved](pictures/bootstrap-5.3.3/42-flex-center.png) | [✗ appearance: moved](pictures/odoo-17.0/42-flex-center.png) | [✓ same](pictures/odoo-18.0/42-flex-center.png) | [✓ same](pictures/odoo-19.0/42-flex-center.png) | [✓ same](pictures/odoo-20.0/42-flex-center.png) |
| Vertical centring: .d-flex .align-items-center | [✗ appearance: moved](pictures/bootstrap-5.1.3/43-flex-align-center.png) | [✗ appearance: moved](pictures/bootstrap-5.3.3/43-flex-align-center.png) | [✗ appearance: moved](pictures/odoo-17.0/43-flex-align-center.png) | [✓ same](pictures/odoo-18.0/43-flex-align-center.png) | [✓ same](pictures/odoo-19.0/43-flex-align-center.png) | [✓ same](pictures/odoo-20.0/43-flex-align-center.png) |
| Flex column: .d-flex .flex-column | [✓ same](pictures/bootstrap-5.1.3/44-flex-column.png) | [✓ same](pictures/bootstrap-5.3.3/44-flex-column.png) | [✗ appearance: reflow, moved](pictures/odoo-17.0/44-flex-column.png) | [✓ same](pictures/odoo-18.0/44-flex-column.png) | [✓ same](pictures/odoo-19.0/44-flex-column.png) | [✓ same](pictures/odoo-20.0/44-flex-column.png) |
| Filling the row: .flex-grow-1 | [✗ appearance: moved](pictures/bootstrap-5.1.3/45-flex-grow.png) | [✗ appearance: moved](pictures/bootstrap-5.3.3/45-flex-grow.png) | [✗ appearance: reflow, moved](pictures/odoo-17.0/45-flex-grow.png) | [✓ same](pictures/odoo-18.0/45-flex-grow.png) | [✓ same](pictures/odoo-19.0/45-flex-grow.png) | [✓ same](pictures/odoo-20.0/45-flex-grow.png) |
| Pushed to the right in a flex row: .ms-auto | [✗ appearance: moved](pictures/bootstrap-5.1.3/46-flex-ms-auto.png) | [✗ appearance: moved](pictures/bootstrap-5.3.3/46-flex-ms-auto.png) | [✗ appearance: reflow, moved](pictures/odoo-17.0/46-flex-ms-auto.png) | [✗ appearance: reflow](pictures/odoo-18.0/46-flex-ms-auto.png) | [✗ appearance: reflow](pictures/odoo-19.0/46-flex-ms-auto.png) | [✗ appearance: reflow](pictures/odoo-20.0/46-flex-ms-auto.png) |
| Space between flex items: .gap-3 | [✗ appearance: reflow](pictures/bootstrap-5.1.3/47-flex-gap.png) | [✗ appearance: reflow](pictures/bootstrap-5.3.3/47-flex-gap.png) | [✗ appearance: spacing](pictures/odoo-17.0/47-flex-gap.png) | [✗ appearance: spacing](pictures/odoo-18.0/47-flex-gap.png) | [✗ appearance: spacing](pictures/odoo-19.0/47-flex-gap.png) | [✗ appearance: spacing](pictures/odoo-20.0/47-flex-gap.png) |
| Wrapping flex items: .flex-wrap | [✗ appearance: reflow](pictures/bootstrap-5.1.3/48-flex-wrap.png) | [✗ appearance: reflow](pictures/bootstrap-5.3.3/48-flex-wrap.png) | [✗ appearance: reflow, moved](pictures/odoo-17.0/48-flex-wrap.png) | [✗ appearance: reflow](pictures/odoo-18.0/48-flex-wrap.png) | [✗ appearance: reflow](pictures/odoo-19.0/48-flex-wrap.png) | [✗ appearance: reflow](pictures/odoo-20.0/48-flex-wrap.png) |
| Stacks: .hstack and .vstack with .gap-* | [✗ appearance: moved, reflow](pictures/bootstrap-5.1.3/49-stacks.png) | [✗ appearance: moved, reflow](pictures/bootstrap-5.3.3/49-stacks.png) | [✗ appearance: moved, reflow](pictures/odoo-17.0/49-stacks.png) | [✗ appearance: reflow, moved](pictures/odoo-18.0/49-stacks.png) | [✗ appearance: reflow, moved](pictures/odoo-19.0/49-stacks.png) | [✗ appearance: reflow, moved](pictures/odoo-20.0/49-stacks.png) |
| Grid display: .d-grid .gap-2 | [✗ appearance: moved](pictures/bootstrap-5.1.3/50-d-grid.png) | [✗ appearance: moved](pictures/bootstrap-5.3.3/50-d-grid.png) | [✗ appearance: moved](pictures/odoo-17.0/50-d-grid.png) | [✗ appearance: moved](pictures/odoo-18.0/50-d-grid.png) | [✗ appearance: moved](pictures/odoo-19.0/50-d-grid.png) | [✗ appearance: moved](pictures/odoo-20.0/50-d-grid.png) |
| **Spacing and sizing** | | | | | | |
| Spacing: .p-3, .px-5, .mt-4 | [✓ same](pictures/bootstrap-5.1.3/55-spacing.png) | [✓ same](pictures/bootstrap-5.3.3/55-spacing.png) | [✗ appearance: moved, drawing](pictures/odoo-17.0/55-spacing.png) | [✓ same](pictures/odoo-18.0/55-spacing.png) | [✓ same](pictures/odoo-19.0/55-spacing.png) | [✓ same](pictures/odoo-20.0/55-spacing.png) |
| Centred block: .w-50 .mx-auto | [✓ same](pictures/bootstrap-5.1.3/56-mx-auto.png) | [✓ same](pictures/bootstrap-5.3.3/56-mx-auto.png) | [✗ appearance: moved](pictures/odoo-17.0/56-mx-auto.png) | [✓ same](pictures/odoo-18.0/56-mx-auto.png) | [✓ same](pictures/odoo-19.0/56-mx-auto.png) | [✓ same](pictures/odoo-20.0/56-mx-auto.png) |
| Widths: .w-25, .w-50, .w-100 | [✓ same](pictures/bootstrap-5.1.3/57-sizing.png) | [✓ same](pictures/bootstrap-5.3.3/57-sizing.png) | [✗ appearance: moved, drawing](pictures/odoo-17.0/57-sizing.png) | [✓ same](pictures/odoo-18.0/57-sizing.png) | [✓ same](pictures/odoo-19.0/57-sizing.png) | [✓ same](pictures/odoo-20.0/57-sizing.png) |
| Print-only display: .d-print-none, .d-print-block | [✗ content: text](pictures/bootstrap-5.1.3/58-d-print.png) | [✗ content: text](pictures/bootstrap-5.3.3/58-d-print.png) | [✗ content: missing](pictures/odoo-17.0/58-d-print.png) | [✗ content: missing](pictures/odoo-18.0/58-d-print.png) | [✗ content: missing](pictures/odoo-19.0/58-d-print.png) | [✗ content: missing](pictures/odoo-20.0/58-d-print.png) |
| Hidden for sight: .visually-hidden | [✗ content: added](pictures/bootstrap-5.1.3/59-visually-hidden.png) | [✗ content: added](pictures/bootstrap-5.3.3/59-visually-hidden.png) | [✓ same](pictures/odoo-17.0/59-visually-hidden.png) | [✓ same](pictures/odoo-18.0/59-visually-hidden.png) | [✓ same](pictures/odoo-19.0/59-visually-hidden.png) | [✗ content: added](pictures/odoo-20.0/59-visually-hidden.png) |
| Floats: .float-end with .clearfix | [✗ appearance: reflow, moved](pictures/bootstrap-5.1.3/60-float.png) | [✗ appearance: reflow, moved](pictures/bootstrap-5.3.3/60-float.png) | [✗ appearance: moved](pictures/odoo-17.0/60-float.png) | [✓ same](pictures/odoo-18.0/60-float.png) | [✓ same](pictures/odoo-19.0/60-float.png) | [✓ same](pictures/odoo-20.0/60-float.png) |
| Positioned stamp: .position-absolute .top-50 .start-50 .translate-middle | [✗ appearance: moved](pictures/bootstrap-5.1.3/61-position.png) | [✗ appearance: moved](pictures/bootstrap-5.3.3/61-position.png) | [✗ appearance: moved](pictures/odoo-17.0/61-position.png) | [✗ appearance: moved](pictures/odoo-18.0/61-position.png) | [✗ appearance: moved](pictures/odoo-19.0/61-position.png) | [✗ appearance: moved](pictures/odoo-20.0/61-position.png) |
| Opacity: .opacity-50 | [✗ content: missing, picture-added](pictures/bootstrap-5.1.3/62-opacity.png) | [✗ content: missing, picture-added](pictures/bootstrap-5.3.3/62-opacity.png) | [✗ content: missing, picture-added](pictures/odoo-17.0/62-opacity.png) | [✗ content: missing, picture-added](pictures/odoo-18.0/62-opacity.png) | [✗ content: missing, picture-added](pictures/odoo-19.0/62-opacity.png) | [✗ content: missing, picture-added](pictures/odoo-20.0/62-opacity.png) |
| **Borders, corners, shadows** | | | | | | |
| Box border: .border | [✓ same](pictures/bootstrap-5.1.3/65-border.png) | [✗ appearance: drawing](pictures/bootstrap-5.3.3/65-border.png) | [✗ appearance: moved](pictures/odoo-17.0/65-border.png) | [✓ same](pictures/odoo-18.0/65-border.png) | [✓ same](pictures/odoo-19.0/65-border.png) | [✓ same](pictures/odoo-20.0/65-border.png) |
| Rule above the total: .border-top | [✓ same](pictures/bootstrap-5.1.3/66-border-top.png) | [✗ appearance: drawing](pictures/bootstrap-5.3.3/66-border-top.png) | [✗ appearance: moved](pictures/odoo-17.0/66-border-top.png) | [✓ same](pictures/odoo-18.0/66-border-top.png) | [✓ same](pictures/odoo-19.0/66-border-top.png) | [✓ same](pictures/odoo-20.0/66-border-top.png) |
| Border colour and width: .border-primary .border-2 | [✓ same](pictures/bootstrap-5.1.3/67-border-colour.png) | [✗ appearance: drawing](pictures/bootstrap-5.3.3/67-border-colour.png) | [✗ appearance: moved, drawing](pictures/odoo-17.0/67-border-colour.png) | [✗ appearance: drawing](pictures/odoo-18.0/67-border-colour.png) | [✗ appearance: drawing](pictures/odoo-19.0/67-border-colour.png) | [✗ appearance: drawing](pictures/odoo-20.0/67-border-colour.png) |
| Rounded corners: .rounded-3 | [✓ same](pictures/bootstrap-5.1.3/68-rounded.png) | [✗ appearance: corners](pictures/bootstrap-5.3.3/68-rounded.png) | [✓ same](pictures/odoo-17.0/68-rounded.png) | [✗ appearance: corners](pictures/odoo-18.0/68-rounded.png) | [✗ appearance: corners](pictures/odoo-19.0/68-rounded.png) | [✗ appearance: corners](pictures/odoo-20.0/68-rounded.png) |
| Pill shape: .rounded-pill | [✓ same](pictures/bootstrap-5.1.3/69-rounded-pill.png) | [✗ appearance: corners](pictures/bootstrap-5.3.3/69-rounded-pill.png) | [✓ same](pictures/odoo-17.0/69-rounded-pill.png) | [✗ appearance: corners](pictures/odoo-18.0/69-rounded-pill.png) | [✗ appearance: corners](pictures/odoo-19.0/69-rounded-pill.png) | [✗ appearance: corners](pictures/odoo-20.0/69-rounded-pill.png) |
| Shadow: .shadow | [✗ content: picture-added, drawing](pictures/bootstrap-5.1.3/70-shadow.png) | [✗ appearance: drawing](pictures/bootstrap-5.3.3/70-shadow.png) | [✗ content: picture-added, moved](pictures/odoo-17.0/70-shadow.png) | [✗ appearance: drawing](pictures/odoo-18.0/70-shadow.png) | [✗ appearance: drawing](pictures/odoo-19.0/70-shadow.png) | [✗ appearance: drawing](pictures/odoo-20.0/70-shadow.png) |
| **Tables** | | | | | | |
| Invoice lines: .table | [✗ appearance: moved, drawing](pictures/bootstrap-5.1.3/75-table.png) | [✗ appearance: moved, colour](pictures/bootstrap-5.3.3/75-table.png) | [✗ appearance: moved, drawing](pictures/odoo-17.0/75-table.png) | [✗ appearance: moved, drawing](pictures/odoo-18.0/75-table.png) | [✗ appearance: moved, drawing](pictures/odoo-19.0/75-table.png) | [✗ appearance: moved, drawing](pictures/odoo-20.0/75-table.png) |
| A plain &lt;table&gt; without classes, under Bootstrap | [✗ appearance: moved](pictures/bootstrap-5.1.3/76-table-plain.png) | [✗ appearance: moved](pictures/bootstrap-5.3.3/76-table-plain.png) | [✗ appearance: moved](pictures/odoo-17.0/76-table-plain.png) | [✗ appearance: moved, drawing](pictures/odoo-18.0/76-table-plain.png) | [✗ appearance: moved, drawing](pictures/odoo-19.0/76-table-plain.png) | [✗ appearance: moved, drawing](pictures/odoo-20.0/76-table-plain.png) |
| Striped rows: .table-striped | [✗ appearance: moved, drawing](pictures/bootstrap-5.1.3/77-table-striped.png) | [✗ appearance: moved, colour](pictures/bootstrap-5.3.3/77-table-striped.png) | [✗ appearance: moved, drawing](pictures/odoo-17.0/77-table-striped.png) | [✗ appearance: moved, drawing](pictures/odoo-18.0/77-table-striped.png) | [✗ appearance: moved, drawing](pictures/odoo-19.0/77-table-striped.png) | [✗ appearance: moved, drawing](pictures/odoo-20.0/77-table-striped.png) |
| Ruled cells: .table-bordered | [✗ appearance: moved, drawing](pictures/bootstrap-5.1.3/78-table-bordered.png) | [✗ appearance: moved, colour](pictures/bootstrap-5.3.3/78-table-bordered.png) | [✗ appearance: moved](pictures/odoo-17.0/78-table-bordered.png) | [✗ appearance: moved, drawing](pictures/odoo-18.0/78-table-bordered.png) | [✗ appearance: drawing](pictures/odoo-19.0/78-table-bordered.png) | [✗ appearance: drawing](pictures/odoo-20.0/78-table-bordered.png) |
| Compact rows: .table-sm | [✗ appearance: moved, drawing](pictures/bootstrap-5.1.3/79-table-sm.png) | [✗ appearance: moved, colour](pictures/bootstrap-5.3.3/79-table-sm.png) | [✗ appearance: moved, drawing](pictures/odoo-17.0/79-table-sm.png) | [✗ appearance: moved, drawing](pictures/odoo-18.0/79-table-sm.png) | [✗ appearance: moved, drawing](pictures/odoo-19.0/79-table-sm.png) | [✗ appearance: moved, drawing](pictures/odoo-20.0/79-table-sm.png) |
| No lines: .table-borderless | [✗ appearance: moved](pictures/bootstrap-5.1.3/80-table-borderless.png) | [✗ appearance: moved, colour](pictures/bootstrap-5.3.3/80-table-borderless.png) | [✗ appearance: moved](pictures/odoo-17.0/80-table-borderless.png) | [✗ appearance: drawing](pictures/odoo-18.0/80-table-borderless.png) | [✗ appearance: drawing](pictures/odoo-19.0/80-table-borderless.png) | [✗ appearance: drawing](pictures/odoo-20.0/80-table-borderless.png) |
| Header colour: thead.table-light | [✗ appearance: moved, drawing](pictures/bootstrap-5.1.3/81-table-light.png) | [✗ appearance: moved, colour](pictures/bootstrap-5.3.3/81-table-light.png) | [✗ appearance: moved, drawing](pictures/odoo-17.0/81-table-light.png) | [✗ appearance: moved, drawing](pictures/odoo-18.0/81-table-light.png) | [✗ appearance: moved, drawing](pictures/odoo-19.0/81-table-light.png) | [✗ appearance: moved, drawing](pictures/odoo-20.0/81-table-light.png) |
| Dark table: .table-dark | [✗ appearance: moved, drawing](pictures/bootstrap-5.1.3/82-table-dark.png) | [✗ appearance: moved, colour](pictures/bootstrap-5.3.3/82-table-dark.png) | [✗ appearance: moved, drawing](pictures/odoo-17.0/82-table-dark.png) | [✗ appearance: moved, drawing](pictures/odoo-18.0/82-table-dark.png) | [✗ appearance: moved, drawing](pictures/odoo-19.0/82-table-dark.png) | [✗ appearance: moved, drawing](pictures/odoo-20.0/82-table-dark.png) |
| **Components** | | | | | | |
| Card: .card, .card-header, .card-body | [✗ content: picture-added, drawing](pictures/bootstrap-5.1.3/85-card.png) | [✗ appearance: moved](pictures/bootstrap-5.3.3/85-card.png) | [✗ content: moved, picture-added, drawing](pictures/odoo-17.0/85-card.png) | [✗ appearance: moved](pictures/odoo-18.0/85-card.png) | [✗ appearance: moved](pictures/odoo-19.0/85-card.png) | [✗ appearance: moved](pictures/odoo-20.0/85-card.png) |
| Badges: .badge .bg-success, .rounded-pill | [✗ appearance: moved](pictures/bootstrap-5.1.3/86-badge.png) | [✗ appearance: reflow, moved, font](pictures/bootstrap-5.3.3/86-badge.png) | [✗ appearance: moved](pictures/odoo-17.0/86-badge.png) | [✗ appearance: reflow, moved, font](pictures/odoo-18.0/86-badge.png) | [✗ appearance: reflow, moved, font](pictures/odoo-19.0/86-badge.png) | [✗ appearance: reflow, moved, font](pictures/odoo-20.0/86-badge.png) |
| Alert: .alert .alert-info | [✗ content: picture-added, drawing](pictures/bootstrap-5.1.3/87-alert.png) | [✗ appearance: moved, colour](pictures/bootstrap-5.3.3/87-alert.png) | [✗ content: picture-added, moved](pictures/odoo-17.0/87-alert.png) | [✗ appearance: drawing](pictures/odoo-18.0/87-alert.png) | [✗ appearance: drawing](pictures/odoo-19.0/87-alert.png) | [✗ appearance: drawing](pictures/odoo-20.0/87-alert.png) |
| List group: .list-group | [✗ content: picture-added, drawing](pictures/bootstrap-5.1.3/88-list-group.png) | [✗ appearance: moved](pictures/bootstrap-5.3.3/88-list-group.png) | [✗ content: moved, picture-added](pictures/odoo-17.0/88-list-group.png) | [✗ appearance: moved](pictures/odoo-18.0/88-list-group.png) | [✗ appearance: moved](pictures/odoo-19.0/88-list-group.png) | [✗ appearance: moved](pictures/odoo-20.0/88-list-group.png) |
| Button: .btn .btn-primary | [✗ content: picture-added, drawing](pictures/bootstrap-5.1.3/89-button.png) | [✗ appearance: moved, colour](pictures/bootstrap-5.3.3/89-button.png) | [✗ content: picture-added, drawing](pictures/odoo-17.0/89-button.png) | [✗ content: picture-added, drawing](pictures/odoo-18.0/89-button.png) | [✗ content: picture-added, drawing](pictures/odoo-19.0/89-button.png) | [✗ content: picture-added, drawing](pictures/odoo-20.0/89-button.png) |
| Horizontal rule: &lt;hr&gt; | [✗ content: picture-added, drawing](pictures/bootstrap-5.1.3/90-hr.png) | [✗ appearance: moved, drawing](pictures/bootstrap-5.3.3/90-hr.png) | [✗ content: picture-added, drawing](pictures/odoo-17.0/90-hr.png) | [✗ content: picture-added, drawing](pictures/odoo-18.0/90-hr.png) | [✗ content: picture-added, drawing](pictures/odoo-19.0/90-hr.png) | [✗ content: picture-added, drawing](pictures/odoo-20.0/90-hr.png) |
| Responsive image: .img-fluid | [✓ same](pictures/bootstrap-5.1.3/91-img-fluid.png) | [✓ same](pictures/bootstrap-5.3.3/91-img-fluid.png) | [✓ same](pictures/odoo-17.0/91-img-fluid.png) | [✓ same](pictures/odoo-18.0/91-img-fluid.png) | [✓ same](pictures/odoo-19.0/91-img-fluid.png) | [✓ same](pictures/odoo-20.0/91-img-fluid.png) |
| Aspect ratio box: .ratio .ratio-16x9 | [✗ appearance: moved](pictures/bootstrap-5.1.3/92-ratio.png) | [✗ appearance: moved](pictures/bootstrap-5.3.3/92-ratio.png) | [✗ appearance: moved, reflow](pictures/odoo-17.0/92-ratio.png) | [✗ appearance: moved](pictures/odoo-18.0/92-ratio.png) | [✗ appearance: moved](pictures/odoo-19.0/92-ratio.png) | [✗ appearance: moved](pictures/odoo-20.0/92-ratio.png) |
| **Your own CSS** | | | | | | |
| Custom properties: var(--x) | [✗ appearance: moved, size, colour](pictures/bootstrap-5.1.3/95-css-var.png) | [✗ appearance: moved, size, colour](pictures/bootstrap-5.3.3/95-css-var.png) | [✗ appearance: moved, size, colour](pictures/odoo-17.0/95-css-var.png) | [✗ appearance: moved, size, colour](pictures/odoo-18.0/95-css-var.png) | [✗ appearance: moved, size, colour](pictures/odoo-19.0/95-css-var.png) | [✗ appearance: moved, size, colour](pictures/odoo-20.0/95-css-var.png) |
| calc() | [✗ appearance: drawing](pictures/bootstrap-5.1.3/96-css-calc.png) | [✗ appearance: drawing](pictures/bootstrap-5.3.3/96-css-calc.png) | [✗ appearance: moved, drawing](pictures/odoo-17.0/96-css-calc.png) | [✗ appearance: drawing](pictures/odoo-18.0/96-css-calc.png) | [✗ appearance: drawing](pictures/odoo-19.0/96-css-calc.png) | [✗ appearance: drawing](pictures/odoo-20.0/96-css-calc.png) |
| Colour functions: rgba(), rgb( / ), 8-digit hex | [✗ appearance: colour](pictures/bootstrap-5.1.3/97-css-colours.png) | [✗ appearance: colour](pictures/bootstrap-5.3.3/97-css-colours.png) | [✗ appearance: colour](pictures/odoo-17.0/97-css-colours.png) | [✗ appearance: colour](pictures/odoo-18.0/97-css-colours.png) | [✗ appearance: colour](pictures/odoo-19.0/97-css-colours.png) | [✗ appearance: colour](pictures/odoo-20.0/97-css-colours.png) |
| Selectors: :is(), :where(), :not(a, b), :has() | [✗ appearance: colour](pictures/bootstrap-5.1.3/98-css-selectors.png) | [✗ appearance: colour](pictures/bootstrap-5.3.3/98-css-selectors.png) | [✗ appearance: colour](pictures/odoo-17.0/98-css-selectors.png) | [✗ appearance: colour](pictures/odoo-18.0/98-css-selectors.png) | [✗ appearance: colour](pictures/odoo-19.0/98-css-selectors.png) | [✗ appearance: colour](pictures/odoo-20.0/98-css-selectors.png) |
| CSS grid: display: grid | [✗ content: missing, moved, added](pictures/bootstrap-5.1.3/99-css-grid.png) | [✗ content: missing, moved, added](pictures/bootstrap-5.3.3/99-css-grid.png) | [✗ content: moved, missing, added](pictures/odoo-17.0/99-css-grid.png) | [✗ content: missing, moved, added](pictures/odoo-18.0/99-css-grid.png) | [✗ content: missing, moved, added](pictures/odoo-19.0/99-css-grid.png) | [✗ content: missing, moved, added](pictures/odoo-20.0/99-css-grid.png) |
| Logical properties: margin-inline-start, padding-inline | [✗ appearance: moved](pictures/bootstrap-5.1.3/100-css-logical.png) | [✗ appearance: moved](pictures/bootstrap-5.3.3/100-css-logical.png) | [✗ appearance: moved](pictures/odoo-17.0/100-css-logical.png) | [✗ appearance: moved](pictures/odoo-18.0/100-css-logical.png) | [✗ appearance: moved](pictures/odoo-19.0/100-css-logical.png) | [✗ appearance: moved](pictures/odoo-20.0/100-css-logical.png) |
| aspect-ratio | [✗ appearance: moved](pictures/bootstrap-5.1.3/101-css-aspect.png) | [✗ appearance: moved](pictures/bootstrap-5.3.3/101-css-aspect.png) | [✗ appearance: moved](pictures/odoo-17.0/101-css-aspect.png) | [✗ appearance: moved](pictures/odoo-18.0/101-css-aspect.png) | [✗ appearance: moved](pictures/odoo-19.0/101-css-aspect.png) | [✗ appearance: moved](pictures/odoo-20.0/101-css-aspect.png) |
| transform without and with the -webkit- prefix | [✗ appearance: moved](pictures/bootstrap-5.1.3/102-css-transform.png) | [✗ appearance: moved](pictures/bootstrap-5.3.3/102-css-transform.png) | [✗ appearance: moved](pictures/odoo-17.0/102-css-transform.png) | [✗ appearance: moved](pictures/odoo-18.0/102-css-transform.png) | [✗ appearance: moved](pictures/odoo-19.0/102-css-transform.png) | [✗ appearance: moved](pictures/odoo-20.0/102-css-transform.png) |
| position: sticky | [✓ same](pictures/bootstrap-5.1.3/103-css-sticky.png) | [✓ same](pictures/bootstrap-5.3.3/103-css-sticky.png) | [✗ appearance: moved](pictures/odoo-17.0/103-css-sticky.png) | [✓ same](pictures/odoo-18.0/103-css-sticky.png) | [✓ same](pictures/odoo-19.0/103-css-sticky.png) | [✓ same](pictures/odoo-20.0/103-css-sticky.png) |
| **Odoo-style report** | | | | | | |
| Report header: logo row, addresses, invoice details | [✗ content: missing, added, reflow](pictures/bootstrap-5.1.3/110-report-header.png) | [✗ content: missing, added, reflow](pictures/bootstrap-5.3.3/110-report-header.png) | [✗ appearance: reflow](pictures/odoo-17.0/110-report-header.png) | [✗ appearance: moved](pictures/odoo-18.0/110-report-header.png) | [✗ appearance: moved, colour](pictures/odoo-19.0/110-report-header.png) | [✗ appearance: moved, colour](pictures/odoo-20.0/110-report-header.png) |
| Report lines: .table .table-sm with .text-end amounts | [✗ appearance: moved, drawing](pictures/bootstrap-5.1.3/111-report-lines.png) | [✗ appearance: moved, colour](pictures/bootstrap-5.3.3/111-report-lines.png) | [✗ appearance: moved, drawing](pictures/odoo-17.0/111-report-lines.png) | [✗ appearance: moved, drawing](pictures/odoo-18.0/111-report-lines.png) | [✗ appearance: moved, drawing](pictures/odoo-19.0/111-report-lines.png) | [✗ appearance: moved, drawing](pictures/odoo-20.0/111-report-lines.png) |
| Report totals: .row &gt; .col-6 .ms-auto with .border-top | [✗ appearance: moved, drawing](pictures/bootstrap-5.1.3/112-report-totals.png) | [✗ appearance: moved, colour](pictures/bootstrap-5.3.3/112-report-totals.png) | [✗ appearance: moved](pictures/odoo-17.0/112-report-totals.png) | [✗ appearance: moved, drawing](pictures/odoo-18.0/112-report-totals.png) | [✗ appearance: moved, drawing](pictures/odoo-19.0/112-report-totals.png) | [✗ appearance: moved, drawing](pictures/odoo-20.0/112-report-totals.png) |

## Why: what each program read

**Body text: Bootstrap's font, size, line height and colour**

- Bootstrap 5.1.3 alone: the line "Fremont CA 94538" moved 51.7 pt up; computed (wkhtmltopdf / Chrome): body line height (--bs-body-line-height) normal / 24px; line height of a block of lines normal / 24px; body font family (--bs-body-font-family) Times / system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", "Liberation Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"; body text colour (--bs-body-color) rgb(0, 0, 0) / rgb(33, 37, 41)
- Bootstrap 5.3.3 alone: the line "Fremont CA 94538" moved 51.7 pt up; computed (wkhtmltopdf / Chrome): body line height (--bs-body-line-height) normal / 24px; line height of a block of lines normal / 24px; body font family (--bs-body-font-family) Times / system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", "Noto Sans", "Liberation Sans", Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"; body text colour (--bs-body-color) rgb(0, 0, 0) / rgb(33, 37, 41)
- Odoo 17 report CSS: the line "Fremont CA 94538" moved 13.3 pt up; computed (wkhtmltopdf / Chrome): body line height (--bs-body-line-height) 16px / 24px; line height of a block of lines 16px / 24px

**Headings h1 to h4**

- Bootstrap 5.1.3 alone: 2 words of 14.8 pt are now 10.2 pt; computed (wkhtmltopdf / Chrome): h1 size (calc() and vw in Bootstrap 5) 32px / 35.95px; h4 size 16px / 23.19px
- Bootstrap 5.3.3 alone: 2 words of 14.8 pt are now 10.2 pt; computed (wkhtmltopdf / Chrome): h1 size (calc() and vw in Bootstrap 5) 32px / 35.95px; h4 size 16px / 23.19px
- Odoo 19 report CSS: 9 words in #000000 are now in #212529
- Odoo 20 report CSS: 9 words in #000000 are now in #212529

**.lead, &lt;small&gt; and &lt;mark&gt;**

- Bootstrap 5.1.3 alone: the same letters, divided into words differently
- Bootstrap 5.3.3 alone: the same letters, divided into words differently; computed (wkhtmltopdf / Chrome): &lt;mark&gt; background rgb(255, 255, 0) / rgb(255, 243, 205)
- Odoo 17 report CSS: the line "Thank you for choosing YourCompany.": the words stand up to 3.6 pt from where they stood along the line
- Odoo 18 report CSS: 3 words in #212529 are now in #000000; computed (wkhtmltopdf / Chrome): &lt;mark&gt; background rgba(0, 0, 0, 0) / rgb(255, 243, 205)
- Odoo 19 report CSS: 3 words in #212529 are now in #000000; computed (wkhtmltopdf / Chrome): &lt;mark&gt; background rgba(0, 0, 0, 0) / rgb(255, 243, 205)
- Odoo 20 report CSS: 3 words in #212529 are now in #000000; computed (wkhtmltopdf / Chrome): &lt;mark&gt; background rgba(0, 0, 0, 0) / rgb(255, 243, 205)

**Display headings: .display-4**

- Bootstrap 5.1.3 alone: the line "Amount due" moved 25.5 pt up; computed (wkhtmltopdf / Chrome): .display-4 size 16px / 48.71px
- Bootstrap 5.3.3 alone: the line "Amount due" moved 25.5 pt up; computed (wkhtmltopdf / Chrome): .display-4 size 16px / 48.71px
- Odoo 17 report CSS: the line "Amount due" moved 26.1 pt up; computed (wkhtmltopdf / Chrome): .display-4 size 16px / 48.71px

**Font size utilities: .fs-1, .fs-4, .fs-6**

- Bootstrap 5.1.3 alone: the line "Payment terms: 30 days" moved 26.7 pt up; computed (wkhtmltopdf / Chrome): .fs-1 (calc() and vw) 16px / 35.95px
- Bootstrap 5.3.3 alone: the line "Payment terms: 30 days" moved 26.7 pt up; computed (wkhtmltopdf / Chrome): .fs-1 (calc() and vw) 16px / 35.95px
- Odoo 17 report CSS: the line "Payment terms: 30 days" moved 27.4 pt up; computed (wkhtmltopdf / Chrome): .fs-1 (calc() and vw) 16px / 35.95px

**Weight and style: .fw-bold, .fw-light, .fst-italic**

- Odoo 17 report CSS: the line "Untaxed amount: $ 8,400.00": the words stand up to 2.7 pt from where they stood along the line; computed (wkhtmltopdf / Chrome): .fw-bold bold / 700
- Odoo 18 report CSS: the line "Untaxed amount: $ 8,400.00": the words stand up to 2.4 pt from where they stood along the line; computed (wkhtmltopdf / Chrome): .fw-bold bold / 700
- Odoo 19 report CSS: the line "Untaxed amount: $ 8,400.00": the words stand up to 2.4 pt from where they stood along the line; computed (wkhtmltopdf / Chrome): .fw-bold bold / 700
- Odoo 20 report CSS: the line "Untaxed amount: $ 8,400.00": the words stand up to 2.4 pt from where they stood along the line; computed (wkhtmltopdf / Chrome): .fw-bold bold / 700

**Monospace: .font-monospace**

- Bootstrap 5.1.3 alone: 4 words set in liberationmono are now in liberationsans; computed (wkhtmltopdf / Chrome): .font-monospace 'Liberation Sans', Arial, sans-serif / SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace
- Bootstrap 5.3.3 alone: 4 words set in liberationmono are now in liberationsans; computed (wkhtmltopdf / Chrome): .font-monospace 'Liberation Sans', Arial, sans-serif / SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace
- Odoo 17 report CSS: 4 words set in liberationmono are now in lato; computed (wkhtmltopdf / Chrome): .font-monospace Lato / SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace
- Odoo 18 report CSS: 4 words set in liberationmono are now in lato; computed (wkhtmltopdf / Chrome): .font-monospace Lato / SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace
- Odoo 19 report CSS: 4 words set in liberationmono are now in lato; computed (wkhtmltopdf / Chrome): .font-monospace Lato / SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace
- Odoo 20 report CSS: 4 words set in liberationmono are now in lato; computed (wkhtmltopdf / Chrome): .font-monospace Lato / SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace

**Wrapping: .text-nowrap, .text-truncate, .text-break**

- Bootstrap 5.1.3 alone: "…" is now "D…"
- Bootstrap 5.3.3 alone: "…" is now "D…"
- Odoo 17 report CSS: "De…" is now "Des…"
- Odoo 18 report CSS: "De…" is now "Des…"
- Odoo 19 report CSS: "De…" is now "Des…"
- Odoo 20 report CSS: "De…" is now "Des…"

**Text colours: .text-primary, -success, -danger, -warning, -info, -secondary**

- Bootstrap 5.1.3 alone: 2 words in #6c757d are now in #212529; computed (wkhtmltopdf / Chrome): .text-primary rgb(33, 37, 41) / rgb(13, 110, 253); .text-danger rgb(33, 37, 41) / rgb(220, 53, 69)
- Bootstrap 5.3.3 alone: 2 words in #6c757d are now in #212529; computed (wkhtmltopdf / Chrome): .text-primary rgb(33, 37, 41) / rgb(13, 110, 253); .text-danger rgb(33, 37, 41) / rgb(220, 53, 69)

**Backgrounds: .bg-light, .bg-primary, .bg-warning**

- Bootstrap 5.1.3 alone: page 1 lacks rules, frames or tints in 1 place where the old page has them; computed (wkhtmltopdf / Chrome): .bg-light rgba(0, 0, 0, 0) / rgb(248, 249, 250); .bg-primary rgba(0, 0, 0, 0) / rgb(13, 110, 253)
- Bootstrap 5.3.3 alone: page 1 lacks rules, frames or tints in 1 place where the old page has them; computed (wkhtmltopdf / Chrome): .bg-light rgba(0, 0, 0, 0) / rgb(248, 249, 250); .bg-primary rgba(0, 0, 0, 0) / rgb(13, 110, 253)
- Odoo 17 report CSS: the line "Paid in full" moved 13.3 pt up

**Text and background together: .text-bg-success (5.2 and later)**

- Bootstrap 5.3.3 alone: page 1 lacks rules, frames or tints in 1 place where the old page has them; computed (wkhtmltopdf / Chrome): .text-bg-success background rgba(0, 0, 0, 0) / rgb(25, 135, 84)
- Odoo 18 report CSS: page 1 lacks rules, frames or tints in 1 place where the old page has them; computed (wkhtmltopdf / Chrome): .text-bg-success background rgba(0, 0, 0, 0) / rgb(40, 167, 69)
- Odoo 19 report CSS: page 1 lacks rules, frames or tints in 1 place where the old page has them; computed (wkhtmltopdf / Chrome): .text-bg-success background rgba(0, 0, 0, 0) / rgb(40, 167, 69)
- Odoo 20 report CSS: page 1 lacks rules, frames or tints in 1 place where the old page has them; computed (wkhtmltopdf / Chrome): .text-bg-success background rgba(0, 0, 0, 0) / rgb(40, 167, 69)

**Background opacity and gradient: .bg-opacity-25, .bg-gradient**

- Bootstrap 5.1.3 alone: page 1 lacks rules, frames or tints in 1 place where the old page has them; computed (wkhtmltopdf / Chrome): .bg-opacity-25 rgba(0, 0, 0, 0) / rgba(13, 110, 253, 0.25)
- Bootstrap 5.3.3 alone: page 1 lacks rules, frames or tints in 1 place where the old page has them; computed (wkhtmltopdf / Chrome): .bg-opacity-25 rgba(0, 0, 0, 0) / rgba(13, 110, 253, 0.25)
- Odoo 17 report CSS: the line "Thank you" moved 8.2 pt up
- Odoo 18 report CSS: rules, frames or tints differ on page 1: 1 place only in the old, 1 only in the new
- Odoo 19 report CSS: rules, frames or tints differ on page 1: 1 place only in the old, 1 only in the new
- Odoo 20 report CSS: rules, frames or tints differ on page 1: 1 place only in the old, 1 only in the new

**Links**

- Bootstrap 5.3.3 alone: 1 words in #0d6efd are now in #0000ee; computed (wkhtmltopdf / Chrome): link colour rgb(0, 0, 238) / rgb(13, 110, 253)
- Odoo 18 report CSS: 1 words in #66598f are now in #0000ee; computed (wkhtmltopdf / Chrome): link colour rgb(0, 0, 238) / rgb(102, 89, 143)
- Odoo 19 report CSS: 1 words in #66598f are now in #0000ee; computed (wkhtmltopdf / Chrome): link colour rgb(0, 0, 238) / rgb(102, 89, 143)
- Odoo 20 report CSS: 1 words in #66598f are now in #0000ee; computed (wkhtmltopdf / Chrome): link colour rgb(0, 0, 238) / rgb(102, 89, 143)

**Two columns: .row &gt; .col-6 (no gutter, .g-0)**

- Bootstrap 5.1.3 alone: "Delivery address Deco Addict" is new; computed (wkhtmltopdf / Chrome): .row display block / flex
- Bootstrap 5.3.3 alone: "Delivery address Deco Addict" is new; computed (wkhtmltopdf / Chrome): .row display block / flex
- Odoo 17 report CSS: 2 lines from "Fremont CA 94538 Pleasant Hill CA" moved 13.3 pt up; computed (wkhtmltopdf / Chrome): .row display -webkit-box / flex

**Three columns: .row &gt; .col-4 (no gutter)**

- Bootstrap 5.1.3 alone: "Source" is new
- Bootstrap 5.3.3 alone: "Source" is new
- Odoo 17 report CSS: the line "S00042" moved 3.1 pt up

**Columns sized by content: .col-auto and .col (no gutter)**

- Bootstrap 5.1.3 alone: the paragraph beginning "Customer:Azure Interior, 4557 De Silva St," breaks into lines differently (1 lines, now 2)
- Bootstrap 5.3.3 alone: the paragraph beginning "Customer:Azure Interior, 4557 De Silva St," breaks into lines differently (1 lines, now 2)
- Odoo 17 report CSS: "u s t o m e r :" is new

**Gutter between columns: .row &gt; .col-6 with the default gutter**

- Bootstrap 5.1.3 alone: "Delivery address Deco Addict" is new; computed (wkhtmltopdf / Chrome): column padding (half of --bs-gutter-x) 0px / 12px
- Bootstrap 5.3.3 alone: "Delivery address Deco Addict" is new; computed (wkhtmltopdf / Chrome): column padding (half of --bs-gutter-x) 0px / 12px
- Odoo 17 report CSS: the line "Pleasant Hill CA 94523" moved 8 pt to the left, 13.3 pt up; computed (wkhtmltopdf / Chrome): column padding (half of --bs-gutter-x) 0px / 12px
- Odoo 18 report CSS: the line "Pleasant Hill CA 94523" moved 10.6 pt to the left; computed (wkhtmltopdf / Chrome): column padding (half of --bs-gutter-x) 0px / 16px
- Odoo 19 report CSS: the line "Pleasant Hill CA 94523" moved 10.6 pt to the left; computed (wkhtmltopdf / Chrome): column padding (half of --bs-gutter-x) 0px / 16px
- Odoo 20 report CSS: the line "Pleasant Hill CA 94523" moved 10.6 pt to the left; computed (wkhtmltopdf / Chrome): column padding (half of --bs-gutter-x) 0px / 16px

**Wrapping: three .col-6 in one row (no gutter)**

- Bootstrap 5.1.3 alone: "Delivery address Deco Addict" is new
- Bootstrap 5.3.3 alone: "Delivery address Deco Addict" is new
- Odoo 17 report CSS: "Shipping method Truck Incoterm: EXW" is gone
- Odoo 18 report CSS: "Shipping method Truck Incoterm: EXW" is gone
- Odoo 19 report CSS: "Shipping method Truck Incoterm: EXW" is gone
- Odoo 20 report CSS: "Shipping method Truck Incoterm: EXW" is gone

**Offset: .col-5.offset-7, the customer address on the right (no gutter)**

- Odoo 17 report CSS: the line "Fremont CA 94538" moved 13.3 pt up

**Columns pushed apart: .col-5 + .col-5.ms-auto (no gutter)**

- Bootstrap 5.1.3 alone: "Invoicing address Azure Interior" is new
- Bootstrap 5.3.3 alone: "Invoicing address Azure Interior" is new
- Odoo 17 report CSS: "Fremont CA 94538" is now "Fre"
- Odoo 18 report CSS: "Fremont CA 94538" is now "Fremo"
- Odoo 19 report CSS: "Fremont CA 94538" is now "Fremo"
- Odoo 20 report CSS: "Fremont CA 94538" is now "Fremo"

**Order: .order-last (no gutter)**

- Bootstrap 5.1.3 alone: "Delivery address Deco Addict" is new
- Bootstrap 5.3.3 alone: "Delivery address Deco Addict" is new
- Odoo 17 report CSS: the line "Fremont CA 94538" moved 288.3 pt to the left, 13.3 pt up
- Odoo 18 report CSS: the line "Fremont CA 94538" moved 271.7 pt to the left
- Odoo 19 report CSS: the line "Fremont CA 94538" moved 271.7 pt to the left
- Odoo 20 report CSS: the line "Fremont CA 94538" moved 271.7 pt to the left

**Breakpoint columns: .col-md-6 (no gutter)**

- Bootstrap 5.1.3 alone: "Delivery address Deco Addict" is new; computed (wkhtmltopdf / Chrome): media query (min-width: 768px) matches false / true; window width seen by scripts (CSS px) 0 / 930
- Bootstrap 5.3.3 alone: "Delivery address Deco Addict" is new; computed (wkhtmltopdf / Chrome): media query (min-width: 768px) matches false / true; window width seen by scripts (CSS px) 0 / 930
- Odoo 17 report CSS: "Pleasant Hill CA 94523" is now "Ple"; computed (wkhtmltopdf / Chrome): media query (min-width: 768px) matches false / true; window width seen by scripts (CSS px) 0 / 930
- Odoo 18 report CSS: "Pleasant Hill CA 94523" is now "Pleasa"; computed (wkhtmltopdf / Chrome): media query (min-width: 768px) matches false / true; window width seen by scripts (CSS px) 0 / 930
- Odoo 19 report CSS: "Pleasant Hill CA 94523" is now "Pleasa"; computed (wkhtmltopdf / Chrome): media query (min-width: 768px) matches false / true; window width seen by scripts (CSS px) 0 / 930
- Odoo 20 report CSS: "Pleasant Hill CA 94523" is now "Pleasa"; computed (wkhtmltopdf / Chrome): media query (min-width: 768px) matches false / true; window width seen by scripts (CSS px) 0 / 930

**Breakpoint columns: .col-lg-6 (no gutter)**

- Odoo 17 report CSS: "Delivery address Deco Addict 77 Santa Barbara Rd Pleasant Hill CA 94523" is now "Ple"
- Odoo 18 report CSS: "Delivery address Deco Addict 77 Santa Barbara Rd Pleasant Hill CA 94523" is now "Pleasa"
- Odoo 19 report CSS: "Delivery address Deco Addict 77 Santa Barbara Rd Pleasant Hill CA 94523" is now "Pleasa"
- Odoo 20 report CSS: "Delivery address Deco Addict 77 Santa Barbara Rd Pleasant Hill CA 94523" is now "Pleasa"

**Row columns: .row-cols-2 (no gutter)**

- Bootstrap 5.1.3 alone: the line "Mitchell Admin" moved 272.3 pt to the left, 60.9 pt down
- Bootstrap 5.3.3 alone: the line "Mitchell Admin" moved 272.3 pt to the left, 60.9 pt down
- Odoo 17 report CSS: "Source Salesperson S00042 Mitchell Admin" is now "S0"

**Nested rows (no gutter)**

- Bootstrap 5.1.3 alone: "11/21/2026" is gone
- Bootstrap 5.3.3 alone: "11/21/2026" is gone
- Odoo 17 report CSS: the line "Fremont CA 94538" moved 13.3 pt up

**Container padding: .container**

- Bootstrap 5.1.3 alone: the line "Payment terms: 30 days. Please use" moved 49.6 pt to the left; computed (wkhtmltopdf / Chrome): .container padding 0px / 12px
- Bootstrap 5.3.3 alone: the line "Payment terms: 30 days. Please use" moved 49.6 pt to the left; computed (wkhtmltopdf / Chrome): .container padding 0px / 12px
- Odoo 17 report CSS: the line "Payment terms: 30 days. Please use" moved 57.9 pt to the left, 3.1 pt up
- Odoo 18 report CSS: the line "Payment terms: 30 days. Please use" moved 41.3 pt to the left; computed (wkhtmltopdf / Chrome): .container padding 41px / 41.5748px
- Odoo 19 report CSS: the line "Payment terms: 30 days. Please use" moved 41.3 pt to the left; computed (wkhtmltopdf / Chrome): .container padding 41px / 41.5748px
- Odoo 20 report CSS: the line "Payment terms: 30 days. Please use" moved 41.3 pt to the left; computed (wkhtmltopdf / Chrome): .container padding 41px / 41.5748px

**Flex row, ends apart: .d-flex .justify-content-between**

- Bootstrap 5.1.3 alone: the line "INV/2026/00042" moved 470.6 pt to the left, 30.2 pt down; computed (wkhtmltopdf / Chrome): .d-flex display block / flex
- Bootstrap 5.3.3 alone: the line "INV/2026/00042" moved 470.6 pt to the left, 30.2 pt down; computed (wkhtmltopdf / Chrome): .d-flex display block / flex
- Odoo 17 report CSS: the paragraph beginning "YourCompany" breaks into lines differently (4 lines, now 2); computed (wkhtmltopdf / Chrome): .d-flex display -webkit-box / flex

**Flex row, at the end: .d-flex .justify-content-end**

- Bootstrap 5.1.3 alone: the line "Total $ 9,660.00" moved 469.7 pt to the left
- Bootstrap 5.3.3 alone: the line "Total $ 9,660.00" moved 469.7 pt to the left

**Flex row, centred: .d-flex .justify-content-center**

- Bootstrap 5.1.3 alone: the line "Thank you for your business." moved 206.6 pt to the left
- Bootstrap 5.3.3 alone: the line "Thank you for your business." moved 206.6 pt to the left
- Odoo 17 report CSS: the line "Thank you for your business." moved 224.9 pt to the left, 3.1 pt up

**Vertical centring: .d-flex .align-items-center**

- Bootstrap 5.1.3 alone: 2 lines from "YourCompany 250 Executive Park Blvd" moved 57.6 pt to the left, 43.7 pt down
- Bootstrap 5.3.3 alone: 2 lines from "YourCompany 250 Executive Park Blvd" moved 57.6 pt to the left, 43.7 pt down
- Odoo 17 report CSS: the line "250 Executive Park Blvd" moved 16.5 pt up

**Flex column: .d-flex .flex-column**

- Odoo 17 report CSS: the line "Invoice" moved 3.1 pt up

**Filling the row: .flex-grow-1**

- Bootstrap 5.1.3 alone: the line "$ 1,260.00" moved 496.2 pt to the left, 30.2 pt down
- Bootstrap 5.3.3 alone: the line "$ 1,260.00" moved 496.2 pt to the left, 30.2 pt down
- Odoo 17 report CSS: the line "Untaxed" moved 3.1 pt up

**Pushed to the right in a flex row: .ms-auto**

- Bootstrap 5.1.3 alone: the line "30 days" moved 508.8 pt to the left, 14.9 pt down
- Bootstrap 5.3.3 alone: the line "30 days" moved 508.8 pt to the left, 14.9 pt down
- Odoo 17 report CSS: the line "Payment" moved 3.1 pt up
- Odoo 18 report CSS: the paragraph beginning "Payment terms" breaks into lines differently (1 lines, now 1)
- Odoo 19 report CSS: the paragraph beginning "Payment terms" breaks into lines differently (1 lines, now 1)
- Odoo 20 report CSS: the paragraph beginning "Payment terms" breaks into lines differently (1 lines, now 1)

**Space between flex items: .gap-3**

- Bootstrap 5.1.3 alone: the paragraph beginning "Furniture" breaks into lines differently (1 lines, now 1)
- Bootstrap 5.3.3 alone: the paragraph beginning "Furniture" breaks into lines differently (1 lines, now 1)
- Odoo 17 report CSS: the same letters, divided into words differently
- Odoo 18 report CSS: the same letters, divided into words differently
- Odoo 19 report CSS: the same letters, divided into words differently
- Odoo 20 report CSS: the same letters, divided into words differently

**Wrapping flex items: .flex-wrap**

- Bootstrap 5.1.3 alone: the paragraph beginning "Four Person Desk Meeting Table" breaks into lines differently (3 lines, now 5)
- Bootstrap 5.3.3 alone: the paragraph beginning "Four Person Desk Meeting Table" breaks into lines differently (3 lines, now 5)
- Odoo 17 report CSS: the line "Four" moved 3.1 pt up
- Odoo 18 report CSS: the paragraph beginning "Four Person Desk" breaks into lines differently (5 lines, now 1)
- Odoo 19 report CSS: the paragraph beginning "Four Person Desk" breaks into lines differently (5 lines, now 1)
- Odoo 20 report CSS: the paragraph beginning "Four Person Desk" breaks into lines differently (5 lines, now 1)

**Stacks: .hstack and .vstack with .gap-***

- Bootstrap 5.1.3 alone: the line "Source: S00042" moved 9.7 pt down
- Bootstrap 5.3.3 alone: the line "Source: S00042" moved 9.7 pt down
- Odoo 17 report CSS: the line "Source: S00042" moved 18.4 pt up
- Odoo 18 report CSS: the line "Source: S00042" moved 6.3 pt up
- Odoo 19 report CSS: the line "Source: S00042" moved 6.3 pt up
- Odoo 20 report CSS: the line "Source: S00042" moved 6.3 pt up

**Grid display: .d-grid .gap-2**

- Bootstrap 5.1.3 alone: the line "Account: 1234 5678 9012" moved 5.6 pt up
- Bootstrap 5.3.3 alone: the line "Account: 1234 5678 9012" moved 5.6 pt up
- Odoo 17 report CSS: the line "Account: 1234 5678 9012" moved 13.3 pt up
- Odoo 18 report CSS: the line "Account: 1234 5678 9012" moved 6.3 pt up
- Odoo 19 report CSS: the line "Account: 1234 5678 9012" moved 6.3 pt up
- Odoo 20 report CSS: the line "Account: 1234 5678 9012" moved 6.3 pt up

**Spacing: .p-3, .px-5, .mt-4**

- Odoo 17 report CSS: the line "Due date: 12/21/2026" moved 8.2 pt up

**Centred block: .w-50 .mx-auto**

- Odoo 17 report CSS: the line "Thank you for your business." moved 3.1 pt up

**Widths: .w-25, .w-50, .w-100**

- Odoo 17 report CSS: the line "w-100" moved 13.3 pt up

**Print-only display: .d-print-none, .d-print-block**

- Bootstrap 5.1.3 alone: "Printed copy" is now "Pay online at example.com (screen only)"
- Bootstrap 5.3.3 alone: "Printed copy" is now "Pay online at example.com (screen only)"
- Odoo 17 report CSS: "Printed copy" is gone
- Odoo 18 report CSS: "Printed copy" is gone
- Odoo 19 report CSS: "Printed copy" is gone
- Odoo 20 report CSS: "Printed copy" is gone

**Hidden for sight: .visually-hidden**

- Bootstrap 5.1.3 alone: "(amount due, taxes included)" is new
- Bootstrap 5.3.3 alone: "(amount due, taxes included)" is new
- Odoo 20 report CSS: "(amount due, taxes included)" is new

**Floats: .float-end with .clearfix**

- Bootstrap 5.1.3 alone: the line "Thank you." moved 14.9 pt down
- Bootstrap 5.3.3 alone: the line "Thank you." moved 14.9 pt down
- Odoo 17 report CSS: the line "Thank you." moved 6.3 pt up

**Positioned stamp: .position-absolute .top-50 .start-50 .translate-middle**

- Bootstrap 5.1.3 alone: the line "PAID" moved 11.5 pt to the right, 7.2 pt down
- Bootstrap 5.3.3 alone: the line "PAID" moved 11.5 pt to the right, 7.2 pt down
- Odoo 17 report CSS: the line "PAID" moved 11.6 pt to the right, 6.5 pt down
- Odoo 18 report CSS: the line "PAID" moved 11.6 pt to the right, 6.5 pt down
- Odoo 19 report CSS: the line "PAID" moved 11.6 pt to the right, 6.5 pt down
- Odoo 20 report CSS: the line "PAID" moved 11.6 pt to the right, 6.5 pt down

**Opacity: .opacity-50**

- Bootstrap 5.1.3 alone: "DRAFT, not a valid invoice" is gone
- Bootstrap 5.3.3 alone: "DRAFT, not a valid invoice" is gone
- Odoo 17 report CSS: "DRAFT, not a valid invoice" is gone
- Odoo 18 report CSS: "DRAFT, not a valid invoice" is gone
- Odoo 19 report CSS: "DRAFT, not a valid invoice" is gone
- Odoo 20 report CSS: "DRAFT, not a valid invoice" is gone

**Box border: .border**

- Bootstrap 5.3.3 alone: page 1 lacks rules, frames or tints in 1 place where the old page has them; computed (wkhtmltopdf / Chrome): .border width 0px / 1px
- Odoo 17 report CSS: the line "Payment reference: INV/2026/00042" moved 3.1 pt up

**Rule above the total: .border-top**

- Bootstrap 5.3.3 alone: page 1 lacks rules, frames or tints in 1 place where the old page has them; computed (wkhtmltopdf / Chrome): .border-top width 0px / 1px
- Odoo 17 report CSS: the line "Total $ 9,660.00" moved 6.3 pt up

**Border colour and width: .border-primary .border-2**

- Bootstrap 5.3.3 alone: page 1 lacks rules, frames or tints in 1 place where the old page has them; computed (wkhtmltopdf / Chrome): .border-primary rgb(33, 37, 41) / rgb(13, 110, 253)
- Odoo 17 report CSS: page 1 lacks rules, frames or tints in 1 place where the old page has them
- Odoo 18 report CSS: rules, frames or tints differ on page 1: 1 place only in the old, 1 only in the new; computed (wkhtmltopdf / Chrome): .border-primary rgb(33, 37, 41) / rgb(113, 99, 158)
- Odoo 19 report CSS: rules, frames or tints differ on page 1: 1 place only in the old, 1 only in the new; computed (wkhtmltopdf / Chrome): .border-primary rgb(33, 37, 41) / rgb(113, 99, 158)
- Odoo 20 report CSS: rules, frames or tints differ on page 1: 1 place only in the old, 1 only in the new; computed (wkhtmltopdf / Chrome): .border-primary rgb(33, 37, 41) / rgb(113, 99, 158)

**Rounded corners: .rounded-3**

- Bootstrap 5.3.3 alone: .rounded-3: 0px in wkhtmltopdf, 8px in Chrome (computed style; compare does not compare corner shapes); computed (wkhtmltopdf / Chrome): .rounded-3 0px / 8px
- Odoo 18 report CSS: .rounded-3: 0px in wkhtmltopdf, 12px in Chrome (computed style; compare does not compare corner shapes); computed (wkhtmltopdf / Chrome): .rounded-3 0px / 12px
- Odoo 19 report CSS: .rounded-3: 0px in wkhtmltopdf, 12px in Chrome (computed style; compare does not compare corner shapes); computed (wkhtmltopdf / Chrome): .rounded-3 0px / 12px
- Odoo 20 report CSS: .rounded-3: 0px in wkhtmltopdf, 12px in Chrome (computed style; compare does not compare corner shapes); computed (wkhtmltopdf / Chrome): .rounded-3 0px / 12px

**Pill shape: .rounded-pill**

- Bootstrap 5.3.3 alone: .rounded-pill: 0px in wkhtmltopdf, 800px in Chrome (computed style; compare does not compare corner shapes); computed (wkhtmltopdf / Chrome): .rounded-pill 0px / 800px
- Odoo 18 report CSS: .rounded-pill: 0px in wkhtmltopdf, 800px in Chrome (computed style; compare does not compare corner shapes); computed (wkhtmltopdf / Chrome): .rounded-pill 0px / 800px
- Odoo 19 report CSS: .rounded-pill: 0px in wkhtmltopdf, 800px in Chrome (computed style; compare does not compare corner shapes); computed (wkhtmltopdf / Chrome): .rounded-pill 0px / 800px
- Odoo 20 report CSS: .rounded-pill: 0px in wkhtmltopdf, 800px in Chrome (computed style; compare does not compare corner shapes); computed (wkhtmltopdf / Chrome): .rounded-pill 0px / 800px

**Shadow: .shadow**

- Bootstrap 5.1.3 alone: a picture on page 1 is new; computed (wkhtmltopdf / Chrome): .shadow rgba(0, 0, 0, 0.148438) 0px 8px 16px 0px / rgba(0, 0, 0, 0.15) 0px 8px 16px 0px
- Bootstrap 5.3.3 alone: page 1 lacks rules, frames or tints in 1 place where the old page has them; computed (wkhtmltopdf / Chrome): .shadow none / rgba(0, 0, 0, 0.15) 0px 8px 16px 0px
- Odoo 17 report CSS: a picture on page 1 is new; computed (wkhtmltopdf / Chrome): .shadow rgba(0, 0, 0, 0.148438) 0px 8px 16px 0px / rgba(0, 0, 0, 0.15) 0px 8px 16px 0px
- Odoo 18 report CSS: page 1 lacks rules, frames or tints in 1 place where the old page has them; computed (wkhtmltopdf / Chrome): .shadow none / rgba(0, 0, 0, 0.15) 0px 8px 16px 0px
- Odoo 19 report CSS: page 1 lacks rules, frames or tints in 1 place where the old page has them; computed (wkhtmltopdf / Chrome): .shadow none / rgba(0, 0, 0, 0.15) 0px 8px 16px 0px
- Odoo 20 report CSS: page 1 lacks rules, frames or tints in 1 place where the old page has them; computed (wkhtmltopdf / Chrome): .shadow none / rgba(0, 0, 0, 0.15) 0px 8px 16px 0px

**Invoice lines: .table**

- Bootstrap 5.1.3 alone: rules, frames or tints differ on page 1: 3 places only in the old, 24 only in the new
- Bootstrap 5.3.3 alone: 5 lines from "[E-COM07] Large Cabinet 3.00 320.00 15%" moved 2.4 pt up; computed (wkhtmltopdf / Chrome): line under each row 0px / 1px
- Odoo 17 report CSS: 5 lines from "[E-COM07] Large Cabinet 3.00 320.00 15%" moved 18.4 pt up
- Odoo 18 report CSS: 5 lines from "[E-COM07] Large Cabinet 3.00 320.00 15%" moved 2.4 pt up; computed (wkhtmltopdf / Chrome): line under each row 0px / 1px
- Odoo 19 report CSS: 5 lines from "[E-COM07] Large Cabinet 3.00 320.00 15%" moved 2.4 pt up; computed (wkhtmltopdf / Chrome): line under each row 0px / 1px
- Odoo 20 report CSS: 5 lines from "[E-COM07] Large Cabinet 3.00 320.00 15%" moved 2.4 pt up; computed (wkhtmltopdf / Chrome): line under each row 0px / 1px

**A plain &lt;table&gt; without classes, under Bootstrap**

- Bootstrap 5.1.3 alone: the line "Description" moved 96.3 pt to the right
- Bootstrap 5.3.3 alone: the line "Description" moved 96.3 pt to the right
- Odoo 17 report CSS: 5 lines from "[E-COM07] Large Cabinet 3.00 320.00 15%" moved 18.4 pt up
- Odoo 18 report CSS: page 1 has rules, frames or tints in 1 place where the old page has none
- Odoo 19 report CSS: page 1 has rules, frames or tints in 1 place where the old page has none
- Odoo 20 report CSS: page 1 has rules, frames or tints in 1 place where the old page has none

**Striped rows: .table-striped**

- Bootstrap 5.1.3 alone: rules, frames or tints differ on page 1: 3 places only in the old, 24 only in the new; computed (wkhtmltopdf / Chrome): stripe on odd rows none / rgba(0, 0, 0, 0.05) 0px 0px 0px 9999px inset
- Bootstrap 5.3.3 alone: 5 lines from "[E-COM07] Large Cabinet 3.00 320.00 15%" moved 2.4 pt up; computed (wkhtmltopdf / Chrome): stripe on odd rows none / rgba(0, 0, 0, 0.05) 0px 0px 0px 9999px inset
- Odoo 17 report CSS: 5 lines from "[E-COM07] Large Cabinet 3.00 320.00 15%" moved 18.4 pt up; computed (wkhtmltopdf / Chrome): stripe on odd rows none / rgba(0, 0, 0, 0.05) 0px 0px 0px 9999px inset
- Odoo 18 report CSS: 5 lines from "[E-COM07] Large Cabinet 3.00 320.00 15%" moved 2.4 pt up; computed (wkhtmltopdf / Chrome): stripe on odd rows none / rgba(0, 0, 0, 0) 0px 0px 0px 9999px inset
- Odoo 19 report CSS: 5 lines from "[E-COM07] Large Cabinet 3.00 320.00 15%" moved 2.4 pt up; computed (wkhtmltopdf / Chrome): stripe on odd rows none / rgba(0, 0, 0, 0) 0px 0px 0px 9999px inset
- Odoo 20 report CSS: 5 lines from "[E-COM07] Large Cabinet 3.00 320.00 15%" moved 2.4 pt up; computed (wkhtmltopdf / Chrome): stripe on odd rows none / rgba(0, 0, 0, 0) 0px 0px 0px 9999px inset

**Ruled cells: .table-bordered**

- Bootstrap 5.1.3 alone: the line "Description" moved 91.5 pt to the right
- Bootstrap 5.3.3 alone: 10 lines from "[FURN_6741] Large Meeting Table 1.00 4,000.00" moved 2.4 pt up; computed (wkhtmltopdf / Chrome): side borders 0px / 1px
- Odoo 17 report CSS: 5 lines from "[E-COM07] Large Cabinet 3.00 320.00 15%" moved 18.4 pt up
- Odoo 18 report CSS: 4 lines from "3.00 320.00 15% 960.00" moved 3.1 pt up; computed (wkhtmltopdf / Chrome): side borders 0px / 1px
- Odoo 19 report CSS: page 1 lacks rules, frames or tints in 20 places where the old page has them
- Odoo 20 report CSS: page 1 lacks rules, frames or tints in 20 places where the old page has them

**Compact rows: .table-sm**

- Bootstrap 5.1.3 alone: rules, frames or tints differ on page 1: 3 places only in the old, 24 only in the new
- Bootstrap 5.3.3 alone: 5 lines from "[E-COM07] Large Cabinet 3.00 320.00 15%" moved 2.4 pt up
- Odoo 17 report CSS: 5 lines from "[E-COM07] Large Cabinet 3.00 320.00 15%" moved 18.4 pt up
- Odoo 18 report CSS: 5 lines from "[E-COM07] Large Cabinet 3.00 320.00 15%" moved 2.4 pt up
- Odoo 19 report CSS: 5 lines from "[E-COM07] Large Cabinet 3.00 320.00 15%" moved 2.4 pt up
- Odoo 20 report CSS: 5 lines from "[E-COM07] Large Cabinet 3.00 320.00 15%" moved 2.4 pt up

**No lines: .table-borderless**

- Bootstrap 5.1.3 alone: the line "Description" moved 91.8 pt to the right
- Bootstrap 5.3.3 alone: 29 words in #000000 are now in #212529
- Odoo 17 report CSS: 5 lines from "[E-COM07] Large Cabinet 3.00 320.00 15%" moved 18.4 pt up
- Odoo 18 report CSS: page 1 lacks rules, frames or tints in 2 places where the old page has them
- Odoo 19 report CSS: page 1 lacks rules, frames or tints in 2 places where the old page has them
- Odoo 20 report CSS: page 1 lacks rules, frames or tints in 2 places where the old page has them

**Header colour: thead.table-light**

- Bootstrap 5.1.3 alone: rules, frames or tints differ on page 1: 3 places only in the old, 24 only in the new; computed (wkhtmltopdf / Chrome): header background rgba(0, 0, 0, 0) / rgb(248, 249, 250)
- Bootstrap 5.3.3 alone: 5 lines from "[E-COM07] Large Cabinet 3.00 320.00 15%" moved 2.4 pt up; computed (wkhtmltopdf / Chrome): header background rgba(0, 0, 0, 0) / rgb(248, 249, 250)
- Odoo 17 report CSS: 5 lines from "[E-COM07] Large Cabinet 3.00 320.00 15%" moved 18.4 pt up; computed (wkhtmltopdf / Chrome): header background rgba(0, 0, 0, 0) / rgb(248, 249, 250)
- Odoo 18 report CSS: 5 lines from "[E-COM07] Large Cabinet 3.00 320.00 15%" moved 2.4 pt up
- Odoo 19 report CSS: 5 lines from "[E-COM07] Large Cabinet 3.00 320.00 15%" moved 2.4 pt up
- Odoo 20 report CSS: 5 lines from "[E-COM07] Large Cabinet 3.00 320.00 15%" moved 2.4 pt up

**Dark table: .table-dark**

- Bootstrap 5.1.3 alone: rules, frames or tints differ on page 1: 2 places only in the old, 18 only in the new; computed (wkhtmltopdf / Chrome): background rgba(0, 0, 0, 0) / rgb(33, 37, 41)
- Bootstrap 5.3.3 alone: 5 lines from "[E-COM07] Large Cabinet 3.00 320.00 15%" moved 2.4 pt up; computed (wkhtmltopdf / Chrome): background rgba(0, 0, 0, 0) / rgb(33, 37, 41); text colour rgb(33, 37, 41) / rgb(255, 255, 255)
- Odoo 17 report CSS: 5 lines from "[E-COM07] Large Cabinet 3.00 320.00 15%" moved 18.4 pt up; computed (wkhtmltopdf / Chrome): background rgba(0, 0, 0, 0) / rgb(33, 37, 41)
- Odoo 18 report CSS: 5 lines from "[E-COM07] Large Cabinet 3.00 320.00 15%" moved 2.4 pt up
- Odoo 19 report CSS: 5 lines from "[E-COM07] Large Cabinet 3.00 320.00 15%" moved 2.4 pt up
- Odoo 20 report CSS: 5 lines from "[E-COM07] Large Cabinet 3.00 320.00 15%" moved 2.4 pt up

**Card: .card, .card-header, .card-body**

- Bootstrap 5.1.3 alone: a picture on page 1 is new; computed (wkhtmltopdf / Chrome): .card-header background rgba(0, 0, 0, 0.0273438) / rgba(0, 0, 0, 0.03)
- Bootstrap 5.3.3 alone: 3 lines from "Bank of America Account 1234 5678" moved 10.9 pt to the left, 22.3 pt up; computed (wkhtmltopdf / Chrome): card border 0px / 1px; .card-body padding 0px / 16px; .card-header background rgba(0, 0, 0, 0) / rgba(33, 37, 41, 0.03)
- Odoo 17 report CSS: a picture on page 1 is new; computed (wkhtmltopdf / Chrome): .card-header background rgba(0, 0, 0, 0.0273438) / rgba(0, 0, 0, 0.03)
- Odoo 18 report CSS: 2 lines from "Account 1234 5678 9012 BIC BOFAUS3N" moved 11.2 pt to the left, 30.6 pt up; computed (wkhtmltopdf / Chrome): card border 0px / 1px; .card-body padding 0px / 16px; .card-header background rgba(0, 0, 0, 0) / rgba(33, 37, 41, 0.03)
- Odoo 19 report CSS: 2 lines from "Account 1234 5678 9012 BIC BOFAUS3N" moved 11.2 pt to the left, 30.6 pt up; computed (wkhtmltopdf / Chrome): card border 0px / 1px; .card-body padding 0px / 16px; .card-header background rgba(0, 0, 0, 0) / rgba(33, 37, 41, 0.03)
- Odoo 20 report CSS: 2 lines from "Account 1234 5678 9012 BIC BOFAUS3N" moved 11.2 pt to the left, 30.6 pt up; computed (wkhtmltopdf / Chrome): card border 0px / 1px; .card-body padding 0px / 16px; .card-header background rgba(0, 0, 0, 0) / rgba(33, 37, 41, 0.03)

**Badges: .badge .bg-success, .rounded-pill**

- Bootstrap 5.1.3 alone: 2 lines from "Overdue Draft" moved 2.2 pt to the left; computed (wkhtmltopdf / Chrome): .badge background rgba(0, 0, 0, 0) / rgb(25, 135, 84); .badge padding 7px / 7.8px
- Bootstrap 5.3.3 alone: the line "Draft" moved 13.5 pt to the left; computed (wkhtmltopdf / Chrome): .badge background rgba(0, 0, 0, 0) / rgb(25, 135, 84); .badge padding 0px / 7.8px
- Odoo 17 report CSS: the line "Draft" moved 2.8 pt to the left; computed (wkhtmltopdf / Chrome): .badge padding 7px / 7.8px
- Odoo 18 report CSS: the line "Draft" moved 18 pt to the left; computed (wkhtmltopdf / Chrome): .badge padding 0px / 9.84px
- Odoo 19 report CSS: the line "Draft" moved 18 pt to the left; computed (wkhtmltopdf / Chrome): .badge padding 0px / 9.84px
- Odoo 20 report CSS: the line "Draft" moved 18 pt to the left; computed (wkhtmltopdf / Chrome): .badge padding 0px / 9.84px

**Alert: .alert .alert-info**

- Bootstrap 5.1.3 alone: a picture on page 1 is new
- Bootstrap 5.3.3 alone: 9 words in #055160 are now in #212529; computed (wkhtmltopdf / Chrome): .alert-info background rgba(0, 0, 0, 0) / rgb(207, 244, 252); .alert padding 0px / 16px
- Odoo 17 report CSS: a picture on page 1 is new
- Odoo 18 report CSS: page 1 lacks rules, frames or tints in 1 place where the old page has them
- Odoo 19 report CSS: page 1 lacks rules, frames or tints in 1 place where the old page has them
- Odoo 20 report CSS: page 1 lacks rules, frames or tints in 1 place where the old page has them

**List group: .list-group**

- Bootstrap 5.1.3 alone: a picture on page 1 is new
- Bootstrap 5.3.3 alone: the line "Large Cabinet" moved 10.9 pt to the left, 28 pt up; computed (wkhtmltopdf / Chrome): item border 0px / 1px
- Odoo 17 report CSS: a picture on page 1 is new
- Odoo 18 report CSS: the line "Large Cabinet" moved 11.2 pt to the left, 28.7 pt up; computed (wkhtmltopdf / Chrome): item border 0px / 1px
- Odoo 19 report CSS: the line "Large Cabinet" moved 11.2 pt to the left, 28.7 pt up; computed (wkhtmltopdf / Chrome): item border 0px / 1px
- Odoo 20 report CSS: the line "Large Cabinet" moved 11.2 pt to the left, 28.7 pt up; computed (wkhtmltopdf / Chrome): item border 0px / 1px

**Button: .btn .btn-primary**

- Bootstrap 5.1.3 alone: a picture on page 1 is new
- Bootstrap 5.3.3 alone: 2 words in #ffffff are now in #0000ee; computed (wkhtmltopdf / Chrome): .btn-primary background rgba(0, 0, 0, 0) / rgb(13, 110, 253)
- Odoo 17 report CSS: a picture on page 1 is new
- Odoo 18 report CSS: a picture on page 1 is new
- Odoo 19 report CSS: a picture on page 1 is new
- Odoo 20 report CSS: a picture on page 1 is new

**Horizontal rule: &lt;hr&gt;**

- Bootstrap 5.1.3 alone: a picture on page 1 is new
- Bootstrap 5.3.3 alone: the line "Total $ 9,660.00" moved 11.4 pt up; computed (wkhtmltopdf / Chrome): &lt;hr&gt; line 0px / 1px
- Odoo 17 report CSS: a picture on page 1 is new
- Odoo 18 report CSS: a picture on page 1 is new
- Odoo 19 report CSS: a picture on page 1 is new
- Odoo 20 report CSS: a picture on page 1 is new

**Aspect ratio box: .ratio .ratio-16x9**

- Bootstrap 5.1.3 alone: the line "Delivery address: Deco Addict" moved 115.7 pt up
- Bootstrap 5.3.3 alone: the line "Delivery address: Deco Addict" moved 115.7 pt up
- Odoo 17 report CSS: the line "Delivery" moved 116.3 pt up
- Odoo 18 report CSS: the line "Delivery address: Deco Addict" moved 116.3 pt up
- Odoo 19 report CSS: the line "Delivery address: Deco Addict" moved 116.3 pt up
- Odoo 20 report CSS: the line "Delivery address: Deco Addict" moved 116.3 pt up

**Custom properties: var(--x)**

- Bootstrap 5.1.3 alone: 3 words in #0d6efd are now in #212529; computed (wkhtmltopdf / Chrome): colour from var() rgb(33, 37, 41) / rgb(13, 110, 253)
- Bootstrap 5.3.3 alone: 3 words in #0d6efd are now in #212529; computed (wkhtmltopdf / Chrome): colour from var() rgb(33, 37, 41) / rgb(13, 110, 253)
- Odoo 17 report CSS: 3 words in #0d6efd are now in #000000; computed (wkhtmltopdf / Chrome): colour from var() rgb(0, 0, 0) / rgb(13, 110, 253)
- Odoo 18 report CSS: 3 words in #0d6efd are now in #212529; computed (wkhtmltopdf / Chrome): colour from var() rgb(33, 37, 41) / rgb(13, 110, 253)
- Odoo 19 report CSS: 3 words in #0d6efd are now in #212529; computed (wkhtmltopdf / Chrome): colour from var() rgb(33, 37, 41) / rgb(13, 110, 253)
- Odoo 20 report CSS: 3 words in #0d6efd are now in #212529; computed (wkhtmltopdf / Chrome): colour from var() rgb(33, 37, 41) / rgb(13, 110, 253)

**calc()**

- Bootstrap 5.1.3 alone: page 1 has rules, frames or tints in 1 place where the old page has none
- Bootstrap 5.3.3 alone: page 1 has rules, frames or tints in 1 place where the old page has none
- Odoo 17 report CSS: the line "Thank you for your business." moved 3.1 pt up
- Odoo 18 report CSS: page 1 has rules, frames or tints in 1 place where the old page has none
- Odoo 19 report CSS: page 1 has rules, frames or tints in 1 place where the old page has none
- Odoo 20 report CSS: page 1 has rules, frames or tints in 1 place where the old page has none

**Colour functions: rgba(), rgb( / ), 8-digit hex**

- Bootstrap 5.1.3 alone: 8 words in #0d6efd are now in #212529
- Bootstrap 5.3.3 alone: 8 words in #0d6efd are now in #212529
- Odoo 17 report CSS: 8 words in #0d6efd are now in #000000
- Odoo 18 report CSS: 8 words in #0d6efd are now in #212529
- Odoo 19 report CSS: 8 words in #0d6efd are now in #212529
- Odoo 20 report CSS: 8 words in #0d6efd are now in #212529

**Selectors: :is(), :where(), :not(a, b), :has()**

- Bootstrap 5.1.3 alone: 8 words in #198754 are now in #212529
- Bootstrap 5.3.3 alone: 8 words in #198754 are now in #212529
- Odoo 17 report CSS: 8 words in #198754 are now in #000000
- Odoo 18 report CSS: 8 words in #198754 are now in #212529
- Odoo 19 report CSS: 8 words in #198754 are now in #212529
- Odoo 20 report CSS: 8 words in #198754 are now in #212529

**CSS grid: display: grid**

- Bootstrap 5.1.3 alone: "Delivery address Deco Addict" is new
- Bootstrap 5.3.3 alone: "Delivery address Deco Addict" is new
- Odoo 17 report CSS: "Delivery address Deco Addict" is new
- Odoo 18 report CSS: "Delivery address Deco Addict" is new
- Odoo 19 report CSS: "Delivery address Deco Addict" is new
- Odoo 20 report CSS: "Delivery address Deco Addict" is new

**Logical properties: margin-inline-start, padding-inline**

- Bootstrap 5.1.3 alone: 2 lines from "Delivery address: Deco Addict Invoicing address:" moved 128 pt to the left
- Bootstrap 5.3.3 alone: 2 lines from "Delivery address: Deco Addict Invoicing address:" moved 128 pt to the left
- Odoo 17 report CSS: 2 lines from "Delivery address: Deco Addict Invoicing address:" moved 128 pt to the left
- Odoo 18 report CSS: 2 lines from "Delivery address: Deco Addict Invoicing address:" moved 128.4 pt to the left
- Odoo 19 report CSS: 2 lines from "Delivery address: Deco Addict Invoicing address:" moved 128.4 pt to the left
- Odoo 20 report CSS: 2 lines from "Delivery address: Deco Addict Invoicing address:" moved 128.4 pt to the left

**aspect-ratio**

- Bootstrap 5.1.3 alone: the line "YourCompany" moved 49.1 pt up
- Bootstrap 5.3.3 alone: the line "YourCompany" moved 49.1 pt up
- Odoo 17 report CSS: the line "YourCompany" moved 54.9 pt up
- Odoo 18 report CSS: the line "YourCompany" moved 49.8 pt up
- Odoo 19 report CSS: the line "YourCompany" moved 49.8 pt up
- Odoo 20 report CSS: the line "YourCompany" moved 49.8 pt up

**transform without and with the -webkit- prefix**

- Bootstrap 5.1.3 alone: 2 lines from "PAID -webkit- transform" moved 26.1 pt up
- Bootstrap 5.3.3 alone: 2 lines from "PAID -webkit- transform" moved 26.1 pt up
- Odoo 17 report CSS: the line "transform" moved 33.6 pt up
- Odoo 18 report CSS: 2 lines from "PAID -webkit- transform" moved 26.7 pt up
- Odoo 19 report CSS: 2 lines from "PAID -webkit- transform" moved 26.7 pt up
- Odoo 20 report CSS: 2 lines from "PAID -webkit- transform" moved 26.7 pt up

**position: sticky**

- Odoo 17 report CSS: the line "Lines follow." moved 6.3 pt up

**Report header: logo row, addresses, invoice details**

- Bootstrap 5.1.3 alone: "Source" is new
- Bootstrap 5.3.3 alone: "Source" is new
- Odoo 17 report CSS: the paragraph beginning "YourCompany" breaks into lines differently (10 lines, now 12)
- Odoo 18 report CSS: 2 lines from "Invoice Date Due Date Source 11/21/2026": the words stand up to 41.3 pt from where they stood along the line
- Odoo 19 report CSS: 2 lines from "Invoice Date Due Date Source 11/21/2026": the words stand up to 41.3 pt from where they stood along the line
- Odoo 20 report CSS: 2 lines from "Invoice Date Due Date Source 11/21/2026": the words stand up to 41.3 pt from where they stood along the line

**Report lines: .table .table-sm with .text-end amounts**

- Bootstrap 5.1.3 alone: rules, frames or tints differ on page 1: 3 places only in the old, 24 only in the new
- Bootstrap 5.3.3 alone: 5 lines from "[E-COM07] Large Cabinet 3.00 320.00 15%" moved 2.4 pt up
- Odoo 17 report CSS: 5 lines from "[E-COM07] Large Cabinet 3.00 320.00 15%" moved 18.4 pt up
- Odoo 18 report CSS: 5 lines from "[E-COM07] Large Cabinet 3.00 320.00 15%" moved 2.4 pt up
- Odoo 19 report CSS: 5 lines from "[E-COM07] Large Cabinet 3.00 320.00 15%" moved 2.4 pt up
- Odoo 20 report CSS: 5 lines from "[E-COM07] Large Cabinet 3.00 320.00 15%" moved 2.4 pt up

**Report totals: .row &gt; .col-6 .ms-auto with .border-top**

- Bootstrap 5.1.3 alone: the line "Please use the following communication for" moved 10.7 pt up
- Bootstrap 5.3.3 alone: the line "Please use the following communication for" moved 12.7 pt up
- Odoo 17 report CSS: the line "Please use the following communication for" moved 26.7 pt up
- Odoo 18 report CSS: the line "Please use the following communication for" moved 12.7 pt up
- Odoo 19 report CSS: the line "Please use the following communication for" moved 12.7 pt up
- Odoo 20 report CSS: the line "Please use the following communication for" moved 12.7 pt up
