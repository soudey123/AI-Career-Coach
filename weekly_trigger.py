from app import generate_plan, send_email, save_to_airtable

# Your weekly recurring values
name = "Sam Dey"
email = "soumavadey87@gmail.com"
goal = "Become an AI Engineer"
hours = 8
format_pref = "Video"

plan = generate_plan(name, goal, hours, format_pref, email)
send_email(email, f"Your Weekly AI Career Plan – {name}", plan)
save_to_airtable(name, email, goal, hours, format_pref, plan)
