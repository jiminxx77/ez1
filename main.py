import streamlit as st
import random

st.set_page_config(page_title="1:1 대전 게임", page_icon="⚔️", layout="centered")

MAX_HP = 100

ATTACK_LINES = ["찰싹!!", "짜악!!", "퍽!! 정통으로 맞음", "따귀 작렬!!"]
MISS_LINES = ["헛스윙... 창피함", "어이쿠 빗나감"]
ULT_LINE = "🔥 필살 싸대기 콤보!! 🔥"

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
    "scene": None,  # (text, kind, direction, anim_key)
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
    st.session_state.scene = None
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


def set_scene(text, kind, direction):
    anim_key = random.randint(0, 999999)
    st.session_state.scene = (text, kind, direction, anim_key)


# ---------------------------
# 캐릭터 SVG (같은 모양, 색만 다름)
# ---------------------------
def character_svg(shirt_color, hat_color="#2b2b2b", flip=False):
    scale_x = -1 if flip else 1
    return f"""
    <svg width="100" height="100" viewBox="0 0 100 100" style="transform: scaleX({scale_x});">
      <path d="M18 30 Q18 4 50 4 Q82 4 82 30 Z" fill="{hat_color}"/>
      <ellipse cx="50" cy="30" rx="33" ry="8" fill="{hat_color}"/>
      <circle cx="50" cy="48" r="29" fill="#ffe3c9"/>
      <circle cx="28" cy="54" r="6.5" fill="#ff9e9e" opacity="0.55" class="blush"/>
      <circle cx="72" cy="54" r="6.5" fill="#ff9e9e" opacity="0.55" class="blush"/>
      <path d="M33 45 Q39 37 46 45" stroke="#222" stroke-width="2.6" fill="none" stroke-linecap="round"/>
      <path d="M54 45 Q61 37 67 45" stroke="#222" stroke-width="2.6" fill="none" stroke-linecap="round"/>
      <path d="M40 60 Q50 72 60 60 Q50 65 40 60 Z" fill="#ff6f91"/>
      <rect x="22" y="76" width="56" height="24" rx="11" fill="{shirt_color}"/>
    </svg>
    """


BATTLE_CSS = """
<style>
.arena {
    position: relative;
    height: 150px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 8%;
    margin: 6px 0 6px 0;
    background: repeating-linear-gradient(45deg, #fff8e1, #fff8e1 10px, #ffecb3 10px, #ffecb3 20px);
    border: 3px solid #333;
    border-radius: 10px;
    overflow: hidden;
}
.char-box { position: relative; text-align: center; z-index: 1; }
.char-box .cheek-mark {
    position: absolute;
    top: 46%;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: radial-gradient(circle, #ff1744 0%, rgba(255,23,68,0) 70%);
    opacity: 0;
}
.char-box.left .cheek-mark { right: 8px; }
.char-box.right .cheek-mark { left: 8px; }
.char-box.hit svg { animation: headShake 0.45s ease-in-out; }
.char-box.hit .cheek-mark { animation: markPop 0.5s ease-out 0.32s forwards; }
@keyframes headShake {
    0%, 100% { transform: rotate(0deg); }
    25% { transform: rotate(-10deg); }
    50% { transform: rotate(8deg); }
    75% { transform: rotate(-6deg); }
}
@keyframes markPop {
    0%   { opacity: 0; transform: scale(0.2); }
    55%  { opacity: 0.9; transform: scale(1.6); }
    100% { opacity: 0.75; transform: scale(1.2); }
}
.hand {
    position: absolute;
    top: 45px;
    font-size: 2.6rem;
    opacity: 0;
    z-index: 2;
}
.hand.ult { font-size: 3.6rem; }
.hand.r2l.hit { animation: slapR2L 0.55s ease-in forwards; }
.hand.l2r.hit { animation: slapL2R 0.55s ease-in forwards; }
.hand.r2l.miss { animation: missR2L 0.7s ease-in forwards; }
.hand.l2r.miss { animation: missL2R 0.7s ease-in forwards; }
@keyframes slapL2R {
    0%   { left: 18%; opacity: 0; transform: rotate(-40deg) scale(0.6); }
    20%  { opacity: 1; }
    65%  { left: 62%; transform: rotate(15deg) scale(1.4); }
    100% { left: 68%; opacity: 0; transform: rotate(35deg) scale(0.9); }
}
@keyframes slapR2L {
    0%   { left: 68%; opacity: 0; transform: rotate(40deg) scaleX(-1) scale(0.6); }
    20%  { opacity: 1; }
    65%  { left: 24%; transform: rotate(-15deg) scaleX(-1) scale(1.4); }
    100% { left: 18%; opacity: 0; transform: rotate(-35deg) scaleX(-1) scale(0.9); }
}
@keyframes missL2R {
    0%   { left: 18%; top: 45px; opacity: 0; transform: rotate(-20deg) scale(0.6); }
    20%  { opacity: 1; }
    55%  { left: 55%; top: 5px; transform: rotate(30deg) scale(1.1); }
    100% { left: 75%; top: 45px; opacity: 0; transform: rotate(180deg) scale(0.7); }
}
@keyframes missR2L {
    0%   { left: 68%; top: 45px; opacity: 0; transform: rotate(20deg) scaleX(-1) scale(0.6); }
    20%  { opacity: 1; }
    55%  { left: 30%; top: 5px; transform: rotate(-30deg) scaleX(-1) scale(1.1); }
    100% { left: 10%; top: 45px; opacity: 0; transform: rotate(-180deg) scaleX(-1) scale(0.7); }
}
.arena.shake { animation: shakeStage 0.45s ease-in-out; }
@keyframes shakeStage {
    0%, 100% { transform: translateX(0); }
    25% { transform: translateX(-6px); }
    50% { transform: translateX(6px); }
    75% { transform: translateX(-4px); }
}
.caption-line { text-align: center; font-weight: 900; margin: 4px 0 12px 0; }
.caption-line.hit { color: #ff5252; }
.caption-line.ult { color: #d50000; font-size: 1.2rem; }
.caption-line.miss { color: #9e9e9e; }
</style>
"""


def render_battle_scene():
    st.markdown(BATTLE_CSS, unsafe_allow_html=True)

    p1_svg = character_svg("#b39ddb")            # 플레이어1: 보라색
    p2_svg = character_svg("#4fc3f7", flip=True)  # 플레이어2: 하늘색 (서로 마주보게 좌우반전)

    p1_hit_class = ""
    p2_hit_class = ""
    hand_html = ""
    shake_class = ""

    if st.session_state.scene:
        text, kind, direction, anim_key = st.session_state.scene
        shake_class = "shake" if kind != "miss" else ""
        anim_result_class = "hit" if kind in ("hit", "ult") else "miss"
        hand_kind_class = "ult" if kind == "ult" else ""

        if direction == "l2r":
            hand_dir_class = "l2r"
            if kind != "miss":
                p2_hit_class = "hit"
        else:
            hand_dir_class = "r2l"
            if kind != "miss":
                p1_hit_class = "hit"

        hand_html = f'<div class="hand {hand_dir_class} {anim_result_class} {hand_kind_class}" id="h{anim_key}">🖐️</div>'
        caption = f'<div class="caption-line {kind}">{text}</div>'
    else:
        caption = '<div class="caption-line">&nbsp;</div>'

    html = f"""
    <div class="arena {shake_class}">
        <div class="char-box left {p1_hit_class}">
            {p1_svg}
            <div class="cheek-mark"></div>
        </div>
        {hand_html}
        <div class="char-box right {p2_hit_class}">
            {p2_svg}
            <div class="cheek-mark"></div>
        </div>
    </div>
    {caption}
    """
    st.markdown(html, unsafe_allow_html=True)


def do_action(action):
    attacker = st.session_state.turn
    target = other(attacker)
    direction = "l2r" if attacker == "p1" else "r2l"

    if action == "attack":
        dmg = random.randint(12, 20)
        actual = apply_damage(target, dmg)
        add_log(f"⚔️ {name(attacker)}의 공격! {name(target)}에게 {actual}의 피해!")
        set_scene(random.choice(ATTACK_LINES), "hit", direction)

    elif action == "heavy":
        if random.randint(1, 100) <= 65:
            dmg = random.randint(25, 38)
            actual = apply_damage(target, dmg)
            add_log(f"💥 {name(attacker)}의 강공격 명중! {name(target)}에게 {actual}의 피해!")
            set_scene(random.choice(ATTACK_LINES), "hit", direction)
        else:
            add_log(f"❌ {name(attacker)}의 강공격이 빗나갔습니다!")
            set_scene(random.choice(MISS_LINES), "miss", direction)

    elif action == "defend":
        st.session_state.defending[attacker] = True
        add_log(f"🛡️ {name(attacker)}이(가) 방어 태세를 갖췄습니다. (다음 피해 50% 감소)")
        st.session_state.scene = None

    elif action == "ultimate":
        dmg = random.randint(35, 50)
        st.session_state.hp[target] = max(0, st.session_state.hp[target] - dmg)
        st.session_state.defending[target] = False
        st.session_state.ultimate_used[attacker] = True
        add_log(f"🔥 {name(attacker)}의 필살기 작렬! {name(target)}에게 {dmg}의 피해! (방어 무시)")
        set_scene(ULT_LINE, "ult", direction)

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
    st.caption("같은 화면에서 두 명이 번갈아 플레이하는 핫시트 PVP 게임입니다. 공격할 때마다 캐릭터가 싸대기를 날립니다.")
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

    render_battle_scene()

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
