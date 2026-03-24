#!/bin/bash

# Generate UUIDs for blocks
generate_uuid() {
  cat /proc/sys/kernel/random/uuid
}

# Generate unique UUIDs
Q1_TITLE_UUID=$(generate_uuid)
Q1_GROUP_UUID=$(generate_uuid)
Q1_OPT1_UUID=$(generate_uuid)
Q1_OPT2_UUID=$(generate_uuid)
Q1_OPT3_UUID=$(generate_uuid)
Q1_OPT4_UUID=$(generate_uuid)
Q1_OPT5_UUID=$(generate_uuid)

Q2_TITLE_UUID=$(generate_uuid)
Q2_GROUP_UUID=$(generate_uuid)
Q2_OPT1_UUID=$(generate_uuid)
Q2_OPT2_UUID=$(generate_uuid)
Q2_OPT3_UUID=$(generate_uuid)
Q2_OPT4_UUID=$(generate_uuid)
Q2_OPT5_UUID=$(generate_uuid)

Q3_TITLE_UUID=$(generate_uuid)
Q3_DESC_UUID=$(generate_uuid)
Q3_DESC_GROUP_UUID=$(generate_uuid)
Q3_GROUP_UUID=$(generate_uuid)
Q3_INPUT_UUID=$(generate_uuid)

# Update the form with proper structure
curl -X PATCH 'https://api.tally.so/forms/44jMAo' \
  -H 'Authorization: Bearer tly-mS95xU2YkVkiwVslE5C1DebC3BUbC2k8' \
  -H 'Content-Type: application/json' \
  -d '{
    "status": "PUBLISHED",
    "blocks": [
      {
        "uuid": "9df27aac-81ce-4d71-90ad-e5ca6cb2e183",
        "type": "FORM_TITLE",
        "groupUuid": "999a3a87-7480-4323-98f4-0458eb35985a",
        "groupType": "TEXT",
        "payload": {
          "title": "Can'\''t Sleep? Take Our Free 2-Minute Sleep Assessment",
          "html": "Can'\''t Sleep? Take Our Free 2-Minute Sleep Assessment"
        }
      },
      {
        "uuid": "'$Q1_TITLE_UUID'",
        "type": "TITLE",
        "groupUuid": "'$Q1_GROUP_UUID'",
        "groupType": "QUESTION",
        "payload": {
          "html": "What'\''s your biggest struggle when trying to sleep?"
        }
      },
      {
        "uuid": "'$Q1_OPT1_UUID'",
        "type": "MULTIPLE_CHOICE_OPTION",
        "groupUuid": "'$Q1_GROUP_UUID'",
        "groupType": "MULTIPLE_CHOICE",
        "payload": {
          "index": 0,
          "text": "My mind races with thoughts and worries",
          "isFirst": true,
          "isLast": false
        }
      },
      {
        "uuid": "'$Q1_OPT2_UUID'",
        "type": "MULTIPLE_CHOICE_OPTION",
        "groupUuid": "'$Q1_GROUP_UUID'",
        "groupType": "MULTIPLE_CHOICE",
        "payload": {
          "index": 1,
          "text": "I fall asleep fine but wake up at 3-4 AM",
          "isFirst": false,
          "isLast": false
        }
      },
      {
        "uuid": "'$Q1_OPT3_UUID'",
        "type": "MULTIPLE_CHOICE_OPTION",
        "groupUuid": "'$Q1_GROUP_UUID'",
        "groupType": "MULTIPLE_CHOICE",
        "payload": {
          "index": 2,
          "text": "I sleep 7-8 hours but still wake up exhausted",
          "isFirst": false,
          "isLast": false
        }
      },
      {
        "uuid": "'$Q1_OPT4_UUID'",
        "type": "MULTIPLE_CHOICE_OPTION",
        "groupUuid": "'$Q1_GROUP_UUID'",
        "groupType": "MULTIPLE_CHOICE",
        "payload": {
          "index": 3,
          "text": "I feel anxious or restless when I try to sleep",
          "isFirst": false,
          "isLast": false
        }
      },
      {
        "uuid": "'$Q1_OPT5_UUID'",
        "type": "MULTIPLE_CHOICE_OPTION",
        "groupUuid": "'$Q1_GROUP_UUID'",
        "groupType": "MULTIPLE_CHOICE",
        "payload": {
          "index": 4,
          "text": "I'\''m naturally alert late at night (night owl)",
          "isFirst": false,
          "isLast": true
        }
      },
      {
        "uuid": "'$Q2_TITLE_UUID'",
        "type": "TITLE",
        "groupUuid": "'$Q2_GROUP_UUID'",
        "groupType": "QUESTION",
        "payload": {
          "html": "On average, how long does it take you to fall asleep?"
        }
      },
      {
        "uuid": "'$Q2_OPT1_UUID'",
        "type": "MULTIPLE_CHOICE_OPTION",
        "groupUuid": "'$Q2_GROUP_UUID'",
        "groupType": "MULTIPLE_CHOICE",
        "payload": {
          "index": 0,
          "text": "Less than 15 minutes",
          "isFirst": true,
          "isLast": false
        }
      },
      {
        "uuid": "'$Q2_OPT2_UUID'",
        "type": "MULTIPLE_CHOICE_OPTION",
        "groupUuid": "'$Q2_GROUP_UUID'",
        "groupType": "MULTIPLE_CHOICE",
        "payload": {
          "index": 1,
          "text": "15-30 minutes",
          "isFirst": false,
          "isLast": false
        }
      },
      {
        "uuid": "'$Q2_OPT3_UUID'",
        "type": "MULTIPLE_CHOICE_OPTION",
        "groupUuid": "'$Q2_GROUP_UUID'",
        "groupType": "MULTIPLE_CHOICE",
        "payload": {
          "index": 2,
          "text": "30-60 minutes",
          "isFirst": false,
          "isLast": false
        }
      },
      {
        "uuid": "'$Q2_OPT4_UUID'",
        "type": "MULTIPLE_CHOICE_OPTION",
        "groupUuid": "'$Q2_GROUP_UUID'",
        "groupType": "MULTIPLE_CHOICE",
        "payload": {
          "index": 3,
          "text": "More than 1 hour",
          "isFirst": false,
          "isLast": false
        }
      },
      {
        "uuid": "'$Q2_OPT5_UUID'",
        "type": "MULTIPLE_CHOICE_OPTION",
        "groupUuid": "'$Q2_GROUP_UUID'",
        "groupType": "MULTIPLE_CHOICE",
        "payload": {
          "index": 4,
          "text": "I don'\''t even know anymore",
          "isFirst": false,
          "isLast": true
        }
      },
      {
        "uuid": "'$Q3_TITLE_UUID'",
        "type": "TITLE",
        "groupUuid": "'$Q3_GROUP_UUID'",
        "groupType": "QUESTION",
        "payload": {
          "html": "Where should we send your personalized Sleep Reset Plan?"
        }
      },
      {
        "uuid": "'$Q3_DESC_UUID'",
        "type": "TEXT",
        "groupUuid": "'$Q3_DESC_GROUP_UUID'",
        "groupType": "TEXT",
        "payload": {
          "html": "We'\''ll send you: ✅ Your Sleep Type breakdown ✅ Custom 7-day reset plan ✅ Science-backed tips. No spam."
        }
      },
      {
        "uuid": "'$Q3_INPUT_UUID'",
        "type": "INPUT_EMAIL",
        "groupUuid": "'$Q3_GROUP_UUID'",
        "groupType": "QUESTION",
        "payload": {
          "isRequired": true,
          "placeholder": "your@email.com"
        }
      }
    ]
  }'
