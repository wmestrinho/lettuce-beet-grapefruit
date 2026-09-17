# Lettuce Beet Grapefruit

Sharing Earth Rights

Repository version: **0.1.0-alpha.1** (canonical source: [VERSION](VERSION)).

This umbrella repository currently contains brand documentation and release
tracking. The live `lettucebeetgrapefruit.com` and `lettucebeetgrapefruit.org`
sites are built from [Recyclopedia](https://github.com/wmestrinho/recyclopedia).
Website changes and their versions belong there; this repository has no deploy.

Follow the workspace [version rules](https://github.com/wmestrinho/ap-ops-workspace/blob/main/PROJECT-RULES.md).
Every commit is tracked by Git. Behavior/UI changes require a VERSION increase
and dated CHANGELOG entry; docs/CI-only changes are exempt from bumping.
Tags and GitHub releases are created by a human after review.

Validation: `python3 scripts/check_release_version.py`.
For source PRs: `python3 scripts/check_release_version.py --base origin/main`.

The pre-existing LICENSE is preserved by this version-tracking change.
