import streamlit as st
import pandas as pd
import pydeck as pdk

# --- ここから追加：パスワード認証 ---
def check_password():
    """パスワードが正しいか確認する関数"""
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if st.session_state["password_correct"]:
        return True

    # パスワード入力画面
    st.title("認証が必要です")
    password = st.text_input("合言葉を入力してください", type="password")
    if st.button("ログイン"):
        if password == "fukushima2025": # ← ここに好きな合言葉を設定
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("合言葉が違います")
    return False

# パスワードが通った場合のみ、以下のメインコードを実行
if check_password():
    # --- ここから元のメインコード ---
    st.title("福島県 放射線量 3Dマップ")
    
    # データの読み込み（GitHubに上げるときはパスから「11/」を消すのを忘れずに）
    df = pd.read_csv('final_radiation_data_for_viz.csv')
    # ...（以下、以前のマップ表示コードをそのまま入れる）...
    
    st.sidebar.success("ログイン成功！")
    # --- ここまで元のメインコード ---
