#!/usr/bin/env python3

import requests
import argparse
import re
import os

def main():
  parser = argparse.ArgumentParser(
    description='Test Codeforces sample tests')
  parser.add_argument('prob', type=str,
      help='Codeforces problem ID (Ex: 514A)')
  args = parser.parse_args()

  if os.path.exists("sample-%s-000.in" % args.prob) == False:
    os.system("cf-fetch %s" % args.prob)

  if os.path.exists(args.prob) == False:
    print("Please compile your code first!")
    return

  cid, pid = [re.search(r'(\d+)(\w+)', args.prob).group(x) for x in [1, 2]]
  
  i = 0
  while os.path.exists("sample-%03d.in" % i):
    infile = "sample-%s-%03d.in" % (args.prob, i)
    userout = "sample-%s-%03d.out" % (args.prob, i)
    outfile = "sample-%s-%03d.ans" % (args.prob, i)
    print("======= Sample #%d =======" % i)
    os.system("./%s < %s > %s", args.prob, infilfe, userout)
    os.system("cat %s", userout)
    os.system("cat %s", outfile)
    i += 1
  
  
if __name__ == "__main__":
  main()
