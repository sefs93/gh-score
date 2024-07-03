#!/usr/bin/env python3
import json
import urllib.request

score_mapping = {
  "PullRequestEvent": 5,
  "PushEvent": 4,
  "IssueCommentEvent": 3,
  "CreateEvent": 2,
  "default": 1
}

gh_score = 0

with urllib.request.urlopen('https://api.github.com/users/josevalim/events') as response:
   raw_events = response.read()

json_events = json.loads(raw_events)

for event in json_events:
    if event["type"] in score_mapping:
        gh_score += score_mapping[event["type"]]
    else:
        gh_score += score_mapping["default"]

print(gh_score)