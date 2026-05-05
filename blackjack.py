import streamlit as st
import bj
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# =====================
# 認証設定の読み込み
# =====================
def to_dict(obj):
    if isinstance(obj, dict):
        return {k: to_dict(v) for k, v in obj.items()}
    else:
        return obj

# Secrets を深い階層まで dict 化
config = to_dict(st.secrets)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)
st.title("ブラックジャックアプリ")

# -------------------------
# ログインフォームの表示制御
# -------------------------
login_placeholder = st.empty()

# 未ログイン時
if not st.session_state.get("authentication_status"):
    # ★ ログアウト後に state が残っていたら削除
    if "state" in st.session_state:
        del st.session_state["state"]
        st.rerun()

    with login_placeholder.container():
        authenticator.login(location="main")

# -------------------------
# ログイン成功時
# -------------------------
if st.session_state.get("authentication_status"):
    login_placeholder.empty()

    st.sidebar.success(f"ログイン中: {st.session_state['name']} さん")

    # ★ ログアウトボタン（v0.3.2 対応）
    if st.sidebar.button("ログアウト"):
        st.session_state['authentication_status'] = None
        st.session_state['name'] = None
        st.session_state['username'] = None

        if "state" in st.session_state:
            del st.session_state["state"]

        st.rerun()

    # =====================
    # ブラックジャック本体
    # =====================

    class State:
        def __init__(self):
            self.state = "play"
            self.deck = bj.Deck()
            self.player = bj.Player(self.deck)

    if "state" not in st.session_state:
        st.session_state.state = State()
    state = st.session_state.state

    container_dealer = st.container(border=True)
    container_dealer.markdown("**Dealer**")
    container_player = st.container(border=True)
    container_player.markdown("**Player**")

    if state.state == "play":
        with st.sidebar:
            if st.button("カードを引く"):
                state.player.draw()
                if state.player.score is None:
                    state.state = "bust"
                    st.rerun()

            if st.button("勝負する"):
                state.state = "showdown"
                st.rerun()

        container_dealer.html(bj.back_cards())
        container_player.html(state.player.show_html())

    elif state.state == "bust":
        with st.sidebar:
            if st.button("再勝負?"):
                del st.session_state.state
                st.rerun()

        container_dealer.html(bj.back_cards())
        container_player.html(state.player.show_html())
        container_player.markdown("どぼん")

    else:
        with st.sidebar:
            if st.button("再勝負？"):
                del st.session_state.state
                st.rerun()

        dealer = bj.Player(state.deck)
        dealer.auto_draw()
        message = state.player.showdown(dealer)

        container_dealer.html(dealer.show_html())
        container_player.html(state.player.show_html())
        container_player.markdown(f"**{message}**")

        if message == "勝ち":
            st.balloons()

elif st.session_state.get("authentication_status") is False:
    st.error("ユーザー名またはパスワードが正しくありません。")

else:
    st.warning("ユーザー名とパスワードを入力してください。")
