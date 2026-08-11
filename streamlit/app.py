import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor 
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    r2_score
)


# =========================================================
# 0. 페이지 기본 설정
# =========================================================

st.set_page_config(
    page_title="Garments Productivity AI",
    page_icon="🏭",
    layout="wide"
)


# =========================================================
# 1. 데이터 불러오기
# =========================================================

@st.cache_data
def load_data():

    df = pd.read_csv(
        "garments_worker_productivity.csv"
    )

    return df


df = load_data()


# =========================================================
# 2. 공통 함수
# =========================================================

def preprocessing(df):

    data = df.copy()

    # 날짜 변환
    data["date"] = pd.to_datetime(
        data["date"],
        errors="coerce"
    )

    # 날짜 파생변수
    data["year"] = data["date"].dt.year
    data["month"] = data["date"].dt.month
    data["day_of_month"] = data["date"].dt.day

    # department 공백 제거
    data["department"] = (
        data["department"]
        .astype(str)
        .str.strip()
    )

    # 목표변수
    target = "actual_productivity"

    X = data.drop(
        columns=[target, "date"]
    )

    y = data[target]

    return X, y


def create_pipeline(model):

    X, y = preprocessing(df)

    numeric_features = X.select_dtypes(
        include=["int64", "float64"]
    ).columns.tolist()

    categorical_features = X.select_dtypes(
        include=["object"]
    ).columns.tolist()

    numeric_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(
                    strategy="median"
                )
            ),
            (
                "scaler",
                StandardScaler()
            )
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(
                    strategy="most_frequent"
                )
            ),
            (
                "encoder",
                OneHotEncoder(
                    handle_unknown="ignore"
                )
            )
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "num",
                numeric_pipeline,
                numeric_features
            ),
            (
                "cat",
                categorical_pipeline,
                categorical_features
            )
        ]
    )

    pipeline = Pipeline(
        steps=[
            (
                "preprocessor",
                preprocessor
            ),
            (
                "model",
                model
            )
        ]
    )

    return pipeline


# =========================================================
# 3. Session State 초기화
# =========================================================

if "model" not in st.session_state:
    st.session_state.model = None

if "model_name" not in st.session_state:
    st.session_state.model_name = None

if "metrics" not in st.session_state:
    st.session_state.metrics = None

if "test_data" not in st.session_state:
    st.session_state.test_data = None


# =========================================================
# 4. 사이드바
# =========================================================

st.sidebar.title("🏭 Productivity AI")

st.sidebar.divider()

page = st.sidebar.radio(
    "페이지 선택",
    [
        "📊 1. 데이터 EDA",
        "🔎 2. 데이터 분석",
        "🤖 3. 모델 학습",
        "🔮 4. 모델 예측"
    ]
)

st.sidebar.divider()

st.sidebar.info(
    f"""
데이터

행: {df.shape[0]:,}
열: {df.shape[1]}
"""
)


# =========================================================
# PAGE 1
# 데이터 EDA
# =========================================================

if page == "📊 1. 데이터 EDA":

    st.title("📊 1. 데이터 EDA")

    st.write(
        "Garments Worker Productivity 데이터를 "
        "탐색적으로 분석합니다."
    )

    # -----------------------------------------------------
    # 데이터 기본 정보
    # -----------------------------------------------------

    st.header("1-1. 데이터 기본 정보")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "데이터 수",
            f"{len(df):,}"
        )

    with col2:
        st.metric(
            "변수 수",
            df.shape[1]
        )

    with col3:
        st.metric(
            "결측값",
            int(df.isnull().sum().sum())
        )

    with col4:
        st.metric(
            "목표변수",
            "actual_productivity"
        )

    # -----------------------------------------------------
    # 원본 데이터
    # -----------------------------------------------------

    st.header("1-2. 원본 데이터")

    st.dataframe(
        df,
        use_container_width=True
    )

    # -----------------------------------------------------
    # 데이터 타입
    # -----------------------------------------------------

    st.header("1-3. 데이터 타입")

    dtype_df = pd.DataFrame({
        "변수": df.columns,
        "데이터 타입": df.dtypes.astype(str),
        "결측값": df.isnull().sum().values,
        "고유값": [
            df[col].nunique()
            for col in df.columns
        ]
    })

    st.dataframe(
        dtype_df,
        use_container_width=True
    )

    # -----------------------------------------------------
    # 결측값
    # -----------------------------------------------------

    st.header("1-4. 결측값 확인")

    missing_df = pd.DataFrame({
        "변수": df.columns,
        "결측값": df.isnull().sum(),
        "결측률(%)": (
            df.isnull().mean() * 100
        ).round(2)
    })

    missing_df = missing_df.sort_values(
        "결측값",
        ascending=False
    )

    st.dataframe(
        missing_df,
        use_container_width=True
    )

    # -----------------------------------------------------
    # 기술통계
    # -----------------------------------------------------

    st.header("1-5. 기술통계")

    st.dataframe(
        df.describe().T,
        use_container_width=True
    )

    # -----------------------------------------------------
    # 변수 시각화
    # -----------------------------------------------------

    st.header("1-6. 변수별 분포")

    numeric_columns = df.select_dtypes(
        include=["int64", "float64"]
    ).columns.tolist()

    selected_column = st.selectbox(
        "분석할 변수",
        numeric_columns
    )

    fig, ax = plt.subplots()

    ax.hist(
        df[selected_column].dropna(),
        bins=30
    )

    ax.set_title(
        f"{selected_column} Distribution"
    )

    ax.set_xlabel(
        selected_column
    )

    ax.set_ylabel(
        "Frequency"
    )

    st.pyplot(fig)


# =========================================================
# PAGE 2
# 데이터 분석
# =========================================================

elif page == "🔎 2. 데이터 분석":

    st.title("🔎 2. 데이터 분석")

    st.write(
        "생산성(actual_productivity)과 "
        "주요 변수의 관계를 분석합니다."
    )

    # -----------------------------------------------------
    # 상관관계
    # -----------------------------------------------------

    st.header("2-1. 상관관계 분석")

    numeric_df = df.select_dtypes(
        include=["int64", "float64"]
    )

    corr = numeric_df.corr()

    st.dataframe(
        corr.round(3),
        use_container_width=True
    )

    # -----------------------------------------------------
    # 목표변수와 상관관계
    # -----------------------------------------------------

    st.header(
        "2-2. 실제 생산성과 변수의 상관관계"
    )

    target_corr = (
        corr["actual_productivity"]
        .drop("actual_productivity")
        .sort_values()
    )

    st.bar_chart(target_corr)

    # -----------------------------------------------------
    # 변수 선택
    # -----------------------------------------------------

    st.header(
        "2-3. 변수와 생산성의 관계"
    )

    numeric_features = [
        col
        for col in numeric_df.columns
        if col != "actual_productivity"
    ]

    selected_feature = st.selectbox(
        "분석할 변수",
        numeric_features
    )

    fig, ax = plt.subplots()

    sns.regplot(x = selected_feature, y = 'actual_productivity', data = df, ax = ax)
    
    # ax.scatter(
    #     df[selected_feature],
    #     df["actual_productivity"],
    #     alpha=0.5
    # )

    ax.set_xlabel(
        selected_feature
    )

    ax.set_ylabel(
        "Actual Productivity"
    )

    ax.set_title(
        f"{selected_feature} vs Productivity"
    )

    st.pyplot(fig)

    # -----------------------------------------------------
    # 범주형 변수별 생산성
    # -----------------------------------------------------

    st.header(
        "2-4. 범주형 변수별 생산성"
    )

    categorical_columns = df.select_dtypes(
        include=["object"]
    ).columns.tolist()

    selected_category = st.selectbox(
        "범주형 변수",
        categorical_columns
    )

    category_mean = (
        df.groupby(selected_category)[
            "actual_productivity"
        ]
        .mean()
        .sort_values(
            ascending=False
        )
    )

    st.bar_chart(
        category_mean
    )

    # -----------------------------------------------------
    # 주요 통계
    # -----------------------------------------------------

    st.header("2-5. 생산성 통계")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "평균",
            f"{df['actual_productivity'].mean():.3f}"
        )

    with col2:
        st.metric(
            "최소",
            f"{df['actual_productivity'].min():.3f}"
        )

    with col3:
        st.metric(
            "최대",
            f"{df['actual_productivity'].max():.3f}"
        )

    with col4:
        st.metric(
            "표준편차",
            f"{df['actual_productivity'].std():.3f}"
        )


# =========================================================
# PAGE 3
# 모델 학습
# =========================================================

elif page == "🤖 3. 모델 학습":

    st.title("🤖 3. 모델 학습")

    st.write(
        "전처리부터 머신러닝 모델 학습 및 평가까지 수행합니다."
    )

    # -----------------------------------------------------
    # 모델 선택
    # -----------------------------------------------------

    st.header("3-1. 모델 설정")

    model_name = st.selectbox(
        "사용할 모델",
        [
            "Linear Regression",
            "Random Forest"
        ]
    )

    test_size = st.slider(
        "테스트 데이터 비율",
        0.1,
        0.4,
        0.2,
        0.05
    )

    random_state = st.number_input(
        "Random State",
        min_value=0,
        max_value=100,
        value=42
    )

    # -----------------------------------------------------
    # 전처리 정보
    # -----------------------------------------------------

    st.header("3-2. 전처리")

    X, y = preprocessing(df)

    numeric_features = X.select_dtypes(
        include=["int64", "float64"]
    ).columns.tolist()

    categorical_features = X.select_dtypes(
        include=["object"]
    ).columns.tolist()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("수치형 변수")

        st.write(
            numeric_features
        )

        st.info(
            "결측값 → 중앙값 대체 → 표준화"
        )

    with col2:

        st.subheader("범주형 변수")

        st.write(
            categorical_features
        )

        st.info(
            "결측값 → 최빈값 대체 → One-Hot Encoding"
        )

    # -----------------------------------------------------
    # 데이터 분할
    # -----------------------------------------------------

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state
    )

    st.write(
        f"학습 데이터: {len(X_train):,}건"
    )

    st.write(
        f"테스트 데이터: {len(X_test):,}건"
    )

    # -----------------------------------------------------
    # 모델 생성
    # -----------------------------------------------------

    if model_name == "Linear Regression":

        model = LinearRegression()

    else:

        model = RandomForestRegressor(
            n_estimators=200,
            max_depth=10,
            random_state=random_state,
            n_jobs=-1
        )

    pipeline = create_pipeline(model)

    # -----------------------------------------------------
    # 학습 버튼
    # -----------------------------------------------------

    st.header("3-3. 모델 학습")

    if st.button(
        "🚀 모델 학습하기",
        type="primary"
    ):

        with st.spinner(
            "모델을 학습하고 있습니다..."
        ):

            pipeline.fit(
                X_train,
                y_train
            )

            y_pred = pipeline.predict(
                X_test
            )

            mse = mean_squared_error(
                y_test,
                y_pred
            )

            rmse = np.sqrt(mse)

            mae = mean_absolute_error(
                y_test,
                y_pred
            )

            r2 = r2_score(
                y_test,
                y_pred
            )

        # Session State 저장
        st.session_state.model = pipeline

        st.session_state.model_name = (
            model_name
        )

        st.session_state.metrics = {
            "MSE": mse,
            "RMSE": rmse,
            "MAE": mae,
            "R2": r2
        }

        st.session_state.test_data = {
            "y_test": y_test,
            "y_pred": y_pred
        }

        st.success(
            "모델 학습이 완료되었습니다."
        )

    # -----------------------------------------------------
    # 평가 결과
    # -----------------------------------------------------

    if st.session_state.metrics is not None:

        st.header("3-4. 모델 평가")

        metrics = (
            st.session_state.metrics
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "MSE",
                f"{metrics['MSE']:.6f}"
            )

        with col2:
            st.metric(
                "RMSE",
                f"{metrics['RMSE']:.6f}"
            )

        with col3:
            st.metric(
                "MAE",
                f"{metrics['MAE']:.6f}"
            )

        with col4:
            st.metric(
                "R²",
                f"{metrics['R2']:.4f}"
            )

        # -------------------------------------------------
        # 실제값 vs 예측값
        # -------------------------------------------------

        st.header(
            "3-5. 실제값 vs 예측값"
        )

        test_data = (
            st.session_state.test_data
        )

        result_df = pd.DataFrame({
            "Actual": test_data["y_test"].values,
            "Prediction": test_data["y_pred"]
        })

        result_df["Error"] = (
            result_df["Actual"]
            - result_df["Prediction"]
        )

        st.dataframe(
            result_df.head(20),
            use_container_width=True
        )

        fig, ax = plt.subplots()

        ax.scatter(
            result_df["Actual"],
            result_df["Prediction"],
            alpha=0.5
        )

        min_value = min(
            result_df["Actual"].min(),
            result_df["Prediction"].min()
        )

        max_value = max(
            result_df["Actual"].max(),
            result_df["Prediction"].max()
        )

        ax.plot(
            [min_value, max_value],
            [min_value, max_value]
        )

        ax.set_xlabel(
            "Actual Productivity"
        )

        ax.set_ylabel(
            "Predicted Productivity"
        )

        ax.set_title(
            "Actual vs Predicted"
        )

        st.pyplot(fig)


# =========================================================
# PAGE 4
# 모델 예측
# =========================================================

elif page == "🔮 4. 모델 예측":

    st.title("🔮 4. 모델 예측")

    # -----------------------------------------------------
    # 모델 확인
    # -----------------------------------------------------

    if st.session_state.model is None:

        st.warning(
            "학습된 모델이 없습니다."
        )

        st.info(
            "먼저 사이드바에서 "
            "'3. 모델 학습' 페이지로 이동하여 "
            "모델을 학습해주세요."
        )

        st.stop()

    model = st.session_state.model

    st.success(
        f"현재 사용 모델: "
        f"{st.session_state.model_name}"
    )

    # -----------------------------------------------------
    # 입력
    # -----------------------------------------------------

    st.header("4-1. 작업 조건 입력")

    col1, col2, col3 = st.columns(3)

    with col1:

        quarter = st.selectbox(
            "Quarter",
            sorted(
                df["quarter"]
                .dropna()
                .unique()
            )
        )

        department = st.selectbox(
            "Department",
            sorted(
                df["department"]
                .astype(str)
                .str.strip()
                .unique()
            )
        )

        day = st.selectbox(
            "Day",
            sorted(
                df["day"]
                .dropna()
                .unique()
            )
        )

        team = st.number_input(
            "Team",
            min_value=1,
            max_value=20,
            value=1,
            step=1
        )

        no_of_workers = st.number_input(
            "No. of Workers",
            min_value=0.0,
            value=float(
                df["no_of_workers"].median()
            )
        )

    with col2:

        targeted_productivity = st.number_input(
            "Targeted Productivity",
            min_value=0.0,
            max_value=1.0,
            value=0.80,
            step=0.01
        )

        smv = st.number_input(
            "SMV",
            min_value=0.0,
            value=float(
                df["smv"].median()
            )
        )

        wip = st.number_input(
            "WIP",
            min_value=0.0,
            value=float(
                df["wip"].median()
            )
        )

        over_time = st.number_input(
            "Over Time",
            min_value=0,
            value=int(
                df["over_time"].median()
            ),
            step=1
        )

    with col3:

        incentive = st.number_input(
            "Incentive",
            min_value=0,
            value=int(
                df["incentive"].median()
            ),
            step=1
        )

        idle_time = st.number_input(
            "Idle Time",
            min_value=0.0,
            value=float(
                df["idle_time"].median()
            )
        )

        idle_men = st.number_input(
            "Idle Men",
            min_value=0,
            value=int(
                df["idle_men"].median()
            ),
            step=1
        )

        no_of_style_change = st.number_input(
            "No. of Style Change",
            min_value=0,
            value=int(
                df["no_of_style_change"].median()
            ),
            step=1
        )

    # -----------------------------------------------------
    # 날짜
    # -----------------------------------------------------

    st.subheader("작업 날짜")

    prediction_date = st.date_input(
        "Date"
    )

    # -----------------------------------------------------
    # 입력 데이터 생성
    # -----------------------------------------------------

    input_data = pd.DataFrame({
        "quarter": [quarter],
        "department": [department],
        "day": [day],
        "team": [team],
        "targeted_productivity": [
            targeted_productivity
        ],
        "smv": [smv],
        "wip": [wip],
        "over_time": [over_time],
        "incentive": [incentive],
        "idle_time": [idle_time],
        "idle_men": [idle_men],
        "no_of_style_change": [
            no_of_style_change
        ],
        "no_of_workers": [
            no_of_workers
        ],
        "year": [
            prediction_date.year
        ],
        "month": [
            prediction_date.month
        ],
        "day_of_month": [
            prediction_date.day
        ]
    })

    # -----------------------------------------------------
    # 입력 데이터 확인
    # -----------------------------------------------------

    st.header("4-2. 입력 데이터")

    st.dataframe(
        input_data,
        use_container_width=True
    )

    # -----------------------------------------------------
    # 예측
    # -----------------------------------------------------

    st.header("4-3. 생산성 예측")

    if st.button(
        "🔮 생산성 예측하기",
        type="primary"
    ):

        prediction = model.predict(
            input_data
        )

        prediction_value = prediction[0]

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "예측 생산성",
                f"{prediction_value:.4f}"
            )

        with col2:

            st.metric(
                "예측 생산성 (%)",
                f"{prediction_value * 100:.2f}%"
            )

        # -------------------------------------------------
        # 결과 해석
        # -------------------------------------------------

        if prediction_value >= 0.8:

            st.success(
                "높은 생산성이 예상됩니다."
            )

        elif prediction_value >= 0.6:

            st.info(
                "보통 수준의 생산성이 예상됩니다."
            )

        else:

            st.warning(
                "상대적으로 낮은 생산성이 예상됩니다."
            )