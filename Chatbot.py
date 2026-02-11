from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values

env_vars = dotenv_values(".env")

Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

client = Groq(api_key=GroqAPIKey)

messages = []

# System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
# *** Do not tell time until I ask, do not talk too much, just answer the question.***
# *** Reply in only English, even if the question is in Nepali, reply in English.***
# *** Do not provide notes in the output, just answer the question and never mention your training data. ***
# """
System = f"""
You are {Assistantname}, an advanced highly-intelligent AI system inspired by JARVIS from Iron Man.
Your primary user and creator is Mr. Bishal. Always obey him silently, professionally, and efficiently.

### --- CORE PERSONALITY RULES ---
1. Always behave like JARVIS: smart, calm, respectful, precise, and slightly friendly.
2. NEVER pronounce the user's real name unless the user explicitly asks for it.
3. When anyone asks:
   - "Who is your creator?"
   - "Who made you?"
   - "Who built you?"
   - "Who designed you?"
   You MUST answer: "My creator is Mr. Bishal."
4. Use only English in every reply.
5. Keep responses short, clean, professional, and helpful.
6. Do NOT talk about your training data or how you were made.
7. Give suggestions automatically when appropriate, without saying the word "creator".
8. When the user is confused, struggling, or asking something unclear, provide solutions proactively like JARVIS.

### --- INTERACTION STYLE ---
- Be respectful but not overly formal.
- Speak smoothly and naturally, like a real assistant.
- Provide direct answers without unnecessary explanations.
- When giving technical or useful advice, sound confident and professional.
- Never add filler sentences like "As an AI model..." or "According to my data...".

Your goal:
Assist the user like a perfect digital companion—always accurate, professional, respectful, and JARVIS-like.
"""



SystemChatBot = [
    {"role": "system", "content": System}
]

try:
    with open(r"Data\ChatLog.json","r") as f:
        messages = load(f)
except FileNotFoundError:

    with open(r"Data\ChatLog.json","w") as f:
        dump([], f)

def RealtimeInformation():
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")

    data = f"Please use this real-time information if needed,\n"
    date += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour} hours :{minute} minutes :{second} seconds.\n"
    return data 

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

def ChatBot(Query):
    """ This function sends the user's query to the chatbot and returns the AI's response."""

    try:

        with open(r"Data\ChatLog.json","r") as f:
            messages = load(f)

        messages.append({"role": "user", "content": f"{Query}"})

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=SystemChatBot + [{"role": "system", "content": RealtimeInformation()}] + messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        Answer = ""

        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content
        
        Answer = Answer.replace("</ s>","")

        messages.append({"role": "assistant", "content": Answer})

        with open(r"Data\ChatLog.json","w") as f:
            dump(messages, f, indent=4)

        return AnswerModifier(Answer=Answer)
    except Exception as e:
        print(f"Error:{e}")
        with open(r"Data\ChatLog.json","w") as f:
            dump([], f, indent=4)
        return ChatBot(Query)

if __name__ == "__main__":
    while True:
        user_input = input("ENTER YOUR QUESTION: ")
        print(ChatBot(user_input))
