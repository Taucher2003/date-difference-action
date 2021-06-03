# Date Difference Action

```yaml
name: Date Differences

on:
  workflow_dispatch:
  schedule:
    # Runs at 12am UTC
    - cron: "0 0 * * *"

jobs:
  update-readme:
    name: Update this repo's README
    runs-on: ubuntu-latest
    steps:
      - uses: Taucher2003/date-difference-action@master
        with:
          COMMIT_MESSAGE: ⏰ Updated time differences # Custom Commit Message
```