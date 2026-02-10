import re
import os

path = r"c:\Users\Mamadou Bassirou Dia\OneDrive\Documents\Projet Revisions-EduQuiz AI\app.py"

with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Replace the broken lines using broad regex
content = re.sub(r'st\.markdown\("\*\*.*?Historique des Scores\*\*"\)', 'st.markdown("**🏆 Historique des Scores**")', content)
content = re.sub(r'st\.markdown\("\*\*.*?Statistiques\*\*"\)', 'st.markdown("**📊 Statistiques**")', content)

# Also ensure the CSS is correct (just in case)
content = content.replace('.stMarkdown, .stText, p, li, span, label {{', '.stMarkdown, .stText, p, li, .stMetric div, .stDownloadButton button {{')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Repair complete.")
