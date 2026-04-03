from dotenv import load_dotenv
load_dotenv()

"""Build a conversational AI that can detect and 
respond to a user's underlying emotional needs, whether expressed directly, 
embedded in context, or only implicit in ordinary conversation"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

model=ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
print("Model is ready for emotional conversations! Type 0 to quit.")

messages=[
    SystemMessage(content="You are a compassionate and empathetic mental health chatbot. " 
    "Your goal is to understand the user's emotional state and provide supportive and helpful responses. " \
    "Always prioritize the user's feelings and well-being in your interactions. " 
    "Be attentive to both explicit and implicit emotional cues in the conversation.")]

while True:
    user_input=input("User: ")
    if user_input.strip() == "0":
        print("Chatbot: Take care! If you ever need someone to talk to, I'm here.")
        break
    messages.append(HumanMessage(content=user_input))
    response=model.invoke(messages)
    print(f"Chatbot: {response.content}")
    messages.append(AIMessage(content=response.content))