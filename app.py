from flask import Flask, request
from datetime import datetime

app = Flask(__name__)
messages = []

@app.route("/")
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Rendi Chat</title>
        <style>
            body { font-family: Arial; background: #f0f0f0; margin: 0; padding: 0; }
            #container { max-width: 600px; margin: auto; padding: 20px; background: white; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); animation: fadeIn 1s ease-in-out; }
            @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
            input, button { padding: 10px; margin: 5px 0; width: 100%; }
            #chat { border: 1px solid #ccc; padding: 10px; height: 200px; overflow-y: scroll; background: #fafafa; }
        </style>
    </head>
    <body>
        <div id="container">
            <h2>Rendi Marzikri Realtime Chat</h2>
            <div id="chat"></div>
            <input type="text" id="msg" placeholder="Ketik pesan..." />
            <button onclick="sendMsg()">Kirim</button>
        </div>
        <script>
            async function loadChat() {
                let res = await fetch("/chat");
                let data = await res.text();
                document.getElementById("chat").innerHTML = data;
            }
            async function sendMsg() {
                let msg = document.getElementById("msg").value;
                if (msg.trim() === "") return;
                await fetch("/send", {
                    method: "POST",
                    headers: { "Content-Type": "application/x-www-form-urlencoded" },
                    body: "msg=" + encodeURIComponent(msg)
                });
                document.getElementById("msg").value = "";
            }
            setInterval(loadChat, 1000);
            loadChat();
        </script>
    </body>
    </html>
    '''

@app.route("/chat")
def chat():
    return "<br>".join(f"{m['time']} - {m['text']}" for m in messages[-50:])

@app.route("/send", methods=["POST"])
def send():
    text = request.form.get("msg")
    if text:
        messages.append({"time": datetime.now().strftime("%H:%M:%S"), "text": text})
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
