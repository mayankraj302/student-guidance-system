import json 
import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
def save_progress(name, interest, day):
    data = {}
    if os.path.exists("progress.json"):
        with open("progress.json", "r") as f:
            data = json.load(f)
    data[name.lower()] = {
        "interest": interest,
        "day": day
    }
    with open("progress.json", "w") as f:
        json.dump(data, f)

def load_progress(name):
    if os.path.exists("progress.json"):
        with open("progress.json", "r") as f:
            data = json.load(f)
            return data.get(name.lower(), None)
    return None

def ask_ai(prompt):
    chat = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a student career guidance assistant made by Mayank, a 15-year-old student from a small in India who built this to help confused students find their path. If asked who made you, say: 'I was built by Mayank, a student just like you.'If a user asks which day they are on, tell them their progress is being tracked and they can check it next time they open the app."},
            {"role": "user", "content": prompt}
        ]
    )
    return chat.choices[0].message.content


def generate_day_plan(name, interest):
    prompt = f"""Create a 7-day action plan for a student named {name} who is interested in {interest}.
Format it exactly like this:
Day 1: [title] | [specific action]
Day 2: [title] | [specific action]
Day 3: [title] | [specific action]
Day 4: [title] | [specific action]
Day 5: [title] | [specific action]
Day 6: [title] | [specific action]
Day 7: [title] | [specific action]
Keep each day short, specific,motivated and actionable. No extra text."""
    return ask_ai(prompt)


while True:
    print("\nWelcome to Student Guidance System.\n")
    print("Hey! I am your simple AI guider made by Mayank, I can guide you for the best skill for your future.\n")

    name = input("Can I have your name? ")
    if not name:
        name = "Student"
    existing = load_progress(name)
    if existing:
        print(f"\nWelcome back {name}! Last time you were exploring {existing['interest']} on Day {existing['day']}.")
        resume = input("Do you want to continue from where you left off? (yes/no): ").lower()
        if resume in ["yes", "y"]:
            interest = existing["interest"]
            day = existing["day"]
            print(f"\nGreat! Continuing your {interest} journey from Day {day}.")
            prompt = f"A student named {name} is continuing their {interest} journey on Day {day}. Give them specific guidance for what to focus on today."
            print("\nThinking...\n")
            print(ask_ai(prompt))
            continue  

    else:
        print(f"\nHello {name}! Let's guide you for your future.\n")

    print("What do you like?")
    print("1. Technology")
    print("2. Business")
    print("3. Creativity")
    print("4. Something else")

    choice = input("Enter your choice: ").lower()

    # TECHNOLOGY PATH
    if choice in ["1", "tech", "technology", "first one"]:
        print(f"\nExcellent choice {name}!")
        print("But in technology what do you like?\n")

        print("1. Cloud and security")
        print("2. Robotics")
        print("3. Data science")
        print("4. Programming")

        tech_choice = input("Enter your choice: ").lower()

        if tech_choice == "1":
            interest = "Cloud and Security"
        elif tech_choice == "2":
            interest = "Robotics"
        elif tech_choice == "3":
            interest = "Data Science"
        elif tech_choice == "4":
            interest = "Programming"
        else:
            interest = tech_choice
        feeling = input("How are you feeling right now about your future ?confident/scared/both:")
        prompt = f"A student named {name} enjoys: {interest}. If they feel {feeling} about their future career give them detailed,focused, specific,helpful,non-generic ,friendly guidance on what skill or path to explore. Keep it simple, warm and encouraging. Max 5 lines and also include realistic salary ranges in Indian Rupees for the career paths you suggest."

        print("\nThinking...\n")
        response = ask_ai(prompt)
        print(response)


        plan = input("\nWould you like a 7-day action plan? (yes/no): ").lower()
        if plan in ["yes", "y","of course","yeah"]:
            print("\nGenerating your personal 7-day plan...\n")
            print(generate_day_plan(name, interest))
            save_progress(name, interest, 1)
        else:
            print("No problem start with small actions.")

    # CONFUSED PATH
    elif choice in ["4", "i am confused", "confused", "i don't know", "dont know"]:
        print("\nIt's okay to feel confused. Most people feel this way.\n")

        interest = input("Tell me what you enjoy doing or what interests you: ")
        feeling = input("How are you feeling right now about your future ?confident/scared/both:")

        prompt = f"A student named {name} enjoys: {interest}. If they feel {feeling} about their future career give them detailed,focused, specific,helpful,non-generic ,friendly guidance on what skill or path to explore. Keep it simple, warm and encouraging. Max 5 lines and also include realistic salary ranges in Indian Rupees for the career paths you suggest."

        print("\nThinking...\n")
        response = ask_ai(prompt)
        print(response)

     
        plan = input("\nWould you like a 7-day action plan? (yes/no): ").lower()
        if plan in ["yes", "y","of course","yeah"]:
            print("\nGenerating your personal 7-day plan...\n")
            print(generate_day_plan(name, interest))
            save_progress(name, interest, 1)
        else:
            print("No problem start with small actions.")

    # OTHER PATHS
    else:
        interest = input("Tell me more about your interests: ")
        feeling = input("How are you feeling right now about your future ?confident/scared/both:")

        prompt = f"A student named {name} enjoys: {interest}. If they feel {feeling} about their future career give them detailed,focused, specific,helpful,non-generic ,friendly guidance on what skill or path to explore. Keep it simple, warm and encouraging. Max 5 lines and also include realistic salary ranges in Indian Rupees for the career paths you suggest."


        print("\nThinking...\n")
        response = ask_ai(prompt)
        print(response)

     
        plan = input("\nWould you like a 7-day action plan? (yes/no): ").lower()
        if plan in ["yes", "y","of course","yeah"]:
            print("\nGenerating your personal 7-day plan...\n")
            print(generate_day_plan(name, interest))
            save_progress(name,interest,1)
        else:
            print("No problem start with small actions.")

       

    # FOLLOW-UP LOOP
    while True:
        follow = input(f"You can ask follow up questions or type 'change' to explore a different interest or simply type 'exit/no' to exit: ").lower()

        if follow == "change":
            interest = input("Tell me about your new interest: ")
            feeling = input("How are you feeling right now about your future ?confident/scared/both:")
            prompt = f"A student named {name} enjoys: {interest}. If they feel {feeling} about their future career give them detailed,focused, specific,helpful,non-generic ,friendly guidance on what skill or path to explore. Keep it simple, warm and encouraging. Max 5 lines and also include realistic salary ranges in Indian Rupees for the career paths you suggest."


            print("\nThinking...\n")
            response = ask_ai(prompt)
            print(response)
            continue

        if follow in ["exit", "no"]:
            break

        prompt = f"Student named {name} who enjoys {interest} is asking: {follow}. Answer helpfully and encouragingly in max 4 lines."

        print("\nThinking...\n")
        print(ask_ai(prompt))

    again = input("\nDo you want to try again? (yes/no): ").lower()
    if again != "yes":
        print("\nGood luck with your future, keep learning!")
        break