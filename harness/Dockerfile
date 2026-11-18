# Two helper images, both built on the reference system (the image wkhtmltopdf 0.12.6 runs in),
# pinned by digest in harness/images.env. run.sh builds them; nothing else is downloaded.
#
#   --target cjk      the reference system with Alpine's Noto CJK fonts added, for the
#                     international set and for your own templates in Chinese, Japanese or Korean.
#                     Both programs run in it; the published sets never do.
#   --target scorer   the reference system with poppler (pdftotext, pdfinfo, pdffonts), Python
#                     and Pillow (small copies of compare's pictures), which score.py needs.
#                     It only reads PDFs; no converter runs in it.
ARG REFERENCE=surnet/alpine-wkhtmltopdf:3.24.3-0.12.6-full@sha256:ce8cbcdfd11a8f73ba0bb5a86301e17325c93a39485cf4165e3e99a08503dca9

FROM ${REFERENCE} AS cjk
RUN apk add --no-cache font-noto-cjk && fc-cache -f > /dev/null

FROM ${REFERENCE} AS scorer
RUN apk add --no-cache python3 py3-pillow poppler-utils
