#!/usr/bin/env python3
# Run in the repo folder: python3 update.py  (needs dpkg-deb, i.e. Linux/macOS with dpkg)
import os, subprocess, hashlib, gzip
out = []
for f in sorted(os.listdir("debs")):
    if not f.endswith(".deb"): continue
    p = os.path.join("debs", f)
    ctl = subprocess.check_output(["dpkg-deb", "-f", p]).decode().strip()
    data = open(p, "rb").read()
    out.append(ctl + "\nFilename: ./debs/%s\nSize: %d\nMD5sum: %s\nSHA1: %s\nSHA256: %s\n" % (
        f, len(data), hashlib.md5(data).hexdigest(), hashlib.sha1(data).hexdigest(), hashlib.sha256(data).hexdigest()))
txt = "\n".join(out)
open("Packages", "w").write(txt)
open("Packages.gz", "wb").write(gzip.compress(txt.encode(), 9))
print("Done:", len(out), "package(s)")
