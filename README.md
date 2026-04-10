# PHONETICS-AND-LANGUAGE-PERCEPTION



Here’s a clean, professional **README.md** you can directly copy into your GitHub project 👇

---

# 🎙️ Pronunciation Coach Pro

**AI-Powered Speech Analysis & Pronunciation Training System**

---

## 🚀 Overview

**Pronunciation Coach Pro** is an advanced NLP-based web application built using **Streamlit**, designed to help users improve their English pronunciation.

It uses:

* 🎧 Speech recognition (Whisper)
* 🤖 AI feedback (Ollama - Llama 3.2)
* 🔊 Text-to-Speech (pyttsx3)
* 📊 Audio signal analysis (waveform & spectrogram)

This project focuses especially on **Tamil Mother Tongue Influence (MTI)** and provides **detailed pronunciation feedback**.

---

## ✨ Features

* 🎤 Record or upload speech
* 🧠 AI-based pronunciation analysis
* 📊 Waveform & spectrogram visualization
* 🔁 Comparison with correct pronunciation
* 🎯 Pronunciation score (out of 10)
* 📚 Tamil MTI-specific feedback
* 🔊 AI-generated correct pronunciation audio

---

## 🛠️ Tech Stack

* **Frontend/UI:** Streamlit
* **Speech Recognition:** OpenAI Whisper
* **AI Feedback:** Ollama (Llama 3.2)
* **Audio Processing:** NumPy, SciPy, SoundFile
* **Visualization:** Matplotlib
* **Text-to-Speech:** pyttsx3

---

## 📦 Installation Guide

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/phonetics-and-language-perception.git
cd phonetics-and-language-perception
```

---

### 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv venv
venv\Scripts\activate   # Windows
# OR
source venv/bin/activate  # Mac/Linux
```

---

### 3️⃣ Install Required Libraries

```bash
pip install -r requirements.txt
```

If you don’t have `requirements.txt`, install manually:

```bash
pip install streamlit whisper ollama numpy matplotlib scipy pyttsx3 soundfile
```

---

### 4️⃣ Install & Run Ollama

Download Ollama from:
👉 [https://ollama.com/download](https://ollama.com/download)

Then run:

```bash
ollama run llama3.2:1b
```

⚠️ Keep Ollama running in the background.

---

### 5️⃣ Run the Streamlit App

```bash
streamlit run pro.py
```

---

## 🎯 How to Use

### 🔹 Option 1: Record Your Voice

1. Click **🎙️ Record Mode**
2. Press the microphone button
3. Speak clearly (5–10 seconds)
4. Release to stop recording

---

### 🔹 Option 2: Upload Audio

1. Go to **📤 Upload Mode**
2. Upload `.wav`, `.mp3`, or `.m4a` file
3. Wait for processing

---

## 📊 What You Get

After submitting audio, the system will:

### 🧪 1. Speech Detection

* Converts your speech → text

### 🎯 2. AI Feedback

* Pronunciation score (1–10)
* Strengths
* Tamil MTI issues
* Improvement suggestions

### 🔊 3. Correct Pronunciation

* AI-generated perfect audio

### 📈 4. Audio Analysis

* Waveform
* Spectrogram

### 📊 5. Feature Comparison

* Duration
* Energy
* Amplitude

---

## 📁 Project Structure

```
📦 phonetics-and-language-perception
 ┣ 📜 pro.py
 ┣ 📜 README.md
 ┣ 📂 recordings/
```

---

## ⚠️ Important Notes

* 🎤 Speak clearly for at least **5 seconds**
* 🔌 Ensure **Ollama is running**
* 📁 Audio files should be clean (less noise)
* 💻 Works best on systems with good CPU/GPU

---

## 🧠 Future Improvements

* Real-time pronunciation feedback
* Accent detection
* Multi-language support
* Mobile app integration

---

## 🎓 Academic Use

This project is developed as a **Final Year NLP Project** focusing on:

* Phonetics
* Speech perception
* Language acquisition

---

## 🙌 Acknowledgment

* OpenAI Whisper
* Ollama LLM
* Streamlit

---

## 🎧Demo

**Link : https://drive.google.com/file/d/1lL2zCkyaEPe8Ckc9ZZwP7f80s8WUiU8A/view?usp=drive_link**

---

## 💡 Author

**Deepshika P**

B.E. Computer Science Engineering

---
