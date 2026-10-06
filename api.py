from flask import Flask, jsonify

app = Flask(__name__)

# Ek simple API route banate hain jo news data return karega
@app.route('/get-news', methods=['GET'])
def get_news():
    news_data = {
        "status": "success",
        "headlines": [
            "Python programming language ab aur bhi popular ho rahi hai.",
            "Jarvis AI assistant successfully update ho gaya hai.",
            "Aaj ka mausam bilkul saaf aur accha hai."
        ]
    }
    return jsonify(news_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)