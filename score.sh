#!/bin/bash
TOTAL_SCORE=0
while read -r line
do
    EVENT_SCORE=1
    case $line in

        PullRequestEvent)
            EVENT_SCORE=5
            ;;

        PushEvent)
            EVENT_SCORE=4
            ;;

        IssueCommentEvent)
            EVENT_SCORE=3
            ;;

        CreateEvent)
            EVENT_SCORE=2
            ;;

    esac
    ((TOTAL_SCORE+=EVENT_SCORE))
done < <(curl -s https://api.github.com/users/josevalim/events | jq -r .[].type)
echo $TOTAL_SCORE
