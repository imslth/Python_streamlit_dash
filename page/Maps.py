import streamlit as st
from .frontend import Map
from .backend import Session_state
from .backend.Graphs_Data import data_foliumMap
from .backend.Load_Data import load_maps


# Отображение страницы с картой
def main():
    Session_state()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Кол-во проектов в мониторинге", st.session_state.count_obj)
    col2.metric("Кол-во конкурентных проектов", st.session_state.count_related_obj)
    col3.metric("Дата первого мониторинга", st.session_state.date_past.strftime("%Y-%m-%d"))
    col4.metric("Дата последнего мониторинга", st.session_state.date_present.strftime("%Y-%m-%d"))

    st.subheader('Карта расположения объектов')
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown('''
        На карте справа отображены проекты, которые находятся в ежедневном мониторинге. <p> Проекты 
        отличаются цветом отображения маркеров. Цвет маркера подобран в зависимости от рейтинга проекта:
        <html>
        <head>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.2/font/bootstrap-icons.css">
        </head>
        <body>
        </body>
        </html>
        <p>
        <i class="bi bi-house-door-fill" style="font-size: 1rem; color: green;"></i> - рейтинг выше 4.5 ед.
        <p>
        <i class="bi bi-house-door-fill" style="font-size: 1rem; color: lightblue;"></i> - рейтинг от 3 до 4.5 ед.
        <p>
        <i class="bi bi-house-door-fill" style="font-size: 1rem; color: red;"></i> - рейтинг ниже 3 ед.
        <p>
        <i class="bi bi-house-door-fill" style="font-size: 1rem; color: gray;"></i> - конкурент.
        ''', unsafe_allow_html=True)

        # Выбор отображения конкурентов на карте. Изначально выключен т.к. очень грузит сайт
        related_place = st.checkbox('Включить отображение конкурентов')

        if related_place:
            st.session_state.related = True

    with col2:
        data = load_maps(date_present=st.session_state.date_present.strftime("%Y-%m-%d"))
        Map(data_foliumMap(data=data))


if __name__ == '__main__':
    main()
