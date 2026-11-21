# The program under test is wkhtmltopdf exactly as Odoo's official Docker image ships it
# (/usr/local/bin/wkhtmltopdf, upstream's 0.12.6.1-3 package, with patched Qt), with its fonts.
# Google Chrome is added beside it as the reference, plus the tools that read the PDFs; the URW
# font clones are hidden so both programs use the same fonts (same-fonts.conf).
ARG ODOO_IMAGE=odoo:19.0
FROM ${ODOO_IMAGE}
USER root
RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends ca-certificates curl poppler-utils python3-numpy python3-pil; \
    curl -fsSL --retry 5 -o /tmp/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb; \
    apt-get install -y --no-install-recommends /tmp/chrome.deb; \
    rm -f /tmp/chrome.deb; \
    rm -rf /var/lib/apt/lists/*
COPY same-fonts.conf /etc/fonts/conf.d/99-same-fonts.conf
RUN fc-cache -f
ENTRYPOINT []
