import streamlit as st
from .frontend import Map
from .backend import Session_state
from .backend.Graphs_Data import data_foliumMap
from .backend.Load_Data import load_maps


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
        st.markdown('На карте справа отображены проекты, которые находятся в ежедневном мониторинге.')
        st.markdown('')
        st.markdown(
            'Проекты отличаются цветом отображения маркеров. Цвет маркера подобран в зависимости от рейтинга проекта')

    with col2:
        data = load_maps(date_present=st.session_state.date_present.strftime("%Y-%m-%d"))
        Map(data_foliumMap(data=data))


if __name__ == '__main__':
    main()
