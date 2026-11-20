#!/bin/sh
# Runs inside the reference container (surnet/alpine-wkhtmltopdf, BusyBox sh), with no network
# unless run.sh was given --network. Both programs convert every document of every set here, on
# the same system with the same fonts, one document after another:
#
#   wk   wkhtmltopdf 0.12.6, as the image has it
#   mq   marqius-wkhtmltopdf, taken out of its Docker image by run.sh and started under the name
#        wkhtmltopdf, as the programs that call wkhtmltopdf start it
#
# Mounts:   /parity/harness (this folder, read-only)   /parity/corpus (the sets, read-only)
#           /parity/work (outputs; work/bin holds the marqius-wkhtmltopdf program)
# Settings: PARITY_SETS    the sets to convert: folders of /parity/corpus, in order
#           PARITY_RUNS    timed runs of each program over all the sets (the PDFs are kept from the first)
#           PARITY_NOWAIT  1: one more run of each over print and everyday with --javascript-delay 0
#           PARITY_OPTIONS a file of options for documents that have no .cmd file of their own
#           PARITY_LABEL   a name for this pass in the logs (main, international, mine)
#
# A set's documents: its .cmd files if it has any (each line one argument, the output left out;
# lines starting with # are notes), otherwise every .html file at its top level, converted with
# -q --enable-local-file-access, then the options file's options, then the file.
set -u
W=/parity/work
C=/parity/corpus
L=${PARITY_LABEL:-main}
RUNS=${PARITY_RUNS:-3}
mkdir -p "$W/times" "$W/env" "$W/logs" /tmp/parity

# a clock in microseconds (BusyBox's adjtimex reads the system clock without changing it), or
# /proc/uptime's hundredths where adjtimex is refused. Once a time daemon has set the kernel's
# NANO status (8192), tv_usec holds nanoseconds: they are brought back to microseconds
now_us() {
    busybox adjtimex 2> /dev/null | awk '/status:/ { n = int($2) % 16384 >= 8192 } /tv_sec/ { s = $2 } /tv_usec/ { u = $2 }
        END { if (s) printf "%d%06d\n", s, n ? int(u / 1000) : u }'
}
[ -n "$(now_us)" ] || now_us() { awk '{ printf "%d\n", $1 * 1000000 }' /proc/uptime; }
# per document, as the published compare lane timed it: /proc/uptime before and after
up() { cut -d' ' -f1 /proc/uptime; }
ms() { awk -v a="$1" -v b="$2" 'BEGIN { printf "%d", (b - a) * 1000 }'; }

# marqius-wkhtmltopdf, copied into the container (a program run from a shared folder is read
# across the share at every start) and named wkhtmltopdf
mkdir -p /tmp/parity/bin
cp "$W/bin/marqius-wkhtmltopdf" /tmp/parity/bin/marqius-wkhtmltopdf
chmod 755 /tmp/parity/bin/marqius-wkhtmltopdf
ln -sf /tmp/parity/bin/marqius-wkhtmltopdf /tmp/parity/bin/wkhtmltopdf
WK=$(command -v wkhtmltopdf)
MQ=/tmp/parity/bin/wkhtmltopdf

# a set's own fonts (mine/fonts): put where fontconfig looks for a user's fonts, for both programs
for s in $PARITY_SETS; do
    if [ -d "$C/$s/fonts" ]; then
        mkdir -p "$HOME/.local/share/fonts/parity-$s" "$HOME/.fonts"
        find "$C/$s/fonts" -type f \( -iname '*.ttf' -o -iname '*.otf' -o -iname '*.ttc' -o -iname '*.otc' \) -exec cp {} "$HOME/.local/share/fonts/parity-$s/" \;
        cp "$HOME/.local/share/fonts/parity-$s/"* "$HOME/.fonts/" 2> /dev/null
        fc-cache -f > /dev/null 2>&1
        echo "$(ls "$HOME/.local/share/fonts/parity-$s" | wc -l | tr -d ' ')" > "$W/env/fonts-added-$s.txt"
    fi
done

# what this system is: the report prints it beside the scores
{
    echo "label	$L"
    echo "alpine	$(cat /etc/alpine-release 2> /dev/null)"
    echo "machine	$(uname -m)"
    echo "kernel	$(uname -r)"
    echo "cpus	$(nproc 2> /dev/null)"
    echo "cpu	$(grep -m1 -E 'model name|Model' /proc/cpuinfo 2> /dev/null | cut -d: -f2- | sed 's/^ *//')"
    echo "memory	$(awk '/MemTotal/ { printf "%.1f GB", $2 / 1048576 }' /proc/meminfo)"
    echo "wk_path	$WK"
    echo "wk_version	$("$WK" -V 2> /dev/null | head -1)"
    echo "mq_as_wkhtmltopdf	$("$MQ" -V 2> /dev/null | head -1)"
    echo "mq_version	$(/tmp/parity/bin/marqius-wkhtmltopdf --version 2> /dev/null | head -1)"
    echo "mq_sha256	$(sha256sum /tmp/parity/bin/marqius-wkhtmltopdf | cut -d' ' -f1)"
    echo "fontconfig	$(fc-list --version 2>&1 | head -1)"
    echo "font_files	$(fc-list : file | wc -l | tr -d ' ')"
    for g in sans-serif serif monospace Arial Helvetica 'Times New Roman' Verdana Georgia 'Courier New'; do
        echo "match_$g	$(fc-match "$g" 2> /dev/null)"
    done
} > "$W/env/$L.tsv"
fc-list : family | sort -u > "$W/env/$L-families.txt"

# the documents of a set, one a line: NAME, a tab, the file of arguments made for it
jobs_of() {
    _set=$1
    _d="$C/$_set"
    _j="/tmp/parity/jobs-$_set"
    mkdir -p "$_j"
    : > "$_j/list"
    if ls "$_d"/*.cmd > /dev/null 2>&1; then
        for _f in "$_d"/*.cmd; do
            _n=$(basename "$_f" .cmd)
            grep -v -e '^#' -e '^[[:space:]]*$' "$_f" > "$_j/$_n.args"
            printf '%s\t%s\n' "$_n" "$_j/$_n.args" >> "$_j/list"
        done
    else
        # options for every document of the set: the options file, split as a shell would (quotes
        # kept together, nothing run); the files they name (headers, footers, a cover) are no
        # documents of their own
        : > "$_j/options"
        if [ -n "${PARITY_OPTIONS:-}" ] && [ -s "$PARITY_OPTIONS" ]; then
            grep -v -e '^#' "$PARITY_OPTIONS" | xargs -r printf '%s\n' > "$_j/options"
        fi
        _skip=$(awk 'prev ~ /^(--header-html|--footer-html|cover|--user-style-sheet|--xsl-style-sheet)$/ { print } { prev = $0 }' "$_j/options" | sed 's#.*/##')
        for _f in "$_d"/*.html "$_d"/*.htm; do
            [ -f "$_f" ] || continue
            _b=$(basename "$_f")
            if [ -n "$_skip" ] && printf '%s\n' "$_skip" | grep -qxF "$_b"; then
                continue
            fi
            _n=${_b%.*}
            { echo "-q"; echo "--enable-local-file-access"; cat "$_j/options"; echo "$_f"; } > "$_j/$_n.args"
            printf '%s\t%s\n' "$_n" "$_j/$_n.args" >> "$_j/list"
        done
    fi
}

# convert PROG LABEL RUN SET [EXTRA]: each document of SET through PROG, timed; the PDFs, the
# standard error and the times are kept from run 1 (later runs only time, into a scratch folder)
convert_set() {
    _p=$1 _who=$2 _run=$3 _set=$4 _extra=${5:-}
    if [ "$_run" = 1 ]; then
        _o="$W/pdf/$_who/$_set"
    else
        _o="/tmp/parity/out-$_who-$_run/$_set"
    fi
    _e="$W/logs/$_who/$_set"
    mkdir -p "$_o" "$_e"
    while IFS='	' read -r _n _args; do
        [ -n "$_n" ] || continue
        # the arguments, one a line, as positional parameters (no shell parses them)
        set --
        [ -n "$_extra" ] && set -- "$_extra" 0
        while IFS= read -r _a || [ -n "$_a" ]; do set -- "$@" "$_a"; done < "$_args"
        _a0=$(up)
        if [ "$_run" = 1 ]; then
            (cd "$C/$_set" && timeout 180 "$_p" "$@" "$_o/$_n.pdf" > "$_e/$_n.out" 2> "$_e/$_n.err" < /dev/null)
        else
            (cd "$C/$_set" && timeout 180 "$_p" "$@" "$_o/$_n.pdf" > /dev/null 2>&1 < /dev/null)
        fi
        _s=$?
        printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$_who" "$_run" "$_set" "$_n" "$_s" "$(ms "$_a0" "$(up)")" >> "$W/times/$L.tsv"
    done < "/tmp/parity/jobs-$_set/list"
}

# run PROG LABEL RUN [EXTRA] [SETS]: every set in turn, each set's wall time in microseconds
run_all() {
    _p=$1 _who=$2 _run=$3 _extra=${4:-} _sets=${5:-$PARITY_SETS}
    for _set in $_sets; do
        _t0=$(now_us)
        convert_set "$_p" "$_who" "$_run" "$_set" "$_extra"
        _t1=$(now_us)
        _us=$((${_t1:-0} - ${_t0:-0}))
        # a time outside 0 < t < 3600 s is a clock that misread, never a run: it is dropped
        if [ -n "$_t0" ] && [ -n "$_t1" ] && [ "$_us" -gt 0 ] && [ "$_us" -lt 3600000000 ]; then
            printf '%s\t%s\t%s\t%s\n' "$_who" "$_run" "$_set" "$_us" >> "$W/times/$L-sets.tsv"
        else
            echo "convert.sh: $_who, run $_run, $_set: the clock read ${_t0:-nothing} then ${_t1:-nothing}; that time is dropped" >&2
        fi
    done
}

for s in $PARITY_SETS; do jobs_of "$s"; done
# the names of the options used, never their values (./run.sh share can tell which features a run used)
cat /tmp/parity/jobs-*/*.args 2> /dev/null | grep -E -x -e '--?[A-Za-z][A-Za-z0-9-]*' -e 'cover' -e 'toc' | sort -u > "$W/options-used.txt"
first_set=${PARITY_SETS%% *}
first_doc=$(head -1 "/tmp/parity/jobs-$first_set/list" | cut -f1)
: > "$W/times/$L.tsv"
: > "$W/times/$L-sets.tsv"

# a first run of each, not timed: a server pays for loading (and marqius for its font index) once
for p in "$WK" "$MQ"; do
    set --
    while IFS= read -r a || [ -n "$a" ]; do set -- "$@" "$a"; done < "/tmp/parity/jobs-$first_set/$first_doc.args"
    (cd "$C/$first_set" && timeout 180 "$p" "$@" /tmp/parity/warm.pdf > /dev/null 2>&1 < /dev/null)
done

# the timed runs: wkhtmltopdf over every set, then marqius-wkhtmltopdf, and again
r=1
while [ "$r" -le "$RUNS" ]; do
    run_all "$WK" wk "$r"
    run_all "$MQ" mq "$r"
    r=$((r + 1))
done
# with wkhtmltopdf's 200 ms wait for scripts turned off (--javascript-delay 0), on the published sets
if [ "${PARITY_NOWAIT:-0}" = 1 ]; then
    nw=""
    for s in $PARITY_SETS; do case "$s" in print | everyday) nw="$nw $s" ;; esac; done
    if [ -n "$nw" ]; then
        run_all "$WK" wk nowait --javascript-delay "$nw"
        run_all "$MQ" mq nowait --javascript-delay "$nw"
    fi
fi

# document by document, with the program's own comparison: verdicts, causes, marked pages
mkdir -p "$W/compare"
for s in $PARITY_SETS; do
    if [ -d "$W/pdf/wk/$s" ] && [ -d "$W/pdf/mq/$s" ]; then
        /tmp/parity/bin/marqius-wkhtmltopdf compare "$W/pdf/wk/$s" "$W/pdf/mq/$s" -o "$W/compare/$s" --quiet > "$W/compare/$s.out" 2> "$W/compare/$s.err"
        echo "$?" > "$W/compare/$s.status"
    fi
done
echo "done" > "$W/env/$L.done"
