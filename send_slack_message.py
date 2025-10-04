import os
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

def load_last_question_index():
    try:
        with open('last_question_index.txt', 'r') as file:
            index = int(file.read().strip())
    except FileNotFoundError:
        index = 0
    return index

def save_last_question_index(index):
    with open('last_question_index.txt', 'w') as file:
        file.write(str(index))

def main():
    webhook_url = os.environ["SLACK_WEBHOOK_URL"]
    last_index = load_last_question_index()
    question_of_the_day = questions[last_index]
    message = f"📚 Boekje open! Het boekje van vandaag is... 📖\n\n🎤 {question_of_the_day}"
    
    if last_index == len(questions) - 1:
        message += "\n\n⚠️ DE VRAGEN ZIJN OP!"

    payload = {"text": message}
    response = requests.post(webhook_url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
    
    if response.status_code != 200:
        raise Exception(f"Slack webhook failed: {response.status_code}, {response.text}")
    else:
        print("✅ Vraag succesvol verzonden via webhook")
    
    next_index = (last_index + 1) % len(questions)
    save_last_question_index(next_index)

if __name__ == "__main__":
    main()
