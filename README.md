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

That runs eight sample documents. For yours, take the samples out of `mine/` (keep its README), put your templates there with the pictures and style sheets they load, write the options your app passes in `mine/options.txt`, and run `./run.sh mine` again. Then open `out/mine/report.html`. For each template it gives the score, what differs and where, both PDFs, and pictures of the pages that differ. It also marks the templates that come out better from marqius-wkhtmltopdf than from wkhtmltopdf. A few dozen templates take under a minute once the images are downloaded (about 175 MB the first time). [What goes in `mine/`](mine/README.md).

### If you want help with the differences

`./run.sh share` shows you the summary of your last `./run.sh mine` and sends it to us only if you type yes. The summary holds the versions and the platform, how many templates there were, each template's scores in order of score without its name, the kinds of difference `compare` found (such as "moved" or "font"), and the names of the options you use, never their values. It never holds a template, a file name, a path or any text from your templates. Add `--email` with your address if you want an answer, and `--note` with a question. A copy of what was sent stays beside the report. We use it only to answer you and to learn which differences matter most, keep it for twelve months, and delete it when you ask. Our [privacy notice](https://marqius.com/privacy/#parity-shares) says the same.

## The scoreboard

<!-- scoreboard:start (written by harness/publish.py from results/; edits here are overwritten) -->
**marqius-wkhtmltopdf 0.12.8** beside **wkhtmltopdf 0.12.6**, checked 20 November 2026, 07:30 UTC on GitHub Actions, x86-64, 4 CPUs: [the run's log](https://github.com/marqiushq/wkhtmltopdf-parity/actions/runs/44695350780) · [full report](results/0.12.8/linux-amd64/report.md) · [every document](results/0.12.8/linux-amd64/scores.csv)

| What was converted | Documents | Parity | Overlay | Same pages | Appearance only | Content differs | Speed |
|---|---:|---:|---:|---:|---:|---:|---:|
| Business documents (`everyday`) | 8 | 0.9909 | 0.996 | 3 | 4 | 1 | 38× |
| CSS features, one to a page (`print`) | 78 | 0.9926 | 0.987 | 61 | 12 | 5 | 40× |
| **The 86 published documents together** | **86** | **0.9924** | 0.988 | 64 | 16 | 6 | **40×** |
| wkhtmltopdf's own options (`options`) | 19 | 0.9361 | 0.919 | 2 | 15 | 2 | 27× |
| Languages and scripts (`international`) | 10 | 0.8193 | 0.994 | 1 | 3 | 6 | 22× |

Speed is the time to convert the published documents one after another, wkhtmltopdf's divided by marqius-wkhtmltopdf's: 19.5 s against 0.49 s (median of 3 runs); 5× with wkhtmltopdf's 200 ms script wait turned off for both.

Sizes: the 86 PDFs come to 1.1 MB from wkhtmltopdf and 0.8 MB from marqius-wkhtmltopdf. The `marqius/wkhtmltopdf` image is 26 MB unpacked; the image wkhtmltopdf runs in here, with its fonts, 330 MB.

On GitHub Actions, ARM64, 4 CPUs: the same parity in every set, 29× faster ([report](results/0.12.8/linux-arm64/report.md)).

#### Every version

| Version | Checked | Business documents | CSS features | Published 86 | Options | Languages | Speed |
|---|---|---:|---:|---:|---:|---:|---:|
| [0.12.8](results/0.12.8/linux-amd64/report.md) | 2026-11-20 | 0.9909 | 0.9926 | 0.9924 | 0.9361 | 0.8193 | 40× |
| [0.12.7](results/0.12.7/linux-amd64/report.md) | 2026-11-20 | 0.9908 | 0.9925 | 0.9924 | 0.9354 | 0.7599 | 38× |
| [0.12.6](results/0.12.6/linux-amd64/report.md) | 2026-11-20 | 0.9902 | 0.9920 | 0.9919 | 0.8611 | 0.7073 | 37× |
| [0.12.5](results/0.12.5/linux-amd64/report.md) | 2026-11-20 | 0.9902 | 0.9920 | 0.9919 | 0.8436 | 0.7073 | 38× |
| [0.12.4](results/0.12.4/linux-amd64/report.md) | 2026-11-20 | 0.9902 | 0.9920 | 0.9919 | 0.8611 | 0.7073 | 28× |
| [0.12.3](results/0.12.3/linux-amd64/report.md) | 2026-11-20 | 0.9902 | 0.9921 | 0.9919 | 0.8611 | 0.7073 | 32× |
| [0.12.2](results/0.12.2/linux-amd64/report.md) | 2026-11-20 | 0.9902 | 0.9921 | 0.9919 | 0.8611 | 0.7073 | 36× |
| [0.12.1](results/0.12.1/linux-amd64/report.md) | 2026-11-20 | 0.9902 | 0.9921 | 0.9919 | 0.8611 | 0.7073 | 37× |
| [0.12.0](results/0.12.0/linux-amd64/report.md) | 2026-11-20 | 0.9902 | 0.9921 | 0.9919 | 0.8611 | 0.7073 | 34× |
| [0.11.0](results/0.11.0/linux-amd64/report.md) | 2026-11-20 | 0.9902 | 0.9921 | 0.9919 | 0.8611 | 0.6034 | 36× |

<details>
<summary><b>The 23 documents below 0.99 or with different content, and why; 5 of them come out better from marqius-wkhtmltopdf</b></summary>

[![marqius better](.github/better.svg)](#the-measures) marks a document where every difference goes marqius-wkhtmltopdf's way: its PDF has the page's own words where wkhtmltopdf's has garbled letters, look-alike characters, words split into letters or a picture of the words, and nothing else on the page looks different. Its score is lower only because the score measures how alike the two PDFs are. Each run decides it again, from the page itself.

Each reason was written for the result beside it, and each run checks that the result is still the same; where it is not, the reason given is what `compare` found.

| Document | Parity | Overlay | Why | Pages |
|---|---:|---:|---|---|
| `options/script-file`<br>[tracking issue](https://github.com/marqiushq/wkhtmltopdf-parity/issues/1) | 0.3501 | 0.259 | A real difference: marqius-wkhtmltopdf runs scripts written in the page, but not one the page loads from a file (&lt;script src&gt;), so the delivery note's number, lines and parcel count, which script-file.js writes, are missing. | [1](results/0.12.8/linux-amd64/pictures/options--script-file.page-1.png) |
| `international/invoice-ar` | 0.4318 | 0.998 | The pages look the same. Copied or searched, marqius-wkhtmltopdf's text gives back 48 of the invoice's 56 words as written, wkhtmltopdf's 2: it stores the Arabic as separate letter shapes, which is most of the text measure's loss. | [1](results/0.12.8/linux-amd64/pictures/international--invoice-ar.page-1.png) |
| `international/notice-he` | 0.6071 | 1.000 | The pages look the same. Copied or searched, marqius-wkhtmltopdf's text gives back 43 of the notice's 48 words as written, wkhtmltopdf's 28: it splits many Hebrew words into single letters, which is the text measure's loss. | [1](results/0.12.8/linux-amd64/pictures/international--notice-he.page-1.png) |
| `options/no-charset`<br>[![marqius better](.github/better.svg)](#the-measures) | 0.6307 | 0.890 | An invoice that does not name its character set: wkhtmltopdf garbles every accented letter and the euro sign (SociÃ©tÃ© for Société, â‚¬ for €); marqius-wkhtmltopdf prints them as written. With --encoding utf-8 both agree (options/encoding). | [1](results/0.12.8/linux-amd64/pictures/options--no-charset.page-1.png) |
| `print/67-unicode`<br>[![marqius better](.github/better.svg)](#the-measures) | 0.6694 | 0.795 | The page does not name its character set. wkhtmltopdf assumes an old Western one, so every Greek, Cyrillic and accented letter, maths sign and curly quote comes out garbled (Î±Î²Î³ for αβγ, cafÃ© for café); marqius-wkhtmltopdf prints them as written. Name the character set in the page, or pass --encoding utf-8, and both agree (options/encoding). | [1](results/0.12.8/linux-amd64/pictures/print--67-unicode.page-1.png) |
| `international/receipt-th`<br>[![marqius better](.github/better.svg)](#the-measures) | 0.6769 | 1.000 | The pages look the same. Copied or searched, marqius-wkhtmltopdf's text comes back as clean Thai; wkhtmltopdf's has its tone and vowel marks split off. | [1](results/0.12.8/linux-amd64/pictures/international--receipt-th.page-1.png) |
| `international/letter-hi`<br>[tracking issue](https://github.com/marqiushq/wkhtmltopdf-parity/issues/2) | 0.7550 | 0.948 | Both pages look alike. marqius-wkhtmltopdf's text reads back as clean Hindi; wkhtmltopdf's does not (16 of its letters have no text at all), which is most of the text measure's loss. Letters joined with र (ra), as in प्रिय and ग्राहक, come out apart, with the halant showing, where wkhtmltopdf joins them. | [1](results/0.12.8/linux-amd64/pictures/international--letter-hi.page-1.png) |
| `print/70-visibility`<br>[![marqius better](.github/better.svg)](#the-measures) | 0.8196 | 1.000 | wkhtmltopdf turns the half-transparent line into a low-resolution picture (96 dots an inch), so it prints blurred and its words cannot be searched or copied; marqius-wkhtmltopdf keeps them as sharp text. The rest of the page is the same. | [1](results/0.12.8/linux-amd64/pictures/print--70-visibility.page-1.png) |
| `international/letter-ja` | 0.8569 | 0.996 | The pages look the same. wkhtmltopdf sets the text in Noto Sans Mono CJK HK, marqius-wkhtmltopdf in Noto Sans CJK JP, the face lang="ja" asks for; wkhtmltopdf's text reads back with some characters as radicals. | [1](results/0.12.8/linux-amd64/pictures/international--letter-ja.page-1.png) |
| `international/invoice-zh`<br>[![marqius better](.github/better.svg)](#the-measures) | 0.8818 | 1.000 | The pages look the same, but wkhtmltopdf's text has look-alike signs in place of some characters, so a search for the company's name in its PDF finds nothing; marqius-wkhtmltopdf's has the real characters. | [1](results/0.12.8/linux-amd64/pictures/international--invoice-zh.page-1.png) |
| `options/landscape-letter` | 0.9241 | 1.000 | The table's columns stand 1 to 2 pt further right. The pages look the same. | [1](results/0.12.8/linux-amd64/pictures/options--landscape-letter.page-1.png) |
| `options/a5-portrait`<br>[tracking issue](https://github.com/marqiushq/wkhtmltopdf-parity/issues/4) | 0.9544 | 0.778 | Uses report.html (12 px Arial, line-height 1.45) on A5 paper. Page 1 matches line for line, but wkhtmltopdf moves the table's "Midlands" row to page 2 where marqius-wkhtmltopdf still fits it at the foot of page 1, so page 2 starts a row later and its lines sit 17.4 pt higher. | [1](results/0.12.8/linux-amd64/pictures/options--a5-portrait.page-1.png) [2](results/0.12.8/linux-amd64/pictures/options--a5-portrait.page-2.png) |
| `everyday/certificate` | 0.9564 | 0.975 | wkhtmltopdf writes the letter-spaced title as single letters (it reads back as C E RT IFIC AT E); marqius-wkhtmltopdf keeps the word whole. The pages look the same. | [1](results/0.12.8/linux-amd64/pictures/everyday--certificate.page-1.png) |
| `options/zoom`<br>[tracking issue](https://github.com/marqiushq/wkhtmltopdf-parity/issues/3) | 0.9697 | 0.606 | Uses report.html at --zoom 1.25. marqius-wkhtmltopdf scales text a little differently: the 21 pt title comes out 20.7 pt, and words stand up to 3.5 pt along their lines from where wkhtmltopdf puts them; the page breaks are the same. | [1](results/0.12.8/linux-amd64/pictures/options--zoom.page-1.png) [2](results/0.12.8/linux-amd64/pictures/options--zoom.page-2.png) |
| `options/long-statement` | 0.9741 | 0.999 | The amounts stand 1.2 pt further right. The pages look the same. | [1](results/0.12.8/linux-amd64/pictures/options--long-statement.page-1.png) [2](results/0.12.8/linux-amd64/pictures/options--long-statement.page-2.png) [3](results/0.12.8/linux-amd64/pictures/options--long-statement.page-3.png) |
| `everyday/statement` | 0.9789 | 1.000 | The pages look the same. The customer's name block is read back in another order, which the text measure counts. | [1](results/0.12.8/linux-amd64/pictures/everyday--statement.page-1.png) |
| `options/print-media` | 0.9872 | 0.938 | In the order table, marqius-wkhtmltopdf wraps "12 × A4 copier paper" onto two lines; wkhtmltopdf keeps it on one. | [1](results/0.12.8/linux-amd64/pictures/options--print-media.page-1.png) |
| `print/42-inline-format` | 0.9888 | 0.998 | The first line's words stand up to 1.4 pt along the line from where wkhtmltopdf puts them (subscript and superscript). The pages look the same. | [1](results/0.12.8/linux-amd64/pictures/print--42-inline-format.page-1.png) |
| `international/mixed-scripts` | 0.9890 | 1.000 | The pages look the same. wkhtmltopdf sets all the Chinese, Japanese and Korean words in Noto Sans CJK HK, marqius-wkhtmltopdf in Noto Sans CJK JP. | [1](results/0.12.8/linux-amd64/pictures/international--mixed-scripts.page-1.png) |
| `print/71-forms`<br>[tracking issue](https://github.com/marqiushq/wkhtmltopdf-parity/issues/5) | 0.9892 | 0.682 | Form fields: wkhtmltopdf draws the drop-down arrow as a picture, which marqius-wkhtmltopdf leaves out; a ticked box shows a filled square where wkhtmltopdf draws a tick; marqius-wkhtmltopdf sets the Send button's label at 7.8 pt where wkhtmltopdf uses 9.6 pt; and the lines under the fields sit up to 2.4 pt higher. | [1](results/0.12.8/linux-amd64/pictures/print--71-forms.page-1.png) |
| `international/receipt-ko` | 0.9995 | 0.999 | The pages look the same. The wide space after the time reads back as a different space character in the two PDFs. | [1](results/0.12.8/linux-amd64/pictures/international--receipt-ko.page-1.png) |
| `print/61-svg-inline` | 0.9995 | 1.000 | The pages look the same: both paint the gradient red to blue, wkhtmltopdf as a picture and marqius-wkhtmltopdf as a gradient, and both set the label in Arial. Compare's picture of this page shows marqius-wkhtmltopdf's box flat grey because compare does not draw gradients. | [1](results/0.12.8/linux-amd64/pictures/print--61-svg-inline.page-1.png) |
| `print/69-borders` | 0.9999 | 0.966 | wkhtmltopdf draws the rounded box as a picture, marqius-wkhtmltopdf as shapes. The pages look the same. | [1](results/0.12.8/linux-amd64/pictures/print--69-borders.page-1.png) |

</details>
<!-- scoreboard:end -->

## What works differently today

<!-- gaps:start (written by harness/publish.py from the open tracking issues; edits here are overwritten) -->
What marqius-wkhtmltopdf **0.12.8**, the version on the scoreboard, has yet to match. Each difference has a tracking issue, closed once the difference is gone: watch the one you care about.

- [Scripts that a page loads from a file (`<script src>`) do not run](https://github.com/marqiushq/wkhtmltopdf-parity/issues/1) (`options/script-file`)
- [Hindi: letters joined with र (ra) come out apart, with the halant showing](https://github.com/marqiushq/wkhtmltopdf-parity/issues/2) (`international/letter-hi`)
- [With `--zoom`, text is scaled a little differently](https://github.com/marqiushq/wkhtmltopdf-parity/issues/3) (`options/zoom`)
- [On A5 paper, a table row stays on the page where wkhtmltopdf moves it to the next](https://github.com/marqiushq/wkhtmltopdf-parity/issues/4) (`options/a5-portrait`)
- [Form fields are drawn more plainly](https://github.com/marqiushq/wkhtmltopdf-parity/issues/5) (`print/71-forms`)
<!-- gaps:end -->

Other points, each with a document in the corpus, so the scoreboard shows when one changes:

- **Scripts written in the page** run with the page's DOM, as wkhtmltopdf runs them (`options/javascript`). wkhtmltopdf's header and footer variables work, both as text (`[page] of [topage]`) and through the usual script in an HTML header or footer.
- **Arabic and Hebrew** pages look the same. Copied or searched, marqius-wkhtmltopdf's text gives back most of their words as written, where wkhtmltopdf's breaks them into separate letters or letter shapes (`international/invoice-ar` and `notice-he`).
- **Files are smaller in general.** The 86 published documents come to about two thirds of wkhtmltopdf's size. Pages set in the FreeFont fallback fonts are larger: here the Hindi and Thai pages (`international/letter-hi` and `receipt-th`).
- **Pages that do not name their character set.** wkhtmltopdf prints their accented and non-Latin letters garbled; marqius-wkhtmltopdf prints them as written. With `--encoding utf-8` the two agree (`print/67-unicode`, `options/no-charset` and `options/encoding`).
- **The PDF version** is 1.4, as wkhtmltopdf's, unless a file needs a later one (1.5 for the Arabic, Hindi and Thai pages here), and every file names the page's language when the page gives one.

## Rerun everything

```bash
./run.sh
```

This converts the four sets (115 documents) with both programs three times, once more with wkhtmltopdf's 200 ms script wait turned off, and scores every pair. It takes about two minutes on a laptop once the images are downloaded, and the report lands in `out/corpus/`. `./run.sh --tag 0.12.2` tests an earlier version, and `./run.sh --help` lists everything else.

Every score comes out the same on x86-64 and on ARM64, for all 115 documents, to six decimal places.

## How it works

1. **One system for both.** `run.sh` takes the program out of the `marqius/wkhtmltopdf` image (it is a single static file) and puts it beside wkhtmltopdf 0.12.6 in the image the published figures were measured in, [`surnet/alpine-wkhtmltopdf`](https://hub.docker.com/r/surnet/alpine-wkhtmltopdf) `3.24.3-0.12.6-full`, pinned by digest in [`harness/images.env`](harness/images.env). Both programs see the same Alpine system and the same fonts. The program is started under the name `wkhtmltopdf`, as the libraries that call wkhtmltopdf start it.
2. **Every document through each.** [`harness/convert.sh`](harness/convert.sh) converts each document with `-q --enable-local-file-access`, or with its own command line in `corpus/options`. Each program converts one document untimed first, then the whole corpus is converted and timed three times, one document after another.
3. **Every pair scored.** [`harness/score.py`](harness/score.py) scores each pair with the measures below, and `marqius-wkhtmltopdf compare` reports what differs in each pair and where, with both PDFs marked up.
4. **In public.** [The workflow](.github/workflows/parity.yml) runs it all on GitHub's machines, x86-64 and ARM64: daily for each new version on Docker Hub, weekly for the latest. It files the reports under [`results/`](results/) with a link to the run's log, and rewrites the scoreboard and the list of open differences above, filling in the versions it tested; opening or closing a tracking issue rewrites the list too. GitHub keeps each log for 90 days; the reports stay in the repository.

## What the suite sends

Nothing on its own: there is no counter and no call home, in the runner or in marqius-wkhtmltopdf. It uses the network only to download the images from Docker Hub, when you add `--network` (for both programs), and when you run `./run.sh share` and say yes. What we can see is what GitHub and Docker Hub show any publisher: how often this repository is cloned and viewed (GitHub keeps 14 days of it), its stars and forks, the runs of its workflow in public forks, and how often our images are downloaded.

## The measures

- **Parity** is the marqius engine's own measure, copied unchanged into `harness/score.py`, so the published figures can be checked: 50% text (how much of the text agrees, in reading order), 30% word positions (each word beside its twin: full marks when they coincide, nothing at 60 points apart) and 20% page count. A set's parity is the mean of its documents'. It reads the text inside the PDFs, so it counts some differences you cannot see, such as a line read back in another order or text that wkhtmltopdf turned into a picture. It also misses some that you can see, such as a colour.
- **Overlay** lays one page on the other at 72 dots an inch and gives the share of ink with ink from the other page within 2 points. It catches what the text cannot: pictures, rules, letters drawn in another order. It is strict on purpose: a column 3 points lower counts as different.
- **`compare`'s verdict** for each pair: *same pages* (the files themselves may still differ, as PDF 1.4 and 1.7 do), *appearance only* (something moved, or changed size or colour) or *content differs* (words, numbers or pictures). Its notes say what differs and where.
- **marqius better**, the medal beside a document, means every difference goes marqius-wkhtmltopdf's way: its PDF has the page's own words where wkhtmltopdf's has garbled letters, look-alike characters, words split into letters or a picture of the words, and the rest of the page looks the same, in place, shape, colour and weight. Each run decides it again from the page itself ([`harness/score.py`](harness/score.py)). One difference of any other kind, such as a missing word or another font, and there is no medal.
- **Speed** is the time to convert a set one document after another, wkhtmltopdf's divided by marqius-wkhtmltopdf's, the median of three runs, with wkhtmltopdf's default settings. Each program has converted one document beforehand, as a running server would have.

## The corpus

| Set | Documents | What it holds |
|---|---:|---|
| [`everyday`](corpus/everyday) | 8 | An invoice, a statement, a letter, a receipt, a shipping label, a certificate, a report and a product sheet |
| [`print`](corpus/print) | 78 | Short pages, each on one part of HTML and CSS: text, lists, tables, floats, flexbox, grid, positioning, columns, images, SVG, forms, page rules |
| [`options`](corpus/options) | 19 | wkhtmltopdf's own command-line features: text and HTML headers and footers, a cover and a table of contents, bookmarks, paper sizes, margins, zoom, print media, a page built by a script, a page whose script comes from a file, a 150-row statement over three pages |
| [`international`](corpus/international) | 10 | Chinese, Japanese, Korean, Arabic, Hebrew, Hindi, Thai, Greek, Russian and accented Latin, some mixed on one line; run with Noto CJK added for both programs |

The `everyday` and `print` sets are the 86 documents behind the parity figures marqius.com states. They come from the marqius engine's own tests, unchanged apart from four details that could have pointed at a real company or number. [`corpus/PROVENANCE.tsv`](corpus/PROVENANCE.tsv) gives each file's origin, any change and its checksum, and [`corpus/notes.tsv`](corpus/notes.tsv) the reason for each document that differs, with the result it was written for. Every person, company, address and number is invented. The telephone numbers come from the ranges Ofcom keeps for drama, and the bank details are placeholders.

## What this does not show

- The documents are ours. They cover what invoices, statements and reports use, but your templates may use something they do not. That is what `mine/` is for.
- It is one system: Alpine 3.24 with the reference image's fonts. With other fonts, text is laid out differently, by both programs.
- Nothing is loaded from the internet unless you add `--network`.
- The scores summarise. For anything that matters to you, look at the pictures and the two PDFs in the report.

## Licence

The harness is under the [MIT licence](LICENSE) and the documents in `corpus/` are dedicated to the public domain under [CC0 1.0](corpus/LICENSE): use them in your own tests. marqius-wkhtmltopdf is proprietary software from Simple AI LLC, with a 30-day trial ([marqius.com](https://marqius.com)). wkhtmltopdf is under the LGPL. This suite is not affiliated with or endorsed by the wkhtmltopdf project.
