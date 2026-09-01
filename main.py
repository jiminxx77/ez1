import streamlit as st
import random
import time

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="도박중독 치료용 - 바카라 시뮬레이터",
    page_icon="🃏",
    layout="centered"
)

# 2. 다크 판타지 & 바카라 카지노 CSS (카드 쪼으기 애니메이션 포함)
st.markdown("""
    <style>
    .stApp {
        background-color: #0b1013;
        color: #d4af37;
        font-family: 'Georgia', serif;
    }
    
    h1 {
        color: #f1c40f !important;
        text-shadow: 0 0 15px #8b0000, 2px 2px 5px #000000;
        text-align: center;
        letter-spacing: 2px;
    }
    
    .therapy-warning {
        background-color: #1a0c0c;
        border: 1px solid #8b0000;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
        color: #e74c3c;
        font-size: 0.95rem;
        margin-bottom: 20px;
    }

    /* 테이블 영역 */
    .baccarat-table {
        background: radial-gradient(circle, #0e3a1f 0%, #051a0d 100%);
        border: 4px solid #f1c40f;
        border-radius: 20px;
        padding: 25px;
        box-shadow: inset 0 0 30px #000000, 0 0 20px rgba(0,0,0,0.8);
        margin-bottom: 20px;
    }

    /* 카드 스타일 */
    .card-container {
        display: inline-block;
        width: 80px;
        height: 120px;
        margin: 5px;
        perspective: 1000px;
    }

    .card {
        width: 100%;
        height: 100%;
        border-radius: 8px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.5);
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 1.5rem;
        font-weight: bold;
    }

    .card-front {
        background-color: #ffffff;
        color: #111111;
        border: 1px solid #ccc;
    }

    .card-red {
        color: #d63031 !important;
    }

    .card-back {
        background: linear-gradient(135deg, #b21f1f 0%, #1a0808 100%);
        border: 2px solid #f1c40f;
        color: #f1c40f;
    }

    /* 카드 쪼으기 효과 (Squeeze CSS Animation) */
    @keyframes squeezeEffect {
        0% { transform: translateY(0) rotateX(0deg); }
        50% { transform: translateY(-20px) rotateX(40deg); }
        100% { transform: translateY(0) rotateX(0deg); }
    }

    .squeezing {
        animation: squeezeEffect 1.5s ease-in-out infinite;
    }

    /* 베팅 영역 버튼 */
    div.stButton > button {
        border-radius: 10px !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 덱 생성 및 카드 족보 계산 로직
SUITS = ['♠', '♥', '♦', '♣']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

def get_card_value(rank):
    if rank in ['10', 'J', 'Q', 'K']:
        return 0
    elif rank == 'A':
        return 1
    else:
        return int(rank)

def calculate_score(cards):
    total = sum(get_card_value(c['rank']) for c in cards)
    return total % 10

def draw_card():
    rank = random.choice(RANKS)
    suit = random.choice(SUITS)
    color = 'card-red' if suit in ['♥', '♦'] else ''
    return {'rank': rank, 'suit': suit, 'color': color}

# 4. 세션 상태 초기화
if 'virtual_money' not in st.session_state:
    st.session_state.virtual_money = 1000000  # 가상 치유 코인 100만
if 'game_history' not in st.session_state:
    st.session_state.game_history = []
if 'total_lost_virtual' not in st.session_state:
    st.session_state.total_lost_virtual = 0

# 5. UI 헤더 & 치료 메시지
st.title("🃏 도박 중독 치유용 바카라")
st.markdown("""
    <div class="therapy-warning">
        ⚠️ <b>치료 모드 안내:</b> 본 프로그램은 돈을 걸지 않고 도파민 자극만 완화하기 위한 시뮬레이터입니다.<br>
        실제 도박은 뇌의 도파민 체계를 파괴하고 막대한 재산 손실을 초래합니다.
    </div>
""", unsafe_allow_html=True)

# 모드 선택
mode = st.radio(
    "🎮 쪼으기(Squeeze) 연출 모드 선택",
    ["[모드 1] 카드 쪼으기(Squeeze) 연출", "[모드 2] 슬로우 패 뒤집기 연출"],
    horizontal=True
)

st.markdown("---")

# 6. 메인 바카라 게임 레이아웃
col1, col2 = st.columns(2)

with col1:
    bet_target = st.selectbox("🎯 베팅할 대상 선택", ["플레이어 (Player)", "뱅커 (Banker)", "타이 (Tie)"])
with col2:
    bet_amount = st.select_slider(
        "💰 가상 칩 베팅금액 (가상)",
        options=[10000, 50000, 100000, 500000, 1000000],
        value=50000
    )

# 7. 게임 실행 로직
if st.button("🔥 카드 딜링 및 쪼으기 시작", use_container_width=True):
    if st.session_state.virtual_money < bet_amount:
        st.error("가상 코인이 부족합니다. 리셋 버튼을 눌러 충전하세요.")
    else:
        # 카드 뽑기
        player_cards = [draw_card(), draw_card()]
        banker_cards = [draw_card(), draw_card()]
        
        # 내추럴 조건 판정
        p_score = calculate_score(player_cards)
        b_score = calculate_score(banker_cards)
        
        # 3번째 카드 룰 (간단 적용)
        if p_score <= 5 and b_score < 8:
            player_cards.append(draw_card())
            p_score = calculate_score(player_cards)
        if b_score <= 5 and p_score < 8:
            banker_cards.append(draw_card())
            b_score = calculate_score(banker_cards)

        # 애니메이션 스퀴즈 연출
        st.markdown("<div class='baccarat-table'>", unsafe_allow_html=True)
        
        if "[모드 1]" in mode:
            # 쪼으기 딜레이 연출
            with st.spinner("카드를 천천히 쪼으는 중... (Squeezing...)"):
                time.sleep(1.2)
                st.write("🔍 **플레이어 카드 쪼으는 중...**")
                time.sleep(1.0)
                st.write("🔍 **뱅커 카드 쪼으는 중...**")
                time.sleep(1.0)
        else:
            # 서서히 까기 연출
            with st.spinner("딜러가 카드를 서서히 공개합니다..."):
                time.sleep(2.0)

        st.markdown("</div>", unsafe_allow_html=True)

        # 결과 화면 출력
        res_col1, res_col2 = st.columns(2)
        
        with res_col1:
            st.subheader(f"🟦 PLAYER : {p_score}점")
            p_html = ""
            for c in player_cards:
                p_html += f"<div class='card-container'><div class='card card-front {c['color']}'>{c['suit']}{c['rank']}</div></div>"
            st.markdown(p_html, unsafe_allow_html=True)

        with res_col2:
            st.subheader(f"🟥 BANKER : {b_score}점")
            b_html = ""
            for c in banker_cards:
                b_html += f"<div class='card-container'><div class='card card-front {c['color']}'>{c['suit']}{c['rank']}</div></div>"
            st.markdown(b_html, unsafe_allow_html=True)

        # 승패 판정
        st.markdown("<br>", unsafe_allow_html=True)
        if p_score > b_score:
            winner = "플레이어 (Player)"
        elif b_score > p_score:
            winner = "뱅커 (Banker)"
        else:
            winner = "타이 (Tie)"

        # 정산
        if (bet_target.startswith("플레이어") and winner == "플레이어 (Player)") or \
           (bet_target.startswith("뱅커") and winner == "뱅커 (Banker)"):
            win_amount = bet_amount
            st.session_state.virtual_money += win_amount
            st.success(f"🎉 승리! 가상 칩 +{win_amount:,}원 획득! (현재 잔액: {st.session_state.virtual_money:,}원)")
        elif bet_target.startswith("타이") and winner == "타이 (Tie)":
            win_amount = bet_amount * 8
            st.session_state.virtual_money += win_amount
            st.success(f"🎉 TIE 당첨! 가상 칩 +{win_amount:,}원 획득! (현재 잔액: {st.session_state.virtual_money:,}원)")
        elif winner == "타이 (Tie)":
            st.info(f"🤝 TIE (무승부)! 베팅금이 환불됩니다.")
        else:
            st.session_state.virtual_money -= bet_amount
            st.session_state.total_lost_virtual += bet_amount
            st.error(f"💀 패배... 베팅금 -{bet_amount:,}원 소멸 (현재 잔액: {st.session_state.virtual_money:,}원)")

# 8. 사이드바 - 중독 치료 통계 리포트
st.sidebar.title("📊 도박 예방 리포트")
st.sidebar.write(f"**현재 가상 잔액:** {st.session_state.virtual_money:,}원")
st.sidebar.write(f"**누적 가상 손실액:** {st.session_state.total_lost_virtual:,}원")

st.sidebar.markdown("---")
st.sidebar.caption("💡 **치료 팁:** 도박의 '쪼으는 맛'은 뇌에서 도파민을 과도하게 분비시킵니다. 이 앱을 통해 실제 돈 손실 없이 욕구를 다스려보세요.")

if st.sidebar.button("가상 코인 리셋 (100만 충전)"):
    st.session_state.virtual_money = 1000000
    st.session_state.total_lost_virtual = 0
    st.rerun()
