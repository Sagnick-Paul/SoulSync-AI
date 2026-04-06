import praw
import pickle
import time
from datasets import load_dataset
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()

documents = []

# -------- SOURCE 1: HuggingFace Dataset --------
print("Loading HuggingFace dataset...")
try:
    ds = load_dataset("Amod/mental_health_counseling_conversations")
    for row in ds["train"]:
        combined = row["Context"] + " " + row["Response"]
        if len(combined) > 100:
            documents.append(combined)
    print(f"HuggingFace: {len(documents)} docs loaded")
except Exception as e:
    print(f"HuggingFace failed: {e}")

# -------- SOURCE 2: Reddit via PRAW --------
print("Loading Reddit posts...")
try:
    reddit = praw.Reddit(
        client_id="YOUR_CLIENT_ID",
        client_secret="YOUR_SECRET",
        user_agent="mental_health_bot/1.0"
    )

    subreddits = ["mentalhealth", "depression", "anxiety", "offmychest"]

    for sub_name in subreddits:
        print(f"  Scraping r/{sub_name}...")
        sub = reddit.subreddit(sub_name)
        for post in sub.hot(limit=50):
            if post.selftext and len(post.selftext) > 100:
                documents.append(post.selftext)
            post.comments.replace_more(limit=0)
            for comment in post.comments[:3]:
                if len(comment.body) > 80:
                    documents.append(comment.body)
            time.sleep(0.3)  # be polite

    print(f"After Reddit: {len(documents)} total docs")
except Exception as e:
    print(f"Reddit failed: {e}")

# -------- DEDUPLICATE --------
documents = list(set(documents))
documents = documents[:600]  # cap to keep embedding cost low
print(f"Final document count: {len(documents)}")

# -------- BUILD FAISS INDEX --------
print("Building FAISS index (this may take a few minutes)...")
embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
vector_store = FAISS.from_texts(documents, embeddings)

# -------- SAVE TO DISK --------
vector_store.save_local("knowledge_base")
print("Done! knowledge_base/ folder saved.")