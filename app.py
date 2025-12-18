import streamlit as st
import pandas as pd
import pydeck as pdk
import os

# ページの設定
st.set_page_config(layout="wide", page_title="福島放射線量3Dマップ")

st.title("福島県 放射線量推移 3Dビジュアライゼーション")
st.write("左側のスライダーを動かすと、時代ごとの変化がリアルタイムで反映されます。")

# 1. データの読み込み
@st.cache_data
def load_data():
    file_path = 'final_radiation_data_for_viz.csv'
    if not os.path.exists(file_path):
        st.error(f"エラー: {file_path} が見つかりません。CSVファイルと同じフォルダで実行してください。")
        return None
    df = pd.read_csv(file_path)
    # カラム名の揺れを吸収
    df = df.rename(columns={'線量率(μSv/h)': 'dose', '线量率(μSv/h)': 'dose'})
    return df

df = load_data()

if df is not None:
    # 2. サイドバーにスライダーを設置
    available_dates = sorted(df['測定年月'].unique())
    selected_date = st.sidebar.select_slider(
        "表示する年月を選択",
        options=available_dates,
        value=available_dates[0]
    )

    # 3. データのフィルタリング
    data_filtered = df[df['測定年月'] == selected_date]

    # 4. 高さを自動調整（2011年と現在でバランスを取る）
    scale = 15000 if "2011" in selected_date else 400000

    # 5. Pydeckマップの設定
    layer = pdk.Layer(
        "ColumnLayer",
        data_filtered,
        get_position=["経度", "緯度"],
        get_elevation="dose",
        elevation_scale=scale,
        radius=2000,
        get_fill_color="[dose * 100, 50, 200, 200]",
        pickable=True,
        auto_highlight=True,
    )

    # 6. マップの表示
    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=pdk.ViewState(latitude=37.5, longitude=140.4, zoom=7, pitch=50),
        tooltip={"text": "地点: {測定地点名}\n線量: {dose} μSv/h"},
        map_style='https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json'
    ))

    st.sidebar.write(f"### 現在の表示: {selected_date}")
    st.sidebar.info("右クリックしながらマウスを動かすと、地図の角度を変えられます。")
