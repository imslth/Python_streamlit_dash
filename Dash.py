import streamlit as st
from streamlit_login_auth_ui import __login__
from page import Maps, Main, Dashboard, Reviews, Add
from Pages import page_group
from page.backend.Token import TOKEN


def main():
    page = page_group("p")

    with st.sidebar:
        with st.expander("✉️Общие данные", True):
            page.item('Main page', Main.main, default=True)

        with st.expander("🏢 Жилые комплексы", False):
            page.item("Maps Developers", Maps.main)
            page.item("Dashboard Developers", Dashboard.main)
            page.item("Reviews Developers", Reviews.main)
            page.item("Add Developer", Add.main)

        with st.expander("🚛 Автодилеры", False):
            page.item("Maps Dilers", Maps.main)
            page.item("Dashboard Dilers", Dashboard.main)
            page.item("Reviews Dilers", Reviews.main)
            page.item("Add Diler", Add.main)

    page.show()

if __name__ == "__main__":
    st.set_page_config(page_title="Дашборд - Яндекс.Карты", page_icon="🗺", layout="wide")

    __login__obj = __login__(auth_token=TOKEN,
                             company_name="Shims",
                             width=200, height=250,
                             hide_menu_bool=False,
                             logout_button_name='Выход',
                             hide_footer_bool=False,
                             lottie_url='https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

    LOGGED_IN = __login__obj.build_login_ui()

    if LOGGED_IN:
        main()
