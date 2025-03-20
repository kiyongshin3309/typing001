from flask import Flask, render_template, request, jsonify
import time
import hgtk

app = Flask(__name__, static_folder="static")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/check", methods=["GET", "POST"])
def check():
    """ 사용자의 입력값을 처리하는 엔드포인트 """
    print("📌 /check 엔드포인트가 호출됨")  # 로그 확인

    data = request.get_json()
    if not data or "user_input" not in data:
        return jsonify({"error": "user_input 데이터가 전달되지 않았습니다."}), 400

    user_input = data.get("user_input", "").strip()
    if not user_input:
        return jsonify({"error": "입력값이 비어 있습니다."}), 400

    return jsonify({"message": "정상적으로 데이터가 전달되었습니다.", "user_input": user_input})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
