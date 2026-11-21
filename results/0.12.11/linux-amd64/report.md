# wkhtmltopdf parity report

marqius-wkhtmltopdf **0.12.11** beside **wkhtmltopdf 0.12.6 (with patched qt)**, 2026-11-21T05:21:26Z, on linux/amd64 (4 cpus).

**The published documents (print and everyday, 86 in all): parity 0.9924**, converted 39 times faster than wkhtmltopdf (median of 3 runs).

| Set | Documents | Parity | Lowest | Overlay | Same pages | Appearance only | Content differs | Fonts differ | Speed |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| CSS features, one to a page (`print`) | 78 | 0.9926 | 0.6694 | 0.987 | 61 | 12 | 5 | 1 | 39× |
| Business documents (`everyday`) | 8 | 0.9909 | 0.9564 | 0.996 | 3 | 4 | 1 | 0 | 36× |
| wkhtmltopdf's own options (`options`) | 19 | 0.9703 | 0.6307 | 0.958 | 3 | 15 | 1 | 0 | 23× |
| Languages and scripts (`international`) | 10 | 0.8196 | 0.4318 | 0.999 | 2 | 2 | 6 | 2 | 18× |

Parity is the marqius engine's measure: 50% text, 30% word positions, 20% page count, from 0 to 1, read from the text in the PDFs. *Overlay* lays one page on the other: the share of ink, at 72 dots an inch, with ink from the other page within 2 points. The verdicts are `marqius-wkhtmltopdf compare`'s: *same pages* counts the pairs whose pages are the same (the files themselves may differ, as PDF 1.4 against 1.7 does), *appearance only* those where something moved or changed size or colour, *content differs* those where words, numbers or pictures differ.

*marqius better* marks a document where every difference goes marqius-wkhtmltopdf's way: its PDF has the page's own words where wkhtmltopdf's has garbled letters, look-alike characters, words split into letters or a picture of the words, and nothing else on the page looks different. Its score is lower only because the score measures how alike the two PDFs are.

## CSS features, one to a page (`print`)

| Document | Score | Text | Positions | Pages | Overlay | compare | First difference | Fonts | Size wk / mq | Time wk / mq |
|---|---:|---:|---:|---:|---:|---|---|---|---:|---:|
| 67-unicode<br>🏅 **marqius better** | 0.6694 | 0.703 | 0.393 | 1/1 | 0.793 | content differs | "Î±Î²Î³Î´Îµ Î‘Î’Î“Î”." is now "αβγδε ΑΒΓΔ."; "ÐŸÑ€Ð¸Ð²ÐµÑ‚ Ð¼Ð¸Ñ€." is now "Привет мир."; "cafÃ© naÃ¯ve ZÃ¼rich Ã…ngstrÃ¶m faÃ§ade." is now "café naïve Zürich Ångström façade."; and 2 more — *The page does not name its character set. wkhtmltopdf assumes an old Western one, so every Greek, Cyrillic and accented letter, maths sign and curly quote comes out garbled (Î±Î²Î³ for αβγ, cafÃ© for café); marqius-wkhtmltopdf prints them as written. Name the character set in the page, or pass --encoding utf-8, and both agree (options/encoding).* | differ | 18 KB / 14 KB | 230 ms / <10 ms |
| 70-visibility<br>🏅 **marqius better** | 0.8196 | 0.811 | 0.714 | 1/1 | 1.000 | content differs | "Half opacity." is new; a picture on page 1 is gone — *wkhtmltopdf turns the half-transparent line into a low-resolution picture (96 dots an inch), so it prints blurred and its words cannot be searched or copied; marqius-wkhtmltopdf keeps them as sharp text. The rest of the page is the same.* | same | 8.7 KB / 6.4 KB | 230 ms / <10 ms |
| 42-inline-format | 0.9888 | 0.987 | 0.984 | 1/1 | 0.998 | appearance only | the line "Water is H 2 O and": the words stand up to 1.4 pt from where they stood along the line — *The first line's words stand up to 1.4 pt along the line from where wkhtmltopdf puts them (subscript and superscript). The pages look the same.* | same | 21 KB / 13 KB | 239 ms / <10 ms |
| 71-forms | 0.9892 | 1.000 | 0.964 | 1/1 | 0.682 | content differs | a picture on page 1 is gone; rules, frames or tints differ on page 1: 3 places only in the old, 3 only in the new; the line "Option" moved 1.8 pt to the right; and 4 more — *Form fields: wkhtmltopdf draws the drop-down arrow as a picture, which marqius-wkhtmltopdf leaves out; a ticked box shows a filled square where wkhtmltopdf draws a tick; marqius-wkhtmltopdf sets the Send button's label at 7.8 pt where wkhtmltopdf uses 9.6 pt; and the lines under the fields sit up to 2.4 pt higher.* | same | 11 KB / 7.0 KB | 229 ms / <10 ms |
| 40-list-types | 0.9939 | 1.000 | 0.980 | 1/1 | 0.910 | appearance only | 5 lines from "a. alpha b. beta IV. four" moved 2.9 pt to the right; page 1 lacks rules, frames or tints in 1 place where the old page has them; 3 lines from "i. one ii. two iii. three" moved 2.7 pt to the right | same | 8.8 KB / 6.7 KB | 220 ms / <10 ms |
| 06-ol | 0.9949 | 1.000 | 0.983 | 1/1 | 0.973 | appearance only | 3 lines from "1. Numbered one 2. Numbered two" moved 3 pt to the right | same | 8.0 KB / 6.0 KB | 220 ms / <10 ms |
| 75-nested-lists-mixed | 0.9962 | 1.000 | 0.987 | 1/1 | 0.948 | appearance only | the line "1. One" moved 3 pt to the right; 2 lines from "1. Deep 1 2. Deep 2" moved 3 pt to the right; the line "2. Two" moved 3 pt to the right; and 1 more | same | 9.7 KB / 7.5 KB | 230 ms / <10 ms |
| 46-table-spans | 0.9965 | 1.000 | 0.988 | 1/1 | 0.956 | appearance only | rules, frames or tints differ on page 1: 1 place only in the old, 3 only in the new; the line "3" moved 1.2 pt to the right; the line "6" moved 1.2 pt to the right | same | 15 KB / 8.7 KB | 230 ms / <10 ms |
| 66-list-inside | 0.9978 | 1.000 | 0.993 | 1/1 | 0.991 | appearance only | 2 lines from "1. Custom padding 2. Two" moved 3 pt to the right | same | 10 KB / 7.9 KB | 230 ms / <10 ms |
| 50-inline-block | 0.9980 | 1.000 | 0.993 | 1/1 | 0.997 | same pages | the pages are the same (the files differ: the language of the file is "en", was "") | same | 9.3 KB / 7.1 KB | 220 ms / <10 ms |
| 20-whitespace | 0.9980 | 1.000 | 0.993 | 1/1 | 0.996 | same pages | the pages are the same | same | 9.0 KB / 6.8 KB | 220 ms / 10 ms |
| 62-position | 0.9982 | 1.000 | 0.994 | 1/1 | 0.981 | appearance only | the line "After shifted word." moved 3.2 pt down | same | 10 KB / 7.9 KB | 229 ms / <10 ms |
| 53-text-props | 0.9984 | 1.000 | 0.995 | 1/1 | 0.995 | appearance only | the line "Letter spacing applied here.": the words stand up to 9.2 pt from where they stood along the line | same | 12 KB / 9.1 KB | 230 ms / <10 ms |
| 31-footnote | 0.9987 | 1.000 | 0.996 | 1/1 | 0.999 | same pages | the pages are the same | same | 9.0 KB / 6.7 KB | 230 ms / <10 ms |
| 48-table-widths | 0.9990 | 1.000 | 0.997 | 1/1 | 0.999 | same pages | the pages are the same (the files differ: the language of the file is "en", was "") | same | 17 KB / 11 KB | 230 ms / <10 ms |
| 60-images | 0.9990 | 1.000 | 0.997 | 1/1 | 1.000 | appearance only | a picture on page 1 moved 0.2 pt to the right, 1.1 pt up | same | 16 KB / 11 KB | 240 ms / <10 ms |
| 45-counters | 0.9990 | 1.000 | 0.997 | 1/1 | 1.000 | appearance only | 2 lines from "2.1.a Deep 2.1.b Deep": the words stand up to 1.4 pt from where they stood along the line | same | 15 KB / 9.0 KB | 229 ms / <10 ms |
| 22-links | 0.9992 | 1.000 | 0.997 | 1/1 | 0.999 | same pages | the pages are the same | same | 8.6 KB / 6.6 KB | 220 ms / <10 ms |
| 03-inline | 0.9992 | 1.000 | 0.997 | 1/1 | 0.999 | same pages | the pages are the same | same | 29 KB / 14 KB | 239 ms / <10 ms |
| 25-inline-mixed | 0.9992 | 1.000 | 0.997 | 1/1 | 0.999 | same pages | the pages are the same | same | 24 KB / 13 KB | 239 ms / <10 ms |
| 10-align | 0.9993 | 1.000 | 0.998 | 1/1 | 0.996 | same pages | the pages are the same | same | 7.5 KB / 5.6 KB | 220 ms / <10 ms |
| 44-generated | 0.9995 | 1.000 | 0.998 | 1/1 | 1.000 | same pages | the pages are the same (the files differ: the language of the file is "en", was "") | same | 17 KB / 11 KB | 230 ms / <10 ms |
| 54-justify-hyphens | 0.9995 | 1.000 | 0.998 | 1/1 | 0.999 | same pages | the pages are the same (the files differ: the language of the file is "en", was "") | same | 11 KB / 8.2 KB | 229 ms / <10 ms |
| 61-svg-inline | 0.9995 | 1.000 | 0.998 | 1/1 | 1.000 | content differs | a picture on page 1 is gone; page 1 has rules, frames or tints in 1 place where the old page has none — *The pages look the same: both paint the gradient red to blue, wkhtmltopdf as a picture and marqius-wkhtmltopdf as a gradient, and both set the label in Arial. Compare's picture of this page shows marqius-wkhtmltopdf's box flat grey because compare does not draw gradients.* | same | 15 KB / 9.5 KB | 230 ms / <10 ms |
| 76-long-paragraphs | 0.9997 | 1.000 | 0.999 | 3/3 | 1.000 | same pages | the pages are the same (the files differ: the language of the file is "en", was "") | same | 23 KB / 12 KB | 240 ms / <10 ms |
| 04-css | 0.9997 | 1.000 | 0.999 | 1/1 | 1.000 | same pages | the pages are the same | same | 14 KB / 8.3 KB | 230 ms / <10 ms |
| 58-footnotes | 0.9997 | 1.000 | 0.999 | 1/1 | 1.000 | same pages | the pages are the same (the files differ: the language of the file is "en", was "") | same | 13 KB / 9.3 KB | 229 ms / <10 ms |
| 77-links-outline | 0.9998 | 1.000 | 0.999 | 1/1 | 1.000 | same pages | the pages are the same (the files differ: the language of the file is "en", was "") | same | 16 KB / 11 KB | 230 ms / <10 ms |
| 14-links | 0.9998 | 1.000 | 0.999 | 1/1 | 1.000 | same pages | the pages are the same | same | 8.7 KB / 6.7 KB | 230 ms / <10 ms |
| 68-overflow-wrap | 0.9998 | 1.000 | 0.999 | 1/1 | 0.999 | same pages | the pages are the same (the files differ: the language of the file is "en", was "") | same | 9.6 KB / 7.4 KB | 229 ms / <10 ms |
| 36-svg | 0.9998 | 1.000 | 0.999 | 1/1 | 1.000 | same pages | the pages are the same | same | 18 KB / 10 KB | 230 ms / <10 ms |
| 26-heading-sizes | 0.9998 | 1.000 | 0.999 | 1/1 | 1.000 | same pages | the pages are the same | same | 14 KB / 8.5 KB | 229 ms / <10 ms |
| 47-table-borders | 0.9999 | 1.000 | 1.000 | 1/1 | 1.000 | same pages | the pages are the same (the files differ: the language of the file is "en", was "") | same | 16 KB / 10 KB | 230 ms / <10 ms |
| 13-longword | 0.9999 | 1.000 | 1.000 | 1/1 | 1.000 | same pages | the pages are the same | same | 9.6 KB / 7.4 KB | 220 ms / <10 ms |
| 38-font-keywords | 0.9999 | 1.000 | 1.000 | 1/1 | 1.000 | same pages | the pages are the same (the files differ: the language of the file is "en", was "") | same | 9.5 KB / 7.0 KB | 240 ms / <10 ms |
| 74-media | 0.9999 | 1.000 | 1.000 | 1/1 | 1.000 | same pages | the pages are the same (the files differ: the language of the file is "en", was "") | same | 8.9 KB / 6.7 KB | 230 ms / <10 ms |
| 37-headings-scaled | 0.9999 | 1.000 | 1.000 | 1/1 | 1.000 | same pages | the pages are the same (the files differ: the language of the file is "en", was "") | same | 14 KB / 8.6 KB | 230 ms / <10 ms |
| 27-longtable | 0.9999 | 1.000 | 1.000 | 1/1 | 1.000 | appearance only | the paragraph beginning "k1" breaks into lines differently (18 lines, now 13) | same | 16 KB / 11 KB | 230 ms / <10 ms |
| 73-vars-calc | 0.9999 | 1.000 | 1.000 | 1/1 | 1.000 | same pages | the pages are the same (the files differ: the language of the file is "en", was "") | same | 9.4 KB / 7.3 KB | 219 ms / <10 ms |
| 51-box-model | 0.9999 | 1.000 | 1.000 | 1/1 | 1.000 | same pages | the pages are the same (the files differ: the language of the file is "en", was "") | same | 9.6 KB / 7.4 KB | 219 ms / <10 ms |
| 32-layout-mixed | 0.9999 | 1.000 | 1.000 | 1/1 | 1.000 | same pages | the pages are the same | same | 9.6 KB / 7.4 KB | 229 ms / <10 ms |
| 35-toc-pages | 0.9999 | 1.000 | 1.000 | 2/2 | 1.000 | same pages | the pages are the same | same | 18 KB / 12 KB | 230 ms / <10 ms |
| 24-page-custom | 0.9999 | 1.000 | 1.000 | 1/1 | 1.000 | same pages | the pages are the same | same | 7.8 KB / 5.8 KB | 220 ms / <10 ms |
| 19-empty | 0.9999 | 1.000 | 1.000 | 1/1 | 1.000 | same pages | the pages are the same | same | 7.2 KB / 5.3 KB | 220 ms / <10 ms |
| 16-br | 0.9999 | 1.000 | 1.000 | 1/1 | 1.000 | same pages | the pages are the same | same | 7.0 KB / 5.2 KB | 220 ms / <10 ms |
| 23-page-a4 | 0.9999 | 1.000 | 1.000 | 1/1 | 1.000 | same pages | the pages are the same | same | 9.3 KB / 7.2 KB | 229 ms / <10 ms |
| 34-flex-justify | 0.9999 | 1.000 | 1.000 | 1/1 | 1.000 | same pages | the pages are the same | same | 8.5 KB / 6.4 KB | 220 ms / <10 ms |
| 69-borders | 0.9999 | 1.000 | 1.000 | 1/1 | 0.966 | content differs | a picture on page 1 is gone; page 1 has rules, frames or tints in 1 place where the old page has none — *wkhtmltopdf draws the rounded box as a picture, marqius-wkhtmltopdf as shapes. The pages look the same.* | same | 9.5 KB / 6.4 KB | 230 ms / <10 ms |
| 57-breaks | 0.9999 | 1.000 | 1.000 | 2/2 | 1.000 | same pages | the pages are the same (the files differ: the language of the file is "en", was "") | same | 17 KB / 11 KB | 230 ms / <10 ms |
| 07-pre | 0.9999 | 1.000 | 1.000 | 1/1 | 1.000 | same pages | the pages are the same | same | 12 KB / 7.6 KB | 230 ms / <10 ms |
| 15-table | 0.9999 | 1.000 | 1.000 | 1/1 | 1.000 | same pages | the pages are the same | same | 13 KB / 7.5 KB | 229 ms / <10 ms |
| 64-flex-advanced | 0.9999 | 1.000 | 1.000 | 1/1 | 1.000 | same pages | the pages are the same (the files differ: the language of the file is "en", was "") | same | 9.8 KB / 7.6 KB | 230 ms / <10 ms |
| 28-nested-blockquote | 0.9999 | 1.000 | 1.000 | 1/1 | 1.000 | same pages | the pages are the same | same | 9.7 KB / 7.4 KB | 220 ms / <10 ms |
| 05-ul | 0.9999 | 1.000 | 1.000 | 1/1 | 0.965 | same pages | the pages are the same | same | 9.0 KB / 6.9 KB | 229 ms / <10 ms |
| 29-flex | 0.9999 | 1.000 | 1.000 | 1/1 | 1.000 | same pages | the pages are the same | same | 7.8 KB / 5.7 KB | 230 ms / <10 ms |
| 09-hr | 0.9999 | 1.000 | 1.000 | 1/1 | 1.000 | same pages | the pages are the same | same | 7.6 KB / 5.6 KB | 229 ms / <10 ms |
| 33-grid-fragmented | 0.9999 | 1.000 | 1.000 | 1/1 | 1.000 | same pages | the pages are the same | same | 11 KB / 8.1 KB | 230 ms / <10 ms |
| 43-selectors | 0.9999 | 1.000 | 1.000 | 1/1 | 0.977 | same pages | the pages are the same (the files differ: the language of the file is "en", was "") | same | 16 KB / 10 KB | 230 ms / 10 ms |
| 52-sizing | 0.9999 | 1.000 | 1.000 | 1/1 | 1.000 | same pages | the pages are the same (the files differ: the language of the file is "en", was "") | same | 11 KB / 8.8 KB | 230 ms / <10 ms |
| 01-basic | 0.9999 | 1.000 | 1.000 | 1/1 | 1.000 | same pages | the pages are the same | same | 15 KB / 9.2 KB | 230 ms / <10 ms |
| 02-headings | 0.9999 | 1.000 | 1.000 | 1/1 | 1.000 | same pages | the pages are the same | same | 17 KB / 10 KB | 230 ms / <10 ms |
| 56-margin-boxes | 0.9999 | 1.000 | 1.000 | 2/2 | 1.000 | same pages | the pages are the same (the files differ: the language of the file is "en", was "") | same | 19 KB / 12 KB | 240 ms / <10 ms |
| 78-trim-bleed | 0.9999 | 1.000 | 1.000 | 1/1 | 1.000 | same pages | the pages are the same (the files differ: the language of the file is "en", was "") | same | 16 KB / 10 KB | 230 ms / <10 ms |
| 12-nested-lists | 0.9999 | 1.000 | 1.000 | 1/1 | 0.890 | appearance only | page 1 lacks rules, frames or tints in 2 places where the old page has them | same | 7.6 KB / 5.7 KB | 219 ms / <10 ms |
| 59-toc-leaders | 0.9999 | 1.000 | 1.000 | 2/2 | 1.000 | same pages | the pages are the same (the files differ: the language of the file is "en", was "") | same | 23 KB / 15 KB | 230 ms / <10 ms |
| 63-columns | 0.9999 | 1.000 | 1.000 | 1/1 | 1.000 | same pages | the pages are the same (the files differ: the language of the file is "en", was "") | same | 16 KB / 11 KB | 230 ms / <10 ms |
| 21-img | 0.9999 | 1.000 | 1.000 | 1/1 | 1.000 | same pages | the pages are the same | same | 8.5 KB / 6.9 KB | 230 ms / <10 ms |
| 72-cascade | 0.9999 | 1.000 | 1.000 | 1/1 | 1.000 | same pages | the pages are the same (the files differ: the language of the file is "en", was "") | same | 9.9 KB / 7.6 KB | 230 ms / <10 ms |
| 30-grid | 0.9999 | 1.000 | 1.000 | 1/1 | 1.000 | same pages | the pages are the same | same | 7.2 KB / 5.2 KB | 219 ms / <10 ms |
| 49-floats | 0.9999 | 1.000 | 1.000 | 1/1 | 1.000 | same pages | the pages are the same (the files differ: the language of the file is "en", was "") | same | 11 KB / 8.1 KB | 229 ms / <10 ms |
| 39-dl | 0.9999 | 1.000 | 1.000 | 1/1 | 1.000 | same pages | the pages are the same (the files differ: the language of the file is "en", was "") | same | 9.3 KB / 7.1 KB | 219 ms / <10 ms |
| 41-white-space | 0.9999 | 1.000 | 1.000 | 1/1 | 1.000 | same pages | the pages are the same (the files differ: the language of the file is "en", was "") | same | 15 KB / 10 KB | 230 ms / <10 ms |
| 55-page-sizes | 0.9999 | 1.000 | 1.000 | 1/1 | 1.000 | same pages | the pages are the same (the files differ: the language of the file is "en", was "") | same | 10 KB / 8.0 KB | 219 ms / <10 ms |
| 11-pagination | 0.9999 | 1.000 | 1.000 | 2/2 | 1.000 | same pages | the pages are the same | same | 20 KB / 13 KB | 240 ms / <10 ms |
| 08-blockquote | 0.9999 | 1.000 | 1.000 | 1/1 | 1.000 | same pages | the pages are the same | same | 9.0 KB / 6.8 KB | 230 ms / <10 ms |
| 18-margins | 0.9999 | 1.000 | 1.000 | 1/1 | 1.000 | same pages | the pages are the same | same | 7.8 KB / 5.8 KB | 229 ms / <10 ms |
| 17-fontsize | 0.9999 | 1.000 | 1.000 | 1/1 | 1.000 | same pages | the pages are the same | same | 8.6 KB / 6.5 KB | 229 ms / <10 ms |
| 65-grid-advanced | 0.9999 | 1.000 | 1.000 | 1/1 | 1.000 | same pages | the pages are the same (the files differ: the language of the file is "en", was "") | same | 7.2 KB / 5.3 KB | 219 ms / <10 ms |

## Business documents (`everyday`)

| Document | Score | Text | Positions | Pages | Overlay | compare | First difference | Fonts | Size wk / mq | Time wk / mq |
|---|---:|---:|---:|---:|---:|---|---|---|---:|---:|
| certificate | 0.9564 | 0.990 | 0.871 | 1/1 | 0.975 | appearance only | the same letters, divided into words differently — *wkhtmltopdf writes the letter-spaced title as single letters (it reads back as C E RT IFIC AT E); marqius-wkhtmltopdf keeps the word whole. The pages look the same.* | same | 26 KB / 16 KB | 240 ms / <10 ms |
| statement | 0.9789 | 0.973 | 0.974 | 1/1 | 1.000 | content differs | "Mr" is gone; "Mr" is new — *The pages look the same. The customer's name block is read back in another order, which the text measure counts.* | same | 19 KB / 13 KB | 230 ms / <10 ms |
| columns | 0.9953 | 1.000 | 0.984 | 1/1 | 0.999 | appearance only | the line "Linen napkins" moved 1.9 pt to the right; the line "Set of four, stonewashed, in sage" moved 1.9 pt to the right; the line "£22 BEST SELLER" moved 1.9 pt to the right; and 3 more | same | 17 KB / 15 KB | 229 ms / <10 ms |
| label | 0.9984 | 1.000 | 0.995 | 1/1 | 1.000 | appearance only | the line "Order 2026-118 Weight 14.2 kg Parcel": the words stand up to 2 pt from where they stood along the line | same | 18 KB / 12 KB | 230 ms / <10 ms |
| invoice | 0.9994 | 1.000 | 0.998 | 1/1 | 1.000 | appearance only | the line "Due: 17 Dec 2026" moved 1 pt to the left | same | 21 KB / 15 KB | 230 ms / <10 ms |
| receipt | 0.9996 | 1.000 | 0.999 | 1/1 | 0.991 | same pages | the pages are the same | same | 16 KB / 11 KB | 230 ms / <10 ms |
| letter | 0.9997 | 1.000 | 0.999 | 1/1 | 1.000 | same pages | the pages are the same | same | 18 KB / 16 KB | 230 ms / <10 ms |
| report | 0.9997 | 1.000 | 0.999 | 1/1 | 0.999 | same pages | the pages are the same | same | 23 KB / 16 KB | 239 ms / <10 ms |

## wkhtmltopdf's own options (`options`)

| Document | Score | Text | Positions | Pages | Overlay | compare | First difference | Fonts | Size wk / mq | Time wk / mq |
|---|---:|---:|---:|---:|---:|---|---|---|---:|---:|
| no-charset<br>🏅 **marqius better** | 0.6307 | 0.762 | 0.166 | 1/1 | 0.890 | content differs | "nÂ°" is now "n°"; "SociÃ©tÃ©" is now "Société"; "CafÃ© Ã‰toile," is now "Café Étoile,"; and 7 more — *An invoice that does not name its character set: wkhtmltopdf garbles every accented letter and the euro sign (SociÃ©tÃ© for Société, â‚¬ for €); marqius-wkhtmltopdf prints them as written. With --encoding utf-8 both agree (options/encoding).* | same | 19 KB / 13 KB | 230 ms / <10 ms |
| landscape-letter | 0.9241 | 0.893 | 0.926 | 1/1 | 1.000 | appearance only | 7 lines from "Item Supplier Hull Leeds Bristol Reading" moved 1.4 pt to the right; 7 lines from "A4 copier paper, 80gsm, box of" moved 1.2 pt to the right; 7 lines from "A3 copier paper, 80gsm, box of" moved 1.2 pt to the right; and 7 more — *The table's columns stand 1 to 2 pt further right. The pages look the same.* | same | 18 KB / 16 KB | 230 ms / <10 ms |
| a5-portrait | 0.9544 | 0.991 | 0.863 | 2/2 | 0.778 | appearance only | page 2 began at "Midlands"; page 2 now begins at "South East"; 40 lines from "South East 39,120 95.9% 3.1% South" moved 17.4 pt up; 5 lines from "1. Move small items into labelled" moved 2.2 pt to the right, 17.4 pt up; and 1 more — *Uses report.html (12 px Arial, line-height 1.45) on A5 paper. Page 1 matches line for line, but wkhtmltopdf moves the table's "Midlands" row to page 2 where marqius-wkhtmltopdf still fits it at the foot of page 1, so page 2 starts a row later and its lines sit 17.4 pt higher.* | same | 29 KB / 21 KB | 240 ms / <10 ms |
| zoom | 0.9697 | 1.000 | 0.899 | 2/2 | 0.606 | appearance only | the line "Quarterly operations review": the words stand up to 3.5 pt from where they stood along the line; 3 words of 21 pt are now 20.7 pt; 2 lines from "Three changes made the difference: earlier": the words stand up to 1.3 pt from where they stood along the line; and 57 more — *Uses report.html at --zoom 1.25. marqius-wkhtmltopdf scales text a little differently: the 21 pt title comes out 20.7 pt, and words stand up to 3.5 pt along their lines from where wkhtmltopdf puts them; the page breaks are the same.* | same | 29 KB / 21 KB | 240 ms / <10 ms |
| long-statement | 0.9741 | 0.961 | 0.979 | 3/3 | 0.999 | appearance only | the line "Page 1 of 3" moved 1.1 pt to the left, 1.2 pt up; 12 words of 8 pt are now 8.3 pt; the line "Page 2 of 3" moved 1.1 pt to the left, 1.2 pt up; and 1 more — *The amounts stand 1.2 pt further right. The pages look the same.* | same | 33 KB / 24 KB | 250 ms / <10 ms |
| print-media | 0.9872 | 1.000 | 0.957 | 1/1 | 0.938 | appearance only | the paragraph beginning "12 × A4 copier paper £294.00" breaks into lines differently (1 lines, now 3); 4 lines from "4 × toner cartridge £272.00 Total," moved 7.8 pt down — *In the order table, marqius-wkhtmltopdf wraps "12 × A4 copier paper" onto two lines; wkhtmltopdf keeps it on one.* | same | 18 KB / 13 KB | 229 ms / <10 ms |
| cover-toc | 0.9985 | 1.000 | 0.995 | 4/4 | 0.995 | appearance only | 4 lines from "Quarterly operations review 3 1. Summary" moved 1.2 pt down; 4 lines from "2. Warehouse 3 2.1 Picking and" moved 2.4 pt down; 4 lines from "2.2 Stock 3 3. Delivery 3" moved 3.6 pt down; and 3 more | same | 42 KB / 28 KB | 659 ms / <10 ms |
| html-header-footer | 0.9995 | 1.000 | 0.998 | 2/2 | 0.999 | appearance only | the line "Quarterly operations review" moved 2.7 pt to the right; the line "Page 1 of 2" moved 1.2 pt to the right; 5 lines from "1. Move small items into labelled" moved 2.2 pt to the right; and 2 more | same | 30 KB / 21 KB | 449 ms / 19 ms |
| no-margins | 0.9996 | 1.000 | 0.999 | 1/1 | 1.000 | appearance only | page 1 lacks rules, frames or tints in 1 place where the old page has them | same | 17 KB / 11 KB | 240 ms / <10 ms |
| javascript | 0.9996 | 1.000 | 0.999 | 1/1 | 1.000 | same pages | the pages are the same (the files differ: the language of the file is "en", was "") — *The page builds its invoice table with a script (getElementById, createElement). marqius-wkhtmltopdf runs it with the page's DOM, as wkhtmltopdf does, and the pages look the same.* | same | 18 KB / 13 KB | 230 ms / 29 ms |
| user-style-sheet | 0.9996 | 1.000 | 0.999 | 2/2 | 0.999 | appearance only | 2 lines from "Accuracy Minutes per order" moved 1.2 pt to the left; 2 lines from "41,208 99.62%" moved 1.1 pt to the left; 2 lines from "43,915 99.68%" moved 1.1 pt to the left; and 3 more | same | 32 KB / 23 KB | 240 ms / <10 ms |
| script-file | 0.9997 | 1.000 | 0.999 | 1/1 | 1.000 | same pages | the pages are the same (the files differ: the language of the file is "en", was "") — *The pages are the same: the script file runs, as in wkhtmltopdf, and writes the delivery note's number, lines and parcel count. The files differ only in that marqius-wkhtmltopdf's names its language (en), where wkhtmltopdf's names none.* | same | 17 KB / 12 KB | 230 ms / 20 ms |
| text-headers | 0.9997 | 1.000 | 0.999 | 2/2 | 1.000 | appearance only | the line "Quarterly operations review" moved 1.4 pt to the left, 1.2 pt up; 6 words of 8 pt are now 8.3 pt; 5 lines from "1. Move small items into labelled" moved 2.2 pt to the right; and 1 more | same | 29 KB / 21 KB | 240 ms / <10 ms |
| page-offset | 0.9998 | 1.000 | 0.999 | 2/2 | 1.000 | appearance only | the line "5" moved 1.9 pt up; 5 lines from "1. Move small items into labelled" moved 2.2 pt to the right; the line "6" moved 1.9 pt up | same | 29 KB / 21 KB | 240 ms / <10 ms |
| default-header | 0.9998 | 1.000 | 0.999 | 2/2 | 1.000 | appearance only | 5 lines from "1. Move small items into labelled" moved 2.2 pt to the right | same | 29 KB / 21 KB | 240 ms / <10 ms |
| grayscale | 0.9998 | 1.000 | 0.999 | 2/2 | 1.000 | appearance only | 5 lines from "1. Move small items into labelled" moved 2.2 pt to the right | same | 29 KB / 21 KB | 240 ms / <10 ms |
| lowquality | 0.9998 | 1.000 | 0.999 | 2/2 | 1.000 | appearance only | 5 lines from "1. Move small items into labelled" moved 2.2 pt to the right | same | 29 KB / 21 KB | 239 ms / <10 ms |
| outline | 0.9998 | 1.000 | 0.999 | 2/2 | 1.000 | appearance only | 5 lines from "1. Move small items into labelled" moved 2.2 pt to the right | same | 28 KB / 20 KB | 240 ms / <10 ms |
| encoding | 0.9999 | 1.000 | 1.000 | 1/1 | 1.000 | same pages | the pages are the same (the files differ: the language of the file is "fr", was "") | same | 18 KB / 13 KB | 230 ms / <10 ms |

## Languages and scripts (`international`)

| Document | Score | Text | Positions | Pages | Overlay | compare | First difference | Fonts | Size wk / mq | Time wk / mq |
|---|---:|---:|---:|---:|---:|---|---|---|---:|---:|
| invoice-ar<br>🏅 **marqius better** | 0.4318 | 0.414 | 0.082 | 1/1 | 0.998 | content differs | "ا ﻟ ﺘ ﺎ ر ﯾ ﺦ :" is now "التاريخ:"; "إ ﻟ ﻰ : ﺷ ﺮ ﻛ ﺔ أ ﻛ ﻤ ﻲ ﻟ ﻠ ﺘ ﺠ ﺎ ر ة ، ﺷ ﺎ ر ع ا ﻟ ﻤ ﯿ ﻨ ﺎ ء" is now "إلى: شركة أكمي للتجارة، شارع الميناء"; "ا ﻟ ﺒ ﻨ ﺪ ا ﻟ ﻜ ﻤ ﯿ ﺔ ﺳ ﻌ ﺮ ا ﻟ ﻮ ﺣ ﺪ ة ا ﻟ ﻤ ﺒ ﻠ ﻎ و ر ق ﺗ ﺼ ﻮ ﯾ ﺮ" is now "البند الكمية سعر الوحدة المبلغ ورق تصوير"; and 14 more — *The pages look the same. Copied or searched, marqius-wkhtmltopdf's text gives back 48 of the invoice's 56 words as written, wkhtmltopdf's 2: it stores the Arabic as separate letter shapes, which is most of the text measure's loss.* | same | 24 KB / 17 KB | 230 ms / <10 ms |
| notice-he<br>🏅 **marqius better** | 0.6071 | 0.800 | 0.024 | 1/1 | 1.000 | appearance only | the paragraph beginning "ה ו ד ע ה ע" breaks into lines differently (1 lines, now 1); the paragraph beginning "ה ח ל מ י ו" breaks into lines differently (1 lines, now 1); the paragraph beginning "ר א ש ו ן –" breaks into lines differently (6 lines, now 6); and 3 more — *The pages look the same. Copied or searched, marqius-wkhtmltopdf's text gives back 43 of the notice's 48 words as written, wkhtmltopdf's 28: it splits many Hebrew words into single letters, which is the text measure's loss.* | same | 17 KB / 11 KB | 230 ms / <10 ms |
| receipt-th<br>🏅 **marqius better** | 0.6769 | 0.670 | 0.473 | 1/1 | 1.000 | content differs | "น ้ํ าส มคั ้ น ้" is now "น้ำส้มคั ้น"; "ร ้ านของเราเปิดทุกวันตั งแต ้ เวลาเจ็ดโมงเช ่ าถึงหกโมงเย็น ้ หากต องการใบก ้ ากับภาษีเต็มรูปแบบ … (20 words)" is now "ร้านของเราเปิดทุกวันตั ้งแต่เวลาเจ็ดโมงเช้าถึงหกโมงเย็น หากต้องการใบกำกั บภาษีเต็มรูปแบบ … (8 words)"; "ขอบคุณที ่ ใช บริการ ้" is now "ขอบคุณที่ใช้บริการ"; and 2 more — *The pages look the same. Copied or searched, marqius-wkhtmltopdf's text comes back as clean Thai; wkhtmltopdf's has its tone and vowel marks split off.* | same | 29 KB / 105 KB | 240 ms / <10 ms |
| letter-hi | 0.7579 | 0.795 | 0.535 | 1/1 | 0.999 | content differs | "नॉथ�िवंड स�लाइज़ िदनांक:" is now "नॉर्थविंड सप्लाइज़ दिनांक:"; 16 of the 274 letters of the old document are drawn with no word of what they are (the file gives its font no map to letters): they cannot be compared; "िप � य ग�ाहक," is now "प्रिय ग्राहक,"; and 13 more — *The pages look the same, but for two quantities and the total in the table, which stand 1.2 to 1.5 pt further right. Copied or searched, marqius-wkhtmltopdf's text reads back as clean Hindi; wkhtmltopdf's does not (16 of its letters have no text at all), which is most of the text measure's loss.* | same | 39 KB / 71 KB | 240 ms / 19 ms |
| letter-ja | 0.8569 | 0.942 | 0.619 | 1/1 | 0.996 | content differs | "営業部 御中" is now "営業部 御中"; "営業部 ⼭⽥ 花⼦" is now "営業部 山田 花子"; "拝啓 時下ますますご清祥のこととお慶び申し上げます。平素は格別のご⾼配を賜り、厚く御礼申し上げます。" is now "拝啓 時下ますますご清祥のこととお慶び申し上げます。平素は格別のご高配を賜り、厚く御礼申し上げます。"; and 5 more — *The pages look the same. wkhtmltopdf sets the text in Noto Sans Mono CJK HK, marqius-wkhtmltopdf in Noto Sans CJK JP, the face lang="ja" asks for; wkhtmltopdf's text reads back with some characters as radicals.* | differ | 38 KB / 31 KB | 259 ms / 19 ms |
| invoice-zh<br>🏅 **marqius better** | 0.8818 | 0.923 | 0.734 | 1/1 | 1.000 | content differs | "北⻛办公⽤品有限公司" is now "北风办公用品有限公司" — *The pages look the same, but wkhtmltopdf's text has look-alike signs in place of some characters, so a search for the company's name in its PDF finds nothing; marqius-wkhtmltopdf's has the real characters.* | same | 28 KB / 26 KB | 240 ms / <10 ms |
| mixed-scripts | 0.9890 | 0.995 | 0.972 | 1/1 | 1.000 | appearance only | 11 words set in notosanscjkhk are now in notosanscjkjp — *The pages look the same. wkhtmltopdf sets all the Chinese, Japanese and Korean words in Noto Sans CJK HK, marqius-wkhtmltopdf in Noto Sans CJK JP.* | differ | 28 KB / 21 KB | 240 ms / 19 ms |
| european | 0.9974 | 1.000 | 0.991 | 1/1 | 1.000 | same pages | the pages are the same (the files differ: the language of the file is "en", was "") | same | 23 KB / 17 KB | 239 ms / <10 ms |
| greek-russian | 0.9979 | 1.000 | 0.993 | 1/1 | 1.000 | same pages | the pages are the same | same | 23 KB / 17 KB | 230 ms / <10 ms |
| receipt-ko | 0.9995 | 1.000 | 0.998 | 1/1 | 0.999 | content differs | "08:42 계산대" is now "08:42 계산대" — *The pages look the same. The wide space after the time reads back as a different space character in the two PDFs.* | same | 14 KB / 12 KB | 240 ms / <10 ms |

## Speed

- print: wkhtmltopdf 17.93, 17.94, 17.95 s; marqius-wkhtmltopdf 0.452, 0.465, 0.462 s; 38.9× (median)
  - with wkhtmltopdf's 200 ms script wait off (`--javascript-delay 0`, for both): 2.23 s and 0.492 s, 4.5×
- everyday: wkhtmltopdf 1.92, 1.88, 1.88 s; marqius-wkhtmltopdf 0.053, 0.057, 0.051 s; 36.0× (median)
  - with wkhtmltopdf's 200 ms script wait off (`--javascript-delay 0`, for both): 0.27 s and 0.055 s, 4.8×
- options: wkhtmltopdf 5.16, 5.16, 5.17 s; marqius-wkhtmltopdf 0.218, 0.223, 0.221 s; 23.4× (median)
- international: wkhtmltopdf 2.41, 2.41, 2.41 s; marqius-wkhtmltopdf 0.131, 0.133, 0.129 s; 18.4× (median)

## Sizes

- print: the PDFs come to 967 KB from wkhtmltopdf and 657 KB from marqius-wkhtmltopdf
- everyday: the PDFs come to 157 KB from wkhtmltopdf and 114 KB from marqius-wkhtmltopdf
- options: the PDFs come to 493 KB from wkhtmltopdf and 352 KB from marqius-wkhtmltopdf
- international: the PDFs come to 262 KB from wkhtmltopdf and 329 KB from marqius-wkhtmltopdf
- images, unpacked: `marqius/wkhtmltopdf:0.12.11` 26 MB; the reference system with wkhtmltopdf and its fonts 330 MB

Each set's wall time, one document after another, each program warmed up first. A document's time is the median of its runs, read from /proc/uptime (10 ms steps), as the published figures were.

## What ran

- **international** pass: wkhtmltopdf 0.12.6 (with patched qt); wkhtmltopdf 0.12.6 (with patched qt) (compatible; marqius-wkhtmltopdf 0.12.11); Alpine 3.24.3, x86_64, 4 cpus (Intel(R) Xeon(R) 6975P-C), 15.3 GB; 116 font files, 43 families
- **main** pass: wkhtmltopdf 0.12.6 (with patched qt); wkhtmltopdf 0.12.6 (with patched qt) (compatible; marqius-wkhtmltopdf 0.12.11); Alpine 3.24.3, x86_64, 4 cpus (Intel(R) Xeon(R) 6975P-C), 15.3 GB; 112 font files, 28 families
- image `reference`: `surnet/alpine-wkhtmltopdf:3.24.3-0.12.6-full`, digest `sha256:ce8cbcdfd11a8f73ba0bb5a86301e17325c93a39485cf4165e3e99a08503dca9`, 330 MB unpacked
- image `marqius`: `marqius/wkhtmltopdf:0.12.11`, digest `sha256:dd281e49d67d3794e30b7c503d2fbd6bf5221b53af1db4ee93107aa058ae38fa`, 26 MB unpacked
- image `scorer`: `wkhtmltopdf-parity-scorer (harness/Dockerfile, built here)`
- image `cjk`: `wkhtmltopdf-parity-cjk (harness/Dockerfile, built here)`
- marqius-wkhtmltopdf program: sha256 `501f6ece1f26e130416033107601b8cd21d279ba8e3e2321552056f4856b893b`, 20.0 MB
- scorer: pdftotext version 25.12.0, Python 3.14.10
- suite: 84e6222
- run: https://github.com/marqiushq/wkhtmltopdf-parity/actions/runs/44870467113
