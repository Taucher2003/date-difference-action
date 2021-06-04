# Date Difference Action

Date Difference Action calculates the differences between a given date and today.
As example, this project has been finished <!--timespan:start(%d)(2021-06-04)--><!--timespan:end--> days ago.

You can add these dynamic timespans with `<!--timespan:start(%d)(2021-06-04)--><!--timespan:end-->`.

| Comment Part         | Explanation                       |
|----------------------|-----------------------------------|
| <!--timespan:start   | Marks the beginning of a timespan |
| (%d)                 | declares the format               |
| (2021-06-04)         | defines the date                  |
| -->                  | End of beginning comment          |
| \<!--timespan:end--> | Marks the end of a timespan       |

## Action Setup

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
          COMMIT_MESSAGE: "⏰ Updated time differences" # Custom Commit Message
          REPOSITORY: "Taucher2003/date-difference-action" # Custom Repository
          GITHUB_TOKEN: "some access token" # Custom Access Token
```

The parameters `COMMIT_MESSAGE`, `REPOSITORY` and `GITHUB_TOKEN` are optional.

If you don't want to expose the exact date, you can use environment variables to set the date.
With that, you will use `<!--timespan:start(%d)(env:1)--><!--timespan:end-->` in the README, and the following action setup
<details>
<summary>Action with environment</summary>

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
        env:
          1: ${{ secrets.DATE_1 }}
```
</details>
