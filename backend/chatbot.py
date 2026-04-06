"""Emotionally Intelligent Conversational AI - Track B"""

from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

# This is the correct way for the new package
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_mistralai import MistralAIEmbeddings
import os




import os


# ---------------- DOCUMENTS ----------------
documents = [
    "Procrastination often comes from fear of failure or overwhelm.",
    "Emotional numbness can be a coping response to prolonged stress.",
    "Avoidance behavior is often linked to anxiety or self-doubt.",
    "Feeling like you don't belong is commonly associated with imposter syndrome."
]

# ---------------- EMBEDDINGS ----------------
# Using the prefix 'models/' as some Pydantic versions require it for validation
#embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
embeddings = MistralAIEmbeddings(model="mistral-embed")

# ---------------- VECTOR STORE ----------------
vector_store = FAISS.from_texts(documents, embeddings)

# ---------------- MODEL ----------------
# model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
# print("Model is ready for emotional conversations! Type 0 to quit.\n")

model=ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)

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

#

# ---------------- MEMORY ----------------
# Global defaults (used for CLI)
memory = []
entities = []
user_profile = {
    "common_emotions": [],
    "patterns": [],
    "entities": []
}

#---------------- PROFILE UPDATE FUNCTION ----------------
def update_profile(user_input, emotion_analysis, profile):
    if "avoid" in emotion_analysis.lower():
        profile["patterns"].append("avoidance")

    if "stress" in emotion_analysis.lower():
        profile["common_emotions"].append("stress")

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
def extract_entities(user_input, entities_list):
    if "parent" in user_input.lower():
        entities_list.append("parents")
    if "exam" in user_input.lower():
        entities_list.append("exams")
    if "friend" in user_input.lower():
        entities_list.append("friends")


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

def get_chatbot_response(user_input, history, entities_list, profile):
    """
    Core logic to generate a response given user input and context.
    Returns: (response_text, is_risk, is_early_risk)
    """
    # -------- Safety Check --------
    if detect_risk(user_input):
        return ("I'm really glad you told me this. You don't have to go through this alone. Please consider reaching out to someone you trust or a helpline right now.", True, False)

    if detect_early_risk(user_input):
        return ("That sounds like things have been building up for a while, and it’s getting heavy to carry alone. Have you been able to talk to anyone about how this has been feeling for you?", False, True)

    # -------- Memory + Entity --------
    history.append(user_input)
    extract_entities(user_input, entities_list)

    recent_memory = history[-3:]
    
    #------------------FAISS RETRIEVAL FUNCTION----------------
    retrieved_docs = vector_store.similarity_search(user_input, k=2)
    context = " ".join([doc.page_content for doc in retrieved_docs])

    # -------- Emotion Detection --------
    emotion_analysis = detect_emotion(user_input)
    update_profile(user_input, emotion_analysis, profile)

    # -------- Enhanced Prompt --------
    enhanced_prompt = f"""
    User message:
    {user_input}
    
    Relevant knowledge:
    {context}
    
    User Profile:
    {profile}

    Recent conversation:
    {recent_memory}

    Known context:
    {entities_list}

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

    return (bot_reply, False, False)


# ---------------- CHAT LOOP (CLI) ----------------
def run_cli():
    print("Model is ready for emotional conversations! Type 0 to quit.\n")
    while True:
        u_input = input("User: ")

        if u_input.strip() == "0":
            print("Chatbot: Take care! If you ever need someone to talk to, I'm here.")
            break

        bot_reply, is_risk, is_early_risk = get_chatbot_response(u_input, memory, entities, user_profile)
        
        if is_risk:
            print(f"\n[RISK DETECTED]\nChatbot: {bot_reply}\n")
        elif is_early_risk:
            print(f"\n[EARLY RISK DETECTED]\nChatbot: {bot_reply}\n")
        else:
            print(f"\nChatbot: {bot_reply}\n")

if __name__ == "__main__":
    run_cli()
