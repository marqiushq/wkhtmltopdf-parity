#!/bin/sh
# Bootstrap's CSS as Odoo's own source tree ships it (addons/web/static/lib/bootstrap/dist/css), at
# the commits named below, checked against the same release on npm; the test helpers; and compare,
# the PDF comparison of marqius-wkhtmltopdf, from its GitHub release (checksum checked).
#   sh harness/fetch.sh SITE BIN
set -eu
site=$1
bin=$2
here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$site/css" "$site/harness" "$bin"
cp "$here/markers.css" "$here/base.css" "$here/probe.js" "$site/harness/"

get() { curl -fsSL --retry 5 --retry-all-errors -o "$2" "$1"; }

# version  Odoo branch  Odoo commit (branch head on 2026-11-21)
while read -r v branch commit; do
    get "https://raw.githubusercontent.com/odoo/odoo/$commit/addons/web/static/lib/bootstrap/dist/css/bootstrap.css" "$site/css/bootstrap-$v.css"
    get "https://cdn.jsdelivr.net/npm/bootstrap@$v/dist/css/bootstrap.css" "$site/css/npm-$v.css"
    a=$(sha256sum < "$site/css/bootstrap-$v.css" | cut -c1-64)
    b=$(sha256sum < "$site/css/npm-$v.css" | cut -c1-64)
    same=no
    [ "$a" = "$b" ] && same=yes
    printf 'bootstrap\t%s\todoo %s %s\tsha256 %s\tsame as npm bootstrap@%s: %s\n' "$v" "$branch" "$commit" "$a" "$v" "$same"
    rm -f "$site/css/npm-$v.css"
done <<'EOF'
5.1.3 17.0 d986860360429eaa37aee29c06592041350da850
5.3.3 19.0 10b383d29846b868fdd5e7c481330074d8ca0990
EOF

rel=https://github.com/marqiushq/marqius-wkhtmltopdf/releases/download/v0.12.13
get "$rel/marqius-wkhtmltopdf-linux-x86_64" "$bin/marqius-wkhtmltopdf"
get "$rel/SHA256SUMS" "$bin/SHA256SUMS"
want=$(grep ' marqius-wkhtmltopdf-linux-x86_64$' "$bin/SHA256SUMS" | cut -c1-64)
got=$(sha256sum < "$bin/marqius-wkhtmltopdf" | cut -c1-64)
[ "$want" = "$got" ] || { echo "marqius-wkhtmltopdf: checksum $got is not the release's $want" >&2; exit 1; }
chmod 755 "$bin/marqius-wkhtmltopdf"
printf 'compare\tmarqius-wkhtmltopdf 0.12.13 linux-x86_64\tsha256 %s (as the release lists it)\n' "$got"
