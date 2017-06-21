# CodeSubmit
A command line codeforces submitter for lazy people  
A command line codeforces fetching sample tests and run sample tests for super lazy people

## Usage
`./code_submit.py [username] [prob ID] [filename]`  
`./cf-fetch.py [prob ID]`  
`./cf-test.py [prob ID]`  
`./cf-new [prob ID]`  

or you can run `python3 install.py` so the scripts are installed into `~/.local/bin` directory, and use `cf-fetch`, `cf-test` and `cf-submit` as commands.

### cf-new

sample usage: `cf-new 514A`. This will create a directory called `514` and automatically open `514/514A.cpp` for you.

## Dependency
`RoboBrowser, requests, termcolor`
