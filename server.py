from flask import Flask, request, send_file
import openai
import tempfile
import os
import uuid
from gtts import gTTS  # لتوليد صوت

openai.api_key = "YOUR_OPENAI_API_KEY"

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_audio():
    audio_file = request.files['audio']
    temp_input = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    audio_file.save(temp_input.name)

    transcript = "أهلا وليدي، ما نقدرش نسمع الصوت تاعك، بصح نحكيلك حكاية..."  # تجريبي، بدون تحويل فعلي

    # الرد من OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "أنت عجوزة جزائرية اسمك حبيبة وتكرتوش، عندك 68 سنة، تتكلمي باللهجة الجزائرية القديمة مع حس دعابة."},
            {"role": "user", "content": transcript}
        ]
    )
    reply_text = response.choices[0].message.content

    # تحويل النص إلى صوت باللهجة الجزائرية
    tts = gTTS(reply_text, lang="ar")  # يمكنك استخدام صوت جزائري احترافي من ElevenLabs مستقبلاً
    filename = f"/tmp/{uuid.uuid4()}.mp3"
    tts.save(filename)

    return send_file(filename, mimetype="audio/mpeg")

if __name__ == "__main__":
    app.run(debug=True)
