# Agent instructions

- Check `git status --short --branch` before editing, committing or pushing.
- Read README.md, CHANGELOG.md and HANDOFF.md first; preserve unrelated edits.
- Follow [workspace rules](https://github.com/wmestrinho/ap-ops-workspace/blob/main/PROJECT-RULES.md).
- VERSION is the bare SemVer source; keep package metadata in sync if introduced.
- Behavior/UI changes require a version increase and dated CHANGELOG entry.
  Docs/CI-only changes may retain the version. Every commit remains tracked in Git.
- Validate with `python3 scripts/check_release_version.py`; PRs also run it
  with `--base` to enforce a source version increase.
- Update HANDOFF.md after meaningful work. Tags/releases need human review.
- Website source lives in Recyclopedia. Do not treat this repo version as a live
  website release or create a second copy of the site here.
