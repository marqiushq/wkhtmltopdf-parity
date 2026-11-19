# wkhtmltopdf parity suite

**Will your PDFs change if you replace wkhtmltopdf with marqius-wkhtmltopdf?** This suite answers with evidence you can rerun. The same documents go through wkhtmltopdf 0.12.6 and through marqius-wkhtmltopdf, side by side on one Linux system with one set of fonts, and every pair of PDFs is compared. The numbers below come from runs whose logs you can read, and one command reruns them on your machine, with our documents or with your own templates.

> marqius-wkhtmltopdf is a paid product of Simple AI LLC, which publishes this suite. The suite and its documents are open (MIT and CC0); the program is not. We publish the misses along with the matches.

## Check your own templates

You need Docker and nothing else. Nothing is uploaded: the containers that read your files have no network.

```bash
git clone https://github.com/marqiushq/wkhtmltopdf-parity.git
cd wkhtmltopdf-parity
cp corpus/everyday/*.html mine/
./run.sh mine
```

That runs eight sample documents. For yours, take the samples out of `mine/` (keep its README), put your templates there with the pictures and style sheets they load, write the options your app passes in `mine/options.txt`, and run `./run.sh mine` again. Then open `out/mine/report.html`. For each template it gives the score, what differs and where, both PDFs, and pictures of the pages that differ. A few dozen templates take under a minute once the images are downloaded (about 175 MB the first time). [What goes in `mine/`](mine/README.md).

### If you want help with the differences

`./run.sh share` shows you the summary of your last `./run.sh mine` and sends it to us only if you type yes. The summary holds the versions and the platform, how many templates there were, each template's scores in order of score without its name, the kinds of difference `compare` found (such as "moved" or "font"), and the names of the options you use, never their values. It never holds a template, a file name, a path or any text from your templates. Add `--email` with your address if you want an answer, and `--note` with a question. A copy of what was sent stays beside the report. We use it only to answer you and to learn which differences matter most, keep it for twelve months, and delete it when you ask. Our [privacy notice](https://marqius.com/privacy/#parity-shares) says the same.

## The scoreboard

<!-- scoreboard:start (written by harness/publish.py from results/; edits here are overwritten) -->
**marqius-wkhtmltopdf 0.12.6** beside **wkhtmltopdf 0.12.6**, checked 19 November 2026, 18:41 UTC on GitHub Actions, x86-64, 4 CPUs: [the run's log](https://github.com/marqiushq/wkhtmltopdf-parity/actions/runs/44590368732) · [full report](results/0.12.6/linux-amd64/report.md) · [every document](results/0.12.6/linux-amd64/scores.csv)

| What was converted | Documents | Parity | Overlay | Same pages | Appearance only | Content differs | Speed |
|---|---:|---:|---:|---:|---:|---:|---:|
| Business documents (`everyday`) | 8 | 0.9902 | 0.996 | 3 | 4 | 1 | 34× |
| CSS features, one to a page (`print`) | 78 | 0.9920 | 0.980 | 56 | 17 | 5 | 39× |
| **The 86 published documents together** | **86** | **0.9919** | 0.981 | 59 | 21 | 6 | **38×** |
| wkhtmltopdf's own options (`options`) | 18 | 0.8895 | 0.684 | 1 | 14 | 3 | 28× |
| Languages and scripts (`international`) | 10 | 0.7073 | 0.694 | 0 | 3 | 7 | 1× |

Speed is the time to convert the published documents one after another, wkhtmltopdf's divided by marqius-wkhtmltopdf's: 19.7 s against 0.52 s (median of 3 runs); 4× with wkhtmltopdf's 200 ms script wait turned off for both.

Sizes: the 86 PDFs come to 1.1 MB from wkhtmltopdf and 2.0 MB from marqius-wkhtmltopdf. The `marqius/wkhtmltopdf` image is 25 MB unpacked; the image wkhtmltopdf runs in here, with its fonts, 330 MB.

On GitHub Actions, ARM64, 4 CPUs: the same parity in every set, 32× faster ([report](results/0.12.6/linux-arm64/report.md)).

#### Every version

| Version | Checked | Business documents | CSS features | Published 86 | Options | Languages | Speed |
|---|---|---:|---:|---:|---:|---:|---:|
| [0.12.6](results/0.12.6/linux-amd64/report.md) | 2026-11-19 | 0.9902 | 0.9920 | 0.9919 | 0.8895 | 0.7073 | 38× |

<details>
<summary><b>The 33 documents below 0.99 or with different content, and why</b></summary>

| Document | Parity | Overlay | Why | Pages |
|---|---:|---:|---|---|
| `international/notice-he` | 0.2463 | 0.258 | A real difference: marqius-wkhtmltopdf draws the letters of each Hebrew word in reverse order and does not mirror the right-to-left table. Hebrew is not supported yet. | [1](results/0.12.6/linux-amd64/pictures/international--notice-he.page-1.png) |
| `international/invoice-ar` | 0.2477 | 0.288 | A real difference: marqius-wkhtmltopdf draws Arabic letters unjoined and in reverse order within each word, and does not mirror the right-to-left table. Arabic is not supported yet. | [1](results/0.12.6/linux-amd64/pictures/international--invoice-ar.page-1.png) |
| `options/javascript` | 0.3332 | 0.136 | A real difference: marqius-wkhtmltopdf runs document.write, but the page's DOM is missing (document.getElementById, querySelector and createElement are undefined), so everything this script adds is missing. | [1](results/0.12.6/linux-amd64/pictures/options--javascript.page-1.png) |
| `international/letter-hi` | 0.4659 | 0.734 | Bold Hindi comes out regular: for letters Arial lacks, marqius-wkhtmltopdf falls back to FreeSans but not to FreeSans Bold. Neither PDF gives back clean Devanagari text, which is most of the text measure's loss. | [1](results/0.12.6/linux-amd64/pictures/international--letter-hi.page-1.png) |
| `international/receipt-th` | 0.4669 | 0.984 | The pages look alike; the bold heading comes out regular with marqius-wkhtmltopdf (FreeSerif, not FreeSerif Bold). Neither PDF gives back clean Thai text, so the text measure scores it low. | [1](results/0.12.6/linux-amd64/pictures/international--receipt-th.page-1.png) |
| `options/no-charset` | 0.6307 | 0.890 | The page declares no character set: wkhtmltopdf reads it as Latin-1 (SociÃ©tÃ©), marqius-wkhtmltopdf as UTF-8 (Société). With --encoding utf-8 both agree (options/encoding). | [1](results/0.12.6/linux-amd64/pictures/options--no-charset.page-1.png) |
| `print/67-unicode` | 0.6694 | 0.795 | The page declares no character set. wkhtmltopdf reads it as Latin-1 and prints garbled letters (Î±Î²Î³ for αβγ); marqius-wkhtmltopdf reads it as UTF-8 and prints the right ones. With <meta charset="utf-8"> or --encoding utf-8 both agree (options/encoding). | [1](results/0.12.6/linux-amd64/pictures/print--67-unicode.page-1.png) |
| `print/70-visibility` | 0.8196 | 1.000 | wkhtmltopdf turns the half-transparent line into a picture, so its words cannot be read back from the PDF; marqius-wkhtmltopdf keeps them as text. The pages look the same. | [1](results/0.12.6/linux-amd64/pictures/print--70-visibility.page-1.png) |
| `international/letter-ja` | 0.8546 | 0.993 | The pages look the same. wkhtmltopdf sets the text in Noto Sans Mono CJK HK, marqius-wkhtmltopdf in Noto Sans CJK JP, the face lang="ja" asks for; wkhtmltopdf's text reads back with some characters as radicals. | [1](results/0.12.6/linux-amd64/pictures/international--letter-ja.page-1.png) |
| `options/user-style-sheet` | 0.8573 | 0.429 | Uses report.html (12 px Arial, line-height 1.45): marqius-wkhtmltopdf sets each line a little lower, 1 pt near the top of a page and about 9 pt at the foot, so the overlay falls; the words and the page breaks are the same. One table row is read back in another order, which costs the text measure most of its loss. | [1](results/0.12.6/linux-amd64/pictures/options--user-style-sheet.page-1.png) [2](results/0.12.6/linux-amd64/pictures/options--user-style-sheet.page-2.png) |
| `international/invoice-zh` | 0.8578 | 0.565 | The line with the dates breaks into three lines with marqius-wkhtmltopdf, two with wkhtmltopdf. wkhtmltopdf's text reads back with some characters as radicals (⻛ for 风), which the text measure counts. | [1](results/0.12.6/linux-amd64/pictures/international--invoice-zh.page-1.png) |
| `options/grayscale` | 0.8705 | 0.480 | Uses report.html (12 px Arial, line-height 1.45): marqius-wkhtmltopdf sets each line a little lower, 1 pt near the top of a page and about 9 pt at the foot, so the overlay falls; the words and the page breaks are the same. One table row is read back in another order, which costs the text measure most of its loss. | [1](results/0.12.6/linux-amd64/pictures/options--grayscale.page-1.png) [2](results/0.12.6/linux-amd64/pictures/options--grayscale.page-2.png) |
| `options/lowquality` | 0.8705 | 0.480 | Uses report.html (12 px Arial, line-height 1.45): marqius-wkhtmltopdf sets each line a little lower, 1 pt near the top of a page and about 9 pt at the foot, so the overlay falls; the words and the page breaks are the same. One table row is read back in another order, which costs the text measure most of its loss. | [1](results/0.12.6/linux-amd64/pictures/options--lowquality.page-1.png) [2](results/0.12.6/linux-amd64/pictures/options--lowquality.page-2.png) |
| `options/outline` | 0.8705 | 0.480 | Uses report.html (12 px Arial, line-height 1.45): marqius-wkhtmltopdf sets each line a little lower, 1 pt near the top of a page and about 9 pt at the foot, so the overlay falls; the words and the page breaks are the same. One table row is read back in another order, which costs the text measure most of its loss. | [1](results/0.12.6/linux-amd64/pictures/options--outline.page-1.png) [2](results/0.12.6/linux-amd64/pictures/options--outline.page-2.png) |
| `options/cover-toc` | 0.8824 | 0.887 | Uses report.html (12 px Arial, line-height 1.45): marqius-wkhtmltopdf sets each line a little lower, 1 pt near the top of a page and about 9 pt at the foot, so the overlay falls; the words and the page breaks are the same. One table row is read back in another order, which costs the text measure most of its loss. | [1](results/0.12.6/linux-amd64/pictures/options--cover-toc.page-1.png) [2](results/0.12.6/linux-amd64/pictures/options--cover-toc.page-2.png) [3](results/0.12.6/linux-amd64/pictures/options--cover-toc.page-3.png) [4](results/0.12.6/linux-amd64/pictures/options--cover-toc.page-4.png) |
| `options/landscape-letter` | 0.9357 | 0.999 | The table's columns stand 1 to 2 pt further right. The pages look the same. | [1](results/0.12.6/linux-amd64/pictures/options--landscape-letter.page-1.png) |
| `options/html-header-footer` | 0.9417 | 0.534 | Uses report.html (12 px Arial, line-height 1.45): marqius-wkhtmltopdf sets each line a little lower, 1 pt near the top of a page and about 9 pt at the foot, so the overlay falls; the words and the page breaks are the same. One table row is read back in another order, which costs the text measure most of its loss. | [1](results/0.12.6/linux-amd64/pictures/options--html-header-footer.page-1.png) [2](results/0.12.6/linux-amd64/pictures/options--html-header-footer.page-2.png) |
| `international/greek-russian` | 0.9521 | 0.120 | marqius-wkhtmltopdf sets both floated columns 9.6 pt lower; everything else is the same. | [1](results/0.12.6/linux-amd64/pictures/international--greek-russian.page-1.png) |
| `everyday/certificate` | 0.9529 | 0.976 | wkhtmltopdf writes the letter-spaced title as single letters (it reads back as C E RT IFIC AT E); marqius-wkhtmltopdf keeps the word whole. The lines below the title sit 1.2 pt higher. The pages look the same. | [1](results/0.12.6/linux-amd64/pictures/everyday--certificate.page-1.png) |
| `options/page-offset` | 0.9547 | 0.482 | Uses report.html (12 px Arial, line-height 1.45): marqius-wkhtmltopdf sets each line a little lower, 1 pt near the top of a page and about 9 pt at the foot, so the overlay falls; the words and the page breaks are the same. One table row is read back in another order, which costs the text measure most of its loss. The page numbers (5 and 6) are read back in other places. | [1](results/0.12.6/linux-amd64/pictures/options--page-offset.page-1.png) [2](results/0.12.6/linux-amd64/pictures/options--page-offset.page-2.png) |
| `options/zoom` | 0.9628 | 0.566 | Uses report.html (12 px Arial, line-height 1.45): marqius-wkhtmltopdf sets each line a little lower, 1 pt near the top of a page and about 9 pt at the foot, so the overlay falls; the words and the page breaks are the same. One table row is read back in another order, which costs the text measure most of its loss. At 1.25 times, the title is also 0.3 pt smaller. | [1](results/0.12.6/linux-amd64/pictures/options--zoom.page-1.png) [2](results/0.12.6/linux-amd64/pictures/options--zoom.page-2.png) |
| `options/long-statement` | 0.9712 | 0.999 | The amounts stand 1.2 pt further right. The pages look the same. | [1](results/0.12.6/linux-amd64/pictures/options--long-statement.page-1.png) [2](results/0.12.6/linux-amd64/pictures/options--long-statement.page-2.png) [3](results/0.12.6/linux-amd64/pictures/options--long-statement.page-3.png) |
| `everyday/statement` | 0.9782 | 0.999 | The pages look the same. The customer's name block is read back in another order, which the text measure counts. | [1](results/0.12.6/linux-amd64/pictures/everyday--statement.page-1.png) |
| `options/default-header` | 0.9783 | 0.619 | Uses report.html (12 px Arial, line-height 1.45): marqius-wkhtmltopdf sets each line a little lower, 1 pt near the top of a page and about 9 pt at the foot, so the overlay falls; the words and the page breaks are the same. One table row is read back in another order, which costs the text measure most of its loss. | [1](results/0.12.6/linux-amd64/pictures/options--default-header.page-1.png) [2](results/0.12.6/linux-amd64/pictures/options--default-header.page-2.png) |
| `options/text-headers` | 0.9788 | 0.632 | Uses report.html (12 px Arial, line-height 1.45): marqius-wkhtmltopdf sets each line a little lower, 1 pt near the top of a page and about 9 pt at the foot, so the overlay falls; the words and the page breaks are the same. One table row is read back in another order, which costs the text measure most of its loss. | [1](results/0.12.6/linux-amd64/pictures/options--text-headers.page-1.png) [2](results/0.12.6/linux-amd64/pictures/options--text-headers.page-2.png) |
| `options/a5-portrait` | 0.9861 | 0.759 | Uses report.html (12 px Arial, line-height 1.45): marqius-wkhtmltopdf sets each line a little lower, 1 pt near the top of a page and about 9 pt at the foot, so the overlay falls; the words and the page breaks are the same. One table row is read back in another order, which costs the text measure most of its loss. | [1](results/0.12.6/linux-amd64/pictures/options--a5-portrait.page-1.png) [2](results/0.12.6/linux-amd64/pictures/options--a5-portrait.page-2.png) |
| `options/print-media` | 0.9872 | 0.938 | In the order table, marqius-wkhtmltopdf wraps "12 × A4 copier paper" onto two lines; wkhtmltopdf keeps it on one. | [1](results/0.12.6/linux-amd64/pictures/options--print-media.page-1.png) |
| `international/mixed-scripts` | 0.9874 | 1.000 | The pages look the same. wkhtmltopdf sets all the Chinese, Japanese and Korean words in Noto Sans CJK HK, marqius-wkhtmltopdf in Noto Sans CJK JP. | [1](results/0.12.6/linux-amd64/pictures/international--mixed-scripts.page-1.png) |
| `print/42-inline-format` | 0.9888 | 0.998 | The first line's words stand up to 1.4 pt along the line from where wkhtmltopdf puts them (subscript and superscript). The pages look the same. | [1](results/0.12.6/linux-amd64/pictures/print--42-inline-format.page-1.png) |
| `print/71-forms` | 0.9893 | 0.682 | Form fields: wkhtmltopdf draws the drop-down arrow as a picture, which marqius-wkhtmltopdf leaves out; a ticked box shows a filled square where wkhtmltopdf draws a tick; marqius-wkhtmltopdf sets the Send button's label at 7.8 pt where wkhtmltopdf uses 9.6 pt; and the lines under the fields sit up to 2.4 pt higher. | [1](results/0.12.6/linux-amd64/pictures/print--71-forms.page-1.png) |
| `print/61-svg-inline` | 0.9971 | 1.000 | A real difference: wkhtmltopdf paints the SVG linear gradient red to blue; marqius-wkhtmltopdf fills the box flat grey. | [1](results/0.12.6/linux-amd64/pictures/print--61-svg-inline.page-1.png) |
| `international/receipt-ko` | 0.9995 | 0.999 | The pages look the same. The wide space after the time reads back as a different space character in the two PDFs. | [1](results/0.12.6/linux-amd64/pictures/international--receipt-ko.page-1.png) |
| `print/69-borders` | 0.9999 | 0.966 | wkhtmltopdf draws the rounded box as a picture, marqius-wkhtmltopdf as shapes. The pages look the same. | [1](results/0.12.6/linux-amd64/pictures/print--69-borders.page-1.png) |

</details>
<!-- scoreboard:end -->

## What works differently today

These are what the runs above found in marqius-wkhtmltopdf 0.12.6. Each has a document in the corpus, so the scoreboard shows when one changes.

- **Scripts that change the page.** marqius-wkhtmltopdf runs `document.write`, but the page's DOM is missing: `document.getElementById`, `querySelector` and `createElement` are undefined, so whatever a script builds with them is missing from the PDF (`options/javascript`). wkhtmltopdf's header and footer variables work, both as text (`[page] of [topage]`) and through the usual script in an HTML header or footer.
- **Arabic and Hebrew.** The letters of each word come out in reverse order, Arabic letters are not joined, and right-to-left tables are not mirrored (`international/invoice-ar` and `notice-he`).
- **Bold where the named font lacks the script.** For Hindi and Thai, marqius-wkhtmltopdf falls back to a regular face for bold text (`international/letter-hi` and `receipt-th`).
- **SVG gradients** are painted flat grey (`print/61-svg-inline`).
- **Form fields** are drawn more plainly: a drop-down list has no arrow, a ticked box shows a filled square where wkhtmltopdf draws a tick, and a button's label is smaller (`print/71-forms`).
- **Some long pages sit lower.** In the options set's report (12 px Arial, a line height of 1.45, headings and tables), each line sits a little lower, by about 9 pt at the foot of an A4 page; the page breaks stayed the same (the `options` documents built on `report.html`). Plain paragraphs do not move (`print/76-long-paragraphs`).
- **Fonts in OpenType CFF form are embedded almost whole.** TrueType fonts such as Arial are cut down to the letters a page uses, but CFF fonts are not, so a PDF with Chinese, Japanese or Korean text (Noto CJK) is 13 to 27 MB, against under 40 KB from wkhtmltopdf, and takes about half a second, slower than wkhtmltopdf. Hindi and Thai pages, which fall back to FreeFont, come to 0.5 to 1.1 MB (`international`).
- **Files are larger in general.** The 86 published documents come to about 1.8 times wkhtmltopdf's size.
- **Pages that declare no character set.** wkhtmltopdf reads them as Latin-1 and prints garbled letters; marqius-wkhtmltopdf reads them as UTF-8. With `--encoding utf-8` the two agree (`print/67-unicode`, `options/no-charset` and `options/encoding`).
- **Every file** is PDF 1.7 rather than 1.4, and names the page's language when the page gives one.

## Rerun everything

```bash
./run.sh
```

This converts the four sets (114 documents) with both programs three times, once more with wkhtmltopdf's 200 ms script wait turned off, and scores every pair. It takes about two minutes on a laptop once the images are downloaded, and the report lands in `out/corpus/`. `./run.sh --tag 0.12.2` tests an earlier version, and `./run.sh --help` lists everything else.

Every score comes out the same on x86-64 and on ARM64, for all 114 documents, to six decimal places.

## How it works

1. **One system for both.** `run.sh` takes the program out of the `marqius/wkhtmltopdf` image (it is a single static file) and puts it beside wkhtmltopdf 0.12.6 in the image the published figures were measured in, [`surnet/alpine-wkhtmltopdf`](https://hub.docker.com/r/surnet/alpine-wkhtmltopdf) `3.24.3-0.12.6-full`, pinned by digest in [`harness/images.env`](harness/images.env). Both programs see the same Alpine system and the same fonts. The program is started under the name `wkhtmltopdf`, as the libraries that call wkhtmltopdf start it.
2. **Every document through each.** [`harness/convert.sh`](harness/convert.sh) converts each document with `-q --enable-local-file-access`, or with its own command line in `corpus/options`. Each program converts one document untimed first, then the whole corpus is converted and timed three times, one document after another.
3. **Every pair scored.** [`harness/score.py`](harness/score.py) scores each pair with the measures below, and `marqius-wkhtmltopdf compare` reports what differs in each pair and where, with both PDFs marked up.
4. **In public.** [The workflow](.github/workflows/parity.yml) runs it all on GitHub's machines, x86-64 and ARM64: daily for each new version on Docker Hub, weekly for the latest. It files the reports under [`results/`](results/) with a link to the run's log, and rewrites the scoreboard above. GitHub keeps each log for 90 days; the reports stay in the repository.

## What the suite sends

Nothing on its own: there is no counter and no call home, in the runner or in marqius-wkhtmltopdf. It uses the network only to download the images from Docker Hub, when you add `--network` (for both programs), and when you run `./run.sh share` and say yes. What we can see is what GitHub and Docker Hub show any publisher: how often this repository is cloned and viewed (GitHub keeps 14 days of it), its stars and forks, the runs of its workflow in public forks, and how often our images are downloaded.

## The measures

- **Parity** is the marqius engine's own measure, copied unchanged into `harness/score.py`, so the published figures can be checked: 50% text (how much of the text agrees, in reading order), 30% word positions (each word beside its twin: full marks when they coincide, nothing at 60 points apart) and 20% page count. A set's parity is the mean of its documents'. It reads the text inside the PDFs, so it counts some differences you cannot see, such as a line read back in another order or text that wkhtmltopdf turned into a picture. It also misses some that you can see, such as a colour.
- **Overlay** lays one page on the other at 72 dots an inch and gives the share of ink with ink from the other page within 2 points. It catches what the text cannot: pictures, rules, letters drawn in another order. It is strict on purpose: a column 3 points lower counts as different.
- **`compare`'s verdict** for each pair: *same pages* (the files themselves may still differ, as PDF 1.4 and 1.7 do), *appearance only* (something moved, or changed size or colour) or *content differs* (words, numbers or pictures). Its notes say what differs and where.
- **Speed** is the time to convert a set one document after another, wkhtmltopdf's divided by marqius-wkhtmltopdf's, the median of three runs, with wkhtmltopdf's default settings. Each program has converted one document beforehand, as a running server would have.

## The corpus

| Set | Documents | What it holds |
|---|---:|---|
| [`everyday`](corpus/everyday) | 8 | An invoice, a statement, a letter, a receipt, a shipping label, a certificate, a report and a product sheet |
| [`print`](corpus/print) | 78 | Short pages, each on one part of HTML and CSS: text, lists, tables, floats, flexbox, grid, positioning, columns, images, SVG, forms, page rules |
| [`options`](corpus/options) | 18 | wkhtmltopdf's own command-line features: text and HTML headers and footers, a cover and a table of contents, bookmarks, paper sizes, margins, zoom, print media, a page built by a script, a 150-row statement over three pages |
| [`international`](corpus/international) | 10 | Chinese, Japanese, Korean, Arabic, Hebrew, Hindi, Thai, Greek, Russian and accented Latin, some mixed on one line; run with Noto CJK added for both programs |

The `everyday` and `print` sets are the 86 documents behind the parity figures marqius.com states. They come from the marqius engine's own tests, unchanged apart from four details that could have pointed at a real company or number. [`corpus/PROVENANCE.tsv`](corpus/PROVENANCE.tsv) gives each file's origin, any change and its checksum, and [`corpus/notes.tsv`](corpus/notes.tsv) the reason for each document that differs. Every person, company, address and number is invented. The telephone numbers come from the ranges Ofcom keeps for drama, and the bank details are placeholders.

## What this does not show

- The documents are ours. They cover what invoices, statements and reports use, but your templates may use something they do not. That is what `mine/` is for.
- It is one system: Alpine 3.24 with the reference image's fonts. With other fonts, text is laid out differently, by both programs.
- Nothing is loaded from the internet unless you add `--network`.
- The scores summarise. For anything that matters to you, look at the pictures and the two PDFs in the report.

## Licence

The harness is under the [MIT licence](LICENSE) and the documents in `corpus/` are dedicated to the public domain under [CC0 1.0](corpus/LICENSE): use them in your own tests. marqius-wkhtmltopdf is proprietary software from Simple AI LLC, with a 30-day trial ([marqius.com](https://marqius.com)). wkhtmltopdf is under the LGPL. This suite is not affiliated with or endorsed by the wkhtmltopdf project.
