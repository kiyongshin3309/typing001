from flask import Flask, render_template, request, jsonify
import time
import hgtk

app = Flask(__name__, static_folder="static")

# 연습할 문장 리스트
WORD_LIST = [
    "네가 희망이 있으므로 안전할 것이며 두루 살펴보고 평안히 쉬리라 욥기 11장 18절",
    "You will be secure, because there is hope",
    "you will look about you and take your rest in safety Job 11:18",
]

# 전역 변수
current_count = 0
results = []
start_time = 0

@app.route("/")
def index():
    """ 메인 페이지 렌더링 """
    global current_count, results, start_time
    current_count = 0
    results = []
    start_time = time.time()  # 연습 시작 시간 초기화
    return render_template("index.html", word=WORD_LIST[current_count])

@app.route("/check", methods=["GET", "POST"])
def check():
    """ 사용자가 입력한 문장을 비교하고 결과 반환 """
    global current_count, results, start_time

    if current_count >= len(WORD_LIST):
        return jsonify({"finished": True})

    # 요청 데이터 확인
    data = request.get_json()
    if not data or "user_input" not in data:
        return jsonify({"error": "user_input 데이터가 전달되지 않았습니다."}), 400

    user_input = data.get("user_input", "").strip()

    if not user_input:
        return jsonify({"error": "입력값이 비어 있습니다."}), 400

    # 📌 디버깅: 원본과 입력된 문장 출력
    src = hgtk.text.decompose(WORD_LIST[current_count]).replace("ᴥ", "")
    tar = hgtk.text.decompose(user_input).replace("ᴥ", "")

    print(f"📝 원본 (src): {src}")
    print(f"⌨ 사용자 입력 (tar): {tar}")

    correct = sum(1 for c1, c2 in zip(src, tar) if c1 == c2)
    print(f"✅ 맞은 글자 개수 (correct): {correct}")

    src_len = len(src)
    accuracy = (correct / src_len) * 100 if src_len > 0 else 0
    typo_rate = ((src_len - correct) / src_len) * 100 if src_len > 0 else 0

    # 🚀 속도 계산 (0초 방지)
    end_time = time.time() - start_time
    if end_time < 0.01:
        end_time = 0.01

    speed = (correct / end_time) * 60 if end_time > 0 else 0

    results.append((speed, accuracy, typo_rate))
    current_count += 1

    result_text = f"속도: {speed:.2f} 정확도: {accuracy:.2f}% 오타율: {typo_rate:.2f}%"

    if current_count < len(WORD_LIST):
        next_word = WORD_LIST[current_count]
    else:
        next_word = "연습이 끝났습니다."
        avg_speed = sum(r[0] for r in results) / len(results)
        avg_accuracy = sum(r[1] for r in results) / len(results)
        avg_typo_rate = sum(r[2] for r in results) / len(results)
        avg_result = f"평균 속도: {avg_speed:.2f}, 정확도: {avg_accuracy:.2f}%, 오타율: {avg_typo_rate:.2f}%"
        return jsonify({"result": result_text, "word": next_word, "finished": True, "average_result": avg_result})

    start_time = time.time()  # 다음 문장 시작 시간 초기화
    return jsonify({"result": result_text, "word": next_word, "finished": False})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
