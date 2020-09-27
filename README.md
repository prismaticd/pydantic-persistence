# prismatic-package
This is a Python Package testing ground with Github Actions

![Tests](https://github.com/prismaticd/prismatic-package/workflows/Tests/badge.svg?branch=master)
![Code Coverage](https://img.shields.io/badge/code%20coverage-100%25-success.svg)


## Publish new release

locally run `bump2version patch ` or `bump2version minor` or `bump2version major`

This will update pyproject.toml and the __version__ in __init__.py will commit with message
`bump version from {old_version} to {new_version}` and tag with `v{new_version}`

You then need to do `git push --tags` or normal push if you have set `git config --global push.followTags true`

A few seconds later a Draft release will be visible in the releases tab on github, edit the content and press publish,
this will automatically publish the release on pypi
