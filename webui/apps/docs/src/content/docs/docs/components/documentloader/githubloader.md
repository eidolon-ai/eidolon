---
title: GitHubLoader
description: Description of GitHubLoader component
---
*Loads files from a GitHub repository. Note that you will likely hit rate limits on all but the smallest repositories
unless a TOKEN is provided*

## Properties

- **`owner`** *(string)*
- **`repo`** *(string)*
- **`client_args`** *(object)*: Default: `{}`.
- **`root_path`**: Default: `null`.
  - **Any of**
    - *string*
    - *null*
- **`pattern`**: Default: `"**/*"`.
  - **Any of**
    - *string*
    - *array*
      - **Items** *(string)*
- **`exclude`**: Default: `[]`.
  - **Any of**
    - *string*
    - *array*
      - **Items** *(string)*
- **`token`**: Github token, can also be set via envar 'GITHUB_TOKEN'.
  - **Any of**
    - *string*
    - *null*
