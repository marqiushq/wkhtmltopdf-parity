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
No results yet: the first run of the workflow writes them here.
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
