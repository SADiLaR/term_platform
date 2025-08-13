Upgrades
========
Dependencies are currently spread out in a number of areas. This file tries to
summarise them.

Policy around upgrades will eventually emerge. At the start of the project, the
focus was on the future, and therefore on the latest versions, possibly with a
focus on long-term support (LTS) versions. We are now gradually stabilising on
versions with a long-term outlook where available.


Python
------
See the Python version in `Dockerfile`, and maybe in some CI related bits.

PostgreSQL
----------
Check `docker-compose.yml`, test setups in CI and probably things in any real
deployments.

Python dependencies
-------------------
Review `requirements.txt` and related files. We should still move to transitive
pinning with something like poetry in future. We will likely stay on LTS
releases of Django since version 5.2.

Look up each package at https://pypi.org/

During major Django upgrades, review the Django templates that we override, e.g.
in the admin and the registration templates.

CSS
---
Bootstrap is the main consideration. Versions are available here:
https://getbootstrap.com/docs/versions/

To review supported browsers, see the appropriate page for the version, e.g.
https://getbootstrap.com/docs/5.3/getting-started/browsers-devices/

Obviously you might want to consider support information from
https://caniuse.com or MDN
https://developer.mozilla.org/en-US/docs/Web/CSS/word-break

The Bootstrap icons can easily be swapped with something else, or pinned on a
version that provides what we use (instead of upgrading frequently). The way in
which icons are used and included in the project is likely to change in future.

JavaScript
----------
We try to keep JS dependencies minimal. Check `base.html`. Obviously some JS is
also included via Django, but we only consider Django as a whole. Some minimal
JS is also part of Bootstrap (see above).

For HTMX, release information is available here:
https://github.com/bigskysoftware/htmx/releases

We check for correct functioning through Selenium tests with JS enabled and
disabled. Some things might not work, but we should actively decide if that is
ok. An example is the mobile navigation menu that doesn't work without JS. A
solution for that case would be ideal, but has not yet been prioritised.
