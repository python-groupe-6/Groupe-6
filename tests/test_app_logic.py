
import os
import sys
from report_generator import ReportGenerator
from quiz_generator import QuizGenerator
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def test_quiz_and_report_generation():
    logging.info("Starting Logic Test...")

    # 1. Mock Data
    dummy_text = """
    La Révolution française est une période de bouleversements sociaux et politiques radicaux en France, 
    de 1789 à 1799. Elle a profondément affecté l'histoire de la France et plus largement celle de tout l'Europe.
    La prise de la Bastille le 14 juillet 1789 est considérée comme le début symbolique de la Révolution.
    """
    
    logging.info("1. Text Content Ready")

    # 2. Test Quiz Generation
    logging.info("2. Testing Quiz Generation...")
    quiz_gen = QuizGenerator()
    # Force generic/local generation if OpenAI key is not set to avoid API costs during test or if key is missing
    # But strictly speaking we want to test what the app uses. 
    # Let's try to generate.
    
    try:
        quiz_data = quiz_gen.generate_quiz(dummy_text, num_questions=2, difficulty="Standard")
        logging.info(f"   Quiz Generated: {len(quiz_data)} questions.")
        if len(quiz_data) > 0:
            logging.info(f"   Sample Question: {quiz_data[0]['question']}")
    except Exception as e:
        logging.error(f"   Quiz Generation Failed: {e}")
        return

    # 3. Test PDF Report Generation
    logging.info("3. Testing PDF Report Generation...")
    report_gen = ReportGenerator()
    
    # Mock user answers (all correct for simplicity)
    user_answers = {i: q['answer'] for i, q in enumerate(quiz_data)}
    correct_count = len(quiz_data)
    percentage = 100.0
    
    try:
        pdf_bytes = report_gen.generate_quiz_report(quiz_data, user_answers, correct_count, percentage)
        logging.info(f"   PDF generated successfully. Size: {len(pdf_bytes)} bytes.")
        
        # Save to disk to verify
        output_path = "test_report.pdf"
        with open(output_path, "wb") as f:
            f.write(pdf_bytes)
        logging.info(f"   PDF saved to {output_path} for manual inspection if needed.")
        
    except Exception as e:
        logging.error(f"   PDF Generation Failed: {e}")
        import traceback
        traceback.print_exc()
        return

    logging.info("Test Completed Successfully!")

if __name__ == "__main__":
    test_quiz_and_report_generation()
