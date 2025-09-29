from flask import Flask, render_template, request, jsonify
from google.adk.runners import InMemoryRunner
import character
from google.genai import types
import asyncio

app = Flask(__name__)


runner = InMemoryRunner(
    agent=character.root_agent,
    app_name="Demo App",
)

adk_session = None
session_lock = asyncio.Lock()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
async def chat():
    global adk_session
    if adk_session is None:
        async with session_lock:
            if adk_session is None:
                adk_session = await runner.session_service.create_session(
                    app_name=runner.app_name, user_id="inapp_user"
                )

    user_message = request.json.get('message')
    content = types.Content(parts=[types.Part(text=user_message)])
    response_text = ""
    async for event in runner.run_async(
        user_id=adk_session.user_id,
        session_id=adk_session.id,
        new_message=content,
    ):
        if event.content and event.content.parts and event.content.parts[0].text:
            response_text += event.content.parts[0].text

    return jsonify({'response': response_text})


if __name__ == '__main__':
    app.run(debug=True)