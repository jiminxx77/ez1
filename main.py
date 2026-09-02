import streamlit as st
import random

st.set_page_config(page_title="1:1 대전 게임", page_icon="⚔️", layout="centered")

MAX_HP = 100

ATTACK_LINES = [
    "신태일 등장! 박치기 발사!!",
    "어디서 신태일이 나타나서 냅다 후려침",
    "신태일: \"내가 왔다!\" 퍽!!!",
    "갑자기 나타난 신태일... 그대로 스매시",
]
MISS_LINES = ["신태일... 헛스윙 ㅋㅋㅋ", "어이쿠 빗나감 신태일 창피함"]
ULT_LINE = "신태일 필살! 궁극의 드롭킥!!"

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
    "scene": None,   # (문구, kind, anim_key)
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


def set_scene(text, kind):
    # 매번 다른 key를 줘서 애니메이션이 재생될 때마다 새로 재시작되도록 함
    anim_key = random.randint(0, 999999)
    st.session_state.scene = (text, kind, anim_key)


BATTLE_SCENE_CSS = """
<style>
.stage {
    position: relative;
    height: 150px;
    overflow: hidden;
    margin: 6px 0 14px 0;
    background: repeating-linear-gradient(45deg, #fff8e1, #fff8e1 10px, #ffecb3 10px, #ffecb3 20px);
    border: 3px solid #333;
    border-radius: 10px;
}
.fighter {
    position: absolute;
    top: 40px;
    left: 50%;
    font-size: 3.2rem;
    transform: translate(-50%, -50%) scale(0.3);
    opacity: 0;
}
.fighter.hit {
    animation: flyHit 0.9s ease-out forwards;
}
.fighter.ult {
    animation: flyUlt 1.2s ease-out forwards;
    font-size: 4.2rem;
}
.fighter.miss {
    animation: flyMiss 0.9s ease-in forwards;
}
@keyframes flyHit {
    0%   { transform: translate(-220%, -50%) rotate(-30deg) scale(0.4); opacity: 0; }
    12%  { opacity: 1; }
    45%  { transform: translate(-50%, -50%) rotate(8deg) scale(1.5); opacity: 1; }
    55%  { transform: translate(-50%, -50%) rotate(-12deg) scale(1.3); }
    100% { transform: translate(120%, -50%) rotate(25deg) scale(0.4); opacity: 0; }
}
@keyframes flyUlt {
    0%   { transform: translate(-250%, -80%) rotate(-40deg) scale(0.3); opacity: 0; }
    10%  { opacity: 1; }
    40%  { transform: translate(-50%, -50%) rotate(15deg) scale(2); opacity: 1; }
    50%  { transform: translate(-50%, -50%) rotate(-15deg) scale(1.8); }
    60%  { transform: translate(-50%, -50%) rotate(15deg) scale(1.9); }
    100% { transform: translate(200%, 60%) rotate(50deg) scale(0.3); opacity: 0; }
}
@keyframes flyMiss {
    0%   { transform: translate(-220%, -50%) rotate(-20deg) scale(0.4); opacity: 0; }
    15%  { opacity: 1; }
    50%  { transform: translate(-30%, -80%) rotate(20deg) scale(1.1); }
    100% { transform: translate(220%, 40%) rotate(180deg) scale(0.4); opacity: 0; }
}
.impact {
    position: absolute;
    top: 40px;
    left: 50%;
    font-size: 2.4rem;
    transform: translate(-50%, -50%) scale(0);
    opacity: 0;
}
.impact.hit { animation: burst 0.5s ease-out 0.35s forwards; }
.impact.ult { animation: burstUlt 0.7s ease-out 0.35s forwards; font-size: 3.4rem; }
@keyframes burst {
    0%   { transform: translate(-50%, -50%) scale(0) rotate(0deg); opacity: 0; }
    30%  { transform: translate(-50%, -50%) scale(1.6) rotate(20deg); opacity: 1; }
    100% { transform: translate(-50%, -50%) scale(0.8) rotate(0deg); opacity: 0; }
}
@keyframes burstUlt {
    0%   { transform: translate(-50%, -50%) scale(0) rotate(0deg); opacity: 0; }
    30%  { transform: translate(-50%, -50%) scale(2.2) rotate(30deg); opacity: 1; }
    100% { transform: translate(-50%, -50%) scale(1) rotate(0deg); opacity: 0; }
}
.stage.shake { animation: shakeStage 0.5s ease-in-out; }
@keyframes shakeStage {
    0%, 100% { transform: translateX(0); }
    20% { transform: translateX(-8px); }
    40% { transform: translateX(8px); }
    60% { transform: translateX(-6px); }
    80% { transform: translateX(6px); }
}
.caption-line {
    text-align: center;
    font-weight: 900;
    margin-top: -4px;
    padding: 6px;
}
.caption-line.hit { color: #ff7043; }
.caption-line.ult { color: #e53935; font-size: 1.2rem; }
.caption-line.miss { color: #9e9e9e; }
</style>
"""


def render_battle_scene():
    st.markdown(BATTLE_SCENE_CSS, unsafe_allow_html=True)

    if not st.session_state.scene:
        st.markdown('<div class="stage"></div>', unsafe_allow_html=True)
        return

    text, kind, anim_key = st.session_state.scene
    char = "🐐"
    impact_emoji = "💥⭐" if kind != "ult" else "🔥💥🔥"
    impact_class = "ult" if kind == "ult" else ("hit" if kind == "hit" else "")

    impact_html = f'<div class="impact {impact_class}">{impact_emoji}</div>' if kind != "miss" else ""

    html = f"""
    <div class="stage shake" id="stage-{anim_key}">
        <div class="fighter {kind}">{char}</div>
        {impact_html}
    </div>
    <div class="caption-line {kind}">{text}</div>
    """
    st.markdown(html, unsafe_allow_html=True)


def do_action(action):
    attacker = st.session_state.turn
    target = other(attacker)

    if action == "attack":
        dmg = random.randint(12, 20)
        actual = apply_damage(target, dmg)
        add_log(f"⚔️ {name(attacker)}의 공격! {name(target)}에게 {actual}의 피해!")
        set_scene(random.choice(ATTACK_LINES), "hit")

    elif action == "heavy":
        if random.randint(1, 100) <= 65:
            dmg = random.randint(25, 38)
            actual = apply_damage(target, dmg)
            add_log(f"💥 {name(attacker)}의 강공격 명중! {name(target)}에게 {actual}의 피해!")
            set_scene(random.choice(ATTACK_LINES), "hit")
        else:
            add_log(f"❌ {name(attacker)}의 강공격이 빗나갔습니다!")
            set_scene(random.choice(MISS_LINES), "miss")

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
        set_scene(ULT_LINE, "ult")

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
    st.caption("같은 화면에서 두 명이 번갈아 플레이하는 핫시트 PVP 게임입니다. 공격할 때마다 신태일이 날아와서 때립니다.")
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
