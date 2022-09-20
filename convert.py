from bs4 import BeautifulSoup
import re
import sys
import markdownify
import dateutil.parser
import packaging.version

mdowndata = {}

releases = [
    ['20 Sep 2022', '15.0.1', ['https://discourse.llvm.org/t/llvm-15-0-1-released/65380'],[]],
    ['6 Sep 2022',  '15.0.0', ['llvm', 'clang', 'lld', 'clang-extra', 'libc++', 'polly', 'flang'], ['llvm', 'clang', 'lld', 'clang-extra', 'libc++', 'polly', 'flang']],
    ['24 Jun 2022', '14.0.6', ['https://discourse.llvm.org/t/llvm-14-0-6-release/63431'],[]],
    ['10 Jun 2022', '14.0.5', ['https://discourse.llvm.org/t/llvm-14-0-5-release/63118'],[]],
    ['24 May 2022', '14.0.4', ['https://discourse.llvm.org/t/llvm-14-0-4-release/62751'],[]],
    ['29 Apr 2022', '14.0.3', ['https://discourse.llvm.org/t/llvm-14-0-3-release/62133'],[]],
    ['26 Apr 2022', '14.0.2', ['https://discourse.llvm.org/t/llvm-14-0-2-release/62065'],[]],
    ['12 Apr 2022', '14.0.1', ['https://discourse.llvm.org/t/llvm-14-0-1-release/61700'],[]],
    ['25 Mar 2022', '14.0.0', ['llvm', 'clang', 'lld', 'clang-extra', 'libc++', 'polly', 'flang'], ['llvm', 'clang', 'lld', 'clang-extra', 'libc++', 'polly', 'flang']],
    ['7 Feb 2022', '13.0.1', ['llvm', 'clang', 'lld', 'clang-extra', 'libc++', 'polly', 'flang'], ['llvm', 'clang', 'lld', 'clang-extra', 'libc++', 'polly', 'flang']],
    ['4 Oct 2021', '13.0.0', ['llvm', 'clang', 'lld', 'clang-extra', 'libc++', 'polly', 'flang'], ['llvm', 'clang', 'lld', 'clang-extra', 'libc++', 'polly', 'flang']],
    ['8 July 2021', '12.0.1', ['llvm', 'clang', 'lld', 'clang-extra', 'libc++', 'polly', 'flang'], ['llvm', 'clang', 'lld', 'clang-extra', 'libc++', 'polly', 'flang']],
    ['14 Apr 2021', '12.0.0', ['llvm', 'clang', 'lld', 'clang-extra', 'libc++', 'polly', 'flang'], ['llvm', 'clang', 'lld', 'clang-extra', 'libc++', 'polly', 'flang']],
    ['25 Feb 2021', '11.1.0', ['llvm', 'clang', 'lld', 'clang-extra', 'libc++', 'polly', 'flang'], ['llvm', 'clang', 'lld', 'clang-extra', 'libc++', 'polly', 'flang']],
    ['14 Jan 2021', '11.0.1', ['llvm', 'clang', 'lld', 'clang-extra', 'libc++', 'polly', 'flang'], ['llvm', 'clang', 'lld', 'clang-extra', 'libc++', 'polly', 'flang']],
    ['12 Oct 2020', '11.0.0', ['llvm', 'clang', 'lld', 'clang-extra', 'libc++', 'polly', 'flang'], ['llvm', 'clang', 'lld', 'clang-extra', 'libc++', 'polly', 'flang']],
    ['6 Aug 2020', '10.0.1', ['llvm', 'clang', 'lld', 'clang-extra', 'libc++'], ['llvm', 'clang', 'lld', 'clang-extra', 'libc++', 'polly']],
    ['24 Mar 2020', '10.0.0', ['llvm', 'clang', 'lld', 'clang-extra', 'libc++'], ['llvm', 'clang', 'lld', 'clang-extra', 'libc++', 'polly']],
    ['20 Dec 2019', '9.0.1', ['llvm', 'clang', 'clang-extra', 'libc++'], ['llvm', 'clang', 'clang-extra', 'libc++']],
    ['19 Sep 2019', '9.0.0', ['llvm', 'clang', 'lld', 'clang-extra', 'libc++'], ['llvm', 'clang', 'lld', 'clang-extra', 'libc++']],
    ['19 Jul 2019', '8.0.1'],
    ['10 May 2019', '7.1.0', ['llvm', 'clang', 'clang-extra', 'libc++'], ['llvm', 'clang', 'clang-extra', 'libc++', 'polly']],
    ['20 Mar 2019', '8.0.0', ['llvm', 'clang', 'lld', 'clang-extra', 'libc++'], ['llvm', 'clang', 'lld', 'clang-extra', 'libc++', 'polly']],
    ['21 Dec 2018', '7.0.1'],
    ['19 Sep 2018', '7.0.0', ['llvm', 'clang', 'lld', 'clang-extra'], ['llvm', 'clang', 'lld', 'clang-extra', 'libc++', 'polly']],
    ['5 Jul 2018',  '6.0.1'],
    ['16 May 2018', '5.0.2'],
    ['8 Mar 2018',  '6.0.0'],
    ['21 Dec 2017', '5.0.1'],
    ['07 Sep 2017', '5.0.0'],
    ['04 Jul 2017', '4.0.1'],
    ['13 Mar 2017', '4.0.0'],
    ['23 Dec 2016', '3.9.1'],
    ['02 Sep 2016', '3.9.0'],
    ['11 Jul 2016', '3.8.1'],
    ['08 Mar 2016', '3.8.0'],
    ['05 Jan 2016', '3.7.1'],
    ['01 Sep 2015', '3.7.0'],
    ['16 Jul 2015', '3.6.2'],
    ['26 May 2015', '3.6.1'],
    ['27 Feb 2015', '3.6.0'],
    ['02 Apr 2015', '3.5.2'],
    ['20 Jan 2015', '3.5.1'],
    ['03 Sep 2014', '3.5.0'],
    ['19 Jun 2014', '3.4.2'],
    ['07 May 2014', '3.4.1'],
    ['02 Jan 2014', '3.4'],
    ['17 Jun 2013', '3.3'],
    ['20 Dec 2012', '3.2'],
    ['22 May 2012', '3.1'],
    ['01 Dec 2011', '3.0'],
    ['06 Apr 2011', '2.9'],
    ['05 Oct 2010', '2.8'],
    ['27 Apr 2010', '2.7'],
    ['23 Oct 2009', '2.6'],
    ['02 Mar 2009', '2.5'],
    ['09 Nov 2008', '2.4'],
    ['09 Jun 2008', '2.3'],
    ['11 Feb 2008', '2.2'],
    ['26 Sep 2007', '2.1'],
    ['23 May 2007', '2.0'],
    ['19 Nov 2006', '1.9'],
    ['09 Aug 2006', '1.8'],
    ['20 Apr 2006', '1.7'],
    ['08 Nov 2005', '1.6'],
    ['18 May 2005', '1.5'],
    ['09 Dec 2004', '1.4'],
    ['13 Aug 2004', '1.3'],
    ['19 Mar 2004', '1.2'],
    ['17 Dec 2003', '1.1'],
    ['24 Oct 2003', '1.0']
]

if __name__ == '__main__':
  with open("../www-releases/download.html", "r") as fp:
    data = fp.read()
    s = BeautifulSoup(data, "html.parser")

    for tbl in s.find_all("table", {"class": "rel_section"}):
      for ref in tbl.find("a"):
        match = re.match(r".*\s(\d+\.\d+[\.]?[\d]?)", ref)
        if match:
          version = match.group(1)

          div = tbl.find_next("div", {"class": "rel_boxtext"})
          data = markdownify.markdownify(str(div), strip=["p"])
          sd = re.sub(r"(\[[\sa-zA-Z\+\(\)\-\/\d\.\\_\*]+\])\((\d+\.[\da-zA-Z\/\.\+\-\_]+)\)", r"\g<1>(/\g<2>)", data)
          mdowndata[version] = sd




  for release in releases:
    date, version, releasenotes, docs = (None, None, None, None)
    if len(release) == 2:
      date, version = release
    elif len(release) == 4:
      date, version, releasenotes, docs = release
    else:
      print(release)
      sys.exit(1)

    dt = dateutil.parser.parse(date)
    vd = packaging.version.parse(version)

    github = ""
    if vd > packaging.version.parse("14.0.2"):
      github = "\ngithub: true"

    projects = ""
    if releasenotes:
      if "discourse" in releasenotes[0]:
        projects = f"\ndiscourse: {releasenotes[0]}"
      else:
        projects = f"\nprojects: {str(releasenotes)}"

    filedata = f"""
---
title: "{version}"
date: {dt.strftime('%Y-%m-%d')}
draft: true
layout: release{github}{projects}
---
"""

    if version in mdowndata:
      filedata += mdowndata[version]

    with open(f"content/releases/{version}.md", "w") as out:
      out.write(filedata)
