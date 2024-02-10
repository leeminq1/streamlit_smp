import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# 한글폰트 적용
# 폰트 적용
import os
import matplotlib.font_manager as fm  # 폰트 관련 용도 as fm

# 폰트 설정
plt.rcParams['font.family'] = 'NanumGothic'


def unique(list):
    x = np.array(list)
    return np.unique(x)

@st.cache_data
def fontRegistered():
    font_dirs = [os.getcwd() + '/customFonts']
    font_files = fm.findSystemFonts(fontpaths=font_dirs)

    for font_file in font_files:
        fm.fontManager.addfont(font_file)
    fm._load_fontmanager(try_read_cache=False)


def page_config():
    st.set_page_config(page_title="SMP VISUAL", page_icon="⭐", layout="wide")

def sub_file_upload():
    uploaded_file = st.file_uploader("Choose a file", type="csv")

    ### up load 파일 있을 경우 ###
    if uploaded_file is not None:
        # CSV 파일을 읽기 위해 pandas의 read_csv 함수를 사용합니다.
        df = pd.read_csv(uploaded_file)

        if 'Unnamed: 0' in df.columns:
            df = df.drop(columns='Unnamed: 0' ,axis=1)

        df['date'] = pd.to_datetime(df['date'])
        st.write(df)

        return df


def sub_graph(df,fontname):
    plt.rc('font', family=fontname)
    ### graph ###
    fig, axes = plt.subplots(nrows=2, ncols=1)
    fig.patch.set_facecolor('xkcd:white')
    fig.set_size_inches(11, 6)
    plt.subplots_adjust(hspace=0.5)

    sns.lineplot(x='date', y='smp', data=df, ax=axes[0], label='SMP', color='r', linestyle='--', linewidth=2)
    sns.lineplot(x='date', y='smp_s_1', data=df, ax=axes[1], label='SMP_S1', color='b', linestyle='dashdot', linewidth=2)

    fig.suptitle('SMP 시각화')

    st.pyplot(fig)






def main_core():
    page_config()

    st.title("SMP TEST")
    st.header("Header")
    st.subheader('Sub Header')
    st.write("SMP 관련 시각화 🚒")

    fontRegistered()
    fontNames = [f.name for f in fm.fontManager.ttflist]
    default_font_index = fontNames.index("HYGothic-Medium") if "HYGothic-Medium" in fontNames else 0
    fontname = st.selectbox("폰트 선택", fontNames, index=default_font_index)

    ## radio btn
    sel_data = st.radio("데이터 선택", ["파일 불러오기", "기본 데이터선택"])

    df = None
    if sel_data == '파일 불러오기':
        df = sub_file_upload()
    elif sel_data == '기본 데이터선택':
        df = pd.read_csv('./data/df_merge_smp.csv')
        if 'Unnamed: 0' in df.columns:
            df = df.drop(columns='Unnamed: 0' ,axis=1)

        df['date'] = pd.to_datetime(df['date'])
        st.write(df)

    # btn
    graph_btn = st.button("🔥데이터 시각화")

    # 버튼이 클릭되면 해당 메시지를 출력합니다.
    if graph_btn and df is not None:
        st.write("시각화 시작!🚓")
        sub_graph(df,fontname)
    elif df is None:
        st.write("Data 업로드 후 버튼을 눌러주세요")


if __name__ == '__main__':
    main_core()  # 동적 메뉴 렌더링!



