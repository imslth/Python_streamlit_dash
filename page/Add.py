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
            if 'maps' in title and 'yandex' in title:
                Base().create_new_url(table=st.session_state.option, url=title)
                st.text('Ссылка добавлена в базу!')
            else:
                st.error('Это не ссылка на Яндекс.Карты', icon="🚨")



if __name__=='__main__':
    main()