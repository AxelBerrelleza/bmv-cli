# adopt-uv-build-backend

Swap [build-system] from setuptools to uv_build (pinned with upper bound), remove setuptools-specific config, verify uv build --no-sources produces a valid sdist+wheel, refresh lock. Depends on the src/bmv_cli layout from restructure-publishable-package.
