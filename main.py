import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="검 강화하기", page_icon="⚔️", layout="centered")

MAX_LEVEL = 15

SWORD_NAMES = {
    0: "낡은 단검",
    3: "무쇠 검",
    6: "은빛 검",
    9: "마법의 검",
    12: "전설의 검",
    15: "용살자의 검",
}

SWORD_COLORS = {
    0: "#9e9e9e",
    3: "#8d6e63",
    6: "#90caf9",
    9: "#ba68c8",
    12: "#ffb74d",
    15: "#ef5350",
}


def get_tier_value(level, table):
    value = list(table.values())[0]
    for lv, v in table.items():
        if level >= lv:
            value = v
    return value


def get_sword_name(level):
    return get_tier_value(level, SWORD_NAMES)


def get_sword_color(level):
    return get_tier_value(level, SWORD_COLORS)


def get_success_rate(level):
    if level < 3:
        return 100
    elif level < 5:
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
    return 100 + level * 150


def get_sell_price(level):
    return int(get_cost(level) * 0.6 * (level + 1))


def get_destroy_risk(level):
    if level < 10:
        return 0
    elif level < 13:
        return 20
    else:
        return 40


def sword_svg(level):
    color = get_sword_color(level)
    glow = "filter: drop-shadow(0 0 6px " + color + ");" if level >= 9 else ""
    return f"""
    <div style="text-align:center; padding: 10px 0;">
      <svg width="140" height="140" viewBox="0 0 100 100" style="{glow}">
        <line x1="50" y1="10" x2="50" y2="70" stroke="{color}" stroke-width="10" stroke-linecap="round"/>
        <rect x="35" y="65" width="30" height="8" rx="2" fill="#5d4037"/>
        <rect x="46" y="72" width="8" height="20" rx="3" fill="#3e2723"/>
        <circle cx="50" cy="94" r="6" fill="#3e2723"/>
      </svg>
    </div>
    """


# ---------------------------
# 세션 상태 초기화
# ---------------------------
defaults = {
    "level": 0,
    "money": 1000000,
    "protection": 0,
    "use_protection": False,
    "log": [],
    "success_count": 0,
    "fail_count": 0,
    "destroy_count": 0,
    "last_event": None,
    "view": "홈",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

PROTECTION_PRICE = 50000


def enhance():
    level = st.session_state.level
    if level >= MAX_LEVEL:
        return

    cost = get_cost(level)
    if st.session_state.money < cost:
        st.session_state.last_event = ("돈부족", f"강화 비용 {cost:,}원이 필요합니다.")
        return

    st.session_state.money -= cost
    rate = get_success_rate(level)
    roll = random.randint(1, 100)
    used_protection = False

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
        will_destroy = destroy_risk > 0 and destroy_roll <= destroy_risk

        if will_destroy and st.session_state.use_protection and st.session_state.protection > 0:
            st.session_state.protection -= 1
            used_protection = True
            will_destroy = False

        if will_destroy:
            st.session_state.level = 0
            st.session_state.destroy_count += 1
            st.session_state.last_event = ("파괴", "검이 파괴되었습니다... +0으로 초기화됩니다.")
            result = "파괴"
        else:
            new_level = max(0, level - 1) if level >= 10 else level
            st.session_state.level = new_level
            st.session_state.fail_count += 1
            msg = f"강화에 실패했습니다. (+{level} → +{new_level})"
            if used_protection:
                msg += " 🛡️ 방지권이 사용되어 파괴를 막았습니다!"
            st.session_state.last_event = ("실패", msg)
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


def buy_protection():
    if st.session_state.money >= PROTECTION_PRICE:
        st.session_state.money -= PROTECTION_PRICE
        st.session_state.protection += 1
        st.session_state.last_event = ("구매", "방지권을 1개 구매했습니다.")
    else:
        st.session_state.last_event = ("돈부족", "방지권을 구매할 돈이 부족합니다.")


def sell_sword():
    level = st.session_state.level
    price = get_sell_price(level)
    st.session_state.money += price
    st.session_state.level = 0
    st.session_state.last_event = ("판매", f"+{level} 검을 {price:,}원에 판매했습니다.")


def reset_game():
    for k, v in defaults.items():
        st.session_state[k] = v


# ---------------------------
# 상단 네비게이션
# ---------------------------
nav1, nav2, nav3 = st.columns([1, 2, 1])
with nav1:
    if st.button("🎒 아이템창", use_container_width=True):
        st.session_state.view = "아이템창"
with nav2:
    st.markdown("<h2 style='text-align:center; margin:0;'>⚔️ 검 강화하기</h2>", unsafe_allow_html=True)
with nav3:
    if st.button("🏪 상점가기", use_container_width=True):
        st.session_state.view = "상점"

if st.session_state.view != "홈":
    if st.button("⬅️ 강화 화면으로 돌아가기"):
        st.session_state.view = "홈"

st.divider()

level = st.session_state.level

# ---------------------------
# 상점 화면
# ---------------------------
if st.session_state.view == "상점":
    st.subheader("🏪 상점")
    st.write(f"💰 보유 금액: **{st.session_state.money:,}원**")
    st.write(f"🛡️ 보유 방지권: **{st.session_state.protection}개**")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**방지권 구매** — {PROTECTION_PRICE:,}원")
        st.caption("강화 실패 시 검 파괴를 막아줍니다 (+10 이상에서만 발동)")
        if st.button("구매하기", use_container_width=True):
            buy_protection()
    with c2:
        st.markdown(f"**현재 검 판매** — {get_sell_price(level):,}원")
        st.caption(f"+{level} {get_sword_name(level)}을(를) 판매하고 +0으로 초기화")
        if st.button("판매하기", use_container_width=True, disabled=(level == 0)):
            sell_sword()

# ---------------------------
# 아이템창 화면
# ---------------------------
elif st.session_state.view == "아이템창":
    st.subheader("🎒 아이템창")
    st.write(f"⚔️ 현재 검: **+{level} {get_sword_name(level)}**")
    st.write(f"🛡️ 방지권: **{st.session_state.protection}개**")
    st.write(f"💰 돈: **{st.session_state.money:,}원**")

# ---------------------------
# 홈(강화) 화면
# ---------------------------
else:
    st.markdown(f"**강화비용:** {get_cost(level):,}원&nbsp;&nbsp;&nbsp;**판매가격:** {get_sell_price(level):,}원")

    st.markdown(sword_svg(level), unsafe_allow_html=True)

    st.markdown(
        f"<h1 style='text-align:center;'>+{level} {get_sword_name(level)}</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<h3 style='text-align:center; color:#4caf50;'>성공률 {get_success_rate(level)}%</h3>"
        if level < MAX_LEVEL
        else "<h3 style='text-align:center; color:gold;'>최대 강화 달성!</h3>",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"<p style='text-align:center;'>🛡️ 방지권: {st.session_state.protection}&nbsp;&nbsp;&nbsp;💰 돈: {st.session_state.money:,}원</p>",
        unsafe_allow_html=True,
    )

    if level >= 10:
        st.session_state.use_protection = st.checkbox(
            f"🛡️ 방지권 사용 (파괴 위험 {get_destroy_risk(level)}% 방어, 보유: {st.session_state.protection}개)",
            value=st.session_state.use_protection,
            disabled=(st.session_state.protection == 0),
        )

    if level >= MAX_LEVEL:
        st.success("🏆 최대 강화 레벨에 도달했습니다!")
    else:
        cost = get_cost(level)
        disabled = st.session_state.money < cost
        if st.button(f"🔨 강화하기 ({cost:,}원 소모)", use_container_width=True, disabled=disabled):
            enhance()
        if disabled:
            st.caption("💰 돈이 부족합니다. 상점에서 검을 판매하거나 초기화하세요.")

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
