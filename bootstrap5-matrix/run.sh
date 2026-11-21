#!/bin/sh
# Bootstrap 5 in wkhtmltopdf 0.12.6.1 as Odoo ships it, page by page against Chrome, judged by
# marqius-wkhtmltopdf compare. Needs Docker and curl, and about 15 GB of disk (Odoo's images).
#   sh run.sh [WORK]          the matrix lands in results/ (RESULTS.md, results.json, pictures/)
set -eu
here=$(cd "$(dirname "$0")" && pwd)
work=${1:-$here/work}
img=bootstrap5-matrix-render
mkdir -p "$work/site" "$work/out" "$work/bin"
docker build -q -t "$img" "$here/harness" > /dev/null
sh "$here/harness/fetch.sh" "$work/site" "$work/bin" | tee "$work/sources.tsv"
for v in 17.0 18.0 19.0 20.0; do
    sh "$here/harness/odoo.sh" "$v" "$work/site/odoo/$v" "$img"
done
docker run --rm --user "$(id -u):$(id -g)" -e HOME=/tmp -v "$here:/src:ro" -v "$work:/work" "$img" sh -c '
    python3 /src/harness/build.py /work/site &&
    python3 /src/harness/render.py /work/site /work/out /work/bin/marqius-wkhtmltopdf &&
    python3 /src/harness/judge.py /work/site /work/out /work/results'
# what was measured, with what
cp "$work/sources.tsv" "$work/results/sources.tsv"
for v in 17.0 18.0 19.0 20.0; do
    cp "$work/site/odoo/$v/about.tsv" "$work/results/odoo-$v.tsv"
done
rm -rf "${here:?}/results"
cp -R "$work/results" "$here/results"
echo "the matrix: $here/results/RESULTS.md"
