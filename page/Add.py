import streamlit as st
from .backend import Session_state
from .backend.Databased import Base


def main():
    Session_state()

    st.markdown('Ниже вы можете добавить свой проект в мониторинг в виде ссылки на Яндекс.Карты')
    with st.form("my_form"):
        title = st.text_input('Вставьте ссылку')
        submitted = st.form_submit_button("Отправить")
        if submitted:
            count = 0
            if 'maps' in title and 'yandex' in title:
                ll = title.split('ll=')[1].split('%2C')[0]
                tt = title.split('ll=')[1].split('%2C')[1].split('&')[0]
                for item in st.session_state.list:
                    if ll in item and tt in item:
                        count = 1
                        break
                if count == 1:
                    st.error('Этот проект уже есть в базе', icon="🚨")
                else:
                    Base().create_new_url(table=st.session_state.option, url=title)
                    st.text('Ссылка добавлена в базу!')
            else:
                st.error('Это не ссылка на Яндекс.Карты', icon="🚨")


if __name__ == '__main__':
    main()
