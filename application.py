@app.route("/check", methods=["GET", "POST"])
def check():
    global current_count, results, start_time

    if current_count >= len(WORD_LIST):
        return jsonify({"finished": True})

    data = request.get_json()
    if not data or "user_input" not in data:
        return jsonify({"error": "user_input 데이터가 전달되지 않았습니다."}), 400

    user_input = data.get("user_input", "").strip()
    if not user_input:
        return jsonify({"error": "입력값이 비어 있습니다."}), 400

    # 🚀 `current_count`가 정확하게 증가하는지 확인
    print(f"📌 현재 문장 번호: {current_count}")
    
    # 현재 문장 가져오기 (디버깅용)
    src_word = WORD_LIST[current_count]
    print(f"📝 원본 문장 (WORD_LIST[current_count]): {src_word}")

    # 한글 분해 비교
    src = hgtk.text.decompose(src_word).replace("ᴥ", "")
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
    
    # 🚀 current_count 업데이트 (다음 문장으로 넘어가기)
    current_count += 1

    # 다음 문장 설정
    if current_count < len(WORD_LIST):
        next_word = WORD_LIST[current_count]
    else:
        next_word = "연습이 끝났습니다."
        avg_speed = sum(r[0] for r in results) / len(results)
        avg_accuracy = sum(r[1] for r in results) / len(results)
        avg_typo_rate = sum(r[2] for r in results) / len(results)
        avg_result = f"평균 속도: {avg_speed:.2f}, 정확도: {avg_accuracy:.2f}%, 오타율: {avg_typo_rate:.2f}%"
        return jsonify({"result": f"속도: {speed:.2f} 정확도: {accuracy:.2f}% 오타율: {typo_rate:.2f}%", "word": next_word, "finished": True, "average_result": avg_result})

    # 🚀 새 문장 시작 시 start_time 초기화
    start_time = time.time()

    return jsonify({"result": f"속도: {speed:.2f} 정확도: {accuracy:.2f}% 오타율: {typo_rate:.2f}%", "word": next_word, "finished": False})
