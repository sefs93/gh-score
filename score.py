#!/usr/bin/env python3
import sys
import re
import json
import urllib.request

score_mapping = {
  "PullRequestEvent": 5,
  "PushEvent": 4,
  "IssueCommentEvent": 3,
  "CreateEvent": 2,
  "default": 1
}

def get_user_input():
  # It's better to use `argparse` for this matter, but that is definitely more than 40 min task
  gh_usernames = ["josevalim"]
  try:
    # Definitely doesn't seem like a best check, but at least something
    arg_num = len(sys.argv)
    if arg_num == 1:
      raise Exception("No input parameters")
    elif arg_num == 2:
      reg = re.compile('^[a-z0-9\,]+$')
      if not reg.match(sys.argv[1]):
        raise Exception("Input parameter is not valid")
      gh_usernames = sys.argv[1].split(',')
    else:
      raise Exception("Input parameter number is too big")
      
  except Exception as e:
    print(f"""[WARN] - {e}, failng back to defaults: {gh_usernames}.
              \rYou can speficy usernames as a comma separated list without spaces
              \re.g. ./score.py username1,username2,username3\n""")
  return gh_usernames

def gh_validate_username(gh_username):
  # This check is not actually needed in this implementation, as this regex is narrower
  # than the one in `get_user_input()`, but I'd anyway prefer to leave it here
  # in case we are doing some validation changes in `get_user_input()`
  reg = re.compile('^[a-z0-9]+$')
  if not reg.match(gh_username):
    raise Exception(f"{gh_username} is not valid GH username")

def gh_get_events(gh_username):
  with urllib.request.urlopen(f"https://api.github.com/users/{gh_username}/events") as response:
    raw_events = response.read()

  json_events = json.loads(raw_events)

  return json_events

def gh_calculate_score(json_events):
  gh_score = 0

  for event in json_events:
    if event["type"] in score_mapping:
      gh_score += score_mapping[event["type"]]
    else:
      gh_score += score_mapping["default"]

  return gh_score

def main():
  gh_usernames = get_user_input()
  
  for gh_username in gh_usernames:
    try:
      gh_validate_username(gh_username)
      gh_events = gh_get_events(gh_username)
    except Exception as e:
      # We can create different actions for different exceptions like 404/non-valid user input, etc
      print(f"[WARN] - {gh_username} : {e}")
    else:
      print(f"{gh_username} : {gh_calculate_score(gh_events)}")

if __name__ == "__main__":
    main()