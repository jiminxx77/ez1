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
        margin-bottom: 5px;
    }
    
    .mythic { color: #ff0055; text-shadow: 0 0 10px #ff0055; }
    .legendary { color: #f1c40f; text-shadow: 0 0 10px #f1c40f; }
    .epic { color: #a335ee; text-shadow: 0 0 10px #a335ee; }
    .rare { color: #0070dd; text-shadow: 0 0 10px #0070dd; }
    </style>
""", unsafe_allow_html=True)

# 3. 상품 데이터베이스 (필요 시 img에 직접 가진 기프티콘 이미지 파일명이나 URL을 넣으시면 됩니다)
ITEMS = [
    {
        "grade": "MYTHIC", 
        "name": "황금 치킨 기프티콘", 
        "desc": "마마의 신성한 축복이 담긴 바삭한 치킨 교환권입니다.", 
        "color": "mythic",
        "img": "https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=500&q=80"
    },
    {
        "grade": "LEGENDARY", 
        "name": "스타벅스 커피 교환권", 
        "desc": "마마가 챙겨준 아침의 아메리카노 한 잔입니다.", 
        "color": "legendary",
        "img": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=500&q=80"
    },
    {
        "grade": "EPIC", 
        "name": "편의점 5,000원 상품권", 
        "desc": "마마 몰래 주전부리를 사 먹을 수 있는 소중한 상품권입니다.", 
        "color": "epic",
        "img": "https://images.unsplash.com/photo-1607344645866-009c320c5ab8?w=500&q=80"
    },
    {
        "grade": "RARE", 
        "name": "달콤한 아이스크림 교환권", 
        "desc": "식후에 즐기는 마마 추천 디저트 쿠폰입니다.", 
        "color": "rare",
        "img": "https://images.unsplash.com/photo-1513151233558-d860c5398176?w=500&q=80"
    },
]

# 4. 세션 상태 초기화
if "history" not in st.session_state:
    st.session_state.history = []
if "open_count" not in st.session_state:
    st.session_state.open_count = 0

# 5. UI 헤더
st.title("🎁 마마보이에 깊콘 뽑기")
st.caption("버튼을 눌러 마마의 기프티콘을 당첨 받아보세요!")

st.markdown("<br>", unsafe_allow_html=True)

# 6. 상자 개봉 로직
if st.button("🔮 기프티콘 뽑기"):
    with st.spinner("마마의 은총을 불러오는 중..."):
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
    
    # 기프티콘 이미지 단독 출력 (수식어/캡션 제거)
    st.image(drawn_item["img"], use_container_width=True)

# 7. 사이드바 기록
st.sidebar.title("📜 보관함 현황")
st.sidebar.write(f"**총 뽑은 횟수:** {st.session_state.open_count}회")
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
    st.sidebar.info("버튼을 눌러 기프티콘을 뽑아보세요.")
