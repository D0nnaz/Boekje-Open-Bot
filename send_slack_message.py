import os
import datetime
import json
import requests

questions = [
    "Wat is je favoriete vakantieherinnering?",
    "Wat is het mooiste boek dat je ooit hebt gelezen?",
    "Als je elke superkracht zou kunnen hebben, welke zou je kiezen?",
    "Wat is de beste beslissing die je ooit hebt genomen?",
    "Welke hobby zou je graag willen oppakken als je de tijd had?",
]

def main():
    webhook_url = os.environ["SLACK_WEBHOOK_URL"]

    # Huidige datum
    today = datetime.date.today()

    day_of_year = today.timetuple().tm_yday 
    
    question_index = (day_of_year - 1) % len(questions)
    question_of_the_day = questions[question_index]

    message = f"📚 **Boekje open doen!**\n\nVandaag's vraag: {question_of_the_day}"

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
