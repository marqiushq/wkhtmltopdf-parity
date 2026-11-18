# Your own templates

Put the HTML files you convert with wkhtmltopdf here, then run `./run.sh mine` from the folder above.

- **Templates:** every `.html` file at the top of this folder is converted by both programs.
- **What they load:** keep pictures, style sheets and scripts where the templates expect them, here or in folders below. Files in folders below are not converted on their own.
- **The options your app passes:** write them on one line in `options.txt`, as you would on the command line, for example `--page-size A4 --margin-top 12mm --footer-right "[page] of [topage]"`. Files the options name, such as `--header-html header.html`, are not converted on their own.
- **Fonts your servers have that the reference system lacks:** put the `.ttf` or `.otf` files in `fonts/`. Both programs get them.
- **One template, its own command line:** instead of an `.html` file, write a `.cmd` file with one argument a line, as in `corpus/options`.
- **Pages from a web address:** save the page with its files first (your browser's "Save page as, complete"), then put it here.

Nothing here leaves your machine: the containers that read these files run with no network, unless you add `--network` so that both programs can load files from the internet. `./run.sh share` sends a summary of the scores, never these files, and only if you say yes. Everything in this folder except this README is left out of git.
