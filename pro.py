import streamlit as st
import whisper
import ollama
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import pyttsx3
import io
import soundfile as sf  # pip install soundfile
import re

# ── Page Config ──
st.set_page_config(page_title="Pronunciation Coach Pro", page_icon="🎙️", layout="wide")

# ── PREMIUM DARK INDIGO THEME - DARK GRADIENT + GLASS CARDS ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
    --primary: #6366f1;
    --primary-light: #818cf8;
    --success: #10b981;
    --warning: #f59e0b;
    --danger: #ef4444;
    --bg-dark: #0f172a;
    --bg-card: #1e293b;
    --bg-card-hover: #334155;
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --border: #334155;
}

.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
    font-family: 'Inter', sans-serif;
}

h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; }

/* Hero banner */
.hero-banner {
    background: linear-gradient(135deg, #6366f1, #8b5cf6, #a855f7);
    border-radius: 20px;
    padding: 3rem 2rem;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 20px 60px rgba(99, 102, 241, 0.3);
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-banner h1 {
    color: white !important;
    font-size: 2.8rem !important;
    margin: 0 !important;
    font-weight: 700 !important;
}
.hero-banner p {
    color: rgba(255,255,255,0.9);
    font-size: 1.2rem;
    margin-top: 0.5rem;
}
.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.2);
    backdrop-filter: blur(10px);
    padding: 0.6rem 1.5rem;
    border-radius: 50px;
    color: white;
    font-size: 0.9rem;
    margin-bottom: 1rem;
    font-weight: 600;
}

/* Glass Cards */
.glass-card {
    background: rgba(30, 41, 59, 0.85);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 20px;
    padding: 2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
}

/* Score Circle */
.score-circle {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-size: 2.5rem;
    font-weight: 700;
    font-family: 'Space Grotesk', sans-serif;
    margin: 0 auto 1rem;
    color: white;
    box-shadow: 0 12px 40px rgba(16,185,129,0.4);
}
.score-high { background: linear-gradient(135deg, #10b981, #34d399); }
.score-mid { background: linear-gradient(135deg, #f59e0b, #fbbf24); }
.score-low { background: linear-gradient(135deg, #ef4444, #f87171); }

/* Analysis Results */
.analysis-results {
    background: rgba(30, 41, 59, 0.9);
    border-radius: 24px;
    padding: 2.5rem;
    margin-bottom: 2rem;
    border: 1px solid rgba(99, 102, 241, 0.3);
}

/* Section Headers */
.section-header {
    color: #c7d2fe;
    font-size: 1.5rem;
    font-weight: 600;
    font-family: 'Space Grotesk', sans-serif;
    margin: 2rem 0 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

/* Feedback Container */
.feedback-container {
    background: rgba(30, 41, 59, 0.9);
    border-radius: 20px;
    padding: 2rem;
    border: 1px solid rgba(99, 102, 241, 0.3);
    max-height: 400px;
    overflow-y: auto;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(30, 41, 59, 0.8);
    border-radius: 16px;
    padding: 8px;
    gap: 8px;
    border: 1px solid rgba(99, 102, 241, 0.3);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 12px;
    color: #94a3b8;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
    padding: 0.75rem 1.5rem;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important;
    border: none !important;
    border-radius: 16px !important;
    padding: 0.75rem 2rem !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1rem !important;
    transition: all 0.3s !important;
    box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4) !important;
}
.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 15px 35px rgba(99, 102, 241, 0.6) !important;
}

/* File uploader */
.stFileUploader {
    border: 2px dashed rgba(99, 102, 241, 0.4) !important;
    border-radius: 20px !important;
    background: rgba(30, 41, 59, 0.6) !important;
    padding: 2rem !important;
}

/* Table */
.metric-table {
    background: rgba(30, 41, 59, 0.9);
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid rgba(99, 102, 241, 0.3);
}

/* Footer */
.footer {
    text-align: center;
    color: #64748b;
    padding: 3rem 0 2rem;
    font-size: 1rem;
    border-top: 1px solid rgba(51, 65, 85, 0.5);
    margin-top: 4rem;
}

/* Matplotlib dark theme */
.stPlotlyChart, .stPyplot { 
    border-radius: 20px !important; 
    overflow: hidden !important;
    background: rgba(15, 23, 42, 0.8) !important;
    border: 1px solid rgba(99, 102, 241, 0.3) !important;
}
</style>
""", unsafe_allow_html=True)

# ── Hero Banner ──
st.markdown("""
<div class="hero-banner">
    <div class="hero-badge">🚀 AI-Powered Pronunciation Coach Pro</div>
    <h1>🎙️ Perfect Your English</h1>
    <p>Advanced speech analysis with DETAILED AI feedback, dual audio comparison, and perfect pronunciation models</p>
</div>
""", unsafe_allow_html=True)

SAVE_DIR = "recordings"
os.makedirs(SAVE_DIR, exist_ok=True)

# ── Load Whisper ──
@st.cache_resource
def load_models():
    return whisper.load_model("base")

whisper_model = load_models()

# ── Dark-themed plots ──
plt.rcParams.update({
    'figure.facecolor': '#1e293b',
    'axes.facecolor': '#0f172a',
    'axes.edgecolor': '#334155',
    'axes.labelcolor': '#94a3b8',
    'text.color': '#e2e8f0',
    'xtick.color': '#64748b',
    'ytick.color': '#64748b',
    'grid.color': '#1e293b',
    'grid.alpha': 0.3,
})

def plot_single_audio(audio_data_or_path, title, color="#818cf8", is_path=False):
    """Plot waveform + spectrogram with premium styling"""
    try:
        if is_path:
            audio, fs = sf.read(audio_data_or_path)
        else:
            audio, fs = sf.read(io.BytesIO(audio_data_or_path.getbuffer()))
        
        if len(audio.shape) > 1:
            audio = audio.mean(axis=1)
        
        audio = audio.astype(np.float32)
        if np.max(np.abs(audio)) != 0:
            audio = audio / np.max(np.abs(audio))

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 7))

        # Waveform
        time_axis = np.linspace(0, len(audio) / fs, len(audio))
        ax1.plot(time_axis, audio, color=color, linewidth=1.2, alpha=0.9)
        ax1.fill_between(time_axis, audio, alpha=0.2, color=color)
        ax1.set_title(f"🎵 {title} - Waveform", fontsize=14, fontweight='bold', pad=20, color='#c7d2fe')
        ax1.set_xlabel('Time (s)', fontsize=12)
        ax1.set_ylabel('Amplitude', fontsize=12)
        ax1.grid(True, alpha=0.2)

        # Spectrogram
        f, t, Sxx = signal.spectrogram(audio, fs, nperseg=1024)
        im = ax2.pcolormesh(t, f, 10 * np.log10(Sxx + 1e-10), shading='gouraud', cmap='magma')
        ax2.set_title(f"🎨 {title} - Spectrogram", fontsize=14, fontweight='bold', pad=20, color='#c7d2fe')
        ax2.set_xlabel('Time (s)', fontsize=12)
        ax2.set_ylabel('Frequency (Hz)', fontsize=12)
        cbar = plt.colorbar(im, ax=ax2, shrink=0.8)
        cbar.set_label('Intensity (dB)', color='#94a3b8')
        cbar.ax.yaxis.set_tick_params(color='#64748b')

        plt.tight_layout(pad=2)
        st.pyplot(fig)
        plt.close(fig)
    except Exception as e:
        st.warning(f"📊 {title} visualization error: {e}")

def get_audio_features(audio_data_or_path, is_path=False):
    try:
        if is_path:
            audio, fs = sf.read(audio_data_or_path)
        else:
            audio, fs = sf.read(io.BytesIO(audio_data_or_path.getbuffer()))
        
        if len(audio.shape) > 1:
            audio = audio.mean(axis=1)
        
        duration = len(audio) / fs
        peak = float(np.max(np.abs(audio)))
        rms = float(np.sqrt(np.mean(audio**2)))
        return {
            "Sample Rate": f"{fs:,} Hz",
            "Duration": f"{duration:.2f}s", 
            "Peak Amp": f"{peak:.3f}",
            "RMS Energy": f"{rms:.3f}"
        }
    except:
        return None

def generate_correct_pronunciation(text):
    try:
        tts = pyttsx3.init()
        voices = tts.getProperty('voices')
        
        female_voice = None
        for voice in voices:
            if 'zira' in voice.name.lower() or 'female' in voice.name.lower():
                female_voice = voice.id
                break
        
        if not female_voice and len(voices) > 1:
            female_voice = voices[1].id
        
        if female_voice:
            tts.setProperty('voice', female_voice)
        
        tts.setProperty('rate', 165)
        tts.setProperty('volume', 0.9)
        
        path = os.path.join(SAVE_DIR, "correct.wav")
        tts.save_to_file(text, path)
        tts.runAndWait()
        
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown('<div class="section-header">🔊 Perfect Pronunciation</div>', unsafe_allow_html=True)
            st.audio(path)
        with col2:
            st.success("✅ Play")
        return path
    except Exception as e:
        st.warning(f"TTS error: {e}")
        return None

def render_score(score):
    if score >= 7:
        cls = "score-high"
        label = "Excellent"
    elif score >= 5:
        cls = "score-mid" 
        label = "Good"
    else:
        cls = "score-low"
        label = "Needs Work"
    
    st.markdown(f'''
    <div class="glass-card" style="text-align:center;">
        <div class="score-circle {cls}">
            <div style="font-size:1.8rem;line-height:1;">{score}</div>
            <div style="font-size:0.7rem;opacity:0.8;">/10</div>
        </div>
        <div style="color:#94a3b8;font-weight:500;">{label}</div>
    </div>
    ''', unsafe_allow_html=True)

def analyze_audio(audio_input, is_raw_audio=True):
    if is_raw_audio:
        file_path = os.path.join(SAVE_DIR, "record.wav")
        with open(file_path, "wb") as f:
            f.write(audio_input.getbuffer())
    else:
        file_path = audio_input

    try:
        result = whisper_model.transcribe(file_path, language='en')
        text = result["text"].strip()

        # Detected Text
        st.markdown('<div class="section-header">🧪 Detected Speech</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="glass-card" style="font-size:1.2rem;color:#e2e8f0;text-align:center;padding:2rem;">"{text}"</div>', unsafe_allow_html=True)

        if len(text) < 2:
            st.error("⚠️ No clear speech detected. Speak louder & longer (5+ seconds).")
            return

        # AI Analysis - DETAILED FEEDBACK
        st.markdown('<div class="section-header">🎯 AI Pronunciation Coach Analysis</div>', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown('<div class="analysis-results">', unsafe_allow_html=True)
            with st.spinner("🤖 AI Analyzing Pronunciation (Tamil MTI Focus)..."):
                prompt = f"""You are an expert English pronunciation coach working with Tamil-speaking students.

Analyze this spoken text: "{text}"

Provide DETAILED feedback in EXACTLY this format (250-350 words):

**SCORE: [1-10]**

**STRENGTHS (3 specific positives):**
• [Strength 1 - mention specific sounds/words you heard well]
• [Strength 2 - mention rhythm, stress, or clarity] 
• [Strength 3 - mention any natural English patterns]

**TAMIL MTI ISSUES (3 common problems):**
• [Issue 1 - e.g., "Tamil retroflex /ɽ/ becoming English /r/"]
• [Issue 2 - e.g., "Flat intonation vs English stress patterns"] 
• [Issue 3 - e.g., "Vowel confusion: Tamil short 'a' vs English /æ/"]

**IMPROVEMENTS (3 actionable steps):**
• [Step 1 - specific practice for main issue]
• [Step 2 - drill exercise for sounds]
• [Step 3 - rhythm/stress practice]

**PRO TIP:** [One sentence daily practice tip]

Be SPECIFIC about which words/sounds in "{text}" need work. Focus on Tamil Mother Tongue Influence (MTI). Make it encouraging and detailed!"""
                
                response = ollama.chat(
                    model='llama3.2:1b',
                    messages=[{'role': 'user', 'content': prompt}],
                    options={
                        'temperature': 0.8,
                        'top_p': 0.9,
                        'num_predict': 800
                    }
                )
                feedback = response['message']['content']
            
            # Parse score
            score = 7  # Default
            for line in feedback.split('\n'):
                if 'SCORE' in line.upper():
                    score_match = re.search(r'\b(\d{1,2})\b', line)
                    if score_match:
                        score = min(int(score_match.group(1)), 10)
                        break
            
            render_score(score)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="feedback-container">', unsafe_allow_html=True)
            st.markdown(f'<pre style="color:#e2e8f0;font-family:Inter,sans-serif;font-size:1rem;line-height:1.6;white-space:pre-wrap;">{feedback}</pre>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Correct Audio
        correct_path = generate_correct_pronunciation(text)

        # Dual Comparison
        st.markdown('<div class="section-header">🔄 Audio Comparison Analysis</div>', unsafe_allow_html=True)
        col_graph1, col_graph2 = st.columns(2)
        
        with col_graph1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<div style="color:#818cf8;font-weight:600;font-size:1.1rem;margin-bottom:1rem;">📈 Your Spoken Audio</div>', unsafe_allow_html=True)
            plot_single_audio(file_path, "User Speech", "#818cf8", is_path=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_graph2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<div style="color:#10b981;font-weight:600;font-size:1.1rem;margin-bottom:1rem;">✅ AI Perfect Audio</div>', unsafe_allow_html=True)
            if correct_path and os.path.exists(correct_path):
                plot_single_audio(correct_path, "Correct Speech", "#10b981", is_path=True)
            else:
                st.warning("Correct audio visualization unavailable")
            st.markdown('</div>', unsafe_allow_html=True)

        # Metrics Table
        st.markdown('<div class="section-header">📊 Audio Feature Comparison</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-table">', unsafe_allow_html=True)
        
        user_features = get_audio_features(file_path, is_path=True)
        correct_features = get_audio_features(correct_path, is_path=True) if correct_path and os.path.exists(correct_path) else None
        
        if user_features:
            comparison_data = {
                "Feature": ["Sample Rate", "Duration", "Peak Amplitude", "RMS Energy"],
                "Your Audio": [
                    user_features["Sample Rate"], 
                    user_features["Duration"], 
                    user_features["Peak Amp"], 
                    user_features["RMS Energy"]
                ]
            }
            if correct_features:
                comparison_data["Correct Audio"] = [
                    correct_features["Sample Rate"], 
                    correct_features["Duration"], 
                    correct_features["Peak Amp"], 
                    correct_features["RMS Energy"]
                ]
            st.table(comparison_data)
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="glass-card" style="text-align:center;color:#94a3b8;font-size:1.1rem;">💡 <strong>Pro Tip:</strong> Compare waveforms & spectrograms — smoother patterns = better pronunciation clarity!</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Analysis error: {e}")

# ── Main UI ──
tab1, tab2 = st.tabs(["🎙️ **Record Mode**", "📤 **Upload Mode**"])

with tab1:
    st.markdown('<div class="glass-card" style="text-align:center;padding:2.5rem;">', unsafe_allow_html=True)
    st.markdown('<div class="section-header" style="justify-content:center;">🎤 Record Your Speech (5-10 seconds)</div>', unsafe_allow_html=True)
    st.caption("👆 Click the microphone • Speak clearly • Release when done")
    audio_input = st.audio_input("Record now...", sample_rate=16000, key="record")
    
    if audio_input is not None:
        st.success("✅ Audio captured successfully!")
        st.audio(audio_input)
        analyze_audio(audio_input, is_raw_audio=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="glass-card" style="text-align:center;padding:2.5rem;">', unsafe_allow_html=True)
    st.markdown('<div class="section-header" style="justify-content:center;">📁 Upload Audio File</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader("Choose WAV, MP3, or M4A file", type=["wav", "mp3", "m4a"])
    
    if uploaded:
        st.success("✅ File uploaded successfully!")
        st.audio(uploaded)
        
        file_path = os.path.join(SAVE_DIR, f"user_{uploaded.name}")
        with open(file_path, "wb") as f:
            f.write(uploaded.read())
        
        analyze_audio(file_path, is_raw_audio=False)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ──
st.markdown("""
<div class="footer">
    <strong>🎓 Final Year NLP Project</strong><br>
    Whisper + Llama3.2 (DETAILED Tamil MTI Feedback) + pyttsx3 | Dual Audio Comparison | 
    <span style="color:#6366f1;">Pronunciation Coach Pro v2.0</span>
</div>
""", unsafe_allow_html=True)