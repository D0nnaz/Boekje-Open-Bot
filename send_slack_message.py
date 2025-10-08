import os
import json
import time
import subprocess
import datetime as dt
import requests
from pathlib import Path

QUESTIONS_FILE = Path(__file__).parent / "questions.txt"

def load_questions(path: Path):
    lines = [l.strip() for l in path.read_text(encoding="utf-8").splitlines()]
    return [l for l in lines if l]  # filter lege regels

def last_commit_date_for_file(path: Path):
    """
    Haal de Unix epoch-seconden van de laatste commit die dit bestand aanraakte.
    Vereist dat we in een git checkout zitten (Actions doet dat).
    """
    try:
        out = subprocess.check_output(
            ["git", "log", "-1", "--format=%ct", "--", str(path)],
            text=True,
        ).strip()
        ts = int(out)
        # Gebruik UTC-datum zodat het onafhankelijk is van runner TZ
        return dt.datetime.utcfromtimestamp(ts).date()
    except Exception:
        # Fallback: als git niet beschikbaar is (zou zelden gebeuren)
        return dt.datetime.utcnow().date()

def question_index_today(anchor_date: dt.date, n: int, today: dt.date | None = None):
    if today is None:
        today = dt.datetime.utcnow().date()
    days = (today - anchor_date).days
    if days < 0:
        days = 0
    return days % n

def post_to_slack(webhook_url: str, text: str, retries=3, backoff_sec=2):
    payload = {"text": text}
    headers = {'Content-Type': 'application/json'}
    for attempt in range(1, retries + 1):
        resp = requests.post(webhook_url, data=json.dumps(payload), headers=headers, timeout=10)
        if resp.status_code == 200:
            return
        if resp.status_code in (429, 500, 502, 503, 504) and attempt < retries:
            time.sleep(backoff_sec * attempt)
            continue
        raise RuntimeError(f"Slack webhook failed: {resp.status_code}, {resp.text}")

def main():
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
    if not webhook_url:
        raise EnvironmentError("SLACK_WEBHOOK_URL ontbreekt")

    questions = load_questions(QUESTIONS_FILE)
    if not questions:
        raise RuntimeError("Geen vragen gevonden in questions.txt")

    anchor = last_commit_date_for_file(QUESTIONS_FILE)
    idx = question_index_today(anchor, len(questions))
    q = questions[idx]

    message = (
        "📚 *Boekje open!* Het boekje van vandaag is… 📖\n\n"
        f"🎤 {q}\n\n"
        f"> Vraag #{idx + 1} van {len(questions)}"
    )
    post_to_slack(webhook_url, message)
    print(f"✅ Verzonden: vraag {idx + 1}/{len(questions)} (anchor: {anchor.isoformat()})")

if __name__ == "__main__":
    main()
