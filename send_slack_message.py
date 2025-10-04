import os
import datetime
import json
import requests

questions = [
    "Wat is de grootste geheim die je ooit hebt moeten bewaren?",
    "Wat zou je doen als je morgen onbegrensd rijk zou zijn, maar niemand je zou geloven?",
    "Als je één moment in je leven opnieuw zou kunnen beleven, welk moment zou dat dan zijn en waarom?",
    "Wat is het vreemdste of spannendste dat je ooit hebt gedaan zonder dat iemand het weet?",
    "Heb je ooit iemand bedrogen, zelfs als het voor iets kleins was? Hoe voelde dat?",
    "Wat is je grootste angst die je voor niemand hebt gedeeld?",
    "Als je je leven opnieuw zou kunnen beginnen, maar met alle kennis die je nu hebt, wat zou je dan totaal anders doen?",
    "Wat is de grootste misstap die je ooit hebt begaan en heb je daar ooit spijt van gehad?",
    "Welke persoon in je leven zou je nooit willen verliezen, en waarom?",
    "Als je onzichtbaar zou zijn voor één dag, wat zou je dan doen?"
]

def main():
    webhook_url = os.environ["SLACK_WEBHOOK_URL"]

    # Current date
    today = datetime.date.today()

    day_of_year = today.timetuple().tm_yday 
    
    question_index = (day_of_year - 1) % len(questions)
    question_of_the_day = questions[question_index]

    message = f"📚 Boekje open! Het boekje van vandaag is... 📖\n\n🎤 {question_of_the_day}"

    payload = {
        "text": message
    }

    response = requests.post(
        webhook_url,
        data=json.dumps(payload),
        headers={'Content-Type': 'application/json'}
    )

    if response.status_code != 200:
        raise Exception(f"Slack webhook failed: {response.status_code}, {response.text}")
    else:
        print("✅ Vraag succesvol verzonden via webhook")

if __name__ == "__main__":
    main()
