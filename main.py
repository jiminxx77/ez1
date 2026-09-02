import streamlit as st
import random
import pandas as pd

# ---------------------------
# 기본 설정
# ---------------------------
st.set_page_config(
    page_title="검 강화하기",
    page_icon="⚔️",
    layout="centered",
)

MAX_LEVEL = 15

SWORD_NAMES = {
    0: "낡은 검",
    3: "단단한 검",
    6: "빛나는 검",
    9: "전설의 검",
    12: "신화의 검",
    15: "용살자의 검",
}

def get_sword_name(level):
    name = "낡은 검"
    for lv, n in SWORD_NAMES.items():
        if level >= lv:
            name = n
    return name


def get_success_rate(level):
    """레벨이 높을수록 성공 확률 감소"""
    if level < 5:
        return 90
    elif level < 8:
        return 70
    elif level < 11:
        return 50
    elif level < 13:
        return 30
    else:
        return 15


def get_cost(level):
    """레벨이 높을수록 강화 비용 증가"""
    return 100 + level * 80


def get_destroy_risk(level):
    """레벨 10 이상부터 실패 시 파괴 위험 등장"""
    if level < 10:
        return 0
    elif level < 13:
        return 20
    else:
        return 40


# ---------------------------
# 세션 상태 초기화
# ---------------------------
if "level" not in st.session_state:
    st.session_state.level = 0
if "gold" not in st.session_state:
    st.session_state.gold = 1000
if "log" not in st.session_state:
    st.session_state.log = []
if "success_count" not in st.session_state:
    st.session_state.success_count = 0
if "fail_count" not in st.session_state:
    st.session_state.fail_count = 0
if "destroy_count" not in st.session_state:
    st.session_state.destroy_count = 0
if "last_event" not in st.session_state:
    st.session_state.last_event = None


def enhance():
    level = st.session_state.level
    if level >= MAX_LEVEL:
        return

    cost = get_cost(level)
    if st.session_state.gold < cost:
        st.session_state.last_event = ("골드 부족", f"강화 비용 {cost} 골드가 필요합니다.")
        return

    st.session_state.gold -= cost
    rate = get_success_rate(level)
    roll = random.randint(1, 100)

    if roll <= rate:
        st.session_state.level += 1
        st.session_state.success_count += 1
        st.session_state.last_event = (
            "성공",
            f"+{level} → +{st.session_state.level} 강화 성공! ({get_sword_name(st.session_state.level)})",
        )
        result = "성공"
    else:
        destroy_risk = get_destroy_risk(level)
        destroy_roll = random.randint(1, 100)
        if destroy_risk > 0 and destroy_roll <= destroy_risk:
            st.session_state.level = 0
            st.session_state.destroy_count += 1
            st.session_state.last_event = ("파괴", "검이 파괴되었습니다... +0으로 초기화됩니다.")
            result = "파괴"
        else:
            new_level = max(0, level - 1) if level >= 10 else level
            st.session_state.level = new_level
            st.session_state.fail_count += 1
            st.session_state.last_event = ("실패", f"강화에 실패했습니다. (+{level} → +{new_level})")
            result = "실패"

    st.session_state.log.append(
        {
            "시도": len(st.session_state.log) + 1,
            "시도 전 레벨": f"+{level}",
            "비용": cost,
            "확률": f"{rate}%",
            "결과": result,
        }
    )


def reset_game():
    st.session_state.level = 0
    st.session_state.gold = 1000
    st.session_state.log = []
    st.session_state.success_count = 0
    st.session_state.fail_count = 0
    st.session_state.destroy_count = 0
    st.session_state.last_event = None


# ---------------------------
# 헤더
# ---------------------------
st.title("⚔️ 검 강화하기")
st.caption("골드를 사용해 검을 강화하세요. 레벨이 높아질수록 성공 확률은 낮아지고, +10 이상부터는 실패 시 검이 파괴될 수도 있습니다.")

st.divider()

# ---------------------------
# 현재 상태
# ---------------------------
level = st.session_state.level
col1, col2, col3 = st.columns(3)
col1.metric("현재 검", f"+{level} {get_sword_name(level)}")
col2.metric("보유 골드", f"{st.session_state.gold} G")
col3.metric("성공 확률", f"{get_success_rate(level)}%" if level < MAX_LEVEL else "MAX")

st.progress(min(level / MAX_LEVEL, 1.0), text=f"강화 진행도 ({level} / {MAX_LEVEL})")

if level >= 10:
    st.warning(f"⚠️ 실패 시 파괴 확률 {get_destroy_risk(level)}% — 신중하게 강화하세요!")

st.divider()

# ---------------------------
# 강화 버튼
# ---------------------------
cost = get_cost(level)

if level >= MAX_LEVEL:
    st.success("🏆 최대 강화 레벨에 도달했습니다! 축하합니다!")
else:
    btn_label = f"🔨 강화하기 ({cost} G 소모)"
    disabled = st.session_state.gold < cost
    if st.button(btn_label, use_container_width=True, disabled=disabled):
        enhance()
    if disabled:
        st.caption("💰 골드가 부족합니다. 초기화 후 다시 시도해보세요.")

# ---------------------------
# 최근 결과
# ---------------------------
if st.session_state.last_event:
    event_type, msg = st.session_state.last_event
    if event_type == "성공":
        st.success(msg)
    elif event_type == "실패":
        st.error(msg)
    elif event_type == "파괴":
        st.error(f"💥 {msg}")
    else:
        st.info(msg)

st.divider()

# ---------------------------
# 통계
# ---------------------------
st.subheader("📊 강화 기록")

total = st.session_state.success_count + st.session_state.fail_count + st.session_state.destroy_count

if total == 0:
    st.write("아직 강화 시도가 없습니다. 위 버튼을 눌러 시작해보세요!")
else:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("성공", st.session_state.success_count)
    c2.metric("실패", st.session_state.fail_count)
    c3.metric("파괴", st.session_state.destroy_count)
    c4.metric("총 시도", total)

    chart_df = pd.DataFrame(
        {
            "결과": ["성공", "실패", "파괴"],
            "횟수": [
                st.session_state.success_count,
                st.session_state.fail_count,
                st.session_state.destroy_count,
            ],
        }
    ).set_index("결과")
    st.bar_chart(chart_df)

    with st.expander("전체 강화 기록 보기"):
        log_df = pd.DataFrame(st.session_state.log)
        st.dataframe(log_df, use_container_width=True, hide_index=True)

st.divider()
if st.button("🔄 게임 초기화"):
    reset_game()
    st.rerun()
