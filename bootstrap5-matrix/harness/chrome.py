"""Chrome driven over its DevTools pipe (standard library only), to print a page at a given scale:
the scale at which wkhtmltopdf, with Odoo's --dpi 90 --zoom 1.0667, puts a CSS pixel on paper, so
that the same CSS gives the same page in both programs and compare sees only what the CSS changes."""
import base64
import fcntl
import json
import os
import select
import time

A4 = dict(paperWidth=210 / 25.4, paperHeight=297 / 25.4)
MARGINS = dict(marginTop=10 / 25.4, marginBottom=10 / 25.4, marginLeft=0, marginRight=0)  # as wkhtmltopdf's


class Chrome:
    def __init__(self, exe, profile, width=794):
        r_in, w_in = os.pipe()      # Chrome reads commands on its fd 3
        r_out, w_out = os.pipe()    # and writes replies on its fd 4
        a = fcntl.fcntl(r_in, fcntl.F_DUPFD_CLOEXEC, 10)
        b = fcntl.fcntl(w_out, fcntl.F_DUPFD_CLOEXEC, 10)
        null = os.open(os.devnull, os.O_RDWR)
        args = [exe, "--headless=new", "--remote-debugging-pipe", "--no-sandbox", "--disable-gpu",
                "--hide-scrollbars", "--no-first-run", "--no-default-browser-check", "--user-data-dir=" + profile,
                "--window-size=%d,1400" % width,
                "about:blank"]
        self.pid = os.posix_spawn(exe, args, dict(os.environ), file_actions=[
            (os.POSIX_SPAWN_DUP2, null, 0), (os.POSIX_SPAWN_DUP2, null, 1), (os.POSIX_SPAWN_DUP2, null, 2),
            (os.POSIX_SPAWN_DUP2, a, 3), (os.POSIX_SPAWN_DUP2, b, 4)])
        for fd in (r_in, w_out, a, b, null):
            os.close(fd)
        self.w, self.r, self.buf, self.n, self.events = w_in, r_out, b"", 0, []

    def _messages(self, end):
        while b"\0" not in self.buf:
            left = end - time.time()
            if left <= 0:
                raise TimeoutError("Chrome did not answer in time")
            if select.select([self.r], [], [], left)[0]:
                chunk = os.read(self.r, 1 << 20)
                if not chunk:
                    raise RuntimeError("Chrome closed its pipe")
                self.buf += chunk
        out = []
        while b"\0" in self.buf:
            raw, self.buf = self.buf.split(b"\0", 1)
            out.append(json.loads(raw))
        return out

    def call(self, method, params=None, session=None, timeout=60):
        self.n += 1
        msg = dict(id=self.n, method=method, params=params or {})
        if session:
            msg["sessionId"] = session
        data = json.dumps(msg).encode() + b"\0"
        while data:
            data = data[os.write(self.w, data):]
        end = time.time() + timeout
        while True:
            for m in self._messages(end):
                if m.get("id") == self.n:
                    if "error" in m:
                        raise RuntimeError("%s: %s" % (method, m["error"]))
                    return m.get("result", {})
                if "method" in m:
                    self.events.append(m)

    def wait(self, event, session, timeout=30):
        end = time.time() + timeout
        while True:
            for i, e in enumerate(self.events):
                if e.get("method") == event and e.get("sessionId") == session:
                    del self.events[:i + 1]
                    return e
            self.events = [e for e in self.events if e.get("sessionId") == session]
            self.events += [m for m in self._messages(end) if "method" in m]

    def pdf(self, url, out, scale, timeout=60):
        """prints url to out at scale; returns the page's title once its measurements are in it"""
        target = self.call("Target.createTarget", dict(url="about:blank"))["targetId"]
        s = self.call("Target.attachToTarget", dict(targetId=target, flatten=True))["sessionId"]
        try:
            self.call("Page.enable", session=s)
            self.call("Page.navigate", dict(url=url), session=s)
            self.wait("Page.loadEventFired", s, timeout)
            title, end = "", time.time() + 10
            while time.time() < end:
                title = self.call("Runtime.evaluate", dict(expression="document.title", returnByValue=True),
                                  session=s)["result"].get("value", "")
                if title.startswith("PROBE "):
                    break
                time.sleep(0.05)
            r = self.call("Page.printToPDF", dict(scale=scale, printBackground=True, preferCSSPageSize=False,
                                                  displayHeaderFooter=False, generateTaggedPDF=False, **A4, **MARGINS), session=s, timeout=timeout)
            with open(out, "wb") as f:
                f.write(base64.b64decode(r["data"]))
            return title
        finally:
            self.call("Target.closeTarget", dict(targetId=target))
            self.events = []

    def close(self):
        try:
            self.call("Browser.close", timeout=10)
        except Exception:  # noqa: it may already be gone
            pass
        try:
            os.waitpid(self.pid, 0)
        except ChildProcessError:
            pass
