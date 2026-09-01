import streamlit as st
import random
import time

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="심연의 고대 보물상자",
    page_icon="📦",
    layout="centered"
)

# 2. 어둡고 웅장한 다크 판타지 CSS
st.markdown("""
    <style>
    /* 전체 배경 */
    .stApp {
        background-color: #08070b;
        color: #d4af37;
        font-family: 'Georgia', serif;
    }
    
    /* 타이틀 */
    h1 {
        color: #f1c40f !important;
        text-shadow: 0 0 20px #8b0000, 2px 2px 5px #000000;
        text-align: center;
        letter-spacing: 3px;
    }
    
    .stCaption {
        text-align: center;
        color: #a0a0a0 !important;
        font-size: 1.1rem;
    }

    /* 보물상자 버튼 거대화 및 연출 */
    div.stButton > button:first-child {
        background: linear-gradient(180deg, #2c1a1a 0%, #0f0808 100%);
        color: #f1c40f;
        font-size: 24px !important;
        font-weight: bold;
        padding: 25px 50px;
        border: 2px solid #8b0000;
        border-radius: 12px;
        box-shadow: 0 0 15px rgba(139, 0, 0, 0.6);
        cursor: pointer;
        width: 100%;
        margin-top: 20px;
        transition: all 0.3s ease;
    }
    
    div.stButton > button:first-child:hover {
        background: linear-gradient(180deg, #4a1f1f 0%, #1a0c0c 100%);
        border-color: #f1c40f;
        box-shadow: 0 0 25px rgba(241, 196, 15, 0.8);
        transform: scale(1.02);
    }

    /* 카드 형태의 아이템 출력 상자 */
    .item-card {
        background-color: #121017;
        border: 2px solid #8b0000;
        border-radius: 10px;
        padding: 25px;
        text-align: center;
        margin-top: 25px;
        box-shadow: inset 0 0 15px #000000, 0 0 20px rgba(139, 0, 0, 0.4);
    }

    .item-grade {
        font-size: 1.2rem;
        font-weight: bold;
        letter-spacing: 2px;
        margin-bottom: 10px;
    }

    .item-name {
        font-size: 2rem;
        font-weight: bold;
        color: #ffffff;
        text-shadow: 0 0 10px #f1c40f;
        margin-bottom: 15px;
    }

    .item-desc {
        color: #c5c6c7;
        font-style: italic;
        font-size: 1.05rem;
        line-height: 1.6;
    }
    
    /* 등급별 색상 정의 */
    .mythic { color: #ff0055; text-shadow: 0 0 10px #ff0055; }
    .legendary { color: #f1c40f; text-shadow: 0 0 10px #f1c40f; }
    .epic { color: #a335ee; text-shadow: 0 0 10px #a335ee; }
    .rare { color: #0070dd; text-shadow: 0 0 10px #0070dd; }
    </style>
""", unsafe_allow_html=True)

# 3. 아무 의미 없지만 쓸데없이 웅장한 아이템 데이터베이스
ITEMS = [
    # 신화 등급 (5%)
    {"grade": "MYTHIC", "name": "태초의 먼지 한 털", "desc": "우주가 탄생할 때 튕겨 나간 먼지입니다. 아무런 기능도 없지만 왠지 거룩한 기운이 맴돕니다.", "color": "mythic"},
    {"grade": "MYTHIC", "name": "봉인된 심연의 공기", "desc": "수천 년 동안 닫혀 있던 고대 지하 성전의 공기입니다. 냄새를 맡으면 그저 오래된 먼지 냄새가 납니다.", "color": "mythic"},
    
    # 전설 등급 (15%)
    {"grade": "LEGENDARY", "name": "용의 목에 난 털 1개", "desc": "고대 화염용의 역린 옆에서 뽑아낸 털입니다. 아무 데도 쓸 수 없지만 가만히 두면 살짝 미지근합니다.", "color": "legendary"},
    {"grade": "LEGENDARY", "name": "절대 영도의 촛농", "desc": "마왕의 연회장에서 굳어버린 촛농입니다. 불을 붙이려 해도 절대로 다시 타오르지 않습니다.", "color": "legendary"},
    {"grade": "LEGENDARY", "name": "시간을 달리는 돌멩이", "desc": "1초에 정확히 1초씩 미래로 이동하는 기묘한 능력을 가진 평범한 길거리 돌멩이입니다.", "color": "legendary"},
    
    # 영웅 등급 (30%)
    {"grade": "EPIC", "name": "절대로 펴지지 않는 양피지", "desc": "고대 주문이 적혀 있었으나 마법이 해제되면서 평생 돌돌 말려만 있는 양피지입니다.", "color": "epic"},
    {"grade": "EPIC", "name": "마왕의 오른쪽 깃털 펜", "desc": "마왕이 출근 서류에 결재할 때 쓰던 펜입니다. 잉크가 전부 떨어져 글씨가 써지지 않습니다.", "color": "epic"},
    {"grade": "EPIC", "name": "소리 없는 고대 벨", "desc": "흔들면 아스트랄 계체에만 들리는 주파수의 소리가 납니다. 당신은 아무 소리도 들을 수 없습니다.", "color": "epic"},

    # 희귀 등급 (50%)
    {"grade": "RARE", "name": "녹슨 철제 단추", "desc": "어느 잊혀진 기사의 갑옷 내부에서 떨어진 단추입니다. 주머니에 넣으면 주머니가 무거워집니다.", "color": "rare"},
    {"grade": "RARE", "name": "금이 간 모래시계", "desc": "모래가 떨어지다가 중간에 자꾸 걸려서 유저가 직접 손으로 쳐줘야 하는 모래시계입니다.", "color": "rare"},
    {"grade": "RARE", "name": "식어버린 성수 한 방울", "desc": "유효기간이 약 800년 전에 지나서 그냥 약간 미지근하고 투명한 액체입니다.", "color": "rare"},
]

# 4. 세션 상태 초기화 (뽑기 기록 및 뽑은 횟수)
if "history" not in st.session_state:
    st.session_state.history = []
if "open_count" not in st.session_state:
    st.session_state.open_count = 0

# 5. 메인 헤더 UI
st.title("📦 심연의 봉인된 상자")
st.caption("어둠 속에 묻혀 있던 고대의 상자입니다. 무엇이 나올지는 신조차 알지 못합니다.")

st.markdown("<br>", unsafe_allow_html=True)

# 6. 상자 오픈 버튼 및 무작위 뽑기 로직
if st.button("🔮 상자 개봉하기"):
    # 긴장감을 유도하는 연출
    with st.spinner("심연의 봉인이 풀리는 중..."):
        time.sleep(1.2) # 1.2초 대기 연출
    
    # 등급 가중치 설정 (MYTHIC: 5%, LEGENDARY: 15%, EPIC: 30%, RARE: 50%)
    weights = [0.05 if item["grade"] == "MYTHIC" 
               else 0.15 if item["grade"] == "LEGENDARY" 
               else 0.30 if item["grade"] == "EPIC" 
               else 0.50 for item in ITEMS]
    
    # 아이템 무작위 추출
    drawn_item = random.choices(ITEMS, weights=weights, k=1)[0]
    
    # 세션 상태 업데이트
    st.session_state.open_count += 1
    st.session_state.history.insert(0, drawn_item) # 최근 아이템이 맨 위로 오도록 저장
    
    # 등급별 파티클 효과 연출
    if drawn_item["grade"] in ["MYTHIC", "LEGENDARY"]:
        st.balloons()
    
    # 뽑힌 아이템 카드 출력
    st.markdown(f"""
        <div class="item-card">
            <div class="item-grade {drawn_item['color']}">&lt; {drawn_item['grade']} ITEM &gt;</div>
            <div class="item-name">{drawn_item['name']}</div>
            <div class="item-desc">"{drawn_item['desc']}"</div>
        </div>
    """, unsafe_allow_html=True)

# 7. 사이드바 - 뽑기 통계 및 수집 기록
st.sidebar.title("📜 보관함 현황")
st.sidebar.write(f"**총 열어본 상자:** {st.session_state.open_count}회")
st.sidebar.markdown("---")

if st.session_state.history:
    st.sidebar.subheader(" 최근 획득한 보물")
    for idx, item in enumerate(st.session_state.history[:10]): # 최근 10개만 표시
        st.sidebar.markdown(f"**{idx+1}.** <span class='{item[\"color\"]}'>[{item['grade']}]</span> {item['name']}", unsafe_allow_html=True)
else:
    st.sidebar.info("상자를 열어 보물을 획득하세요.")
