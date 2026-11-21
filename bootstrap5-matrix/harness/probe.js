/* Reads the computed styles a page's checks ask for, in whichever program prints the page, and
   puts them in the document title, which both programs write into the PDF's Title field.
   ES5 only: wkhtmltopdf 0.12.6 runs JavaScriptCore of 2011. Geometry is not measured here but
   in the printed page itself (judge.py), because a program may lay a page out again to print it. */
(function () {
    var errors = [];
    window.onerror = function (msg) { errors.push(String(msg)); };

    function style(el, names) {
        var cs = window.getComputedStyle(el, null), list = names.split('|'), i, v;
        for (i = 0; i < list.length; i++) {
            v = cs.getPropertyValue(list[i]);
            if (v !== null && v !== '') { return v; }
        }
        return '';
    }

    function width(parent, family) {
        var s = document.createElement('span'), w;
        s.style.whiteSpace = 'nowrap';
        s.style.position = 'absolute';
        s.style.visibility = 'hidden';
        if (family) { s.style.fontFamily = family; }
        s.appendChild(document.createTextNode('The quick brown fox jumps over the lazy dog 0123456789 MWmwil'));
        parent.appendChild(s);
        w = s.offsetWidth;
        parent.removeChild(s);
        return w;
    }

    /* which generic family an element's text comes out in, or "other" (a named font of its own) */
    function family(el) {
        var own = width(el, ''), best = 'other', bestd = 0.005, kinds = ['serif', 'sans-serif', 'monospace'], i, d;
        for (i = 0; i < kinds.length; i++) {
            d = Math.abs(own - width(el, kinds[i])) / own;
            if (d < bestd) { bestd = d; best = kinds[i]; }
        }
        return best;
    }

    /* line height as a multiple of the font size, or "normal" (used by checks of type js) */
    function lh(sel) {
        var el = document.querySelector(sel), cs, l;
        if (!el) { return 'missing element'; }
        cs = window.getComputedStyle(el, null);
        l = cs.getPropertyValue('line-height');
        if (l === 'normal') { return 'normal'; }
        return String(Math.round(parseFloat(l) / parseFloat(cs.getPropertyValue('font-size')) * 100) / 100);
    }

    function run() {
        var out = { v: 1, js: {}, vw: document.documentElement.clientWidth, errors: errors }, checks = [], i, c, el;
        try {
            checks = JSON.parse(document.getElementById('checks').text);
        } catch (e) {
            errors.push('checks: ' + e.message);
        }
        for (i = 0; i < checks.length; i++) {
            c = checks[i];
            try {
                if (c.t === 'css' || c.t === 'font') {
                    el = document.querySelector(c.sel);
                    if (!el) { out.js[i] = 'missing element'; continue; }
                    out.js[i] = c.t === 'css' ? style(el, c.p) : family(el);
                } else if (c.t === 'js') {
                    out.js[i] = String(eval(c.x));
                }
            } catch (e) {
                out.js[i] = 'error: ' + e.message;
            }
        }
        document.title = 'PROBE ' + JSON.stringify(out);
    }

    /* a moment after load, so web fonts are in; both programs wait longer than this before printing */
    function later() { window.setTimeout(run, 300); }
    if (document.readyState === 'complete') { later(); } else { window.addEventListener('load', later, false); }
})();
