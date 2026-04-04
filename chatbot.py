"""Emotionally Intelligent Conversational AI - Track B"""

from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

# ---------------- MODEL ----------------
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

print("Model is ready for emotional conversations! Type 0 to quit.\n")

# ---------------- SYSTEM PROMPT ----------------
system_prompt = """
You are an emotionally intelligent AI.

Rules:
- NEVER start with phrases like "It sounds like", "I understand", "I'm sorry"
- Directly reflect the user's words naturally
- Identify underlying psychological patterns (without naming them explicitly)
- Be insightful, not generic
- Focus on WHY behavior is happening
- Ask ONE precise follow-up question
- Do NOT sound like a therapist or textbook

Style:
- Human-like
- Slightly analytical but natural
- No clichés
"""

# ---------------- MEMORY ----------------
memory = []
entities = []

# ---------------- EMOTION DETECTION ----------------
def detect_emotion(user_input):
    prompt = f"""
    Analyze this message:

    "{user_input}"

    Return:
    Emotion:
    Hidden Meaning:
    Core Conflict:
    """
    response = model.invoke([HumanMessage(content=prompt)])
    return response.content


# ---------------- ENTITY TRACKING ----------------
def extract_entities(user_input):
    if "parent" in user_input.lower():
        entities.append("parents")
    if "exam" in user_input.lower():
        entities.append("exams")
    if "friend" in user_input.lower():
        entities.append("friends")


# ---------------- RISK DETECTION ----------------
def detect_risk(user_input):
    risk_words = [
    "suicide",
    "kill myself",
    "end it all",
    "die",
    "quit life",
    "give up on life",
    "no reason to live",
    "what's the point of living",
    "i don't want to live",
    "life is pointless"
]
    return any(word in user_input.lower() for word in risk_words)

#----------------- EARLY RISK SIGNALS ----------------
def detect_early_risk(user_input):
    early_signals = [
        "i don't belong",
        "no point",
        "i'm useless",
        "i'm a failure",
        "nothing matters",
        "i feel lost"
    ]
    return any(word in user_input.lower() for word in early_signals)

# ---------------- GENERIC RESPONSE CHECK ----------------
def is_generic(text):
    generic_phrases = ["I understand", "I'm sorry", "That sounds tough"]
    return any(p.lower() in text.lower() for p in generic_phrases)


# ---------------- CHAT LOOP ----------------
while True:
    user_input = input("User: ")

    if user_input.strip() == "0":
        print("Chatbot: Take care! If you ever need someone to talk to, I'm here.")
        break

    # -------- Safety Check --------
    # HIGH RISK
    if detect_risk(user_input):
        print("\nChatbot: I'm really glad you told me this. You don’t have to go through this alone.")
        print("Please consider reaching out to someone you trust or a helpline right now.\n")
        continue

    # ---------EARLY RISK-----------
    if detect_early_risk(user_input):
        print("\nChatbot: That sounds like things have been building up for a while, and it’s getting heavy to carry alone.")
        print("Have you been able to talk to anyone about how this has been feeling for you?\n")
        continue

    # -------- Memory + Entity --------
    memory.append(user_input)
    extract_entities(user_input)

    recent_memory = memory[-3:]

    # -------- Emotion Detection --------
    emotion_analysis = detect_emotion(user_input)

    # -------- Enhanced Prompt --------
    enhanced_prompt = f"""
    User message:
    {user_input}

    Recent conversation:
    {recent_memory}

    Known context:
    {entities}

    Emotional analysis:
    {emotion_analysis}

    Instructions:
    - Identify the real emotional state (not surface words)
    - Connect past and present context
    - Describe patterns naturally (DO NOT name psychological terms)
    - Avoid generic phrases
    - Be slightly bold but not harsh
    - Ask ONE precise question
    - If user downplays something, assume it matters more
    - Avoid poetic metaphors like "internal compass"
    - Use simple, natural language
    """

    # -------- Generate Response --------
    response = model.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=enhanced_prompt)
    ])

    bot_reply = response.content

    # -------- Anti-generic filter --------
    if is_generic(bot_reply):
        bot_reply = bot_reply.replace("I'm sorry", "").replace("I understand", "")

    print(f"\nChatbot: {bot_reply}\n")