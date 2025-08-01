Upgrades
========
Dependencies are currently spread out in a number of areas. This file tries to
summarise them.

Policy around upgrades will eventually emerge. At the start of the project, the
focus is on the future, and therefore on the latest versions, possibly with a
focus on long-term support (LTS) versions.


Python
------
See the Python version in `Dockerfile`, and maybe in some CI related bits.

PostgreSQL
----------
Check `docker-compose.ytml`, test setups in CI and probably things in any real
deployments.

Python dependencies
-------------------
Review `requirements.txt` and related files. We should still move to transitive
pinning with something like poetry in future. We will likely stay on LTS relases
of Django since version 5.2.

Look up each package at https://pypi.org/

During major Django upgrades, review the Django templates that we override, e.g.
in the admin and the registration templates.

CSS
---
Bootstrap is the main consideration. Versions are available here:
https://getbootstrap.com/docs/versions/

To review supported devices, see the appropriate page for the version, e.g.
https://getbootstrap.com/docs/5.3/getting-started/browsers-devices/

Obviously you might want to consider support information from
https://caniuse.com or MDN
https://developer.mozilla.org/en-US/docs/Web/CSS/word-break

JavaScript
----------
We try to keep JS dependencies minimal. Check `base.html`. Obviously some JS is
also included via Django, but we only consider Django as a whole. Some minimal
JS is also part of Bootstrap (see above).

For HTMX, release information is available here:
https://github.com/bigskysoftware/htmx/releases
