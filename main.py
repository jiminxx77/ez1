import streamlit as st
import time

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="마마보이에 키 키우기!",
    page_icon="👶",
    layout="centered"
)

# 2. 다크 판타지 & 레트로 애니메이션 CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #08070b;
        color: #d4af37;
        font-family: 'Georgia', serif;
    }
    
    h1 {
        color: #f1c40f !important;
        text-shadow: 0 0 20px #8b0000, 2px 2px 5px #000000;
        text-align: center;
        letter-spacing: 2px;
    }
    
    .stCaption {
        text-align: center;
        color: #a0a0a0 !important;
        font-size: 1.1rem;
    }

    /* 거대한 연타 버튼 스타일링 */
    div.stButton > button:first-child {
        background: linear-gradient(180deg, #8b0000 0%, #4a0000 100%);
        color: #ffffff;
        font-size: 28px !important;
        font-weight: 900;
        padding: 20px 40px;
        border: 3px solid #f1c40f;
        border-radius: 50px;
        box-shadow: 0 0 20px rgba(241, 196, 15, 0.6);
        cursor: pointer;
        width: 100%;
        margin-top: 10px;
        transition: transform 0.05s ease, background 0.2s ease;
    }
    
    div.stButton > button:first-child:active {
        transform: scale(0.95);
        background: linear-gradient(180deg, #ff0000 0%, #8b0000 100%);
    }

    /* 캐릭터 출력 프레임 */
    .character-box {
        display: flex;
        justify-content: center;
        align-items: flex-end;
        height: 380px;
        background: radial-gradient(circle, #1a1829 0%, #08070b 80%);
        border: 2px solid #8b0000;
        border-radius: 15px;
        margin-top: 20px;
        padding-bottom: 20px;
        overflow: hidden;
        position: relative;
    }

    /* 키 미터기 스탯 표시 */
    .stat-card {
        background-color: #121017;
        border: 1px solid #f1c40f;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        margin-bottom: 10px;
    }

    .height-text {
        font-size: 2.5rem;
        font-weight: bold;
        color: #f1c40f;
        text-shadow: 0 0 10px #f1c40f;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 세션 상태 초기화 (최소키 120cm ~ 최대키 300cm)
MIN_HEIGHT = 120
MAX_HEIGHT = 300

if "child_height" not in st.session_state:
    st.session_state.child_height = 120.0
if "last_click_time" not in st.session_state:
    st.session_state.last_click_time = time.time()

# 4. 가만히 있을 때 키 감축 로직 (시간 경과에 따라 감소)
current_time = time.time()
time_diff = current_time - st.session_state.last_click_time

# 마지막 클릭 후 시간이 지났다면 키 감소 (초당 약 8cm 감소)
if time_diff > 0.3:
    shrink_amount = (time_diff - 0.3) * 8.0
    st.session_state.child_height = max(MIN_HEIGHT, st.session_state.child_height - shrink_amount)
    st.session_state.last_click_time = current_time

# 5. UI 헤더
st.title("⚡ 존나 눌러서 키 키우기!")
st.caption("클릭을 쉬는 순간 바로 작아집니다! 광클해서 giant로 만들어보세요!")

# 현재 키 수치 표기
st.markdown(f"""
    <div class="stat-card">
        <div>현재 아이의 키</div>
        <div class="height-text">{int(st.session_state.child_height)} cm</div>
    </div>
""", unsafe_allow_html=True)

# 6. 캐릭터 이모지 및 크기 실시간 변경 계산
# 키 수치(120~300)에 따라 이모지 폰트 크기(40px ~ 250px) 동적 변경
font_size = int(40 + (st.session_state.child_height - MIN_HEIGHT) * (210 / (MAX_HEIGHT - MIN_HEIGHT)))

# 키 등급에 따른 캐릭터 상태 표기
if st.session_state.child_height >= 250:
    char_emoji = "👹" # 거인 마왕
    status_label = "🔥 [최종진화] 심연의 거대 마왕!"
elif st.session_state.child_height >= 200:
    char_emoji = "🧔" # 거구
    status_label = "⚡ [3단계] 폭풍 성장한 훈남!"
elif st.session_state.child_height >= 150:
    char_emoji = "👦" # 어린이
    status_label = "🌱 [2단계] 잘 자라고 있는 아이!"
else:
    char_emoji = "👶" # 아기
    status_label = "💧 [1단계] 쪼꼬미 아기 (줄어드는 중...)"

# 캐릭터 시각화 화면
st.markdown(f"""
    <div class="character-box">
        <div style="font-size: {font_size}px; transition: all 0.1s ease; text-align: center;">
            {char_emoji}
        </div>
    </div>
    <div style="text-align: center; color: #a0a0a0; margin-top: 5px;">{status_label}</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 7. 클릭 이벤트 로직
if st.button("🔥 광클하여 키 키우기!!!"):
    # 클릭할 때마다 6cm 상승
    st.session_state.child_height = min(MAX_HEIGHT, st.session_state.child_height + 6.0)
    st.session_state.last_click_time = time.time()
    st.rerun()

# 8. 클릭 안 하고 있을 때 실시간 감축 반응을 위한 자동 대기 (0.15초마다 화면 갱신)
if st.session_state.child_height > MIN_HEIGHT:
    time.sleep(0.15)
    st.rerun()
