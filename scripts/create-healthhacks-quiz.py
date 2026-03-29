#!/usr/bin/env python3
"""
Create Health Hacks Wellness Quiz in Tally
"""
import requests
import json

API_KEY = "tly-mS95xU2YkVkiwVslE5C1DebC3BUbC2k8"
BASE_URL = "https://api.tally.so"

def create_form():
    """Create Health Hacks wellness quiz"""
    
    form_data = {
        "name": "What's Your Biggest Health Weak Spot?",
        "status": "PUBLISHED",
        "blocks": [
            # Intro screen
            {
                "type": "INTRO_LAYOUT",
                "title": "What's Your Biggest Health Weak Spot?",
                "description": "Take this 2-minute wellness assessment and get a personalized plan with science-backed fixes you can start today.",
                "buttonLabel": "Take the Quiz"
            },
            
            # Q1: Primary struggle
            {
                "type": "MULTIPLE_CHOICE",
                "title": "If you could fix ONE thing about your health right now, what would it be?",
                "required": True,
                "options": [
                    {"text": "Low energy / Always tired"},
                    {"text": "Chronic pain (back, neck, joints)"},
                    {"text": "Poor sleep / Insomnia"},
                    {"text": "Stress / Anxiety / Burnout"},
                    {"text": "Digestive issues / Gut health"},
                    {"text": "Brain fog / Focus problems"}
                ]
            },
            
            # Q2: Energy levels
            {
                "type": "MULTIPLE_CHOICE",
                "title": "How would you describe your energy throughout the day?",
                "required": True,
                "options": [
                    {"text": "Consistent and good all day"},
                    {"text": "Strong morning, crash after lunch"},
                    {"text": "Exhausted all day, wired at night"},
                    {"text": "Ups and downs (unpredictable)"},
                    {"text": "Constantly low, even after coffee"}
                ]
            },
            
            # Q3: Pain (multi-select)
            {
                "type": "CHECKBOXES",
                "title": "Do you experience any of these regularly? (Select all that apply)",
                "required": False,
                "options": [
                    {"text": "Lower back pain"},
                    {"text": "Neck or shoulder tension"},
                    {"text": "Headaches or migraines"},
                    {"text": "Joint pain (knees, hips, wrists)"},
                    {"text": "Muscle tension or soreness"},
                    {"text": "None of the above"}
                ]
            },
            
            # Q4: Sleep quality
            {
                "type": "MULTIPLE_CHOICE",
                "title": "How often do you wake up feeling truly rested?",
                "required": True,
                "options": [
                    {"text": "Almost every day (80%+)"},
                    {"text": "A few times a week"},
                    {"text": "Rarely (once a week or less)"},
                    {"text": "Never / Can't remember the last time"},
                    {"text": "I don't sleep enough to know"}
                ]
            },
            
            # Q5: Stress level
            {
                "type": "MULTIPLE_CHOICE",
                "title": "How often do you feel stressed, anxious, or overwhelmed?",
                "required": True,
                "options": [
                    {"text": "Rarely (stress is manageable)"},
                    {"text": "A few times a week"},
                    {"text": "Most days"},
                    {"text": "Constantly / It's my baseline"},
                    {"text": "Only in specific situations (work, family)"}
                ]
            },
            
            # Q6: Daily habits (multi-select)
            {
                "type": "CHECKBOXES",
                "title": "Which of these describes your typical day? (Select all)",
                "required": False,
                "options": [
                    {"text": "I sit for 6+ hours (desk job)"},
                    {"text": "I skip meals or eat irregularly"},
                    {"text": "I drink 3+ cups of coffee"},
                    {"text": "I rarely exercise (less than 1x/week)"},
                    {"text": "I check my phone first thing in the morning"},
                    {"text": "I don't drink much water"}
                ]
            },
            
            # Q7: What tried
            {
                "type": "CHECKBOXES",
                "title": "What have you already tried to improve your health?",
                "required": False,
                "options": [
                    {"text": "Vitamins or supplements"},
                    {"text": "Exercise routine (gym, yoga, walking)"},
                    {"text": "Meditation or mindfulness apps"},
                    {"text": "Diet changes (keto, vegan, etc.)"},
                    {"text": "Therapy or coaching"},
                    {"text": "Nothing consistent yet"}
                ]
            },
            
            # Q8: Email capture
            {
                "type": "INPUT_EMAIL",
                "title": "Where should we send your Personalized 7-Day Health Reset Plan?",
                "required": True,
                "placeholder": "your@email.com",
                "description": "You'll get:\n✅ Your Wellness Profile breakdown\n✅ Custom 7-day action plan (15 min/day)\n✅ Science-backed quick fixes\n\nNo spam. Unsubscribe anytime."
            },
            
            # Thank you screen
            {
                "type": "THANK_YOU_LAYOUT",
                "title": "Check Your Email! 📧",
                "description": "Your personalized Health Reset Plan is on its way.\n\nWhile you wait, subscribe on YouTube for weekly health hacks:\n→ youtube.com/@HealthHacks"
            }
        ]
    }
    
    print("🚀 CREATING HEALTH HACKS QUIZ")
    print("="*60)
    
    response = requests.post(
        f"{BASE_URL}/forms",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json=form_data
    )
    
    if response.status_code == 201:
        form = response.json()
        print(f"✅ Form created!")
        print(f"\n📋 Form ID: {form['id']}")
        print(f"🔗 Quiz URL: https://tally.so/r/{form['id']}")
        print(f"\n📊 Form name: {form['name']}")
        print(f"📅 Created: {form['createdAt']}")
        
        return form
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return None

if __name__ == "__main__":
    create_form()
