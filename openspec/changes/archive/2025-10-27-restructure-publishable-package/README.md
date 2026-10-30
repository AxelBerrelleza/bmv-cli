# restructure-publishable-package

Restructure flat layout (api/, commands/, main.py) into src/bmv_cli package; rename project to bmv-cli; add [project.scripts] bmv entry point; add LICENSE + proper README + classifiers; cleanup cruft (bmv/ dir, requirements.txt). Stays on setuptools (src-layout compatible) so this change is independently valid.
