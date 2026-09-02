import streamlit as st
import random

st.set_page_config(page_title="1:1 대전 게임", page_icon="⚔️", layout="centered")

MAX_HP = 100

# 병맛 효과 문구 (원하는 대로 수정하세요)
ATTACK_MEMES = [
    "신태일 등장! 박치기 발사!! 🐐",
    "어디서 신태일이 나타나서 냅다 후려침 💢",
    "신태일: \"내가 왔다!\" 퍽!!! 👊",
    "갑자기 나타난 신태일... 그대로 스매시 💥",
]

ULTIMATE_MEME = "🌪️ 신태일 필살! 궁극의 드롭킥!! 🐐💥"

# ---------------------------
# 세션 상태 초기화
# ---------------------------
defaults = {
    "stage": "setup",
    "p1_name": "",
    "p2_name": "",
    "hp": {"p1": MAX_HP, "p2": MAX_HP},
    "defending": {"p1": False, "p2": False},
    "ultimate_used": {"p1": False, "p2": False},
    "turn": "p1",
    "log": [],
    "winner": None,
    "effect": None,   # (문구, 타입)
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def name(pid):
    return st.session_state.p1_name if pid == "p1" else st.session_state.p2_name


def other(pid):
    return "p2" if pid == "p1" else "p1"


def start_game():
    if not st.session_state.p1_name.strip():
        st.session_state.p1_name = "플레이어 1"
    if not st.session_state.p2_name.strip():
        st.session_state.p2_name = "플레이어 2"
    st.session_state.hp = {"p1": MAX_HP, "p2": MAX_HP}
    st.session_state.defending = {"p1": False, "p2": False}
    st.session_state.ultimate_used = {"p1": False, "p2": False}
    st.session_state.turn = "p1"
    st.session_state.log = []
    st.session_state.winner = None
    st.session_state.effect = None
    st.session_state.stage = "battle"


def add_log(text):
    st.session_state.log.insert(0, text)


def apply_damage(target, dmg):
    if st.session_state.defending[target]:
        dmg = int(dmg * 0.5)
        st.session_state.defending[target] = False
    st.session_state.hp[target] = max(0, st.session_state.hp[target] - dmg)
    return dmg


def end_turn_check():
    for pid in ["p1", "p2"]:
        if st.session_state.hp[pid] <= 0:
            st.session_state.winner = other(pid)
            st.session_state.stage = "result"
            return True
    return False


def show_effect(text, kind="normal"):
    st.session_state.effect = (text, kind)


def render_effect():
    if not st.session_state.effect:
        return
    text, kind = st.session_state.effect
    color = "#ff5252" if kind == "ultimate" else "#ffca28"
    size = "2.2rem" if kind == "ultimate" else "1.5rem"
    st.markdown(
        f"""
        <style>
        @keyframes popShake {{
            0%   {{ transform: scale(0.2) rotate(-8deg); opacity: 0; }}
            30%  {{ transform: scale(1.15) rotate(4deg); opacity: 1; }}
            45%  {{ transform: scale(0.95) rotate(-3deg); }}
            60%  {{ transform: scale(1.05) rotate(2deg); }}
            100% {{ transform: scale(1) rotate(0deg); opacity: 1; }}
        }}
        @keyframes shakeScreen {{
            0%, 100% {{ transform: translateX(0); }}
            20% {{ transform: translateX(-6px); }}
            40% {{ transform: translateX(6px); }}
            60% {{ transform: translateX(-4px); }}
            80% {{ transform: translateX(4px); }}
        }}
        .effect-box {{
            text-align: center;
            font-size: {size};
            font-weight: 900;
            color: {color};
            -webkit-text-stroke: 1px black;
            animation: popShake 0.5s ease-out, shakeScreen 0.4s ease-in-out;
            padding: 12px;
            margin: 6px 0 14px 0;
            border: 3px dashed {color};
            border-radius: 12px;
            background: #fff8e1;
        }}
        </style>
        <div class="effect-box">💥 {text} 💥</div>
        """,
        unsafe_allow_html=True,
    )


def do_action(action):
    attacker = st.session_state.turn
    target = other(attacker)

    if action == "attack":
        dmg = random.randint(12, 20)
        actual = apply_damage(target, dmg)
        add_log(f"⚔️ {name(attacker)}의 공격! {name(target)}에게 {actual}의 피해!")
        show_effect(random.choice(ATTACK_MEMES), "normal")

    elif action == "heavy":
        if random.randint(1, 100) <= 65:
            dmg = random.randint(25, 38)
            actual = apply_damage(target, dmg)
            add_log(f"💥 {name(attacker)}의 강공격 명중! {name(target)}에게 {actual}의 피해!")
            show_effect(random.choice(ATTACK_MEMES), "normal")
        else:
            add_log(f"❌ {name(attacker)}의 강공격이 빗나갔습니다!")
            show_effect("신태일... 헛스윙 ㅋㅋㅋ 🐐💨", "normal")

    elif action == "defend":
        st.session_state.defending[attacker] = True
        add_log(f"🛡️ {name(attacker)}이(가) 방어 태세를 갖췄습니다. (다음 피해 50% 감소)")
        st.session_state.effect = None

    elif action == "ultimate":
        dmg = random.randint(35, 50)
        st.session_state.hp[target] = max(0, st.session_state.hp[target] - dmg)
        st.session_state.defending[target] = False
        st.session_state.ultimate_used[attacker] = True
        add_log(f"🔥 {name(attacker)}의 필살기 작렬! {name(target)}에게 {dmg}의 피해! (방어 무시)")
        show_effect(ULTIMATE_MEME, "ultimate")

    if end_turn_check():
        return

    st.session_state.turn = target


def reset_all():
    for k, v in defaults.items():
        st.session_state[k] = v


# ---------------------------
# 화면: 설정
# ---------------------------
if st.session_state.stage == "setup":
    st.title("⚔️ 1:1 대전 게임")
    st.caption("같은 화면에서 두 명이 번갈아 플레이하는 핫시트 PVP 게임입니다. 공격할 때마다 병맛 이펙트가 터집니다.")
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.session_state.p1_name = st.text_input("플레이어 1 이름", placeholder="이름 입력")
    with col2:
        st.session_state.p2_name = st.text_input("플레이어 2 이름", placeholder="이름 입력")

    st.divider()
    st.markdown("**게임 규칙**")
    st.markdown(
        "- ⚔️ 공격: 12~20 피해, 항상 명중\n"
        "- 💥 강공격: 25~38 피해, 65% 확률로 명중\n"
        "- 🛡️ 방어: 다음 턴에 받는 피해 50% 감소\n"
        "- 🔥 필살기: 35~50 피해, 방어 무시, 게임당 1회만 사용 가능\n"
        "- 먼저 상대 HP를 0으로 만들면 승리!"
    )

    if st.button("🎮 게임 시작", use_container_width=True):
        start_game()
        st.rerun()

# ---------------------------
# 화면: 전투
# ---------------------------
elif st.session_state.stage == "battle":
    p1, p2 = "p1", "p2"

    st.markdown(f"<h2 style='text-align:center;'>⚔️ {name(p1)} VS {name(p2)}</h2>", unsafe_allow_html=True)
    st.divider()

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**{name(p1)}**" + (" 🎯 (턴)" if st.session_state.turn == p1 else ""))
        st.progress(st.session_state.hp[p1] / MAX_HP, text=f"HP {st.session_state.hp[p1]} / {MAX_HP}")
        if st.session_state.defending[p1]:
            st.caption("🛡️ 방어 중")
    with c2:
        st.markdown(f"**{name(p2)}**" + (" 🎯 (턴)" if st.session_state.turn == p2 else ""))
        st.progress(st.session_state.hp[p2] / MAX_HP, text=f"HP {st.session_state.hp[p2]} / {MAX_HP}")
        if st.session_state.defending[p2]:
            st.caption("🛡️ 방어 중")

    render_effect()

    st.divider()

    current = st.session_state.turn
    st.markdown(f"### 🎯 지금은 **{name(current)}**의 턴입니다")

    b1, b2, b3, b4 = st.columns(4)
    with b1:
        if st.button("⚔️ 공격", use_container_width=True):
            do_action("attack")
            st.rerun()
    with b2:
        if st.button("💥 강공격", use_container_width=True):
            do_action("heavy")
            st.rerun()
    with b3:
        if st.button("🛡️ 방어", use_container_width=True):
            do_action("defend")
            st.rerun()
    with b4:
        ult_used = st.session_state.ultimate_used[current]
        if st.button("🔥 필살기", use_container_width=True, disabled=ult_used):
            do_action("ultimate")
            st.rerun()
        if ult_used:
            st.caption("이미 사용함")

    st.divider()
    st.subheader("📜 전투 로그")
    for entry in st.session_state.log[:8]:
        st.write(entry)

    st.divider()
    if st.button("🔄 처음부터 다시하기"):
        reset_all()
        st.rerun()

# ---------------------------
# 화면: 결과
# ---------------------------
elif st.session_state.stage == "result":
    winner = st.session_state.winner
    st.balloons()
    st.markdown(
        f"<h1 style='text-align:center;'>🏆 {name(winner)} 승리! 🏆</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<p style='text-align:center;'>{name('p1')} {st.session_state.hp['p1']} HP "
        f"&nbsp;&nbsp;vs&nbsp;&nbsp; {name('p2')} {st.session_state.hp['p2']} HP</p>",
        unsafe_allow_html=True,
    )

    st.divider()
    st.subheader("📜 전투 기록")
    for entry in reversed(st.session_state.log):
        st.write(entry)

    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔁 같은 이름으로 다시하기", use_container_width=True):
            p1n, p2n = st.session_state.p1_name, st.session_state.p2_name
            reset_all()
            st.session_state.p1_name = p1n
            st.session_state.p2_name = p2n
            st.session_state.stage = "setup"
            st.rerun()
    with c2:
        if st.button("🏠 처음 화면으로", use_container_width=True):
            reset_all()
            st.rerun()
