import os
from dotenv import load_dotenv

import io
# Robust .env loading for Windows encoding issues
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
if os.path.exists(env_path):
    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(env_path, 'r', encoding='latin-1') as f:
            content = f.read()
    load_dotenv(stream=io.StringIO(content))
else:
    load_dotenv()

# AI Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "YOUR_API_KEY_HERE")
USE_GEMINI = True  # Mode IA avec Google Gemini activé
GEMINI_MODEL = "gemini-2.0-flash" # High performance and modern

# Professional SaaS Design Configuration - Refined Indigo & Slate Palette
COLORS = {
    "primary": "#4F46E5",    # Indigo 600 (More vibrant and professional)
    "primary_dark": "#3730A3", # Indigo 800
    "secondary": "#7C3AED",  # Violet 600
    "accent": "#0EA5E9",     # Sky Blue (More professional than Rose for SaaS)
    "bg_gradient": "linear-gradient(135deg, #F8FAFC 0%, #E2E8F0 100%)",
    "card_bg": "rgba(255, 255, 255, 0.8)",
    "text_main": "#1E293B",  # Slate 800
    "text_muted": "#64748B", # Slate 500
    "border": "rgba(203, 213, 225, 0.5)",
    "success": "#059669",    # Emerald 600
    "warning": "#D97706",    # Amber 600
    "error": "#DC2626",      # Red 600
}

BRAND = {
    "name": "EduQuiz AI",
    "tagline": "L'excellence pédagogique par l'IA.",
    "version": "v2.2.0"
}

STYLES = {
    "shadow_sm": "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1)",
    "shadow_md": "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1)",
    "shadow_lg": "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1)",
    "radius_md": "0.75rem",
    "radius_lg": "1.25rem",
    "glass": "backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); background: rgba(255, 255, 255, 0.85); border: 1px solid rgba(255, 255, 255, 0.3);"
}
