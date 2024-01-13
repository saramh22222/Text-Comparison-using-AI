from flask import Flask, render_template, request
import google.generativeai as genai

app = Flask(__name__)

genai.configure(api_key="AIzaSyAKnWwc0R1eamUpSTTT_LKkB34E9K-Yl90")

defaults = {
    'model': 'models/text-bison-001',
    'temperature': 0.7,
    'candidate_count': 1,
    'top_k': 40,
    'top_p': 0.95,
    'max_output_tokens': 1024,
    'stop_sequences': [],
    'safety_settings': [
        {"category": "HARM_CATEGORY_DEROGATORY", "threshold": 1},
        {"category": "HARM_CATEGORY_TOXICITY", "threshold": 1},
        {"category": "HARM_CATEGORY_VIOLENCE", "threshold": 2},
        {"category": "HARM_CATEGORY_SEXUAL", "threshold": 2},
        {"category": "HARM_CATEGORY_MEDICAL", "threshold": 2},
        {"category": "HARM_CATEGORY_DANGEROUS", "threshold": 2},
    ],
}
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compare', methods=['POST'])
def compare():
    text1 = request.form['text1']
    text2 = request.form['text2']

    prompt = f"Text 1: {text1}\nText 2: {text2} two text has the same meaning:\n"

    response = genai.generate_text(
        **defaults,
        prompt=prompt
    )

    similarity_score = 0  # Default score if no similarity indication is found

    if response.result:
        similarity_text = response.result.lower()
        if 'yes' in similarity_text:
            similarity_score = 2
        elif 'no' in similarity_text:
            similarity_score = 0

    return render_template('index.html', similarity_score=similarity_score)

if __name__ == '__main__':
    app.run(debug=True)