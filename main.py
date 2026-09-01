import streamlit as st
import random
import time

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="마마보이에 깊콘 뽑기",
    page_icon="🎁",
    layout="centered"
)

# 2. 다크 판타지 CSS
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
        letter-spacing: 3px;
    }
    
    .stCaption {
        text-align: center;
        color: #a0a0a0 !important;
        font-size: 1.1rem;
    }

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

    .item-card {
        background-color: #121017;
        border: 2px solid #8b0000;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        margin-top: 20px;
        box-shadow: inset 0 0 15px #000000, 0 0 20px rgba(139, 0, 0, 0.4);
    }

    .item-grade {
        font-size: 1.2rem;
        font-weight: bold;
        letter-spacing: 2px;
        margin-bottom: 8px;
    }

    .item-name {
        font-size: 1.8rem;
        font-weight: bold;
        color: #ffffff;
        text-shadow: 0 0 10px #f1c40f;
        margin-bottom: 10px;
    }

    .item-desc {
        color: #c5c6c7;
        font-style: italic;
        font-size: 1rem;
        margin-bottom: 15px;
    }
    
    .mythic { color: #ff0055; text-shadow: 0 0 10px #ff0055; }
    .legendary { color: #f1c40f; text-shadow: 0 0 10px #f1c40f; }
    .epic { color: #a335ee; text-shadow: 0 0 10px #a335ee; }
    .rare { color: #0070dd; text-shadow: 0 0 10px #0070dd; }
    </style>
""", unsafe_allow_html=True)

# 3. 기프티콘 이미지 및 설명 데이터베이스 (원하는 이미지 URL 및 로컬 파일로 변경 가능)
ITEMS = [
    # 신화 등급 (5%)
    {
        "grade": "MYTHIC", 
        "name": "치킨 기프티콘 (사용완료)", 
        "desc": "이미 전설 속 마왕이 시켜 먹고 바코드까지 깔끔하게 사용 완료된 치킨 쿠폰입니다.", 
        "color": "mythic",
        "img": "https://picsum.photos/seed/giftcon1/400/500" # 샘플 이미지 (원하는 기프티콘 URL로 변경)
    },
    # 전설 등급 (15%)
    {
        "grade": "LEGENDARY", 
        "name": "스타벅스 아메리카노 (만료됨)", 
        "desc": "유효기간이 약 500년 전에 지나서 카운터에 보여주면 쫓겨나는 카페 쿠폰입니다.", 
        "color": "legendary",
        "img": "https://picsum.photos/seed/giftcon2/400/500"
    },
    # 영웅 등급 (30%)
    {
        "grade": "EPIC", 
        "name": "편의점 1,000원 상품권", 
        "desc": "바코드가 너무 찌그러져서 그 어떤 바코드 리더기도 읽지 못하는 비운의 쿠폰입니다.", 
        "color": "epic",
        "img": "https://picsum.photos/seed/giftcon3/400/500"
    },
    # 희귀 등급 (50%)
    {
        "grade": "RARE", 
        "name": "붕어빵 1개 무료 교환권", 
        "desc": "조선시대 한성부 붕어빵 틀에서만 사용 가능했던 기묘한 영수증입니다.", 
        "color": "rare",
        "img": "https://picsum.photos/seed/giftcon4/400/500"
    },
]

# 4. 세션 상태 초기화
if "history" not in st.session_state:
    st.session_state.history = []
if "open_count" not in st.session_state:
    st.session_state.open_count = 0

# 5. UI 헤더
st.title("🎁 심연의 기프티콘 상자")
st.caption("어둠 속에 봉인된 고대의 기프티콘을 뽑아보세요. (사용 여부는 보장하지 않습니다)")

st.markdown("<br>", unsafe_allow_html=True)

# 6. 상자 개봉 로직
if st.button("🔮 상자 개봉하기"):
    with st.spinner("심연의 봉인이 풀리는 중..."):
        time.sleep(1.0)
    
    weights = [0.05 if item["grade"] == "MYTHIC" 
               else 0.15 if item["grade"] == "LEGENDARY" 
               else 0.30 if item["grade"] == "EPIC" 
               else 0.50 for item in ITEMS]
    
    drawn_item = random.choices(ITEMS, weights=weights, k=1)[0]
    
    st.session_state.open_count += 1
    st.session_state.history.insert(0, drawn_item)
    
    if drawn_item["grade"] in ["MYTHIC", "LEGENDARY"]:
        st.balloons()
    
    # 텍스트 카드 출력
    st.markdown(f"""
        <div class="item-card">
            <div class="item-grade {drawn_item['color']}">&lt; {drawn_item['grade']} &gt;</div>
            <div class="item-name">{drawn_item['name']}</div>
            <div class="item-desc">"{drawn_item['desc']}"</div>
        </div>
    """, unsafe_allow_html=True)
    
    # 기프티콘 이미지 출력
    st.image(drawn_item["img"], caption=f"[{drawn_item['name']}] 사용불가 쿠폰 이미지", use_container_width=True)

# 7. 사이드바 기록
st.sidebar.title("📜 보관함 현황")
st.sidebar.write(f"**총 열어본 상자:** {st.session_state.open_count}회")
st.sidebar.markdown("---")

if st.session_state.history:
    st.sidebar.subheader("최근 획득한 기프티콘")
    for idx, item in enumerate(st.session_state.history[:10]):
        color_class = item['color']
        grade_text = item['grade']
        name_text = item['name']
        st.sidebar.markdown(
            f"**{idx+1}.** <span class='{color_class}'>[{grade_text}]</span> {name_text}", 
            unsafe_allow_html=True
        )
else:
    st.sidebar.info("상자를 열어 기프티콘을 획득하세요.")
