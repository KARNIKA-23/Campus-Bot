#Step 1 — Environment Setup (5 minutes)
#Open Google Colab → New Notebook. Run:
import nltk
nltk.download('punkt_tab')
nltk.download('stopwords')
#Step 2 — Build the Preprocessing Pipeline (8 minutes)
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

stop_words = set(stopwords.words('english'))

def preprocess(text):
    tokens = word_tokenize(text.lower())
    return [t for t in tokens if t not in stop_words and t not in string.punctuation]

# Test it
print(preprocess("What are the library working hours?"))
# Expected output: ['library', 'working', 'hours']
#  Checkpoint 1: Preprocessing removes stopwords and punctuation correctly.
#Step 3 — Create the Knowledge Base (5 minutes)
faq = {
"admission process apply college": "Admissions open in June. Apply through the college portal.",
"library working hours timing": "The library is open 8 AM to 8 PM on weekdays.",
"exam schedule date semester": "Semester exams begin in the last week of November.",
"placement training companies": "Placement training starts from the 5th semester.",
"fees payment deadline": "Fees must be paid before the 10th of the semester's first month."
}
#Students may add 2–3 questions of their own.
#Step 4 — Implement the Matching Logic (7 minutes)
def get_response(user_input):
    user_tokens = set(preprocess(user_input))
    best_answer, best_score = None, 0
    for question, answer in faq.items():
        q_tokens = set(preprocess(question))
        score = len(user_tokens & q_tokens) / len(user_tokens | q_tokens)  # Jaccard similarity
        if score > best_score:
            best_score, best_answer = score, answer
    return best_answer if best_score > 0.1 else "Sorry, I don't understand. Please rephrase."
#Checkpoint 2: get_response("When do exams start?") returns the exam schedule answer.
#Step 5 — Run the Chat Loop and Test (5 minutes)
print("CampusBot: Hello! Ask me about college services. Type 'bye' to exit.")
while True:
    user = input("You: ")
    if user.lower() == 'bye':
        print("CampusBot: Goodbye!")
        break
    print("CampusBot:", get_response(user))
#Test with at least 5 queries, including one the bot should fail on.
Optional Stretch Goal — Simple Web UI (for early finishers)
!pip install gradio -q
import gradio as gr
gr.Interface(fn=get_response, inputs="text", outputs="text", title="CampusBot").launch()
