#  Copyright 2021 Niklas van Schrick
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import re
import os
import base64
import sys
from datetime import datetime
from dateutil.relativedelta import relativedelta
from github import Github, GithubException

REGEX = r'(?P<full>(<!--timespan:start' \
        r'\((?P<format>[%a-zA-Z-., \/\\\\]+)\)' \
        r'((\((?P<date>[0-9]{4}[- /.](0[1-9]|1[0-2])[- /.](0[1-9]|[12][0-9]|3[01]))\))' \
        r'|(\(env:(?P<id>[0-9]+)\)))' \
        r'-->(?P<replace>[\S ]*)<!--timespan:end-->))'

repository = os.getenv('INPUT_REPOSITORY')
github_token = os.getenv('INPUT_GITHUB_TOKEN')
commit_message = os.getenv("INPUT_COMMIT_MESSAGE")


def generate_readme_content(old_content: str) -> str:
    content = old_content
    matches = re.findall(REGEX, old_content)
    for match in matches:
        replaced = replace(match[0])
        content = content.replace(match[0], replaced, 1)

    return content


def replace(input: str) -> str:
    reg = re.match(REGEX, input)
    format = reg.group("format")
    if reg.group("date") is not None:
        result = calculate(format, reg.group("date"), input, reg)

    else:
        result = calculate(format, os.getenv(reg.group("id")), input, reg)

    return result


def calculate(format: str, date_str: str, full_string: str, reg: re) -> str:
    result = format
    date = datetime.strptime(date_str, "%Y-%m-%d")

    if format.__contains__('%y'):
        result = re.sub('%y', str(calculate_years(date, datetime.now())), result)

    if format.__contains__('%m'):
        result = re.sub('%m', str(calculate_months(date, datetime.now(), format.__contains__('%y'))), result)

    if format.__contains__('%d'):
        days = str(calculate_days(date, datetime.now(), format.__contains__('%y'), format.__contains__('%m')))
        result = re.sub('%d', days, result)

    if full_string.__contains__('env:'):
        target_day = 'env:' + reg.group('id')
    else:
        target_day = reg.group('date')
    final_result = "<!--timespan:start(" + reg.group('format') + ")(" + target_day + ")-->" + result + "<!--timespan:end-->"
    # return re.sub(reg.group('replace'), result, full_string)
    return final_result


def calculate_days(start: datetime, end: datetime, years: bool, months: bool) -> int:
    delta = end - start
    result = delta.days
    if years:
        """TODO"""
        result = result

    if months:
        """TODO"""
        result = relativedelta(end, start).days

    return result


def calculate_months(start: datetime, end: datetime, years: bool) -> int:
    delta = relativedelta(end, start)
    if years:
        return delta.months
    else:
        return delta.months + (delta.years * 12)


def calculate_years(start: datetime, end: datetime) -> int:
    return relativedelta(end, start).years


def decode_readme(data: str) -> str:
    """Decode the contents of old readme"""
    decoded_bytes = base64.b64decode(data)
    return str(decoded_bytes, 'utf-8')


if __name__ == '__main__':
    github = Github(github_token)
    try:
        repo = github.get_repo(repository)
    except GithubException:
        print("Authentication Error. This workflow requires a Github token.")
        sys.exit(1)
    contents = repo.get_readme()
    readme_content = decode_readme(contents.content)
    replaced_content = generate_readme_content(readme_content)
    if replaced_content != readme_content:
        repo.update_file(path=contents.path, message=commit_message,
                         content=replaced_content, sha=contents.sha)
