from flask import Flask, request, render_template
import openai
import os
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage
import requests

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)


def get_last_plan_from_airtable(email):
    url = f"https://api.airtable.com/v0/{os.getenv('AIRTABLE_BASE_ID')}/CareerPlans"
    headers = {
        "Authorization": f"Bearer {os.getenv('AIRTABLE_TOKEN')}",
    }
    params = {
        "filterByFormula": f"{{Email}}='{email}'",
        "sort": [{
            "field": "Timestamp",
            "direction": "desc"
        }],
        "maxRecords": 1
    }

    response = requests.get(url, headers=headers, params=params)
    records = response.json().get("records", [])
    if records:
        return records[0]["fields"].get("Plan", "")
    return ""


def generate_plan(name, goal, hours, format_pref, email):
    last_plan = get_last_plan_from_airtable(email)
    prompt = f"""
    You are a world-class AI Career Coach. Your client is {name}, who wants to become a {goal}. 
    They are available for {hours} hours this week and prefer {format_pref} content.

    Here is their previous weekly plan:
    {last_plan}

    ✅ Create a *new* 1-week plan that builds upon this and avoids repeating content.
    Be specific. Include links to resources, a stretch goal, and a reflection prompt.
    ✅ The plan should:
    - Be broken down day-by-day (7 days)
    - Include links to YouTube videos, articles, or tutorials
    - Suggest tools (like Jupyter Notebook, Scikit-learn, Hugging Face, etc.)
    - End with a reflection question
    - Be motivating and easy to follow
    """
    response = openai.ChatCompletion.create(model="gpt-4",
                                            messages=[{
                                                "role": "user",
                                                "content": prompt
                                            }])
    return response.choices[0].message['content']


def send_email(to_email, subject, plan, last_plan, name, goal):
    sender = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to_email

    # Read the HTML email template or insert inline here
    html_content = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Your AI Career Plan</title>
  <style>
    body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; }}
    .container {{ max-width: 700px; margin: auto; background: #fff; padding: 30px; border-radius: 10px; }}
    h2 {{ color: #007bff; }}
    h4 {{ color: #555; }}
    .section {{ margin-top: 30px; padding: 20px; background-color: #f8f9fa; border-radius: 8px; }}
    pre {{ white-space: pre-wrap; font-size: 15px; line-height: 1.6; }}
  </style>
</head>
<body>
  <div class="container">
    <h2>🎯 Hello {name} – Here's Your AI Career Plan!</h2>
    <p>Your goal: <strong>{goal}</strong></p>
    <div class="section">
      <h4>🗓️ Last Week's Plan</h4>
      <pre>{last_plan}</pre>
    </div>
    <div class="section">
      <h4>📅 This Week's Plan</h4>
      <pre>{plan}</pre>
    </div>
    <p style="margin-top: 30px; color: #666; font-size: 14px;">
      This weekly plan was generated by your AI Career Coach using GPT-4 and sent just for you. Stay consistent and keep learning! 🚀
    </p>
  </div>
</body>
</html>
"""

    msg.set_content(
        "Your AI Career Plan is ready! View it in an email client that supports HTML."
    )
    msg.add_alternative(html_content, subtype='html')

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)
        print("✅ Email sent successfully!")


def save_to_airtable(name, email, goal, hours, format_pref, plan):
    url = f"https://api.airtable.com/v0/{os.getenv('AIRTABLE_BASE_ID')}/CareerPlans"
    headers = {
        "Authorization": f"Bearer {os.getenv('AIRTABLE_TOKEN')}",
        "Content-Type": "application/json"
    }
    data = {
        "fields": {
            "Name": name,
            "Email": email,
            "Goal": goal,
            "Hours": int(hours),
            "Format": format_pref,
            "Plan": plan
        }
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        print("✅ Airtable entry added successfully!")
    except Exception as e:
        print("❌ Airtable save failed:", e)
        print("🔎 Payload sent:", data)


@app.route('/health')
def health_check():
    return 'OK', 200


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
@app.route('/generate', methods=['POST'])
def generate():
    name = request.form['name']
    email = request.form['email']
    goal = request.form['goal']
    hours = request.form['hours']
    format_pref = request.form['format']

    last_plan = get_last_plan_from_airtable(email)
    plan = generate_plan(name, goal, hours, format_pref, email)

    send_email(email, f"Your Weekly AI Career Plan – {name}", plan, last_plan,
               name, goal)
    save_to_airtable(name, email, goal, hours, format_pref, plan)

    return render_template('plan.html',
                           name=name,
                           plan=plan,
                           last_plan=last_plan)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
