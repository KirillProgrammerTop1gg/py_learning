from flask import Flask, render_template, request, redirect, url_for
from google import genai
from google.genai import types
import os, requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

app = Flask(__name__)
client = genai.Client(api_key=GEMINI_API_KEY)


def run_inference(msg):
    inference = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=msg,
        config=types.GenerateContentConfig(system_instruction="""
                You must return ONLY raw HTML.
                Do NOT use markdown.
                Do NOT wrap the answer in ```html.
                The response must start with <div and end with </div>.
                Use inline styles only.
                Return nothing except the HTML.
            """),
    )

    return {
        "inference_text": inference.text,
        "inference_tokens": inference.usage_metadata.total_token_count,
    }

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/ai_html", methods=["GET", "POST"])
def ai_html():
    if request.method == "POST":
        ai_msg = request.form["msg"]
        ai_response = run_inference(ai_msg)

        return render_template(
            "ai_html.html",
            ai_answer=ai_response["inference_text"],
            ai_token_usage=ai_response["inference_tokens"],
        )

    return render_template("ai_html.html")

@app.route("/qr_generator", methods=["GET", "POST"])
def qr_generator():
    if request.method == "POST":
        qr_data = request.form["info"]

        return render_template("qr_generator.html", qr_url=f'https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={qr_data}')

    return render_template("qr_generator.html")


# API

@app.route("/api/ai/inference", methods=["POST"])
def ai_inference():
    if not request.is_json:
        return {"error": "Request must be JSON"}, 400

    data = request.get_json()
    message_to_ai = data.get("msg", "")

    if not message_to_ai:
        return {"error": "Request must have 'msg' field"}, 400

    return run_inference(message_to_ai)


if __name__ == "__main__":
    app.run(debug=True, port=1700)
