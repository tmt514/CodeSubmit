#!/usr/bin/env python3

import requests
import argparse
from bs4 import BeautifulSoup
import re

def main():
  parser = argparse.ArgumentParser(
    description='Fetch Codeforces sample tests')
  parser.add_argument('prob', type=str,
      help='Codeforces problem ID (Ex: 514A)')
  args = parser.parse_args()

  print("======= Fetching Samples [%s] =======" % args.prob)
  cid, pid = [re.search(r'(\d+)(\w+)', args.prob).group(x) for x in [1, 2]]
  url = "http://codeforces.com/problemset/problem/%s/%s" % (cid, pid)
  page = requests.get(url)
  if page.status_code != 200:
    print("Error on fetching the problem page.")
    return

  page = BeautifulSoup(page.text, 'lxml')
  samples = page.find_all("div", class_="sample-test")[0]
  samples = list(samples.find_all("div", recursive=False))
  for i in range(0, len(samples), 2):
    intext = "\n".join(samples[i].find_all("pre")[0].strings)
    outtext = "\n".join(samples[i+1].find_all("pre")[0].strings)
    infile = "sample-%s-%03d.in" % (args.prob, i//2)
    outfile = "sample-%s-%03d.ans" % (args.prob, i//2)
    with open(infile, "w") as f:
      f.write(intext + "\n")
    with open(outfile, "w") as f:
      f.write(outtext + "\n")
    print("created %s" % infile)
    print("created %s" % outfile)

  
if __name__ == "__main__":
  main()
