import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64

st.set_page_config(page_title="DFB Players Analytics", page_icon="🇩🇪", layout="wide")

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

st.title("🇩🇪 DFB Players - 포지션별 통합 분석 대시보드")

# 포지션별 탭 분리 (골키퍼 vs 수비수/미드필더)
tab_gk, tab_df = st.tabs(["🧤 골키퍼 (GK)", "🛡️ 수비수 & 미드필더 (DF/MF)"])

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
            fig1.update_layout(
                yaxis={'categoryorder':'total ascending'},
                xaxis_title="Save %", 
                yaxis_title="",
                plot_bgcolor="rgba(0,0,0,0)", 
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=100, t=10, b=10),
                height=450
            )
            st.plotly_chart(fig1, use_container_width=True)
            
        with col_b:
            st.subheader("🛡 무실점 경기(Clean Sheets) 비교")
            fig2 = px.bar(gk_df, x="클린시트", y="한글선수명", orientation='h', text_auto=True, color_discrete_sequence=["#2ca02c"])
            fig2.update_layout(
                yaxis={'categoryorder':'total ascending'},
                xaxis_title="Clean Sheets", 
                yaxis_title="",
                plot_bgcolor="rgba(0,0,0,0)", 
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=100, t=10, b=10),
                height=450
            )
            st.plotly_chart(fig2, use_container_width=True)
    else:
        st.error("골키퍼 데이터 파일을 찾을 수 없습니다.")

with tab_df:
    @st.cache_data(ttl=1)
    def load_df_data():
        csv_file = 'dfb_df_stats.csv'
        return pd.read_csv(csv_file) if os.path.exists(csv_file) else pd.DataFrame()

    df_df = load_df_data()
    
    if not df_df.empty:
        col1, col2, col3 = st.columns(3)
        col1.metric("Tracking Defenders", f"{len(df_df)} 명", "Defensive Focus")
        col2.metric("Most Tackles", int(df_df['태클성공'].max()), df_df.loc[df_df['태클성공'].idxmax()]['한글선수명'])
        col3.metric("Most Clearances", int(df_df['클리어링'].max()), df_df.loc[df_df['클리어링'].idxmax()]['한글선수명'])

        st.divider()

        st.subheader("🛡️ DFB Defenders & Defensive Midfielders")
        st.dataframe(
            df_df.style.background_gradient(cmap="Greens", subset=["태클성공", "인터셉트", "클리어링", "블록", "공중볼승리"])
                     .format({"출전시간(분)": "{:.0f}"}),
            width='stretch',
            height=400
        )

        st.divider()
        
        col_c, col_d = st.columns(2)
        with col_c:
            st.subheader("📊 태클 성공 횟수 비교")
            fig3 = px.bar(df_df, x="태클성공", y="한글선수명", orientation='h', text_auto=True, color_discrete_sequence=["#2ca02c"])
            fig3.update_layout(
                yaxis={'categoryorder':'total ascending'},
                xaxis_title="Tackles Won", 
                yaxis_title="",
                plot_bgcolor="rgba(0,0,0,0)", 
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=100, t=10, b=10),
                height=450
            )
            st.plotly_chart(fig3, use_container_width=True)
            
        with col_d:
            st.subheader("🛡 클리어링(위험지역 걷어내기) 비교")
            fig4 = px.bar(df_df, x="클리어링", y="한글선수명", orientation='h', text_auto=True, color_discrete_sequence=["#1f77b4"])
            fig4.update_layout(
                yaxis={'categoryorder':'total ascending'},
                xaxis_title="Clearances", 
                yaxis_title="",
                plot_bgcolor="rgba(0,0,0,0)", 
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=100, t=10, b=10),
                height=450
            )
            st.plotly_chart(fig4, use_container_width=True)
    else:
        st.error("수비수 데이터 파일을 찾을 수 없습니다.")
