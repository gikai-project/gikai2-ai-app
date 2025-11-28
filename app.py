# app.py
# 地方議会 × 生成AI 実証アプリ（日本大学 林研究室）

import streamlit as st
from openai import OpenAI

# ページの設定
st.set_page_config(page_title="一般質問AI評価システム", page_icon="🗳️")

# タイトル
st.title("🗳️ 一般質問 AI自動評価システム")

# APIキーを読み込む（Streamlitのシークレットに登録しておく）
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 入力フォーム
question = st.text_area("🟦 一般質問の内容を入力してください")
answer = st.text_area("🟩 想定答弁（または実際の答弁）を入力してください")

# 評価ボタン
if st.button("✨ AIで評価する"):
    with st.spinner("評価中です。少しお待ちください..."):
        # ChatGPTに送る文章
        prompt = f"以下の質問と答弁を10点満点で評価して、理由も短く教えてください。\n\n質問:{question}\n\n答弁:{answer}"
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        result = response.choices[0].message.content
        st.success("AIの評価結果：")
        st.write(result)
