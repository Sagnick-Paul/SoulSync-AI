# 🧠 OpenAImer 2026 – Track B  
## 💙 Emotionally Intelligent AI Chatbot

> *“Not just a chatbot. A system that understands what users don’t say.”*

---

## 🚀 Overview

This project is an **Emotionally Intelligent Conversational AI System** designed for **mental health support and deep human-centric interaction**.

Unlike traditional chatbots, this system:
- Detects **implicit emotional signals**
- Understands **context across conversations**
- Maintains **long-term memory**
- Generates **deeply personalized, non-generic responses**

---

## 🎯 Objective

To build an AI that can:

- 🧠 Infer **underlying emotional needs** (even if unstated)
- 🔍 Read between the lines of user messages
- 🗂 Maintain **context + memory across conversations**
- 💬 Respond with **specific, tailored, human-like empathy**
- ⚠️ Handle **high-risk mental health scenarios safely**

---

## ⚡ Key Features

### 🧠 Emotional Intelligence Engine
- Detects:
  - Implicit distress
  - Emotional tone
  - Cognitive patterns (self-doubt, burnout, anxiety)
- Built using NLP + Transformer models

---

### 🧩 Context Awareness
- Tracks:
  - Previous conversations
  - Entities (people, events, situations)
  - Emotional progression over time

---

### 🗃 Memory System
- Short-term + Long-term memory
- Stores:
  - User preferences
  - Emotional states
  - Recurring issues

---

### 🔎 Smart Retrieval (Beyond Basic RAG)
- Hybrid retrieval system:
  - Semantic search
  - Context-aware filtering
- Retrieves relevant past context before generating responses

---

### 💬 Response Generation Engine
- Uses advanced LLMs:
  - LLaMA 3 / Gemini / Mistral / DeepSeek / Qwen
- Ensures:
  - No generic replies ❌
  - High specificity ✔️
  - Emotional depth ✔️

---

### 🛡 Safety Layer
- Detects:
  - Self-harm signals
  - Severe distress
- Applies:
  - Safe responses
  - Escalation strategies

---

## 🏗️ System Architecture

```mermaid
flowchart TD

A[User Input] --> B[Emotion & Intent Analyzer]
B --> C[Context & Memory Retrieval]
C --> D[Knowledge Retriever (RAG)]
D --> E[Prompt Constructor]
E --> F[LLM Response Generator]
F --> G[Response Validator]
G --> H[Final Output]

C -->|Update| M[Memory Store]