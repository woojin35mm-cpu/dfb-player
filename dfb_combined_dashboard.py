import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64

st.set_page_config(page_title="DFB Player - Analytics", page_icon="🇩🇪", layout="wide")

def add_bg_watermark():
    image_path = "image_a2a839.png"
    if not os.path.exists(image_path):
        image_path = "dfb_logo.png"
        
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        css = f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(255, 255, 255, 0.88), rgba(255, 255, 255, 0.88)), url("data:image/png;base64,{encoded}") !important;
            background-size: 550px !important;
            background-position: center 150px !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

add_bg_watermark()

st.title("🇩🇪 DFB Player")

tab_gk, tab_cb, tab_fb, tab_mf, tab_wg, tab_st = st.tabs(["🧤 골키퍼 (GK)", "🛡️ 중앙 센터백 (CB)", "🏃‍♂️ 풀백 (FB)", "🎯 미드필더 (MF)", "⚡ 윙어 (WING)", "⚽ 스트라이커 (ST)"])

with tab_gk:
    @st.cache_data(ttl=1)
    def load_gk_data():
        csv_file = 'dfb_gk_stats.csv'
        return pd.read_csv(csv_file) if os.path.exists(csv_file) else pd.DataFrame()

    gk_df = load_gk_data()
    if not gk_df.empty:
        col1, col2, col3 = st.columns(3)
        col1.metric("Tracking German GKs", f"{len(gk_df)} 명", "Goalkeeper Focus")
        col2.metric("Top Save %", f"{gk_df['선방률(%)'].max():.1f}%", gk_df.loc[gk_df['선방률(%)'].idxmax()]['한글선수명'])
        col3.metric("Most Clean Sheets", int(gk_df['클린시트'].max()), gk_df.loc[gk_df['클린시트'].idxmax()]['한글선수명'])

        st.divider()
        st.subheader("🧤 DFB GK 세부 스탯")
        st.dataframe(
            gk_df.style.background_gradient(cmap="Blues", subset=["선방", "선방률(%)", "클린시트", "클린시트율(%)"])
                     .format({"90분환산": "{:.1f}", "90분당실점": "{:.2f}", "선방률(%)": "{:.1f}", "클린시트율(%)": "{:.1f}", "PK선방률(%)": "{:.1f}"}),
            width='stretch',
            height=400
        )
        st.divider()
        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader("📊 골키퍼 선방률 비교 (%)")
            fig1 = px.bar(gk_df, x="선방률(%)", y="한글선수명", orientation='h', text_auto='.1f', color_discrete_sequence=["#1f77b4"])
            fig1.update_layout(yaxis={'categoryorder':'total ascending'}, xaxis_title="Save %", yaxis_title="", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=100, t=10, b=10), height=450)
            st.plotly_chart(fig1, use_container_width=True)
        with col_b:
            st.subheader("🛡 무실점 경기(Clean Sheets) 비교")
            fig2 = px.bar(gk_df, x="클린시트", y="한글선수명", orientation='h', text_auto=True, color_discrete_sequence=["#2ca02c"])
            fig2.update_layout(yaxis={'categoryorder':'total ascending'}, xaxis_title="Clean Sheets", yaxis_title="", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=100, t=10, b=10), height=450)
            st.plotly_chart(fig2, use_container_width=True)

with tab_cb:
    @st.cache_data(ttl=1)
    def load_cb_data():
        csv_file = 'dfb_cb_stats.csv'
        return pd.read_csv(csv_file) if os.path.exists(csv_file) else pd.DataFrame()

    cb_df = load_cb_data()
    if not cb_df.empty:
        col1, col2, col3 = st.columns(3)
        col1.metric("Tracking DFB Center-Backs", f"{len(cb_df)} 명", "CB Focus")
        col2.metric("Top Clearances", int(cb_df['클리어링'].max()), cb_df.loc[cb_df['클리어링'].idxmax()]['한글선수명'])
        col3.metric("Most Defensive Contributions", int(cb_df['수비기여도'].max()), cb_df.loc[cb_df['수비기여도'].idxmax()]['한글선수명'])

        st.divider()
        st.subheader("🛡️ 독일 국대 중앙 센터백(CB) 실전 수비 스탯")
        st.dataframe(
            cb_df.style.background_gradient(cmap="Reds", subset=["수비기여도", "블록슛", "볼탈취", "클리어링", "클린시트"])
                     .format({"출전시간(분)": "{:.0f}", "실점기대값(xG)": "{:.2f}"}),
            width='stretch',
            height=400
        )
        st.divider()
        col_c, col_d = st.columns(2)
        with col_c:
            st.subheader("📊 수비 기여도(Defensive Contributions) 비교")
            fig3 = px.bar(cb_df, x="수비기여도", y="한글선수명", orientation='h', text_auto=True, color_discrete_sequence=["#d62728"])
            fig3.update_layout(yaxis={'categoryorder':'total ascending'}, xaxis_title="Defensive Contributions", yaxis_title="", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=100, t=10, b=10), height=450)
            st.plotly_chart(fig3, use_container_width=True)
        with col_d:
            st.subheader("🛡 클리어링(Clearances) 비교")
            fig4 = px.bar(cb_df, x="클리어링", y="한글선수명", orientation='h', text_auto=True, color_discrete_sequence=["#1f77b4"])
            fig4.update_layout(yaxis={'categoryorder':'total ascending'}, xaxis_title="Clearances", yaxis_title="", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=100, t=10, b=10), height=450)
            st.plotly_chart(fig4, use_container_width=True)

with tab_fb:
    @st.cache_data(ttl=1)
    def load_fb_data():
        csv_file = 'dfb_fb_stats.csv'
        return pd.read_csv(csv_file) if os.path.exists(csv_file) else pd.DataFrame()

    fb_df = load_fb_data()
    if not fb_df.empty:
        col1, col2, col3 = st.columns(3)
        col1.metric("Tracking DFB Fullbacks", f"{len(fb_df)} 명", "Fullback Focus")
        col2.metric("Top Chances Created", int(fb_df['찬스메이킹'].max()), fb_df.loc[fb_df['찬스메이킹'].idxmax()]['한글선수명'])
        col3.metric("Top Pass Accuracy", f"{fb_df['패스성공률(%)'].max():.1f}%", fb_df.loc[fb_df['패스성공률(%)'].idxmax()]['한글선수명'])

        st.divider()
        st.subheader("🏃‍♂️ 독일 국대 풀백(LB/RB) 수비 및 패스 세부 스탯")
        st.dataframe(
            fb_df.style.background_gradient(cmap="Greens", subset=["수비기여도", "볼탈취", "클리어링", "어시스트", "찬스메이킹", "패스성공률(%)"])
                     .format({"출전시간(분)": "{:.0f}", "패스성공률(%)": "{:.1f}", "롱볼성공률(%)": "{:.1f}", "크로스성공률(%)": "{:.1f}", "기대어시스트(xA)": "{:.2f}", "실점기대값(xG)": "{:.2f}"}),
            width='stretch',
            height=400
        )
        st.divider()
        col_e, col_f = st.columns(2)
        with col_e:
            st.subheader("📊 찬스 메이킹(Chances Created) 비교")
            fig5 = px.bar(fb_df, x="찬스메이킹", y="한글선수명", orientation='h', text_auto=True, color_discrete_sequence=["#2ca02c"])
            fig5.update_layout(yaxis={'categoryorder':'total ascending'}, xaxis_title="Chances Created", yaxis_title="", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=100, t=10, b=10), height=450)
            st.plotly_chart(fig5, use_container_width=True)
        with col_f:
            st.subheader("🎯 패스 성공률(Passing Accuracy %) 비교")
            fig6 = px.bar(fb_df, x="패스성공률(%)", y="한글선수명", orientation='h', text_auto='.1f', color_discrete_sequence=["#1f77b4"])
            fig6.update_layout(yaxis={'categoryorder':'total ascending'}, xaxis_title="Successful Passes %", yaxis_title="", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=100, t=10, b=10), height=450)
            st.plotly_chart(fig6, use_container_width=True)

with tab_mf:
    @st.cache_data(ttl=1)
    def load_mf_data():
        csv_file = 'dfb_mf_stats.csv'
        return pd.read_csv(csv_file) if os.path.exists(csv_file) else pd.DataFrame()

    mf_df = load_mf_data()
    if not mf_df.empty:
        col1, col2, col3 = st.columns(3)
        col1.metric("Tracking DFB Midfielders", f"{len(mf_df)} 명", "Midfield Focus")
        col2.metric("Top Pass Accuracy", f"{mf_df['패스성공률(%)'].max():.1f}%", mf_df.loc[mf_df['패스성공률(%)'].idxmax()]['한글선수명'])
        col3.metric("Top Chances Created", int(mf_df['찬스메이킹'].max()), mf_df.loc[mf_df['찬스메이킹'].idxmax()]['한글선수명'])

        st.divider()
        st.subheader("🎯 독일 국대 미드필더(MF) 패스, 점유율 및 수비 스탯")
        st.dataframe(
            mf_df.style.background_gradient(cmap="Purples", subset=["볼탈취", "수비기여도", "성공패스", "패스성공률(%)", "찬스메이킹", "점유율영향력(%)"])
                     .format({"출전시간(분)": "{:.0f}", "패스성공률(%)": "{:.1f}", "롱볼성공률(%)": "{:.1f}", "기대어시스트(xA)": "{:.2f}", "점유율영향력(%)": "{:.1f}"}),
            width='stretch',
            height=400
        )
        st.divider()
        col_g, col_h = st.columns(2)
        with col_g:
            st.subheader("📊 패스 성공률(Passing Accuracy %) 비교")
            fig7 = px.bar(mf_df, x="패스성공률(%)", y="한글선수명", orientation='h', text_auto='.1f', color_discrete_sequence=["#9467bd"])
            fig7.update_layout(yaxis={'categoryorder':'total ascending'}, xaxis_title="Pass Accuracy %", yaxis_title="", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=100, t=10, b=10), height=450)
            st.plotly_chart(fig7, use_container_width=True)
        with col_h:
            st.subheader("🛡 볼 탈취(Ball Recoveries) 비교")
            fig8 = px.bar(mf_df, x="볼탈취", y="한글선수명", orientation='h', text_auto=True, color_discrete_sequence=["#8c564b"])
            fig8.update_layout(yaxis={'categoryorder':'total ascending'}, xaxis_title="Ball Recoveries", yaxis_title="", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=100, t=10, b=10), height=450)
            st.plotly_chart(fig8, use_container_width=True)

with tab_wg:
    @st.cache_data(ttl=1)
    def load_wg_data():
        csv_file = 'dfb_wg_stats.csv'
        return pd.read_csv(csv_file) if os.path.exists(csv_file) else pd.DataFrame()

    wg_df = load_wg_data()
    if not wg_df.empty:
        col1, col2, col3 = st.columns(3)
        col1.metric("Tracking DFB Wingers", f"{len(wg_df)} 명", "Winger Focus")
        col2.metric("Top Goals", int(wg_df['득점'].max()), wg_df.loc[wg_df['득점'].idxmax()]['한글선수명'])
        col3.metric("Top xG", f"{wg_df['예상골(xG)'].max():.2f}", wg_df.loc[wg_df['예상골(xG)'].idxmax()]['한글선수명'])

        st.divider()
        st.subheader("⚡ 독일 국대 윙어(WING) 슈팅, 패스 및 점유율 세부 스탯")
        st.dataframe(
            wg_df.style.background_gradient(cmap="Oranges", subset=["득점", "예상골(xG)", "슛", "유효슈팅", "어시스트", "성공패스", "패스성공률(%)"])
                     .format({"출전시간(분)": "{:.0f}", "예상골(xG)": "{:.2f}", "xGOT": "{:.2f}", "PK제외xG": "{:.2f}", "기대어시스트(xA)": "{:.2f}", "패스성공률(%)": "{:.1f}", "긴패스성공률(%)": "{:.1f}", "점유율영향력(%)": "{:.1f}"}),
            width='stretch',
            height=400
        )
        st.divider()
        col_i, col_j = st.columns(2)
        with col_i:
            st.subheader("📊 득점 및 예상 골(xG) 비교")
            fig9 = px.bar(wg_df, x="예상골(xG)", y="한글선수명", orientation='h', text_auto='.2f', color_discrete_sequence=["#ff7f0e"])
            fig9.update_layout(yaxis={'categoryorder':'total ascending'}, xaxis_title="Expected Goals (xG)", yaxis_title="", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=100, t=10, b=10), height=450)
            st.plotly_chart(fig9, use_container_width=True)
        with col_j:
            st.subheader("🎯 찬스 메이킹(Chances Created) 비교")
            fig10 = px.bar(wg_df, x="찬스메이킹", y="한글선수명", orientation='h', text_auto=True, color_discrete_sequence=["#2ca02c"])
            fig10.update_layout(yaxis={'categoryorder':'total ascending'}, xaxis_title="Chances Created", yaxis_title="", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=100, t=10, b=10), height=450)
            st.plotly_chart(fig10, use_container_width=True)

with tab_st:
    @st.cache_data(ttl=1)
    def load_st_data():
        csv_file = 'dfb_st_stats.csv'
        return pd.read_csv(csv_file) if os.path.exists(csv_file) else pd.DataFrame()

    st_df = load_st_data()
    if not st_df.empty:
        col1, col2, col3 = st.columns(3)
        col1.metric("Tracking DFB Strikers", f"{len(st_df)} 명", "Striker Focus")
        col2.metric("Top Goals", int(st_df['득점'].max()), st_df.loc[st_df['득점'].idxmax()]['한글선수명'])
        col3.metric("Top xG", f"{st_df['예상골(xG)'].max():.2f}", st_df.loc[st_df['예상골(xG)'].idxmax()]['한글선수명'])

        st.divider()
        st.subheader("⚽ 독일 국대 스트라이커(ST) 슈팅, 패스 및 득점/어시스트 기록 세부 스탯")
        st.dataframe(
            st_df.style.background_gradient(cmap="Reds", subset=["득점", "예상골(xG)", "슛", "유효슈팅", "어시스트", "성공패스", "패스성공률(%)"])
                     .format({"출전시간(분)": "{:.0f}", "예상골(xG)": "{:.2f}", "xGOT": "{:.2f}", "PK제외xG": "{:.2f}", "기대어시스트(xA)": "{:.2f}", "패스성공률(%)": "{:.1f}", "긴패스성공률(%)": "{:.1f}", "점유율영향력(%)": "{:.1f}"}),
            width='stretch',
            height=400
        )
        st.divider()
        col_k, col_l = st.columns(2)
        with col_k:
            st.subheader("📊 스트라이커 득점 및 xG 비교")
            fig11 = px.bar(st_df, x="예상골(xG)", y="한글선수명", orientation='h', text_auto='.2f', color_discrete_sequence=["#d62728"])
            fig11.update_layout(yaxis={'categoryorder':'total ascending'}, xaxis_title="Expected Goals (xG)", yaxis_title="", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=100, t=10, b=10), height=450)
            st.plotly_chart(fig11, use_container_width=True)
        with col_l:
            st.subheader("🎯 스트라이커 어시스트 및 찬스메이킹 비교")
            fig12 = px.bar(st_df, x="찬스메이킹", y="한글선수명", orientation='h', text_auto=True, color_discrete_sequence=["#1f77b4"])
            fig12.update_layout(yaxis={'categoryorder':'total ascending'}, xaxis_title="Chances Created", yaxis_title="", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=100, t=10, b=10), height=450)
            st.plotly_chart(fig12, use_container_width=True)
