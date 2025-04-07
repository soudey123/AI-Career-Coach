# 🧠 AI Career Coach

An automated AI assistant that generates personalized weekly career development plans and delivers them to your inbox — powered by GPT-4, Flask, and Airtable. Replit web development framework was leveraged to build this prototype web app that provides learning weekly learning roadmap as shown below:

![User Form Submission](https://github.com/soudey123/AI-Career-Coach/blob/main/User%20Form%20Submission%20New.png)

![Career Coach Screenshot](https://github.com/soudey123/AI-Career-Coach/blob/main/AI%20Career%20Coach%20Weekly%20Plan.png)

---

## 🚀 Features

- ✨ Personalized 1-week career plans tailored to your goals, learning style, and availability
- 🔁 Weekly email automation via Replit or GitHub Actions
- 📬 GPT-4 powered plan generation with real resource links (videos, tools, articles)
- 🧠 AI "memory" — avoids repeating topics by remembering past weeks
- 📊 Airtable integration for tracking history and growth
- 🖥️ Simple web interface with Flask

---

## 🛠️ Tech Stack

- [x] Python 3
- [x] Flask
- [x] OpenAI GPT-4
- [x] Airtable API
- [x] SMTP (Gmail App Password)
- [x] Replit or GitHub Actions (for automation)

---

## 📸 Demo

### 1. Submit a form like this: 

```text
Name: Sam Dey
Email: soumavadey@email.com
Goal: Become an AI Engineer
Hours: 5
Format: Video (can be changed to other formats)
```

### 2. Email notofication containing weekly learning plan from AI:

![Email Notification](https://github.com/soudey123/AI-Career-Coach/blob/main/Weekly%20AI%20Learning%20Plan%20Email%20Notification.png)

### 3. Airtable track learning plan recommendation from AI on a weekly basis:

![Airtable Log](https://github.com/soudey123/AI-Career-Coach/blob/main/Sample_AILearningPlan_Tracker.csv)

![Airtable Log](https://github.com/soudey123/AI-Career-Coach/blob/main/Weekly%20AI%20Learning%20Plan%20Log.png)

## 📦 Setup Instructions

### Clone this repo:

```bash
git clone https://github.com/your-username/ai-career-coach.git
cd ai-career-coach
```

### Create a `.env` file (or use GitHub Actions Secrets) with:

```ini
OPENAI_API_KEY=sk-xxxx
EMAIL_SENDER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
AIRTABLE_TOKEN=patxxxxxxx
AIRTABLE_BASE_ID=appxxxxxxx
```

### Install dependencies:

```bash
pip install -r requirements.txt
```

### Run locally:

```bash
python app.py
```

---

## ⏰ Automate Weekly Delivery

This repo includes a `weekly_trigger.py` and GitHub Actions config to automate weekly career emails:

- 📬 **Generates new plans weekly**
- 🔁 **Uses past plans as memory to avoid repetition**
- ✅ **Logs each plan to Airtable for tracking**

You can schedule it with:
- GitHub Actions (recommended)
- Replit cron jobs (Pro accounts)
- External services like [cron-job.org](https://cron-job.org)

---

## 🤝 Contributions Welcome

Want to add features like:

- Notion export?  
- Web dashboard?  
- Progress tracking or streak badges?

Fork it. PR it. Let’s build it together! 🚀






   


