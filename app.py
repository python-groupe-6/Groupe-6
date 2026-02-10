import streamlit as st
import sys
import os
import textwrap

# Check critical dependencies
try:
    import google.generativeai
except ImportError as e:
    st.error("⚠️ **Bibliothèques Manquantes ou Environnement Incorrect**")
    st.info(f"Détail de l'erreur : `{e}`")
    st.warning("Il semble que l'application ne trouve pas `google-generativeai`.\n\n"
               "👉 **SOLUTION RECOMMANDÉE** :\n"
               "1. Fermez cette fenêtre.\n"
               "2. Double-cliquez sur le fichier **run_app.bat** à la racine du projet.\n\n"
               "Si le problème persiste, lancez : `.venv\\Scripts\\python -m pip install google-generativeai` dans un terminal.")
    st.stop()

# Check Spacy (Optional / Fallback)
try:
    import spacy
except Exception:
    # Spacy might fail on Python 3.14 (ConfigError) or not be installed.
    # We ignore this here because quiz_generator.py handles the fallback.
    pass

import pandas as pd
from src.pdf_processor import PDFProcessor
from src.quiz_generator import QuizGenerator
from src.report_generator import ReportGenerator
import time
import io
import base64
import plotly.graph_objects as go
import random
from gtts import gTTS
import tempfile
from src.config import COLORS, STYLES, USE_GEMINI, GEMINI_MODEL, BRAND
from src.database import init_database, save_score, get_score_history, get_stats, get_db_mode

# Page configuration
st.set_page_config(
    page_title="EduQuiz AI - Le Futur de la Révision",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def get_img_with_href(local_img_path):
    img_format = local_img_path.split('.')[-1]
    binary_data = get_base64_of_bin_file(local_img_path)
    return f"data:image/{img_format};base64,{binary_data}"

# Try to load assets
hero_base64 = ""
logo_base64 = ""
try:
    hero_base64 = get_img_with_href(os.path.join(os.path.dirname(__file__), "assets", "hero.png"))
except:
    pass

try:
    logo_base64 = get_img_with_href(os.path.join(os.path.dirname(__file__), "assets", "logo.png"))
except:
    pass

def text_to_speech(text):
    """
    Generates an audio file from text and displays it in Streamlit.
    """
    try:
        tts = gTTS(text=text, lang='fr')
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
            tts.save(fp.name)
            return fp.name
    except:
        return None

# Custom CSS for a professional, premium experience
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600&display=swap');

    :root {{
        --primary: {COLORS['primary']};
        --primary-dark: {COLORS['primary_dark']};
        --primary-light: rgba(79, 70, 229, 0.1);
        --secondary: {COLORS['secondary']};
        --accent: {COLORS['accent']};
        --bg-main: #F8FAFC;
        --card-bg: {COLORS['card_bg']};
        --text-main: {COLORS['text_main']};
        --text-muted: {COLORS['text_muted']};
        --border: {COLORS['border']};
        --success: {COLORS['success']};
        --error: {COLORS['error']};
    }}

    .stApp {{
        background: linear-gradient(180deg, #FBFDFF 0%, #F6F9FF 100%),
                    radial-gradient(at 10% 10%, rgba(99,102,241,0.04) 0, transparent 40%),
                    radial-gradient(at 90% 90%, rgba(14,165,233,0.03) 0, transparent 40%);
        background-color: var(--bg-main) !important;
        padding-top: 28px; /* space for sticky navbar */
    }}

    /* Global text color override to ensure visibility */
    .stMarkdown, .stText, p, li, .stMetric div, .stDownloadButton button {{
        color: var(--text-main) !important;
        font-family: 'Inter', sans-serif !important;
    }}

    h1, h2, h3, h4, h5, .outfit {{
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700;
        letter-spacing: -0.02em;
        color: var(--text-main) !important;
        margin-bottom: 0.75rem !important;
    }}

    h1 {{ font-size: 2.5rem !important; line-height: 1.1 !important; }}
    h2 {{ font-size: 1.8rem !important; }}
    h3 {{ font-size: 1.4rem !important; }}

    /* Glass Card - SaaS Premium */
    .glass-card {{
        {STYLES['glass']}
        border-radius: 1rem;
        padding: 1.25rem;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
        margin-bottom: 1.25rem;
        transition: transform 0.28s ease, box-shadow 0.28s ease;
        position: relative;
        overflow: hidden;
    }}
    
    .glass-card:hover {{
        transform: translateY(-4px);
        box-shadow: {STYLES['shadow_lg']};
        border-color: var(--primary);
    }}

    /* Hero Section - Compact & Professional */
    .hero {{
        position: relative;
        text-align: center;
        padding: 3.25rem 2rem;
        background: linear-gradient(135deg, rgba(79,70,229,0.98) 0%, rgba(124,58,237,0.95) 45%, rgba(6,182,212,0.92) 100%);
        border-radius: 1.25rem;
        color: white;
        margin-bottom: 2.25rem;
        box-shadow: 0 24px 50px -20px rgba(15, 23, 42, 0.12);
        overflow: hidden;
        max-width: 1200px;
        margin-left: auto;
        margin-right: auto;
    }}

    .hero::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 20% 50%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(255, 255, 255, 0.08) 0%, transparent 50%);
        pointer-events: none;
    }}

    .hero h1 {{
        color: white !important;
        font-size: 2.8rem !important;
        margin-bottom: 0.5rem !important;
        letter-spacing: -0.01em;
        position: relative;
        z-index: 1;
    }}

    .hero p {{
        color: rgba(255, 255, 255, 0.95) !important;
        font-size: 1rem;
        max-width: 600px;
        margin: 0 auto;
        font-weight: 400;
        position: relative;
        z-index: 1;
    }}

    .logo-container {{
        margin-bottom: 0.75rem;
        animation: float 3s ease-in-out infinite;
        position: relative;
        z-index: 1;
    }}

    .main-logo {{
        width: 96px;
        height: 96px;
        object-fit: contain;
        filter: drop-shadow(0 6px 18px rgba(0,0,0,0.2));
        transition: transform 0.28s ease, filter 0.28s ease;
    }}

    .main-logo:hover {{
        transform: scale(1.05);
        filter: drop-shadow(0 0 25px rgba(255,255,255,0.7));
    }}

    @keyframes float {{
        0% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-8px); }}
        100% {{ transform: translateY(0px); }}
    }}

    /* Better Buttons */
    .stButton>button {{
        border: 1px solid rgba(255, 255, 255, 0.1);
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
        color: white;
        padding: 0.6rem 2rem;
        border-radius: 0.75rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.2);
    }}

    .stButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(79, 70, 229, 0.3);
        background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary) 100%);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }}

    /* Sidebar Refinement */
    [data-testid="stSidebar"] {{
        background-color: #ffffff;
        border-right: 1px solid var(--border);
    }}

    /* Fix Inputs Visibility */
    div[data-baseweb="select"] > div, div[data-testid="stTextInput"] input, div[data-testid="stNumberInput"] input {{
        background-color: #F1F5F9 !important;
        color: var(--text-main) !important;
        border: 1px solid var(--border) !important;
        border-radius: 0.6rem !important;
    }}

    /* Premium Quiz Card */
    .premium-quiz-card {{
        background: white;
        padding: 2.5rem;
        border-radius: 1.5rem;
        border: 1px solid rgba(79, 70, 229, 0.1);
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.05);
        position: relative;
    }}

    .question-header {{
        color: var(--primary);
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}

    /* Feature Card - SaaS Style */
    .feature-card {{
        background: white;
        padding: 2rem 1.5rem;
        border-radius: 1.5rem;
        border: 1px solid var(--border);
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
        box-shadow: {STYLES['shadow_sm']};
    }}
    
    .feature-card:hover {{
        border-color: var(--primary);
        box-shadow: {STYLES['shadow_md']};
        transform: translateY(-5px);
    }}
    
    .icon_circle {{
        width: 64px;
        height: 64px;
        background: var(--primary-light);
        border-radius: 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1.25rem;
        font-size: 1.75rem;
        color: var(--primary);
    }}

    /* Badge & Labels */
    .badge {{
        padding: 0.4rem 1rem;
        border-radius: 2rem;
        font-size: 0.75rem;
        font-weight: 700;
        display: inline-block;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    .badge-primary {{ background: var(--primary-light); color: var(--primary); }}

    /* Stepper Styling */
    .step-box {{
        background: #F1F5F9;
        padding: 1.25rem;
        border-radius: 1rem;
        border: 1px solid var(--border);
        text-align: center;
        transition: all 0.3s ease;
        height: 100%;
        opacity: 0.6;
    }}

    .step-box.active {{
        background: white;
        border: 2px solid var(--primary);
        opacity: 1;
        box-shadow: {STYLES['shadow_md']};
        transform: scale(1.02);
    }}

    .step-box.completed {{
        background: #ECFDF5;
        border: 1px solid var(--success);
        opacity: 1;
        color: var(--success) !important;
    }}

    /* Section Titles */
    .section-title {{
        text-align: center;
        margin: 3rem 0 2rem !important;
        position: relative;
    }}
    
    .section-title::after {{
        content: '';
        display: block;
        width: 40px;
        height: 4px;
        background: var(--primary);
        margin: 0.75rem auto 0;
        border-radius: 2px;
    }}

    /* Animations */
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    .animate-fade-in {{
        animation: fadeIn 0.6s ease-out forwards;
    }}

    /* Footer Styling */
    .footer-container {{
        padding: 4rem 2rem 2rem;
        background: white;
        border-top: 1px solid var(--border);
        margin-top: 4rem;
        border-radius: 2rem 2rem 0 0;
    }}
    
    .footer-column h4 {{
        color: var(--text-main) !important;
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        margin-bottom: 1.5rem !important;
        position: relative;
    }}

    .footer-column h4::after {{
        content: '';
        display: block;
        width: 30px;
        height: 3px;
        background: var(--primary);
        margin-top: 0.5rem;
        border-radius: 2px;
    }}
    
    .footer-link {{
        color: var(--text-muted) !important;
        text-decoration: none !important;
        display: block;
        margin-bottom: 0.8rem;
        transition: all 0.3s ease;
        font-size: 0.95rem;
    }}
    
    .footer-link:hover {{
        color: var(--primary) !important;
        transform: translateX(5px);
    }}
    
    .social-icons {{
        display: flex;
        gap: 0.75rem;
        margin-top: 1.25rem;
    }}
    
    .social-icon {{
        width: 36px;
        height: 36px;
        background: var(--primary-light);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--primary) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        text-decoration: none !important;
        font-size: 1.2rem;
    }}
    
    .social-icon:hover {{
        background: var(--primary);
        color: white !important;
        transform: translateY(-5px);
        box-shadow: 0 10px 15px -3px rgba(79, 70, 229, 0.3);
    }}
    
    .copyright-bar {{
        border-top: 1px solid var(--border);
        margin-top: 3rem;
        padding-top: 1.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: var(--text-muted);
        font-size: 0.85rem;
    }}

    .footer-brand {{
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 800;
        font-size: 1.5rem;
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }}

    /* Professional Navbar Styling - Ultra Robust */
    .navbar-container {{
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        padding: 0.5rem 1.25rem;
        border-radius: 999px;
        border: 1px solid rgba(226,232,240,0.6);
        margin: 0 auto 1.25rem;
        display: block;
        box-shadow: 0 8px 30px rgba(2,6,23,0.06);
        max-width: 1200px;
        position: sticky;
        top: 12px;
        z-index: 9999;
    }}

    .nav-brand-container {{
        font-weight: 800;
        font-size: 1.25rem;
        font-family: 'Plus Jakarta Sans', sans-serif;
        background: {COLORS['primary']}; /* Fallback */
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        white-space: nowrap;
        padding-top: 0.4rem;
    }}

    /* Target Streamlit buttons precisely */
    div[data-testid="stColumn"] .stButton > button {{
        background: transparent !important;
        border: none !important;
        color: var(--text-main) !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.25s ease !important;
        box-shadow: none !important;
        white-space: nowrap !important;
        width: auto !important;
        min-width: 0px !important;
        margin: 0 !important;
    }}

    div[data-testid="stColumn"] .stButton > button:hover {{
        color: var(--primary) !important;
        background: rgba(79, 70, 229, 0.08) !important;
        border-radius: 50px !important;
        transform: translateY(-1px);
    }}

    /* Primary Action Button (Login/Rapport) */
    .nav-login-btn .stButton > button {{
        background: var(--primary) !important;
        color: white !important;
        border-radius: 50px !important;
        padding: 0.5rem 1.5rem !important;
        font-size: 0.95rem !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.2) !important;
    }}

    .nav-login-btn .stButton > button:hover {{
        background: var(--primary-dark) !important;
        color: white !important;
        box-shadow: 0 6px 15px rgba(79, 70, 229, 0.3) !important;
        transform: translateY(-2px);
    }}
    </style>
    """, unsafe_allow_html=True)

def render_navbar():
    """Renders a truly professional top navigation bar."""
    st.markdown("<div class='navbar-container'>", unsafe_allow_html=True)
    
    cols = st.columns([2, 1, 1, 1, 2.5, 1.8])
    
    with cols[0]:
        st.markdown(f"<div class='nav-brand-container'>{BRAND['name']}</div>", unsafe_allow_html=True)
        
    with cols[1]:
        if st.button("Accueil", key="nav_home_pro"):
            st.session_state['current_page'] = "Accueil"
            st.rerun()
            
    with cols[2]:
        if st.button("Menu", key="nav_menu_pro"):
            st.session_state['current_page'] = "Menu"
            st.rerun()
            
    with cols[3]:
        if st.button("Contact", key="nav_contact_pro"):
            st.session_state['current_page'] = "Contact"
            st.rerun()
            
    with cols[5]:
        st.markdown("<div class='nav-login-btn'>", unsafe_allow_html=True)
        if st.session_state.get('is_logged_in', False):
            if st.button("Déconnexion", key="nav_logout_pro", use_container_width=True):
                st.session_state['is_logged_in'] = False
                st.session_state['current_page'] = "Accueil"
                st.rerun()
        else:
            if st.button("Connexion", key="nav_action_pro", use_container_width=True):
                st.session_state['current_page'] = "Connexion"
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_page_menu():
    st.markdown("<div class='animate-fade-in'>", unsafe_allow_html=True)
    st.markdown("## 🎯 Explorez nos fonctionnalités")
    st.markdown("<p style='color: var(--text-muted);'>Tout ce dont vous avez besoin pour maîtriser vos connaissances en un record de temps.</p>", unsafe_allow_html=True)
    
    m_col1, m_col2, m_col3 = st.columns(3)
    
    with m_col1:
        st.markdown("""
            <div class='feature-card'>
                <div class='icon_circle'>📄</div>
                <h4>Analyse Documentaire</h4>
                <p>Extraction intelligente de concepts depuis vos PDF, DOCX et TXT.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Lancer l'importation", key="btn_feat_1", use_container_width=True):
            st.session_state['current_page'] = "Accueil"
            st.session_state['step'] = 1
            st.rerun()

    with m_col2:
        st.markdown("""
            <div class='feature-card'>
                <div class='icon_circle'>✨</div>
                <h4>Synthèse IA</h4>
                <p>Générez des résumés structurés et des points clés en un clic.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Voir la synthèse", key="btn_feat_2", use_container_width=True):
            st.session_state['current_page'] = "Accueil"
            st.session_state['step'] = 2
            st.rerun()

    with m_col3:
        st.markdown("""
            <div class='feature-card'>
                <div class='icon_circle'>🎓</div>
                <h4>Quiz Prédictif</h4>
                <p>Testez vos limites avec des questions générées par IA haute performance.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Démarrer un quiz", key="btn_feat_3", use_container_width=True):
            st.session_state['current_page'] = "Accueil"
            st.session_state['step'] = 3
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    
    m_col4, m_col5, m_col6 = st.columns(3)
    with m_col4:
        st.markdown("""
            <div class='feature-card'>
                <div class='icon_circle'>📊</div>
                <h4>Analytique</h4>
                <p>Suivez votre progression et visualisez votre maîtrise par catégorie.</p>
            </div>
        """, unsafe_allow_html=True)
    with m_col5:
        st.markdown("""
            <div class='feature-card'>
                <div class='icon_circle'>💬</div>
                <h4>Chat Interactif</h4>
                <p>Posez vos questions directement à votre document grâce à notre assistant.</p>
            </div>
        """, unsafe_allow_html=True)
    with m_col6:
        st.markdown("""
            <div class='feature-card'>
                <div class='icon_circle'>🎙️</div>
                <h4>Audio (TTS)</h4>
                <p>Écoutez les explications pour une mémorisation auditive renforcée.</p>
            </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def render_page_contact():
    st.markdown("<div class='animate-fade-in'>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; max-width: 800px; margin: 0 auto;'>", unsafe_allow_html=True)
    st.markdown("## 📧 Contactez-nous")
    st.markdown("<p style='color: var(--text-muted);'>Une question, une suggestion ou un besoin spécifique ? Notre équipe est là pour vous.</p>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='glass-card' style='text-align: left;'>", unsafe_allow_html=True)
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            name = st.text_input("Votre Nom", placeholder="Jean Dupont")
            email = st.text_input("Votre Email", placeholder="jean@example.com")
        with col_c2:
            subject = st.selectbox("Objet", ["Support Technique", "Suggestion", "Partenariat", "Autre"])
            
        message = st.text_area("Votre Message", placeholder="Comment pouvons-nous vous aider ?", height=150)
        
        if st.button("Envoyer le message", key="send_contact", type="primary", use_container_width=True):
            if name and email and message:
                st.success("✅ Votre message a été envoyé avec succès ! Nous vous répondrons sous 24h.")
            else:
                st.error("⚠️ Veuillez remplir tous les champs obligatoires.")
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div></div>", unsafe_allow_html=True)


def render_page_login():
    st.markdown("""
    <style>
    .login-card {
        max-width: 420px;
        margin: 3rem auto;
        padding: 2rem 2.2rem;
        border-radius: 14px;
        background: rgba(255,255,255,0.9);
        box-shadow: 0 12px 30px rgba(0,0,0,0.08);
        text-align: center;
    }

    .login-title {
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 0.2rem;
    }

    .login-sub {
        font-size: 0.85rem;
        color: var(--text-muted);
        margin-bottom: 1.2rem;
    }

    .social-row {
        display: flex;
        gap: 0.6rem;
        margin-bottom: 1.2rem;
    }

    .social-btn {
        flex: 1;
        height: 42px;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        background: white;
        font-size: 0.85rem;
        font-weight: 500;
        cursor: pointer;
    }

    .login-footer {
        font-size: 0.8rem;
        margin-top: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='login-card'>", unsafe_allow_html=True)

    st.markdown("<div class='login-title'>Connexion</div>", unsafe_allow_html=True)
    st.markdown("<div class='login-sub'>Accès EduQuiz IA</div>", unsafe_allow_html=True)

    st.markdown("""
        <div class='social-row'>
            <button class='social-btn'>🌐 Google</button>
            <button class='social-btn'> Apple</button>
        </div>
    """, unsafe_allow_html=True)

    email = st.text_input("Email", placeholder="exemple@email.com", key="login_email")
    password = st.text_input("Mot de passe", type="password", placeholder="••••••••", key="login_pass")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.checkbox("Rester connecté", key="remember_me")
    with col2:
        st.markdown(
            "<div style='text-align:right; margin-top: 0.4rem; font-size:0.8rem;'>"
            "<a href='#'>Oublié ?</a></div>",
            unsafe_allow_html=True
        )

    if st.button("Se connecter", type="primary", use_container_width=True, key="btn_login_final"):
        # Simuler une connexion réussie (à remplacer par une vraie authentification)
        st.session_state['is_logged_in'] = True
        st.session_state['current_page'] = "Accueil"
        st.success("✅ Connexion réussie !")
        time.sleep(1)
        st.rerun()

    st.markdown(
        "<div class='login-footer'>Nouveau ? "
        "<a href='#' style='font-weight:600;'>Créer un compte</a></div>",
        unsafe_allow_html=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

def render_stepper():
    """Renders the progress stepper at the top of the page."""
    steps = [
        (1, "📁", "Import", "Documents"),
        (2, "⚙️", "Config", "Options"),
        (3, "📝", "Quiz", "Test"),
        (4, "🏆", "Bilan", "Résultats")
    ]
    
    current_step = st.session_state.get('step', 1)
    
    st.markdown("<div style='margin-bottom: 2rem;'>", unsafe_allow_html=True)
    cols = st.columns(4)
    
    for col, (idx, icon, title, desc) in zip(cols, steps):
        with col:
            # Determine state
            if idx == current_step:
                css_class = "step-box active"
                status_icon = "🔵"
            elif idx < current_step:
                css_class = "step-box completed"
                status_icon = "✅"
            else:
                css_class = "step-box future"
                status_icon = "⚪"
                
            # Render card
            st.markdown(f"""
                <div class='{css_class}' style='padding: 1rem; min-height: 140px; display: flex; flex-direction: column; justify-content: center; align-items: center;'>
                    <div style='font-size: 1.5rem; margin-bottom: 0.5rem;'>{icon}</div>
                    <div style='font-weight: 700; color: var(--text-main); font-size: 1rem;'>{title}</div>
                    <div style='font-size: 0.75rem; color: var(--text-muted);'>{desc}</div>
                    <div style='margin-top: 0.5rem; font-size: 0.8rem;'>{status_icon}</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Interactive 'Back' button for completed steps
            if idx < current_step:
                if st.button("Modifier", key=f"step_btn_{idx}", use_container_width=True):
                    st.session_state['step'] = idx
                    st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

def initialize_session():
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = "Accueil"
    if 'step' not in st.session_state:
        st.session_state['step'] = 1
    if 'quiz_data' not in st.session_state:
        st.session_state['quiz_data'] = None
    if 'user_answers' not in st.session_state:
        st.session_state['user_answers'] = {}
    if 'score' not in st.session_state:
        st.session_state['score'] = None
    if 'current_q' not in st.session_state:
        st.session_state['current_q'] = 0
    if 'show_flashcards' not in st.session_state:
        st.session_state['show_flashcards'] = False
    if 'score_history' not in st.session_state:
        st.session_state['score_history'] = []
    if 'start_time' not in st.session_state:
        st.session_state['start_time'] = None
    if 'end_time' not in st.session_state:
        st.session_state['end_time'] = None
    if 'time_limit' not in st.session_state:
        st.session_state['time_limit'] = 5  # Default 5 minutes
    if 'seen_onboarding' not in st.session_state:
        st.session_state['seen_onboarding'] = False
    if 'summary' not in st.session_state:
        st.session_state['summary'] = None
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    if 'category_mastery' not in st.session_state:
        st.session_state['category_mastery'] = {}
    if 'num_questions' not in st.session_state:
        st.session_state['num_questions'] = 5
    if 'difficulty' not in st.session_state:
        st.session_state['difficulty'] = "Standard"
    if 'use_ai' not in st.session_state:
        st.session_state['use_ai'] = USE_GEMINI
    if 'is_logged_in' not in st.session_state:
        st.session_state['is_logged_in'] = False
        
    # Handle Navigation via Query Params (Clickable Steps)
    try:
        query_params = st.query_params
        if "step" in query_params:
            target_step = int(query_params["step"])
            
            # Validation Logic
            can_navigate = True
            msg = None
            
            if target_step == 2:
                if 'extracted_text' not in st.session_state or not st.session_state['extracted_text']:
                    can_navigate = False
                    msg = "⚠️ Veuillez d'abord importer un document."
            elif target_step == 3:
                if not st.session_state['quiz_data']:
                    can_navigate = False
                    msg = "⚠️ Veuillez d'abord générer le quiz."
            elif target_step == 4:
                if 'end_time' not in st.session_state or not st.session_state['end_time']:
                    can_navigate = False
                    msg = "⚠️ Vous devez terminer le quiz pour voir les résultats."

            if can_navigate:
                st.session_state['step'] = target_step
            elif msg:
                st.toast(msg, icon="🚫")
                
            # Clear params to prevent stuck navigation on reload
            # st.query_params.clear() # Optional: keep it or clear it. Clearing prevents loop.
    except Exception:
        pass

def main():
    initialize_session()
    
    # Render Navigation Bar only if user is logged in
    if st.session_state.get('is_logged_in', False):
        render_navbar()

    # Sidebar
    with st.sidebar:
        st.markdown(f"#### ⚙️ {BRAND['name']}")
        st.caption(f"{BRAND['tagline']}")
        
        # Mode Switch Selector
        st.markdown("**Moteur de réflexion**")
        use_ai = st.toggle("🤖 Intelligence Artificielle", value=st.session_state['use_ai'], help="Utilise Google Gemini pour une meilleure qualité (gratuit jusqu'à un certain seuil via AI Studio).", key="ai_toggle_sidebar")
        st.session_state['use_ai'] = use_ai
        
        if use_ai:
             st.success("✨ Haute Performance")
        else:
             st.info("🏠 Mode Local")


        st.markdown("**Paramètres**")
        num_questions = st.slider("Questions", 3, 15, st.session_state['num_questions'], key="num_questions_slider")
        st.session_state['num_questions'] = num_questions
        
        difficulty = st.select_slider("Difficulté", options=["Standard", "Avancée", "Expert"], value=st.session_state['difficulty'], key="difficulty_slider")
        st.session_state['difficulty'] = difficulty
        
        time_limit = st.selectbox("⏳ Temps (minutes)", options=[1, 2, 5, 10, 15, 20, 30], index=2, key="time_limit_select")
        st.session_state['time_limit'] = time_limit
        
        # Score History Section (PostgreSQL) - BEFORE AI actions
        st.markdown("---")
        st.markdown("**🏆 Historique des Scores**")
        
        # Initialize database on first run
        init_database()
        
        # Database Status
        db_mode = get_db_mode()
        if db_mode == "PostgreSQL":
             st.success(f"🗄️ DB : {db_mode}")
        elif db_mode == "SQLite":
             st.warning(f"📁 DB : {db_mode}")
        else:
             st.error("❌ DB : Déconnectée")

        # Get history from PostgreSQL
        db_history = get_score_history(5)
        
        if db_history:
            for record in db_history:
                with st.expander(f"Quiz {record['date']}", expanded=False):
                    st.metric("Score", f"{record['score']}%")
                    st.caption(f"Temps: {record['time']}")
                    if record.get('difficulty'):
                        st.caption(f"Niveau: {record['difficulty']}")
        else:
            st.caption("ℹ️ Aucun historique disponible.")
        
        # Stats summary
        stats = get_stats()
        if stats and stats['total_quizzes'] > 0:
            st.markdown("---")
            st.markdown("**📊 Statistiques**")
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                st.metric("Meilleur Score", f"{stats['best_score']}%")
            with col_s2:
                st.metric("Moyenne", f"{stats['avg_score']}%")
        
        if st.button("🔄 Réinitialiser", use_container_width=True):
            for key in list(st.session_state.keys()):
                if key != 'score_history':
                    del st.session_state[key]
            st.rerun()

    # Page Routing
    if st.session_state['current_page'] == "Accueil":
        # Hero Section
        logo_html = f"<div class='logo-container'><img src='{logo_base64}' class='main-logo'></div>" if logo_base64 else ""
        st.markdown(f"""
            <div class='hero'>
                {logo_html}
                <h1>{BRAND['name']}</h1>
                <p>{BRAND['tagline']}</p>
            </div>
        """, unsafe_allow_html=True)

        # Onboarding helper for first-time visitors
        if not st.session_state.get('seen_onboarding'):
            with st.expander("🎓 Guide rapide — Comment ça marche", expanded=True):
                st.markdown("- 1) Importez un document (PDF/DOCX/TXT) via la première étape.\n- 2) Passez à la configuration pour définir le nombre et la difficulté des questions.\n- 3) Générez le quiz et répondez aux questions.\n- 4) Obtenez un rapport détaillé et téléchargez-le.")
                st.info("Conseil : Commencez par un document court (1-3 pages) pour tester la génération rapidement.")
                if st.button("Ne plus afficher ce guide", key="dismiss_onboarding"):
                    st.session_state['seen_onboarding'] = True
                    st.rerun()

        # Global Stepper (Always visible in Accueil)
        render_stepper()
        
        # Original workflow from existing code (indented)
        if st.session_state['step'] == 1:
            st.markdown("<div class='animate-fade-in'>", unsafe_allow_html=True)
            st.markdown("<span class='badge badge-primary'>Étape 1 sur 4</span>", unsafe_allow_html=True)
            st.markdown("### 📤 Importez votre connaissance")
            
            # Step Content
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("#### Document source")
                uploaded_file = st.file_uploader("Glissez votre document ici", type=['pdf', 'docx', 'txt'], label_visibility="collapsed")
                
                if uploaded_file:
                    processor = PDFProcessor()
                    with st.spinner("⚡ Analyse sémantique en cours..."):
                        text = processor.extract_text(uploaded_file)
                        st.session_state['extracted_text'] = text
                        st.toast("C'est prêt !", icon="✅")
                        
                        if st.button("Passer à la configuration ➡️", key="btn_to_step_2_new", use_container_width=True):
                            st.session_state['step'] = 2
                            st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div class='feature-card'>
                        <div class='icon_circle'>📄</div>
                        <h5>Formats supportés</h5>
                        <p style='font-size: 0.85rem; color: #64748B;'>Propulsez vos fichiers PDF, DOCX et TXT vers l'IA.</p>
                    </div>
                """, unsafe_allow_html=True)

            # Marketing Section on Landing Page
            st.markdown("<h3 class='section-title'>L'excellence technologique au service de votre réussite</h3>", unsafe_allow_html=True)
            
            f_col1, f_col2, f_col3 = st.columns(3)
            with f_col1:
                st.markdown(f"""
                    <div class='feature-card'>
                        <div class='icon_circle'>⚡</div>
                        <h4>Vitesse Éclair</h4>
                        <p style='color: var(--text-muted); font-size: 0.9rem;'>Générez vos tests complets en un temps record grâce à notre moteur haute performance.</p>
                    </div>
                """, unsafe_allow_html=True)
            with f_col2:
                st.markdown(f"""
                    <div class='feature-card'>
                        <div class='icon_circle'>🎯</div>
                        <h4>Précision IA</h4>
                        <p style='color: var(--text-muted); font-size: 0.9rem;'>Algorithmes de compréhension sémantique qui extraient uniquement l'essentiel.</p>
                    </div>
                """, unsafe_allow_html=True)
            with f_col3:
                st.markdown(f"""
                    <div class='feature-card'>
                        <div class='icon_circle'>📊</div>
                        <h4>Analytique</h4>
                        <p style='color: var(--text-muted); font-size: 0.9rem;'>Visualisez votre progression et identifiez vos lacunes avec intelligence.</p>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)

        elif st.session_state['step'] == 2:
            st.markdown("<span class='badge badge-primary'>Étape 2 sur 4</span>", unsafe_allow_html=True)
            st.markdown(f"### 🧠 Préparation & Étude")
            
            tab_config, tab_summary, tab_chat = st.tabs(["⚙️ Configuration", "📝 Synthèse (Points Clés)", "💬 Chat avec le Document"])
            
            with tab_config:
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                    st.markdown("#### 📝 Aperçu du contenu")
                    extracted = st.session_state.get('extracted_text')
                    if not extracted:
                        st.warning("Aucun document importé — glissez un fichier dans l'étape 1 pour commencer.")
                        st.markdown("<div style='color: var(--text-muted); font-size:0.95rem;'>Formats acceptés : PDF, DOCX, TXT. Le traitement s'effectue côté serveur.</div>", unsafe_allow_html=True)
                        st.text_area("", "", height=200, disabled=True, label_visibility="collapsed")
                    else:
                        preview = extracted[:800] + ("..." if len(extracted) > 800 else "")
                        st.text_area("", preview, height=250, disabled=True, label_visibility="collapsed")
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                with col2:
                    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                    st.markdown("#### 🚀 Lancer le Quiz")
                    st.info(f"Questions prévues : **{st.session_state['num_questions']}**  \nDifficulté : **{st.session_state['difficulty']}**")

                    # Protect generation when no document is uploaded
                    if not st.session_state.get('extracted_text'):
                        st.button("Lancer la génération magique", key="btn_gen_quiz_disabled_new", use_container_width=True, disabled=True)
                        st.markdown("<div style='color: #9CA3AF; font-size:0.9rem;'>Importez d'abord un document pour activer la génération.</div>", unsafe_allow_html=True)
                    else:
                        if st.button("Lancer la génération magique", key="btn_gen_quiz_active_new", use_container_width=True):
                            generator = QuizGenerator()
                            with st.spinner("🚀 L'IA génère votre quiz personnalisé..."):
                                quiz_data = generator.generate_quiz(
                                    st.session_state['extracted_text'], 
                                    st.session_state['num_questions'], 
                                    st.session_state['difficulty'],
                                    use_ai=st.session_state['use_ai']
                                )
                                st.session_state['quiz_data'] = quiz_data
                                st.session_state['step'] = 3
                                st.session_state['start_time'] = time.time()
                                st.rerun()

                    if st.button("⬅️ Choisir un autre fichier", key="btn_back_to_step_1_new", use_container_width=True):
                        st.session_state['step'] = 1
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)

            with tab_summary:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("#### 📄 Points essentiels à retenir")
                extracted = st.session_state.get('extracted_text')
                if not extracted:
                    st.warning("Importez d'abord un document pour générer la synthèse.")
                else:
                    if st.button("✨ Générer la synthèse magique", key="btn_gen_summary_new", use_container_width=True) or st.session_state.get('summary'):
                        if not st.session_state.get('summary'):
                            generator = QuizGenerator()
                            with st.spinner("Analyse approfondie en cours..."):
                                st.session_state['summary'] = generator.generate_summary(
                                    st.session_state['extracted_text'],
                                    use_ai=st.session_state['use_ai']
                                )

                        for i, point in enumerate(st.session_state['summary']):
                            st.markdown(f"**{i+1}.** {point}")
                st.markdown("</div>", unsafe_allow_html=True)

            with tab_chat:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("#### 🎓 Posez vos questions à votre prof IA")
                
                # Display chat history
                extracted = st.session_state.get('extracted_text')
                # Show previous messages (if any)
                for chat in st.session_state.get('chat_history', []):
                    with st.chat_message(chat["role"]):
                        st.markdown(chat["content"])

                if not extracted:
                    st.info("Le chat est disponible après import du document. Importez un fichier à l'étape 1, puis revenez ici.")
                else:
                    if prompt_msg := st.chat_input("Ex: Peux-tu m'expliquer le concept de..."):
                        st.session_state['chat_history'].append({"role": "user", "content": prompt_msg})
                        with st.chat_message("user"):
                            st.markdown(prompt_msg)
                        generator = QuizGenerator()
                        with st.chat_message("assistant"):
                            with st.spinner("Réflexion..."):
                                response = generator.chat_with_document(
                                    st.session_state['extracted_text'], 
                                    prompt_msg, 
                                    st.session_state['chat_history'],
                                    use_ai=st.session_state['use_ai']
                                )
                                st.markdown(response)
                        st.session_state['chat_history'].append({"role": "assistant", "content": response})
                        st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

        elif st.session_state['step'] == 3:
            st.markdown("<span class='badge badge-primary'>Étape 3 sur 4</span>", unsafe_allow_html=True)
            st.markdown("### 📝 Testez vos connaissances")
            
            if st.session_state['quiz_data']:
                quiz_data = st.session_state['quiz_data']
                
                # Check for error state in quiz data
                is_error_state = any("⚠️" in q.get('question', '') for q in quiz_data)
                
                if is_error_state:
                    st.markdown("<div class='glass-card' style='border-left: 5px solid var(--error);'>", unsafe_allow_html=True)
                    st.markdown("### 🛠️ Configuration Requise")
                    st.error(quiz_data[0]['question'])
                    st.write(quiz_data[0]['explanation'])
                    
                    col_err1, col_err2 = st.columns(2)
                    with col_err1:
                         if st.button("⬅️ Retour au document", key="btn_error_back_new", use_container_width=True):
                             st.session_state['step'] = 2
                             st.rerun()
                    with col_err2:
                         st.info("💡 Conseil : Utilisez une clé API OpenAI pour une expérience sans installation locale.")
                    st.markdown("</div>", unsafe_allow_html=True)
                    st.stop()

                current_idx = st.session_state['current_q']
                q = quiz_data[current_idx]
                
                # Progress bar
                progress = (current_idx + 1) / len(quiz_data)
                st.progress(progress)
                st.caption(f"Question {current_idx + 1} sur {len(quiz_data)}")

                st.markdown(f"""
                    <div class='premium-quiz-card'>
                        <div class='question-header'>
                            <span>🧩 Question d'analyse</span>
                        </div>
                        <h2 style='font-size: 1.6rem; color: #1E293B; line-height: 1.4; margin-bottom: 1.5rem;'>
                            {q['question']}
                        </h2>
                    </div>
                """, unsafe_allow_html=True)
                
                # Options in a clean radio group
                selected_option = st.radio(
                    "Votre réponse :",
                    q['options'],
                    index=q['options'].index(st.session_state['user_answers'].get(current_idx)) if current_idx in st.session_state['user_answers'] and st.session_state['user_answers'][current_idx] in q['options'] else None,
                    key=f"q_radio_{current_idx}",
                    label_visibility="collapsed"
                )
                
                if selected_option:
                    st.session_state['user_answers'][current_idx] = selected_option

                # Navigation buttons
                col_prev, col_next = st.columns([1, 1])
                with col_prev:
                    if current_idx > 0:
                        if st.button("⬅️ Précédent", key="btn_q_prev_new", use_container_width=True):
                            st.session_state['current_q'] -= 1
                            st.rerun()
                
                with col_next:
                    if current_idx < len(quiz_data) - 1:
                        if st.button("Suivant ➡️", key="btn_q_next_new", use_container_width=True, disabled=selected_option is None):
                            st.session_state['current_q'] += 1
                            st.rerun()
                    else:
                        total_answered = len(st.session_state['user_answers'])
                        is_ready = total_answered >= len(quiz_data)
                        if st.button("🎯 Terminer le Quiz", key="btn_q_finish_new", use_container_width=True, type="primary", disabled=not is_ready):
                            st.session_state['end_time'] = time.time()
                            st.session_state['step'] = 4
                            
                            # Calculate results and save to history
                            correct = 0
                            for idx, q in enumerate(quiz_data):
                                if st.session_state['user_answers'].get(idx) == q['answer']:
                                    correct += 1
                            perc = round((correct / len(quiz_data)) * 100)
                            duration = round(st.session_state['end_time'] - st.session_state['start_time'])
                            mins, secs = divmod(duration, 60)
                            time_str = f"{mins}m {secs}s"
                            
                            # Save to PostgreSQL database
                            save_score(perc, time_str, len(quiz_data), difficulty)
                            st.rerun()
                
                # Professional Countdown Timer Display
                if st.session_state['start_time'] and not st.session_state['end_time']:
                    total_seconds_allowed = st.session_state['time_limit'] * 60
                    elapsed = time.time() - st.session_state['start_time']
                    remaining = total_seconds_allowed - elapsed
                    
                    if remaining <= 0:
                        remaining = 0
                        # Auto-submit
                        st.session_state['end_time'] = time.time()
                        st.session_state['step'] = 4
                        
                        correct = 0
                        for idx, q in enumerate(quiz_data):
                            if st.session_state['user_answers'].get(idx) == q['answer']:
                                correct += 1
                        perc = round((correct / len(quiz_data)) * 100)
                        
                        # Save to PostgreSQL database
                        save_score(perc, f"{st.session_state['time_limit']}m (Temps écoulé)", len(quiz_data), difficulty)
                        st.warning("⌛ Temps écoulé ! Vos réponses ont été soumises automatiquement.")
                        time.sleep(2)
                        st.rerun()

                    rmins, rsecs = divmod(int(remaining), 60)
                    
                    # Dynamic coloring: Red if less than 30 seconds
                    timer_color = "#EF4444" if remaining < 30 else "#6366F1"
                    bg_color = "rgba(239, 68, 68, 0.1)" if remaining < 30 else "rgba(99, 102, 241, 0.05)"
                    
                    st.markdown(f"""
                        <div style='text-align: center; padding: 1rem; background: {bg_color}; border-radius: 1rem; border: 1px solid {timer_color}33; margin-top: 1rem;'>
                            <p style='margin: 0; color: {timer_color}; font-weight: 600; font-size: 0.9rem;'>⏳ TEMPS RESTANT</p>
                            <h2 style='margin: 0; color: {timer_color};'>{rmins:02d}:{rsecs:02d}</h2>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Small auto-refresh
                    time.sleep(0.1)
                    st.rerun()
            else:
                st.error("Une erreur est survenue lors de la génération. Veuillez réessayer.")
                if st.button("Retour", key="btn_quiz_error_retry_new"):
                    st.session_state['step'] = 2
                    st.rerun()

        elif st.session_state['step'] == 4:
            if not st.session_state.get('quiz_data'):
                st.warning("⚠️ Aucun quiz n'est disponible pour l'affichage des résultats.")
                if st.button("Retour à l'étape 1", key="btn_results_back_step_1_new", use_container_width=True):
                    st.session_state['step'] = 1
                    st.rerun()
                st.stop()
                
            st.markdown("<span class='badge badge-primary'>Étape finale</span>", unsafe_allow_html=True)
            st.markdown("### 🏆 Résultats de la Session")
            
            correct_count = 0
            quiz_data = st.session_state['quiz_data']
            user_answers = st.session_state['user_answers']
            
            for i, q in enumerate(quiz_data):
                if user_answers.get(i) == q['answer']:
                    correct_count += 1
            
            percentage = (correct_count / len(quiz_data)) * 100
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                
                # Gauge Chart for Score
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = percentage,
                    number = {'suffix': "%", 'font': {'color': COLORS['text_main'], 'family': 'Inter'}},
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Points Importants", 'font': {'size': 18, 'color': COLORS['text_muted']}},
                    gauge = {
                        'axis': {'range': [0, 100], 'tickcolor': COLORS['text_muted']},
                        'bar': {'color': COLORS['primary']},
                        'bgcolor': "white",
                        'borderwidth': 2,
                        'bordercolor': COLORS['border'],
                        'steps' : [
                            {'range': [0, 50], 'color': "rgba(239, 68, 68, 0.05)"},
                            {'range': [50, 80], 'color': "rgba(245, 158, 11, 0.05)"},
                            {'range': [80, 100], 'color': "rgba(16, 185, 129, 0.05)"}
                        ],
                    }
                ))
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    height=220, 
                    margin=dict(l=30, r=30, t=50, b=20),
                    font={'color': COLORS['text_main']}
                )
                st.plotly_chart(fig, use_container_width=True)

                st.markdown(f"""
                    <div class='metric-box'>
                        <h3 style='margin:0;'>{correct_count} / {len(quiz_data)}</h3>
                        <p style='color: #64748B; margin:0;'>Questions correctes</p>
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Categories for the radar chart (Mastery per pillar)
                categories = ["Compréhension", "Analyse", "Mémorisation", "Application", "Synthèse"]
                # Map mastery from session state or use default
                mastery = st.session_state.get('category_mastery', {})
                if mastery:
                    categories = list(mastery.keys())
                    values = list(mastery.values())
                else:
                    # Provide dummy values based on overall percentage if no detailed mastery
                    values = [percentage] * len(categories)

                fig_radar = go.Figure(data=go.Scatterpolar(
                    r=values,
                    theta=categories,
                    fill='toself',
                    line=dict(color=COLORS['primary'], width=2),
                    fillcolor=f"rgba(99, 102, 241, 0.15)"
                ))
                
                fig_radar.update_layout(
                    polar=dict(
                        radialaxis=dict(visible=True, range=[0, 100], tickfont={'size': 8}, gridcolor=COLORS['border']),
                        angularaxis=dict(tickfont={'size': 10}, gridcolor=COLORS['border']),
                        bgcolor='rgba(0,0,0,0)'
                    ),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    showlegend=False,
                    height=350,
                    margin=dict(l=60, r=60, t=40, b=40),
                    font={'color': COLORS['text_main']}
                )
                st.plotly_chart(fig_radar, use_container_width=True)

                st.markdown("<br>", unsafe_allow_html=True)
                
                # Download PDF using the new ReportGenerator
                report_gen = ReportGenerator(BRAND['name'])
                pdf_data = report_gen.generate_quiz_report(quiz_data, user_answers, correct_count, percentage)
                
                st.download_button(
                    label="📥 Télécharger le rapport (PDF)",
                    data=pdf_data,
                    file_name="resultats_quiz.pdf",
                    mime="application/pdf",
                    key="btn_download_report_new",
                    use_container_width=True
                )

                if st.button("🔄 Nouveau Quiz", key="btn_new_quiz_final_new", use_container_width=True):
                    st.session_state['step'] = 1
                    st.session_state['quiz_data'] = None
                    st.session_state['user_answers'] = {}
                    st.session_state['current_q'] = 0
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

            with col2:
                st.markdown("<div class='glass-card' style='max-height: 500px; overflow-y: auto; padding: 2rem;'>", unsafe_allow_html=True)
                st.subheader("📝 Correction Détaillée")
                
                for i, q in enumerate(quiz_data):
                    user_ans = user_answers.get(i)
                    if user_ans == q['answer']:
                        st.markdown(f"✅ **Question {i+1}**")
                    else:
                        st.markdown(f"❌ **Question {i+1}**")
                    
                    st.write(q['question'])
                    if user_ans != q['answer']:
                        st.markdown(f"<span style='color: var(--error)'>Votre réponse : {user_ans}</span>", unsafe_allow_html=True)
                    st.markdown(f"<span style='color: var(--success)'>Bonne réponse : {q['answer']}</span>", unsafe_allow_html=True)
                    
                    with st.expander("💡 Pourquoi ? (Explication)"):
                        st.write(q.get('explanation', "Aucune explication disponible."))
                        if st.button("🔊 Play", key=f"tts_exp_new_{i}"):
                            audio_path = text_to_speech(q.get('explanation', ''))
                            if audio_path:
                                st.audio(audio_path, format="audio/mp3", autoplay=True)
                    st.divider()
                st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state['current_page'] == "Menu":
        render_page_menu()
    elif st.session_state['current_page'] == "Contact":
        render_page_contact()
    elif st.session_state['current_page'] == "Connexion":
        render_page_login()

    # Professional Footer
    st.markdown("<div class='footer-container'>", unsafe_allow_html=True)
    f_col1, f_col2, f_col3, f_col4 = st.columns([1.5, 1, 1, 1.2])
    
    with f_col1:
        st.markdown(f"<div class='footer-brand'>{BRAND['name']}</div>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: var(--text-muted); font-size: 0.95rem; line-height: 1.6;'>{BRAND['tagline']}<br>L'IA au service de l'excellence éducative.</p>", unsafe_allow_html=True)
        st.markdown("""
            <div class='social-icons'>
                <a href='#' class='social-icon'>𝕏</a>
                <a href='#' class='social-icon'>in</a>
                <a href='#' class='social-icon'> f </a>
            </div>
        """, unsafe_allow_html=True)
        
    with f_col2:
        st.markdown("<div class='footer-column'><h4>Navigation</h4></div>", unsafe_allow_html=True)
        st.markdown("<a href='#' class='footer-link'>Accueil</a>", unsafe_allow_html=True)
        st.markdown("<a href='#' class='footer-link'>Fonctionnalités</a>", unsafe_allow_html=True)
        st.markdown("<a href='#' class='footer-link'>Tarification</a>", unsafe_allow_html=True)
        st.markdown("<a href='#' class='footer-link'>Contact</a>", unsafe_allow_html=True)
        
    with f_col3:
        st.markdown("<div class='footer-column'><h4>Légal</h4></div>", unsafe_allow_html=True)
        st.markdown("<a href='#' class='footer-link'>Confidentialité</a>", unsafe_allow_html=True)
        st.markdown("<a href='#' class='footer-link'>Conditions d'utilisation</a>", unsafe_allow_html=True)
        st.markdown("<a href='#' class='footer-link'>Mentions Légales</a>", unsafe_allow_html=True)
        
    with f_col4:
        st.markdown("<div class='footer-column'><h4>Newsletter</h4></div>", unsafe_allow_html=True)
        st.markdown("<p style='color: var(--text-muted); font-size: 0.85rem;'>Recevez les dernières mises à jour sur l'IA éducative.</p>", unsafe_allow_html=True)
        # Simple Visual Newsletter Input (since we don't have a backend for this yet)
        email = st.text_input("Email", placeholder="votre@email.com", key="footer_newsletter", label_visibility="collapsed")
        if st.button("S'abonner", key="footer_subscribe_btn", use_container_width=True):
            st.toast("Merci pour votre inscription !", icon="🎉")

    st.markdown(f"""
        <div class='copyright-bar'>
            <div>© 2026 {BRAND['name']}. Tous droits réservés.</div>
            <div style='display: flex; gap: 1.5rem;'>
                <span>Fait avec ❤️ pour l'éducation</span>
                <span>Version 2.2.0</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
