#!/usr/bin/env python3
"""
Create CALMORA and MONEYSTACK quizzes in Tally.so
"""

import requests
import json
import uuid

TOKEN = open('/root/.openclaw/workspace/.credentials/tally-api.txt').read().strip()

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def create_calmora_quiz():
    """Create CALMORA Sleep Type Quiz"""
    
    print("🌙 Creating CALMORA quiz...")
    
    blocks = [
        # Title
        {
            "uuid": str(uuid.uuid4()),
            "type": "FORM_TITLE",
            "groupUuid": str(uuid.uuid4()),
            "groupType": "TEXT",
            "payload": {
                "title": "Can't Sleep? Take Our Free 2-Minute Sleep Assessment",
                "html": "<p>Discover your Sleep Type and get a personalized plan to fall asleep faster — backed by science.</p>"
            }
        },
        
        # Q1: Main Sleep Struggle
        {
            "uuid": str(uuid.uuid4()),
            "type": "MULTIPLE_CHOICE",
            "groupUuid": str(uuid.uuid4()),
            "groupType": "QUESTION",
            "payload": {
                "question": "What's your biggest struggle when trying to sleep?",
                "required": True,
                "options": [
                    {"text": "My mind races with thoughts and worries", "uuid": str(uuid.uuid4())},
                    {"text": "I fall asleep fine but wake up at 3-4 AM", "uuid": str(uuid.uuid4())},
                    {"text": "I sleep 7-8 hours but still wake up exhausted", "uuid": str(uuid.uuid4())},
                    {"text": "I feel anxious or restless when I try to sleep", "uuid": str(uuid.uuid4())},
                    {"text": "I'm naturally alert late at night (night owl)", "uuid": str(uuid.uuid4())}
                ]
            }
        },
        
        # Q2: Time to Fall Asleep
        {
            "uuid": str(uuid.uuid4()),
            "type": "MULTIPLE_CHOICE",
            "groupUuid": str(uuid.uuid4()),
            "groupType": "QUESTION",
            "payload": {
                "question": "On average, how long does it take you to fall asleep?",
                "required": True,
                "options": [
                    {"text": "Less than 15 minutes", "uuid": str(uuid.uuid4())},
                    {"text": "15-30 minutes", "uuid": str(uuid.uuid4())},
                    {"text": "30-60 minutes", "uuid": str(uuid.uuid4())},
                    {"text": "More than 1 hour", "uuid": str(uuid.uuid4())},
                    {"text": "I don't even know anymore", "uuid": str(uuid.uuid4())}
                ]
            }
        },
        
        # Q3: Sleep Environment
        {
            "uuid": str(uuid.uuid4()),
            "type": "MULTIPLE_CHOICE",
            "groupUuid": str(uuid.uuid4()),
            "groupType": "QUESTION",
            "payload": {
                "question": "Which best describes your bedroom at night?",
                "required": True,
                "options": [
                    {"text": "Dark, cool, and quiet", "uuid": str(uuid.uuid4())},
                    {"text": "Bright (street lights, devices)", "uuid": str(uuid.uuid4())},
                    {"text": "Noisy (traffic, neighbors, snoring)", "uuid": str(uuid.uuid4())},
                    {"text": "Too warm or too cold", "uuid": str(uuid.uuid4())},
                    {"text": "I use screens before bed", "uuid": str(uuid.uuid4())}
                ]
            }
        },
        
        # Q4: Pre-Sleep Routine
        {
            "uuid": str(uuid.uuid4()),
            "type": "MULTIPLE_CHOICE",
            "groupUuid": str(uuid.uuid4()),
            "groupType": "QUESTION",
            "payload": {
                "question": "What do you usually do in the hour before bed?",
                "required": True,
                "options": [
                    {"text": "Scroll social media or watch TV", "uuid": str(uuid.uuid4())},
                    {"text": "Work or check emails", "uuid": str(uuid.uuid4())},
                    {"text": "Read or meditate", "uuid": str(uuid.uuid4())},
                    {"text": "Exercise or eat heavy meals", "uuid": str(uuid.uuid4())},
                    {"text": "No consistent routine", "uuid": str(uuid.uuid4())}
                ]
            }
        },
        
        # Q5: Stress Level
        {
            "uuid": str(uuid.uuid4()),
            "type": "LINEAR_SCALE",
            "groupUuid": str(uuid.uuid4()),
            "groupType": "QUESTION",
            "payload": {
                "question": "How would you rate your stress/anxiety level right now?",
                "required": True,
                "min": 1,
                "max": 10,
                "minLabel": "Calm and relaxed",
                "maxLabel": "Extremely stressed"
            }
        },
        
        # Q6: Tried Solutions
        {
            "uuid": str(uuid.uuid4()),
            "type": "CHECKBOXES",
            "groupUuid": str(uuid.uuid4()),
            "groupType": "QUESTION",
            "payload": {
                "question": "What have you already tried to improve your sleep?",
                "required": False,
                "options": [
                    {"text": "Melatonin supplements", "uuid": str(uuid.uuid4())},
                    {"text": "Sleep apps or white noise", "uuid": str(uuid.uuid4())},
                    {"text": "Exercise during the day", "uuid": str(uuid.uuid4())},
                    {"text": "Meditation or breathing exercises", "uuid": str(uuid.uuid4())},
                    {"text": "Sleep medications (prescription)", "uuid": str(uuid.uuid4())},
                    {"text": "Nothing yet", "uuid": str(uuid.uuid4())}
                ]
            }
        },
        
        # Q7: Email Capture
        {
            "uuid": str(uuid.uuid4()),
            "type": "INPUT_EMAIL",
            "groupUuid": str(uuid.uuid4()),
            "groupType": "QUESTION",
            "payload": {
                "question": "Where should we send your personalized Sleep Reset Plan?",
                "placeholder": "your@email.com",
                "description": "We'll send you:\n✅ Your Sleep Type breakdown\n✅ Custom 7-day reset plan\n✅ Science-backed tips\n\nNo spam. Unsubscribe anytime.",
                "required": True
            }
        },
        
        # Thank You
        {
            "uuid": str(uuid.uuid4()),
            "type": "THANK_YOU_PAGE",
            "groupUuid": str(uuid.uuid4()),
            "groupType": "TEXT",
            "payload": {
                "title": "Check Your Email!",
                "html": "<p>Your personalized Sleep Type assessment is on the way.</p><p>Check your inbox in the next 5 minutes.</p>"
            }
        }
    ]
    
    data = {
        "status": "PUBLISHED",
        "name": "CALMORA Sleep Type Quiz",
        "blocks": blocks
    }
    
    response = requests.post(
        "https://api.tally.so/forms",
        headers=HEADERS,
        json=data
    )
    
    if response.status_code == 201:
        form = response.json()
        print(f"✅ CALMORA quiz created!")
        print(f"   ID: {form['id']}")
        print(f"   URL: https://tally.so/r/{form['id']}")
        return form
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return None


def create_moneystack_quiz():
    """Create MONEYSTACK Money Type Quiz"""
    
    print("\n💰 Creating MONEYSTACK quiz...")
    
    blocks = [
        # Title
        {
            "uuid": str(uuid.uuid4()),
            "type": "FORM_TITLE",
            "groupUuid": str(uuid.uuid4()),
            "groupType": "TEXT",
            "payload": {
                "title": "Are You Making These Money Mistakes?",
                "html": "<p>Take our 2-minute Money Type Quiz and discover the #1 thing holding you back financially.</p>"
            }
        },
        
        # Q1: Current Money Situation
        {
            "uuid": str(uuid.uuid4()),
            "type": "MULTIPLE_CHOICE",
            "groupUuid": str(uuid.uuid4()),
            "groupType": "QUESTION",
            "payload": {
                "question": "Where are you right now with money?",
                "required": True,
                "options": [
                    {"text": "Not investing at all (scared to start)", "uuid": str(uuid.uuid4())},
                    {"text": "Following Dave Ramsey / paying off debt", "uuid": str(uuid.uuid4())},
                    {"text": "Saving but not investing (keeping cash)", "uuid": str(uuid.uuid4())},
                    {"text": "Investing but chasing trends (FOMO)", "uuid": str(uuid.uuid4())},
                    {"text": "Already investing consistently (want to optimize)", "uuid": str(uuid.uuid4())}
                ]
            }
        },
        
        # Q2: Income Level
        {
            "uuid": str(uuid.uuid4()),
            "type": "MULTIPLE_CHOICE",
            "groupUuid": str(uuid.uuid4()),
            "groupType": "QUESTION",
            "payload": {
                "question": "What's your approximate annual income?",
                "required": True,
                "options": [
                    {"text": "Under $40K", "uuid": str(uuid.uuid4())},
                    {"text": "$40K - $75K", "uuid": str(uuid.uuid4())},
                    {"text": "$75K - $150K", "uuid": str(uuid.uuid4())},
                    {"text": "$150K - $300K", "uuid": str(uuid.uuid4())},
                    {"text": "Over $300K", "uuid": str(uuid.uuid4())}
                ]
            }
        },
        
        # Q3: Debt Situation
        {
            "uuid": str(uuid.uuid4()),
            "type": "MULTIPLE_CHOICE",
            "groupUuid": str(uuid.uuid4()),
            "groupType": "QUESTION",
            "payload": {
                "question": "How much debt do you have (excluding mortgage)?",
                "required": True,
                "options": [
                    {"text": "No debt", "uuid": str(uuid.uuid4())},
                    {"text": "Under $5K", "uuid": str(uuid.uuid4())},
                    {"text": "$5K - $20K", "uuid": str(uuid.uuid4())},
                    {"text": "$20K - $50K", "uuid": str(uuid.uuid4())},
                    {"text": "Over $50K", "uuid": str(uuid.uuid4())}
                ]
            }
        },
        
        # Q4: Emergency Fund
        {
            "uuid": str(uuid.uuid4()),
            "type": "MULTIPLE_CHOICE",
            "groupUuid": str(uuid.uuid4()),
            "groupType": "QUESTION",
            "payload": {
                "question": "How many months of expenses do you have saved?",
                "required": True,
                "options": [
                    {"text": "Less than 1 month", "uuid": str(uuid.uuid4())},
                    {"text": "1-3 months", "uuid": str(uuid.uuid4())},
                    {"text": "3-6 months", "uuid": str(uuid.uuid4())},
                    {"text": "6-12 months", "uuid": str(uuid.uuid4())},
                    {"text": "Over 12 months", "uuid": str(uuid.uuid4())}
                ]
            }
        },
        
        # Q5: Investment Knowledge
        {
            "uuid": str(uuid.uuid4()),
            "type": "LINEAR_SCALE",
            "groupUuid": str(uuid.uuid4()),
            "groupType": "QUESTION",
            "payload": {
                "question": "How confident are you about investing?",
                "required": True,
                "min": 1,
                "max": 10,
                "minLabel": "No idea where to start",
                "maxLabel": "I could teach others"
            }
        },
        
        # Q6: Biggest Money Fear
        {
            "uuid": str(uuid.uuid4()),
            "type": "MULTIPLE_CHOICE",
            "groupUuid": str(uuid.uuid4()),
            "groupType": "QUESTION",
            "payload": {
                "question": "What scares you most about money?",
                "required": True,
                "options": [
                    {"text": "Not having enough for retirement", "uuid": str(uuid.uuid4())},
                    {"text": "Losing money in the market", "uuid": str(uuid.uuid4())},
                    {"text": "Never getting out of debt", "uuid": str(uuid.uuid4())},
                    {"text": "Missing out on opportunities (FOMO)", "uuid": str(uuid.uuid4())},
                    {"text": "Not knowing if I'm doing it \"right\"", "uuid": str(uuid.uuid4())}
                ]
            }
        },
        
        # Q7: Email Capture
        {
            "uuid": str(uuid.uuid4()),
            "type": "INPUT_EMAIL",
            "groupUuid": str(uuid.uuid4()),
            "groupType": "QUESTION",
            "payload": {
                "question": "Where should we send your personalized Money Action Plan?",
                "placeholder": "your@email.com",
                "description": "We'll send you:\n✅ Your Money Type breakdown\n✅ Custom action plan for your situation\n✅ Resources to start immediately\n\nNo spam. Unsubscribe anytime.",
                "required": True
            }
        },
        
        # Thank You
        {
            "uuid": str(uuid.uuid4()),
            "type": "THANK_YOU_PAGE",
            "groupUuid": str(uuid.uuid4()),
            "groupType": "TEXT",
            "payload": {
                "title": "Check Your Email!",
                "html": "<p>Your personalized Money Type assessment is on the way.</p><p>Check your inbox in the next 5 minutes.</p>"
            }
        }
    ]
    
    data = {
        "status": "PUBLISHED",
        "name": "MONEYSTACK Money Type Quiz",
        "blocks": blocks
    }
    
    response = requests.post(
        "https://api.tally.so/forms",
        headers=HEADERS,
        json=data
    )
    
    if response.status_code == 201:
        form = response.json()
        print(f"✅ MONEYSTACK quiz created!")
        print(f"   ID: {form['id']}")
        print(f"   URL: https://tally.so/r/{form['id']}")
        return form
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return None


if __name__ == '__main__':
    calmora_form = create_calmora_quiz()
    moneystack_form = create_moneystack_quiz()
    
    print("\n" + "="*60)
    print("✅ BOTH QUIZZES CREATED")
    print("="*60)
    
    if calmora_form:
        print(f"\n🌙 CALMORA: https://tally.so/r/{calmora_form['id']}")
    
    if moneystack_form:
        print(f"💰 MONEYSTACK: https://tally.so/r/{moneystack_form['id']}")
    
    # Save URLs
    quiz_data = {
        "calmora": {
            "id": calmora_form['id'] if calmora_form else None,
            "url": f"https://tally.so/r/{calmora_form['id']}" if calmora_form else None
        },
        "moneystack": {
            "id": moneystack_form['id'] if moneystack_form else None,
            "url": f"https://tally.so/r/{moneystack_form['id']}" if moneystack_form else None
        }
    }
    
    with open('/root/.openclaw/workspace/quiz-urls.json', 'w') as f:
        json.dump(quiz_data, f, indent=2)
    
    print(f"\n💾 Quiz URLs saved to: quiz-urls.json")
