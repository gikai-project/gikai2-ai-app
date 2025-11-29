import streamlit as st
import openai
import json

st.set_page_config(page_title="一般質問 AI自動採点システム", layout="wide")

# ===============================
# OpenAI APIキーの入力欄
# ===============================
st.sidebar.header("🔑 APIキー設定")
api_key = st.sidebar.text_input("OpenAI API Key を入力してください", type="password")

if api_key:
    openai.api_key = api_key


# ===============================
# 評価基準（辞書）
# ===============================
criteria = {
    "1. テーマ設定の妥当性": [...],   # ← ここに前回お渡しした基準リスト（10行）をそのまま入れる
    "2. 目的の明確性": [...],
    "3. 論理構成の明確性": [...],
    "4. 根拠・エビデンス": [...],
    "5. 質問の具体性": [...],
    "6. 実現可能性": [...],
    "7. 行政答弁を引き出す力": [...],
    "8. 議会の役割理解": [...],
    "9. 住民視点": [...],
    "10. フォロー可能性": [...],
    "11. 表現・スピーチ": [...],
    "12. 倫理性": [...],
    "13. 将来志向": [...],
    "14. 政策横断性": [...],
    "15. 継続性・成長": [...]
}


# ===============================
# GPTに採点させるプロンプト
# ===============================
def generate_prompt(question_text):
    criteria_text = ""
    for category, items in criteria.items():
        criteria_text += f"■ {category}\n"
        for i, desc in enumerate(items[::-1], 1):
            criteria_text += f"{i}点: {desc}\n"
        criteria_text += "\n"

    prompt = f"""
あなたは「議会質問の専門評価者」です。
以下の文章を、15項目 × 1〜10点で採点してください。

【評価対象の一般質問】
{question_text}

【評価基準】
{criteria_text}

【出力フォーマット（厳守）】
以下のJSON形式で答えてください：

{{
  "scores": {{
      "1": 点数,
      "2": 点数,
      ...
      "15": 点数
  }},
  "total": 合計点,
  "rank": "S / A / B / C / D / E",
  "reason": {{
      "1": "理由",
      "2": "理由",
      ...
      "15": "理由"
  }}
}}

※ 点数は必ず整数1〜10。
※ JSON以外は返さない。
"""

    return prompt


# ===============================
# UI：文章入力欄
# ===============================
st.title("📘 一般質問 AI自動採点システム（150点モデル）")

question_text = st.text_area(
    "▼ 評価したい「一般質問の文章」を貼り付けてください",
    height=300
)

start = st.button("🧠 AIで自動採点する")


# ===============================
# AI 採点の実行
# ===============================
if start:
    if not api_key:
        st.error("APIキーが未入力です。左側に入力してください。")
    elif not question_text.strip():
        st.error("一般質問の文章が入力されていません。")
    else:
        with st.spinner("AIが採点しています…（5〜10秒）"):
            prompt = generate_prompt(question_text)

            response = openai.ChatCompletion.create(
                model="gpt-4.1",
                messages=[{"role": "user", "content": prompt}]
            )

            result_raw = response["choices"][0]["message"]["content"]

            # JSON取り出し
            try:
                result = json.loads(result_raw)
            except:
                st.error("AIの返答をJSONとして読み取れませんでした。")
                st.code(result_raw)
                st.stop()

            scores = result["scores"]
            total = result["total"]
            rank = result["rank"]
            reasons = result["reason"]

            # ===============================
            # 結果表示
            # ===============================
            st.subheader("📊 採点結果")

            for i, (key, score) in enumerate(scores.items(), 1):
                st.markdown(f"### {i}. {list(criteria.keys())[i-1]}")
                st.write(f"**得点：{score}点 / 10点**")
                st.write(f"理由：{reasons[str(i)]}")
                st.markdown("---")

            st.markdown(f"## 🔢 合計点：**{total} / 150点**")
            st.markdown(f"## 🏆 ランク：**{rank}**")


