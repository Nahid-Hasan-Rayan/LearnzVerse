from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
from openai import OpenAI

# Load environment variables
load_dotenv()

# Set up Flask
app = Flask(__name__, static_folder='static')

# Configure OpenRouter API
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# Tutor system prompts
TUTOR_PROMPTS = {
    "physics": (
        "You are Mr. Newton, an expert Physics tutor. Provide detailed, step-by-step explanations "
        "to help students understand physics concepts. Focus on classical mechanics, thermodynamics, "
        "and problem-solving strategies. Break down complex problems into manageable parts using "
        "clear language and real-world examples."
    ),
    "chemistry": (
        "You are Madam Curie, a Chemistry professor. Specialize in organic chemistry and chemical "
        "reactions. Provide clear explanations with laboratory applications. Help students understand "
        "balancing equations and reaction mechanisms with practical examples and step-by-step guidance."
    ),
    "biology": (
        "You are Dr. Darwin, a Biology expert. Focus on evolution, genetics, and ecology. Explain "
        "complex biological systems with clear analogies. Specialize in cellular biology and human "
        "anatomy, providing detailed explanations with visual descriptions when helpful."
    ),
    "math": (
        "You are Prof. Euler, a Mathematics tutor. Specialize in algebra, calculus, and geometry. "
        "Break down problems into understandable steps with clear explanations. Help students develop "
        "problem-solving skills in trigonometry, statistics, and advanced mathematical concepts."
    )
}

# List of fallback models in order of preference
MODELS = [
    "anthropic/claude-3-haiku",  # Fast and affordable
    "anthropic/claude-3-sonnet",  # Balanced
    "openai/gpt-3.5-turbo",      # Widely available
    "google/gemini-pro"           # Alternative option
]

# Route for main page
@app.route('/')
def index():
    return render_template('learnzverse.html')

# Chat endpoint
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    tutor = data.get('tutor')
    message = data.get('message')
    history = data.get('history', [])

    if not tutor or tutor not in TUTOR_PROMPTS:
        return jsonify({
            "response": "Invalid tutor selected",
            "status": "error"
        }), 400

    if not message:
        return jsonify({
            "response": "Message cannot be empty",
            "status": "error"
        }), 400

    try:
        # Prepare chat messages in OpenAI format
        messages = [{"role": "system", "content": TUTOR_PROMPTS[tutor]}]
        for h in history:
            messages.append({"role": h["role"], "content": h["content"]})
        messages.append({"role": "user", "content": message})

        # Try different models until one works
        last_error = None
        for model in MODELS:
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=1000
                )
                reply = response.choices[0].message.content
                return jsonify({
                    "response": reply,
                    "status": "success",
                    "model": model  # Return which model was used
                })
            except Exception as e:
                last_error = e
                print(f"Error with model {model}: {str(e)}")
                continue

        # If all models failed
        raise last_error if last_error else Exception("All models failed")

    except Exception as e:
        print("Final error:", str(e))
        return jsonify({
            "response": "Sorry, I'm having trouble connecting to the tutor service. Please try again later.",
            "status": "error",
            "error": str(e)
        }), 500

# Run the app
if __name__ == '__main__':
    app.run(debug=True)