#!/bin/sh
# Odoo's report CSS for PDFs, as Odoo VERSION's own server compiles it, from Odoo's official Docker
# image: a database with only the base modules, then the two stylesheets web.minimal_layout links
# (web.report_assets_pdf, web.report_assets_common), with the fonts they name. Also notes the
# image's digest, Odoo's version and the wkhtmltopdf inside the image.
#   sh harness/odoo.sh VERSION OUTDIR RENDER_IMAGE
set -eu
v=$1
out=$2
img=$3
here=$(cd "$(dirname "$0")" && pwd)
t=$(echo "$v" | tr . -)
net=bs5-net-$t
pg=bs5-pg-$t
od=bs5-odoo-$t
cleanup() {
    docker rm -f "$od" "$pg" > /dev/null 2>&1 || true
    docker network rm "$net" > /dev/null 2>&1 || true
}
trap cleanup EXIT
cleanup
mkdir -p "$out"
docker pull -q "odoo:$v" > /dev/null
docker network create "$net" > /dev/null
docker run -d --name "$pg" --network "$net" -e POSTGRES_USER=odoo -e POSTGRES_PASSWORD=odoo -e POSTGRES_DB=postgres postgres:16 > /dev/null
i=0
until docker exec "$pg" pg_isready -q -U odoo > /dev/null 2>&1; do
    i=$((i + 1))
    [ "$i" -lt 90 ] || { echo "postgres did not start" >&2; exit 1; }
    sleep 1
done
sleep 2
docker run --rm --network "$net" --entrypoint odoo "odoo:$v" --db_host "$pg" --db_user odoo --db_password odoo -d bs5 \
    -i base --stop-after-init --log-level=warn
docker run -d --name "$od" --network "$net" --entrypoint odoo "odoo:$v" --db_host "$pg" --db_user odoo --db_password odoo -d bs5 \
    --db-filter '^bs5$' --log-level=warn > /dev/null
case "$v" in
17.0 | 18.0) sfx="" ;;
*) sfx=".autoprefixed" ;;
esac
docker run --rm --network "$net" -v "$out:/out" -v "$here:/h:ro" "$img" python3 /h/odoo_fetch.py "http://$od:8069" "$sfx" /out
{
    printf 'image\t%s\n' "$(docker image inspect --format '{{index .RepoDigests 0}}' "odoo:$v")"
    docker run --rm --entrypoint sh "odoo:$v" -c \
        'printf "odoo\t%s\n" "$(odoo --version)"; printf "wkhtmltopdf\t%s\n" "$(wkhtmltopdf --version)"; printf "wkhtmltopdf_sha256\t%s\n" "$(sha256sum /usr/local/bin/wkhtmltopdf | cut -c1-64)"'
    printf 'bundles\tweb.report_assets_pdf%s.min.css, web.report_assets_common%s.min.css\n' "$sfx" "$sfx"
} > "$out/about.tsv"
cat "$out/about.tsv"
