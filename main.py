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
    return
