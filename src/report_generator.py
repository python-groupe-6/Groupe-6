from fpdf import FPDF
from fpdf.enums import XPos, YPos
import io

class ReportGenerator:
    def __init__(self, brand_name="EduQuiz AI"):
        self.brand_name = brand_name

    def clean_text(self, text):
        """
        Force conversion to Latin-1 by replacing unsupported characters.
        This is a fallback since we don't bundle a custom TTF font.
        """
        if not text:
            return ""
        
        # Mapping of common Unicode characters to Latin-1 equivalents
        replacements = {
            '’': "'", '‘': "'", '“': '"', '”': '"',
            '«': '"', '»': '"', '–': '-', '—': '-',
            '\u202f': ' ', '\u00a0': ' ', '…': '...',
            '€': 'EUR', 'œ': 'oe', 'Œ': 'OE'
        }
        
        for old, new in replacements.items():
            text = str(text).replace(old, new)
            
        # Standardize whitespace
        text = " ".join(text.split())
        
        return text.encode('latin-1', 'replace').decode('latin-1')

    def generate_quiz_report(self, quiz_data, user_answers, correct_count, percentage):
        """
        Creates a professional PDF report.
        """
        pdf = FPDF()
        pdf.add_page()
        
        # Header
        pdf.set_font("Helvetica", "B", 20)
        pdf.set_text_color(99, 102, 241) # Primary color hex #6366F1 -> (99, 102, 241)
        pdf.cell(190, 15, self.clean_text(self.brand_name), border=0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        
        pdf.set_font("Helvetica", "B", 16)
        pdf.set_text_color(15, 23, 42) # Text main color
        pdf.cell(190, 10, self.clean_text("Rapport de Performance"), border=0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        pdf.ln(10)
        
        # Summary Box
        pdf.set_fill_color(248, 250, 252)
        pdf.rect(10, 45, 190, 30, 'F')
        
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_xy(15, 50)
        pdf.cell(50, 10, self.clean_text(f"Score : {correct_count} / {len(quiz_data)}"))
        pdf.set_xy(15, 60)
        pdf.cell(50, 10, self.clean_text(f"Taux de réussite : {percentage}%"))
        
        status = "Excellent !" if percentage >= 80 else "Bon travail" if percentage >= 50 else "A réviser"
        pdf.set_xy(140, 55)
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(50, 10, self.clean_text(status), align="R")
        
        pdf.ln(25)
        
        # Questions and Answers
        for i, q in enumerate(quiz_data):
            # Question block
            pdf.set_font("Helvetica", "B", 12)
            pdf.set_text_color(15, 23, 42)
            pdf.multi_cell(190, 10, self.clean_text(f"Question {i+1}: {q['question']}"))
            
            # Answer comparison
            user_ans = user_answers.get(i)
            is_correct = user_ans == q['answer']
            
            pdf.set_font("Helvetica", "", 11)
            if is_correct:
                pdf.set_text_color(16, 185, 129) # Success
                pdf.multi_cell(190, 8, self.clean_text(f"Votre réponse : {user_ans} (Correct)"))
            else:
                pdf.set_text_color(239, 68, 68) # Error
                pdf.multi_cell(190, 8, self.clean_text(f"Votre réponse : {user_ans}"))
                pdf.set_text_color(16, 185, 129)
                pdf.multi_cell(190, 8, self.clean_text(f"Réponse correcte : {q['answer']}"))
            
            # Explanation
            pdf.set_font("Helvetica", "I", 10)
            pdf.set_text_color(100, 116, 139) # Muted
            pdf.multi_cell(190, 7, self.clean_text(f"Explication : {q.get('explanation', '')}"))
            
            pdf.ln(5)
            # Thin line separator
            pdf.set_draw_color(226, 232, 240)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(5)
            
            # Check for page break
            if pdf.get_y() > 250:
                pdf.add_page()

        return bytes(pdf.output())
