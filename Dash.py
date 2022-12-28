import streamlit as st

from page.backend.Custom_login import __login__
from page import Maps, Main, Dashboard, Reviews, Add
from Pages import page_group
from page.backend.Token import TOKEN


# Главный скрипт, который объединяет все и сразу в Streamlit)
def main():
    # Здесь происходит реализация многостраничного приложения. По умолчанию в streamlit есть возможность простого
    # создания многостраничного приложения через добавление в папку pages документов - streamlit сам поймет что это
    # другие страницы и правильно их рендерит. Но! У нас тут аутентификация и этот вариант нам не подходит т.к. доп
    # страницы стандартным способом загружаются в приоритете. Кастомная реализация взята с
    # https://github.com/okld/streamlit-elements
    page = page_group("p")

    with st.sidebar:
        with st.expander("✉️Общие данные", True):
            page.item('Main page', Main.main, default=True)
        # Страницы по жк и дилерам одинаковые, рендерятся одинаково, изменяются только данные внутри графиков. В
        # Session_state прописано как и почему.

        # В зависимости от пользователя, который зашел на страницу, показываем ему только те элементы, которые нужны.
        if st.session_state['user_login'] == 'Developer' or st.session_state['user_login'] == 'dhlybov' or \
                st.session_state['user_login'] == 'admin':
            with st.expander("🏢 Девелопмент", False):
                page.item("Maps Developers", Maps.main)
                page.item("Dashboard Developers", Dashboard.main)
                page.item("Reviews Developers", Reviews.main)
                page.item("Add Developer", Add.main)

        if st.session_state['user_login'] == 'Diler' or st.session_state['user_login'] == 'dhlybov' or st.session_state[
            'user_login'] == 'admin':
            with st.expander("🚛 Автодилеры: Chery", False):
                page.item("Maps Chery", Maps.main)
                page.item("Dashboard Chery", Dashboard.main)
                page.item("Reviews Chery", Reviews.main)
                page.item("Add Chery", Add.main)

            with st.expander("🚛 Автодилеры: Exeed", False):
                page.item("Maps Exeed", Maps.main)
                page.item("Dashboard Exeed", Dashboard.main)
                page.item("Reviews Exeed", Reviews.main)
                page.item("Add Exeed", Add.main)

            with st.expander("🚛 Автодилеры: FAW", False):
                page.item("Maps FAW", Maps.main)
                page.item("Dashboard FAW", Dashboard.main)
                page.item("Reviews FAW", Reviews.main)
                page.item("Add FAW", Add.main)

            with st.expander("🚛 Автодилеры: Gaz", False):
                page.item("Maps Gaz", Maps.main)
                page.item("Dashboard Gaz", Dashboard.main)
                page.item("Reviews Gaz", Reviews.main)
                page.item("Add Gaz", Add.main)

            with st.expander("🚛 Автодилеры: Uaz", False):
                page.item("Maps Uaz", Maps.main)
                page.item("Dashboard Uaz", Dashboard.main)
                page.item("Reviews Uaz", Reviews.main)
                page.item("Add Uaz", Add.main)

            with st.expander("🚛 Автодилеры: Geely", False):
                page.item("Maps Geely", Maps.main)
                page.item("Dashboard Geely", Dashboard.main)
                page.item("Reviews Geely", Reviews.main)
                page.item("Add Geely", Add.main)

            with st.expander("🚛 Автодилеры: Haval", False):
                page.item("Maps Haval", Maps.main)
                page.item("Dashboard Haval", Dashboard.main)
                page.item("Reviews Haval", Reviews.main)
                page.item("Add Haval", Add.main)

            with st.expander("🚛 Автодилеры: Hyundai", False):
                page.item("Maps Hyundai", Maps.main)
                page.item("Dashboard Hyundai", Dashboard.main)
                page.item("Reviews Hyundai", Reviews.main)
                page.item("Add Hyundai", Add.main)

            with st.expander("🚛 Автодилеры: JAC", False):
                page.item("Maps JAC", Maps.main)
                page.item("Dashboard JAC", Dashboard.main)
                page.item("Reviews JAC", Reviews.main)
                page.item("Add JAC", Add.main)

        if st.session_state['user_login'] == 'Farm' or st.session_state['user_login'] == 'dhlybov' or st.session_state[
            'user_login'] == 'admin':
            with st.expander("🌾 Сельхозтехника: Ростсельмаш", False):
                page.item("Maps RSM", Maps.main)
                page.item("Dashboard RSM", Dashboard.main)
                page.item("Reviews RSM", Reviews.main)
                page.item("Add RSM", Add.main)

    page.show()


if __name__ == "__main__":
    # Перед запуском main скрипта мы должны выполнить проверку пользователя по cookie. Если его нет в базе - пусть
    # регистрируется. Взято из https://github.com/GauriSP10/streamlit_login_auth_ui

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
        # Перед рендерингом страниц получаем имя пользователя и заносим его в кэш st.session_state['user_login']
        username = __login__obj.get_username()
        st.session_state['user_login'] = username
        main()
