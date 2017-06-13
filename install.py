#!/usr/bin/env python3

import shutil
import os
from stat import S_IRWXU, S_IXGRP, S_IXOTH

homedir = os.path.expanduser("~")
install_files = [("cf-fetch.py", "cf-fetch"),
    ("cf-test.py", "cf-test"),
    ("code_submit.py", "cf-submit")]
for src, dst in install_files:
  mdst = os.path.join(homedir, ".local", "bin", dst)
  shutil.copyfile(src, mdst)
  os.chmod(mdst, S_IRWXU | S_IXGRP | S_IXOTH)
