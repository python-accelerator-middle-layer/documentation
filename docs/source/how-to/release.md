# Release a new version on PyPI

1. Create a branch for a release
2. Provide a list of changes and release description in the merge request. Justify a version bump is necessary.
3. Tag the corresponding version.
4. Approve and merge the PR.
5. CI/CD will take care of PyPi release. (Make sure the version in CI/CD deployment pipeline matches the one you just tagged.)
