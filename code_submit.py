#! /usr/bin/env python3

from getpass import getpass
import argparse
from robobrowser import RoboBrowser
import requests
import json
import time
from termcolor import colored
from bs4 import BeautifulSoup

def get_submission_data(user):
    req = requests.get('http://codeforces.com/api/user.status?'
                       'handle={}&from=1&count=1'.format(user))
    content = req.content.decode()
    js = json.loads(content)
    if 'status' not in js or js['status'] != 'OK':
        raise ConnectionError('Codeforces BOOM!')
    res = js['result'][0]
    id_, verdict = res['id'], res['verdict']
    testno = res['passedTestCount']
    testtime = res['timeConsumedMillis']
    testmem = res['memoryConsumedBytes']
    return id_, verdict, testno, testtime, testmem


def shout_verdict(id_, verdict, testno, testtime, testmem):
    if verdict == "TESTING":
        req = requests.get('http://codeforces.com/problemset/status')
        page = req.text
        page = BeautifulSoup(page, "lxml")
        sub = list(page.find_all(attrs={"data-submission-id" : id_}))
        if len(sub) == 0:
          print("[%s] Running (too many submissions!)" % (id_))
        else:
          verdict = "".join(sub[0].find_all("span", class_="submissionVerdictWrapper")[0].strings)
          print("[%s] %s" % (id_, verdict))
        # Codeforces API does not provide live update
        # print("[%s] Running on test %d" % (id_, testno+1))
    elif verdict == "OK":
        v_ = colored(verdict, 'green')
        print("[%s] %s (time=%d ms, memory=%d KB)" % (id_, v_, testtime, testmem))
    else:
        v_ = colored(verdict, 'red')
        print("[%s] %s on test %d" % (id_, v_, testno+1))


def main():

    parser = argparse.ArgumentParser(
        description='Submit codeforces in command line')
    parser.add_argument('user', type=str,
                        help='Your codeforces ID')
    parser.add_argument('prob', type=str,
                        help='Codeforces problem ID (Ex: 33C)')
    parser.add_argument('file', type=str,
                        help='path to the source code')
    args = parser.parse_args()

    user_name = args.user
    last_id, *_ = get_submission_data(user_name)

    passwd = getpass()

    browser = RoboBrowser()
    browser.open('http://codeforces.com/enter')

    enter_form = browser.get_form('enterForm')
    enter_form['handle'] = user_name
    enter_form['password'] = passwd
    browser.submit_form(enter_form)

    try:
        checks = list(map(lambda x: x.getText()[1:].strip(),
            browser.select('div.caption.titled')))
        if user_name not in checks:
            print("Login Failed.. probably because you've typed"
                  "a wrong password.")
            return
    except Exception as e:
        print("Login Failed.. probably because you've typed"
              "a wrong password.")
        return 

    browser.open('http://codeforces.com/problemset/submit')
    submit_form = browser.get_form(class_='submit-form')
    submit_form['submittedProblemCode'] = args.prob
    submit_form['sourceFile'] = args.file
    browser.submit_form(submit_form)

    if browser.url[-6:] != 'status':
        print('Your submission has failed, probably '
              'because you have submit the same file before.')
        return

    print('Submitted, wait for result...')
    while True:
        id_, verdict, *blah = get_submission_data(user_name)
        if id_ != last_id:
            shout_verdict(id_, verdict, *blah)
        if id_ != last_id and verdict != 'TESTING':
            # print('Verdict = {}'.format(verdict))
            break
        time.sleep(3)

if __name__ == '__main__':
    main()
