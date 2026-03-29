#!/usr/bin/env python3
"""
Create Health Hacks Wellness Quiz in Tally.so
"""

import requests
import json
import uuid

TOKEN = open('/root/.openclaw/workspace/.credentials/tally-api.txt').read().strip()

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def create_healthhacks_quiz():
    """Create Health Hacks Wellness Quiz"""
    
    print("🏥 Creating HEALTH HACKS quiz...")
    
    blocks = [
        # Title
        {
            "uuid": str(uuid.uuid4()),
            "type": "FORM_TITLE",
            "groupUuid": str(uuid.uuid4()),
            "groupType": "TEXT",
            "payload": {
                "title": "What's Your Biggest Health Weak Spot?",
                "html": "<p>Take this 2-minute wellness assessment and get a personalized plan with science-backed fixes you can start today.</p>"
            }
        },
        
        # Q1: Primary Health Struggle
        {
            "uuid": str(uuid.uuid4()),
            "type": "MULTIPLE_CHOICE",
            "groupUuid": str(uuid.uuid4()),
            "groupType": "QUESTION",
            "payload": {
                "question": "If you could fix ONE thing about your health right now, what would it be?",
                "required": True,
                "options": [
                    {"text": "Low energy / Always tired", "uuid": str(uuid.uuid4())},
                    {"text": "Chronic pain (back, neck, joints)", "uuid": str(uuid.uuid4())},
                    {"text": "Poor sleep / Insomnia", "uuid": str(uuid.uuid4())},
                    {"text": "Stress / Anxiety / Burnout", "uuid": str(uuid.uuid4())},
                    {"text": "Digestive issues / Gut health", "uuid": str(uuid.uuid4())},
                    {"text": "Brain fog / Focus problems", "uuid": str(uuid.uuid4())}
                ]
            }
        },
        
        # Q2: Energy Levels
        {
            "uuid": str(uuid.uuid4()),
            "type": "MULTIPLE_CHOICE",
            "groupUuid": str(uuid.uuid4()),
            "groupType": "QUESTION",
            "payload": {
                "question": "How would you describe your energy throughout the day?",
                "required": True,
                "options": [
                    {"text": "Consistent and good all day", "uuid": str(uuid.uuid4())},
                    {"text": "Strong morning, crash after lunch", "uuid": str(uuid.uuid4())},
                    {"text": "Exhausted all day, wired at night", "uuid": str(uuid.uuid4())},
                    {"text": "Ups and downs (unpredictable)", "uuid": str(uuid.uuid4())},
                    {"text": "Constantly low, even after coffee", "uuid": str(uuid.uuid4())}
                ]
            }
        },
        
        # Q3: Pain (multi-select)
        {
            "uuid": str(uuid.uuid4()),
            "type": "CHECKBOXES",
            "groupUuid": str(uuid.uuid4()),
            "groupType": "QUESTION",
            "payload": {
                "question": "Do you experience any of these regularly? (Select all that apply)",
                "required": False,
                "options": [
                    {"text": "Lower back pain", "uuid": str(uuid.uuid4())},
                    {"text": "Neck or shoulder tension", "uuid": str(uuid.uuid4())},
                    {"text": "Headaches or migraines", "uuid": str(uuid.uuid4())},
                    {"text": "Joint pain (knees, hips, wrists)", "uuid": str(uuid.uuid4())},
                    {"text": "Muscle tension or soreness", "uuid": str(uuid.uuid4())},
                    {"text": "None of the above", "uuid": str(uuid.uuid4())}
                ]
            }
        },
        
        # Q4: Sleep Quality
        {
            "uuid": str(uuid.uuid4()),
            "type": "MULTIPLE_CHOICE",
            "groupUuid": str(uuid.uuid4()),
            "groupType": "QUESTION",
            "payload": {
                "question": "How often do you wake up feeling truly rested?",
                "required": True,
                "options": [
                    {"text": "Almost every day (80%+)", "uuid": str(uuid.uuid4())},
                    {"text": "A few times a week", "uuid": str(uuid.uuid4())},
                    {"text": "Rarely (once a week or less)", "uuid": str(uuid.uuid4())},
                    {"text": "Never / Can't remember the last time", "uuid": str(uuid.uuid4())},
                    {"text": "I don't sleep enough to know", "uuid": str(uuid.uuid4())}
                ]
            }
        },
        
        # Q5: Stress Level
        {
            "uuid": str(uuid.uuid4()),
            "type": "MULTIPLE_CHOICE",
            "groupUuid": str(uuid.uuid4()),
            "groupType": "QUESTION",
            "payload": {
                "question": "How often do you feel stressed, anxious, or overwhelmed?",
                "required": True,
                "options": [
                    {"text": "Rarely (stress is manageable)", "uuid": str(uuid.uuid4())},
                    {"text": "A few times a week", "uuid": str(uuid.uuid4())},
                    {"text": "Most days", "uuid": str(uuid.uuid4())},
                    {"text": "Constantly / It's my baseline", "uuid": str(uuid.uuid4())},
                    {"text": "Only in specific situations (work, family)", "uuid": str(uuid.uuid4())}
                ]
            }
        },
        
        # Q6: Daily Habits (multi-select)
        {
            "uuid": str(uuid.uuid4()),
            "type": "CHECKBOXES",
            "groupUuid": str(uuid.uuid4()),
            "groupType": "QUESTION",
            "payload": {
                "question": "Which of these describes your typical day? (Select all)",
                "required": False,
                "options": [
                    {"text": "I sit for 6+ hours (desk job)", "uuid": str(uuid.uuid4())},
                    {"text": "I skip meals or eat irregularly", "uuid": str(uuid.uuid4())},
                    {"text": "I drink 3+ cups of coffee", "uuid": str(uuid.uuid4())},
                    {"text": "I rarely exercise (less than 1x/week)", "uuid": str(uuid.uuid4())},
                    {"text": "I check my phone first thing in the morning", "uuid": str(uuid.uuid4())},
                    {"text": "I don't drink much water", "uuid": str(uuid.uuid4())}
                ]
            }
        },
        
        # Q7: What Tried (multi-select)
        {
            "uuid": str(uuid.uuid4()),
            "type": "CHECKBOXES",
            "groupUuid": str(uuid.uuid4()),
            "groupType": "QUESTION",
            "payload": {
                "question": "What have you already tried to improve your health?",
                "required": False,
                "options": [
                    {"text": "Vitamins or supplements", "uuid": str(uuid.uuid4())},
                    {"text": "Exercise routine (gym, yoga, walking)", "uuid": str(uuid.uuid4())},
                    {"text": "Meditation or mindfulness apps", "uuid": str(uuid.uuid4())},
                    {"text": "Diet changes (keto, vegan, etc.)", "uuid": str(uuid.uuid4())},
                    {"text": "Therapy or coaching", "uuid": str(uuid.uuid4())},
                    {"text": "Nothing consistent yet", "uuid": str(uuid.uuid4())}
                ]
            }
        },
        
        # Q8: Email Capture
        {
            "uuid": str(uuid.uuid4()),
            "type": "INPUT_EMAIL",
            "groupUuid": str(uuid.uuid4()),
            "groupType": "QUESTION",
            "payload": {
                "question": "Where should we send your Personalized 7-Day Health Reset Plan?",
                "placeholder": "your@email.com",
                "description": "You'll get:\n✅ Your Wellness Profile breakdown\n✅ Custom 7-day action plan (15 min/day)\n✅ Science-backed quick fixes\n\nNo spam. Unsubscribe anytime.",
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
                "title": "Check Your Email! 📧",
                "html": "<p>Your personalized Health Reset Plan is on its way.</p><p>While you wait, subscribe on YouTube for weekly health hacks:</p><p>→ <a href='https://youtube.com/@HealthHacks'>youtube.com/@HealthHacks</a></p>"
            }
        }
    ]
    
    data = {
        "status": "PUBLISHED",
        "name": "What's Your Biggest Health Weak Spot?",
        "blocks": blocks
    }
    
    response = requests.post(
        "https://api.tally.so/forms",
        headers=HEADERS,
        json=data
    )
    
    if response.status_code == 201:
        form = response.json()
        print(f"✅ HEALTH HACKS quiz created!")
        print(f"\n📋 Form ID: {form['id']}")
        print(f"🔗 Quiz URL: https://tally.so/r/{form['id']}")
        print(f"\n📊 Form name: {form['name']}")
        print(f"📅 Created: {form['createdAt']}")
        
        # Save to quiz-urls.json
        try:
            with open('/root/.openclaw/workspace/quiz-urls.json', 'r') as f:
                quiz_data = json.load(f)
        except:
            quiz_data = {}
        
        quiz_data['healthhacks'] = {
            "id": form['id'],
            "url": f"https://tally.so/r/{form['id']}",
            "created": form['createdAt']
        }
        
        with open('/root/.openclaw/workspace/quiz-urls.json', 'w') as f:
            json.dump(quiz_data, f, indent=2)
        
        print(f"\n💾 Quiz URL saved to: quiz-urls.json")
        
        return form
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return None

if __name__ == "__main__":
    create_healthhacks_quiz()
