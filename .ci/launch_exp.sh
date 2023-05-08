#!/bin/bash
echo "CI_COMMIT_REF_PROTECTED: $CI_COMMIT_REF_PROTECTED"
curl  --request POST --header "PRIVATE-TOKEN: $PRIVATE_TOKEN" $CI_API_V4_URL/projects/$CI_PROJECT_ID/repository/commits/$CI_COMMIT_SHORT_SHA/discussions --data-urlencod "body=This message has been automatically generation by CI"
