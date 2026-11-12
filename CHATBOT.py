import argparse
import string
import sys

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)

stop_words = set(stopwords.words('english'))

faq = {
    "admission process apply college": "Admissions open in June. Apply through the college portal.",
    "library working hours timing": "The library is open 8 AM to 8 PM on weekdays.",
    "exam schedule date semester": "Semester exams begin in the last week of November.",
    "placement training companies": "Placement training starts from the 5th semester.",
    "fees payment deadline": "Fees must be paid before the 10th of the semester's first month."
}


def preprocess(text):
    tokens = word_tokenize(text.lower())
    return [t for t in tokens if t not in stop_words and t not in string.punctuation]


def get_response(user_input):
    if not user_input or not user_input.strip():
        return "Please enter a valid question."

    user_tokens = set(preprocess(user_input))
    best_answer, best_score = None, 0.0

    for question, answer in faq.items():
        q_tokens = set(preprocess(question))
        if not user_tokens and not q_tokens:
            score = 1.0
        else:
            score = len(user_tokens & q_tokens) / len(user_tokens | q_tokens) if (user_tokens | q_tokens) else 0.0

        if score > best_score:
            best_score, best_answer = score, answer

    return best_answer if best_score > 0.1 else "Sorry, I don't understand. Please rephrase."


def run_chat_loop():
    print("CampusBot: Hello! Ask me about college services. Type 'bye' to exit.")
    while True:
        try:
            user = input("You: ")
        except EOFError:
            print("\nCampusBot: Input closed. Exiting.")
            break

        if user.strip().lower() == 'bye':
            print("CampusBot: Goodbye!")
            break

        print("CampusBot:", get_response(user))


def launch_gradio():
    try:
        import gradio as gr
    except ImportError as exc:
        raise SystemExit("Install gradio first: pip install gradio") from exc

    demo = gr.Interface(
        fn=get_response,
        inputs=gr.Textbox(
            label="Ask CampusBot",
            placeholder="Ask about college services..."
        ),
        outputs=gr.Textbox(label="CampusBot Response"),
        title="CampusBot - College FAQ Chatbot",
        description="An NLP-based college FAQ chatbot."
    )
    demo.launch()


def main():
    parser = argparse.ArgumentParser(description="CampusBot FAQ chatbot")
    parser.add_argument("--gradio", action="store_true", help="Launch the web interface")
    args = parser.parse_args()

    if args.gradio:
        launch_gradio()
        return

    if sys.stdin.isatty():
        run_chat_loop()
    else:
        print("CampusBot: Running in non-interactive mode.")
        sample_queries = [
            "When do exams start?",
            "What are the library working hours?",
            "How do I apply for admission?",
            "What is the fee payment deadline?"
        ]
        for question in sample_queries:
            print(f"You: {question}\nCampusBot: {get_response(question)}")
        print("Use: python CHATBOT.py to start the interactive chat, or python CHATBOT.py --gradio to launch the web interface.")


if __name__ == "__main__":
    main()
