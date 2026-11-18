#!/usr/bin/env bash
# The wkhtmltopdf parity suite: every document through wkhtmltopdf 0.12.6 and through
# marqius-wkhtmltopdf, side by side in one Linux system with one set of fonts, then scored.
# It needs Docker and nothing else.
#
#   ./run.sh                     the whole corpus with marqius/wkhtmltopdf:latest
#   ./run.sh mine                your own templates, from ./mine
#   ./run.sh --tag 0.12.2        another version (any tag of marqius/wkhtmltopdf)
#   ./run.sh --help              everything else
set -euo pipefail

here=$(cd "$(dirname "$0")" && pwd)
# shellcheck source=harness/images.env
. "$here/harness/images.env"

usage() {
    cat <<'EOF'
Usage: ./run.sh [mine] [options]

  (no word)           convert and score the corpus: corpus/print, everyday, options, international
  mine                convert and score your own templates: every .html file at the top of ./mine

Options
  --tag TAG           the marqius/wkhtmltopdf tag to test (default: latest)
  --sets A,B          only these sets of the corpus (default: all of corpus/sets.tsv)
  --runs N            timed runs of each program (default: 3; 1 for more than 30 templates)
  --quick             one run, and no run with wkhtmltopdf's script wait turned off
  --network           let both programs load files from the internet (default: no network at all)
  --cjk               add Noto CJK fonts for both programs (automatic for mine when the
                      templates hold Chinese, Japanese or Korean text)
  --platform P        linux/amd64 or linux/arm64 (default: this machine's)
  --pull              download the program's image again even when it is here (latest always is)
  --program FILE      test this marqius-wkhtmltopdf program for Linux (a build not yet on Docker Hub)
                      instead of the one in the image
  --mine DIR          your templates from another folder than ./mine (implies mine)
  --out DIR           where the report goes (default: ./out/corpus or ./out/mine)
  -h, --help          this help

The report: OUT/report.html (open it in a browser), report.md, report.json, scores.csv; the PDFs in
OUT/pdf/wk and OUT/pdf/mq; marqius-wkhtmltopdf compare's own report in OUT/compare.
EOF
}

mode=corpus tag=$DEFAULT_TAG sets="" runs="" quick=0 net=none cjk=0 platform="" out="" mine="$here/mine" pull=0 pulled_digest="" program=""
while [ $# -gt 0 ]; do
    case "$1" in
        mine) mode=mine ;;
        corpus) mode=corpus ;;
        --tag) tag=${2:?--tag needs a tag}; shift ;;
        --tag=*) tag=${1#--tag=} ;;
        --sets) sets=${2:?--sets needs a list}; shift ;;
        --sets=*) sets=${1#--sets=} ;;
        --runs) runs=${2:?--runs needs a number}; shift ;;
        --runs=*) runs=${1#--runs=} ;;
        --quick) quick=1 ;;
        --network) net=bridge ;;
        --cjk) cjk=1 ;;
        --pull) pull=1 ;;
        --program) program=${2:?--program needs a file}; shift ;;
        --program=*) program=${1#--program=} ;;
        --platform) platform=${2:?--platform needs linux/amd64 or linux/arm64}; shift ;;
        --platform=*) platform=${1#--platform=} ;;
        --mine) mine=${2:?--mine needs a folder}; mode=mine; shift ;;
        --mine=*) mine=${1#--mine=}; mode=mine ;;
        --out) out=${2:?--out needs a folder}; shift ;;
        --out=*) out=${1#--out=} ;;
        -h | --help) usage; exit 0 ;;
        *) echo "run.sh: unknown argument '$1' (./run.sh --help lists them)" >&2; exit 2 ;;
    esac
    shift
done
case "$runs" in "" | [1-9] | [1-9][0-9]) ;; *) echo "run.sh: --runs takes a number from 1 to 99" >&2; exit 2 ;; esac

say() { printf '%s\n' "$*" >&2; }
die() { say "run.sh: $*"; exit 1; }
command -v docker > /dev/null || die "Docker is needed: https://docs.docker.com/get-docker/"
docker info > /dev/null 2>&1 || die "Docker is installed but not running (docker info failed)"
pf=()
if [ -n "$platform" ]; then
    pf=(--platform "$platform")
    case "$platform" in
        linux/amd64) REFERENCE=$REFERENCE_AMD64 ;;
        linux/arm64 | linux/arm64/v8) REFERENCE=$REFERENCE_ARM64 ;;
        *) die "--platform takes linux/amd64 or linux/arm64" ;;
    esac
fi

# what to convert
if [ "$mode" = mine ]; then
    [ -d "$mine" ] || die "no folder $mine: put your templates there (see mine/README.md)"
    mine=$(cd "$mine" && pwd)
    shopt -s nullglob
    docs=("$mine"/*.html "$mine"/*.htm "$mine"/*.cmd)
    shopt -u nullglob
    [ ${#docs[@]} -gt 0 ] || die "no .html files in $mine: copy your templates there (see mine/README.md)"
    set_list=mine
    out=${out:-$here/out/mine}
    # three timed runs steady the speed figure; with many templates one is enough
    [ ${#docs[@]} -le 30 ] && runs=${runs:-3} || runs=${runs:-1}
    # Chinese, Japanese or Korean text (UTF-8 lead bytes E3 to ED): the reference system has no font for it
    if LC_ALL=C grep -q -E $'[\xe3-\xed][\x80-\xbf][\x80-\xbf]' "${docs[@]}" 2> /dev/null; then
        [ "$cjk" = 1 ] || say "Your templates hold Chinese, Japanese or Korean text: Noto CJK fonts are added for both programs."
        cjk=1
    fi
    if [ "$net" = none ] && grep -q -i -E '(src|href|url)[=(]["'"'"']?(https?:)?//' "${docs[@]}" 2> /dev/null; then
        say "Your templates load files from the internet; without --network neither program can fetch them."
    fi
else
    all=$(awk -F'\t' 'NR > 1 { print $1 }' "$here/corpus/sets.tsv" | tr '\n' ' ')
    if [ -n "$sets" ]; then
        set_list=$(printf '%s' "$sets" | tr ',' ' ')
        for s in $set_list; do
            case " $all " in *" $s "*) ;; *) die "no set '$s' (the sets: $all)" ;; esac
        done
    else
        set_list=$all
    fi
    out=${out:-$here/out/corpus}
    runs=${runs:-3}
fi
[ "$quick" = 1 ] && runs=1
nowait=$([ "$mode" = corpus ] && [ "$quick" = 0 ] && echo 1 || echo 0)

# the images: the reference by its digest, which never changes, so it is downloaded only when it is
# not here; the program by tag: latest every time, a version when it is not here (each download
# counts as a pull on Docker Hub)
image="$MARQIUS:$tag"
say "Images: $REFERENCE"
if [ -n "$program" ]; then say "Program: $program"; else say "        $image"; fi
plat_of() { docker image inspect --format '{{.Os}}/{{.Architecture}}' "$1" 2> /dev/null || true; }
digest() { docker image inspect --format '{{range .RepoDigests}}{{println .}}{{end}}' "$1" 2> /dev/null | grep -m1 "^${2}@" || true; }
if [ -z "$(plat_of "$REFERENCE")" ]; then
    docker pull -q ${pf[@]+"${pf[@]}"} "$REFERENCE" > /dev/null || die "cannot download $REFERENCE"
fi
# everything else runs on the reference's platform
plat=$(plat_of "$REFERENCE")
arch=${plat##*/}
# (also when the image here has lost its registry digest: the report must name the one Docker Hub gives)
if [ -n "$program" ]; then
    [ -f "$program" ] || die "no program $program"
    image="a program from this machine ($program)"
elif [ "$tag" = latest ] || [ "$pull" = 1 ] || [ "$(plat_of "$image")" != "$plat" ] || [ -z "$(digest "$image" "$MARQIUS")" ]; then
    if pulled=$(docker pull --platform "$plat" "$image" 2>&1); then
        # the digest Docker Hub gave, in case the image store keeps none
        pulled_digest=$(printf '%s\n' "$pulled" | sed -n 's/^Digest: //p' | head -1)
    elif [ "$(plat_of "$image")" = "$plat" ]; then
        say "(Docker Hub cannot be reached: using the $image already here)"
    else
        die "cannot download $image for $plat (is '$tag' a tag of $MARQIUS?)"
    fi
fi

if [ -d "$out" ] && [ -n "$(ls -A "$out" 2> /dev/null)" ]; then
    [ -f "$out/meta.tsv" ] || die "$out is not empty and holds no earlier report: choose another --out"
    rm -rf "${out:?}"
fi
mkdir -p "$out/bin"
out=$(cd "$out" && pwd)
# what the containers see: the sets (read-only), the harness (read-only) and the report folder
if [ "$mode" = mine ]; then
    corpus_mount=(-v "$mine:/parity/corpus/mine:ro")
else
    corpus_mount=(-v "$here/corpus:/parity/corpus:ro")
fi

# the program, out of its image (the static binary at /marqius-wkhtmltopdf), or the one given
if [ -n "$program" ]; then
    cp "$program" "$out/bin/marqius-wkhtmltopdf"
else
    cid=$(docker create --platform "$plat" "$image")
    docker cp "$cid:/marqius-wkhtmltopdf" "$out/bin/marqius-wkhtmltopdf" > /dev/null 2>&1 \
        || docker cp "$cid:/usr/local/bin/marqius-wkhtmltopdf" "$out/bin/marqius-wkhtmltopdf" > /dev/null 2>&1 \
        || { docker rm "$cid" > /dev/null; die "no marqius-wkhtmltopdf program in $image"; }
    docker rm "$cid" > /dev/null
fi

# the helper images, built on the reference: the scorer, and the reference with Noto CJK
say "Building the scorer (poppler and Python on the reference system)..."
docker build -q --platform "$plat" --build-arg "REFERENCE=$REFERENCE" --target scorer -t "wkhtmltopdf-parity-scorer:$arch" -f "$here/harness/Dockerfile" "$here/harness" > /dev/null
need_cjk=$cjk
for s in $set_list; do
    [ "$mode" = corpus ] && [ "$(awk -F'\t' -v s="$s" '$1 == s { print $2 }' "$here/corpus/sets.tsv")" = cjk ] && need_cjk=1
done
if [ "$need_cjk" = 1 ]; then
    say "Building the reference system with Noto CJK fonts..."
    docker build -q --platform "$plat" --build-arg "REFERENCE=$REFERENCE" --target cjk -t "wkhtmltopdf-parity-cjk:$arch" -f "$here/harness/Dockerfile" "$here/harness" > /dev/null
fi

# what is known before the run, for the report
sha() { if command -v sha256sum > /dev/null; then sha256sum "$1" | cut -d' ' -f1; else shasum -a 256 "$1" | cut -d' ' -f1; fi; }
size_mb() { docker image inspect --format '{{.Size}}' "$1" | awk '{ printf "%.1f", $1 / 1048576 }'; }
commit=$(git -C "$here" rev-parse --short HEAD 2> /dev/null || echo "")
[ -n "$commit" ] && [ -n "$(git -C "$here" status --porcelain 2> /dev/null)" ] && commit="$commit (with local changes)"
{
    printf 'when\t%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    printf 'platform\t%s\n' "$plat"
    printf 'mode\t%s\n' "$mode"
    printf 'network\t%s\n' "$net"
    printf 'sets_list\t%s\n' "$set_list"
    printf 'marqius.image\t%s\n' "$image"
    printf 'marqius.tag\t%s\n' "$([ -n "$program" ] && echo local || echo "$tag")"
    printf 'marqius.version\t%s\n' "$tag"
    printf 'marqius.sha256\t%s\n' "$(sha "$out/bin/marqius-wkhtmltopdf")"
    printf 'marqius.size_mb\t%s\n' "$(ls -l "$out/bin/marqius-wkhtmltopdf" | awk '{ printf "%.1f", $5 / 1048576 }')"
    printf 'images.reference.name\t%s\n' "${REFERENCE%@*}"
    printf 'images.reference.digest\t%s\n' "${REFERENCE#*@}"
    printf 'images.reference.size_mb\t%s\n' "$(size_mb "$REFERENCE")"
    printf 'images.marqius.name\t%s\n' "$image"
    if [ -z "$program" ]; then
        d=$(digest "$image" "$MARQIUS" | sed 's/.*@//')
        printf 'images.marqius.digest\t%s\n' "${d:-$pulled_digest}"
        printf 'images.marqius.size_mb\t%s\n' "$(size_mb "$image")"
    fi
    printf 'images.scorer.name\t%s\n' "wkhtmltopdf-parity-scorer (harness/Dockerfile, built here)"
    [ "$need_cjk" = 1 ] && printf 'images.cjk.name\t%s\n' "wkhtmltopdf-parity-cjk (harness/Dockerfile, built here)"
    printf 'suite.commit\t%s\n' "$commit"
    if [ -n "${GITHUB_RUN_ID:-}" ]; then
        printf 'run_url\t%s\n' "${GITHUB_SERVER_URL:-https://github.com}/${GITHUB_REPOSITORY:-}/actions/runs/$GITHUB_RUN_ID"
    fi
} > "$out/meta.tsv"

# convert: each pass in its own container, with no network unless --network
convert() { # LABEL IMAGE SETS...
    local label=$1 img=$2
    shift 2
    local opts=()
    [ "$mode" = mine ] && [ -f "$mine/options.txt" ] && opts=(-e "PARITY_OPTIONS=/parity/corpus/mine/options.txt")
    for s in "$@"; do printf 'label.%s\t%s\n' "$s" "$label" >> "$out/meta.tsv"; done
    docker run --rm --platform "$plat" --network "$net" --user "$(id -u):$(id -g)" -e HOME=/tmp -e LANG=C.UTF-8 \
        -e "PARITY_SETS=$*" -e "PARITY_RUNS=$runs" -e "PARITY_NOWAIT=$nowait" -e "PARITY_LABEL=$label" ${opts[@]+"${opts[@]}"} \
        -v "$here/harness:/parity/harness:ro" "${corpus_mount[@]}" -v "$out:/parity/work" \
        --entrypoint sh "$img" /parity/harness/convert.sh
}
plain=() withcjk=()
for s in $set_list; do
    if [ "$mode" = mine ]; then
        if [ "$cjk" = 1 ]; then withcjk+=("$s"); else plain+=("$s"); fi
    elif [ "$(awk -F'\t' -v s="$s" '$1 == s { print $2 }' "$here/corpus/sets.tsv")" = cjk ]; then
        withcjk+=("$s")
    else
        plain+=("$s")
    fi
done
t0=$(date +%s)
if [ ${#plain[@]} -gt 0 ]; then
    say "Converting ${plain[*]} with both programs ($runs timed run$([ "$runs" = 1 ] || echo s))..."
    convert main "$REFERENCE" "${plain[@]}"
fi
if [ ${#withcjk[@]} -gt 0 ]; then
    say "Converting ${withcjk[*]} with both programs, Noto CJK added ($runs timed run$([ "$runs" = 1 ] || echo s))..."
    convert "$([ "$mode" = mine ] && echo mine || echo international)" "wkhtmltopdf-parity-cjk:$arch" "${withcjk[@]}"
fi

# score, with the network off: nothing leaves the machine
say "Scoring..."
docker run --rm --platform "$plat" --network none --user "$(id -u):$(id -g)" -e HOME=/tmp -e LANG=C.UTF-8 \
    -v "$here/harness:/parity/harness:ro" "${corpus_mount[@]}" -v "$out:/parity/work" \
    --entrypoint python3 "wkhtmltopdf-parity-scorer:$arch" /parity/harness/score.py /parity/work /parity/corpus /parity/work/meta.tsv
rm -rf "${out:?}/bin"
say ""
say "Done in $(($(date +%s) - t0)) s. The report: $out/report.html (also report.md, report.json, scores.csv)"
