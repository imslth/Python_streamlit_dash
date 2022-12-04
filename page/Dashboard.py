from streamlit_elements import elements, dashboard
from .backend import Session_state
from .frontend.Mui.Mui import Mui
from .backend.Load_Data import load_yandex_all, load_yandex_aspect, load_aspect_count, load_yandex_all_rating, \
    load_yandex_related_rating, load_yandex_count_votes_reviews, load_reviews
import streamlit as st
from .backend.Graphs_Data import data_Table, data_BarRating, data_BarReviews, data_RadianBar, data_LineReviews, \
    data_LineRating, data_Calendar, data_Reviews, data_Pie


def main():
    Session_state()

    with elements("dashboard"):
        layout = [
            dashboard.Item('slider', 0, 0, 3, 1),
            dashboard.Item('multiselect', 0, 1, 3, 1),
            dashboard.Item('table', 3, 0, 7, 2),
            dashboard.Item('bar_rating', 0, 2, 5, 3),
            dashboard.Item('bar_reviews', 5, 2, 5, 3),
            dashboard.Item('select', 0, 5, 4, 1),
            dashboard.Item('radian_reviews', 4, 5, 6, 3),
            dashboard.Item('line_reviews', 0, 6, 4, 2),

            dashboard.Item('line_rating', 0, 8, 4, 2),
            dashboard.Item('pie_related', 4, 8, 6, 2),


            dashboard.Item('reviews_calendar', 0, 11, 12, 2),
            dashboard.Item('votes_calendar', 0, 13, 12, 2),
            dashboard.Item('reviews_like', 0, 15, 5, 3),
            dashboard.Item('reviews_dislike', 5, 15, 5, 3),

            dashboard.Item('network', 0, 18, 6, 3),
        ]

        with dashboard.Grid(layout):
            dash = Mui()

            dash('slider', name='Выбор Даты')

            dash('multiselect', 'Выбор проектов')

            data_load_yandex_all = load_yandex_all(table=f'{st.session_state.option}_all',
                                                   date_present=st.session_state.date_present.strftime("%Y-%m-%d"),
                                                   date_past=st.session_state.date_past.strftime("%Y-%m-%d"),
                                                   project=st.session_state.multiselect)

            dash('table', 'Динамика изменения метрик', content=data_Table(data_load_yandex_all))

            dash('bar_rating', 'Распределение по рейтингу', content=data_BarRating(data_load_yandex_all))

            dash('bar_reviews', 'Распределение по кол-ву отзывов', content=data_BarReviews(data_load_yandex_all))

            dash('select', 'Выбор проекта')

            data_load_yandex_aspect = load_yandex_aspect(table=f'{st.session_state.option}_aspect',
                                                         date_present=st.session_state.date_present.strftime(
                                                             "%Y-%m-%d"),
                                                         date_past=st.session_state.date_past.strftime("%Y-%m-%d"),
                                                         project=[st.session_state.select],
                                                         coordinates=st.session_state.select_coordinates)

            dash('radian_reviews', 'Группировка отзывов по тематикам', content=data_RadianBar(data_load_yandex_aspect))

            data_load_aspect_count = load_aspect_count(table=f'{st.session_state.option}_aspect',
                                                       project=st.session_state.select,
                                                       coordinates=st.session_state.select_coordinates)

            dash('line_reviews', 'Динамика изменения тональности отзывов',
                 content=data_LineReviews(data=data_load_aspect_count))

            data_load_yandex_all_rating = load_yandex_all_rating(table=f'{st.session_state.option}_all',
                                                                 project=st.session_state.select,
                                                                 coordinates=st.session_state.select_coordinates)
            data_load_yandex_related_rating = load_yandex_related_rating(table=f'{st.session_state.option}_related',
                                                                         project=st.session_state.select,
                                                                         coordinates=st.session_state.select_coordinates,
                                                                         date_present=st.session_state.max_time)

            data = {'project': data_load_yandex_all_rating, 'related': data_load_yandex_related_rating}

            dash('line_rating', 'Динамика изменения рейтинга', content=data_LineRating(data))

            dash('pie_related', 'Рейтинг конкурентов', content=data_Pie(data))

            data_load_yandex_count_votes_reviews = load_yandex_count_votes_reviews(
                table=f'{st.session_state.option}_all',
                project=st.session_state.select,
                coordinates=st.session_state.select_coordinates)

            content_calendar = data_Calendar(data_load_yandex_count_votes_reviews)

            dash('reviews_calendar', 'Динамика публикации отзывов',
                 content=content_calendar['reviews'])

            dash('votes_calendar', 'Динамика публикации оценок',
                 content=content_calendar['votes'])

            data_load_reviews = load_reviews(table=f'{st.session_state.option}_reviews',
                                             project=st.session_state.select, coordinates=st.session_state.select_coordinates)

            content_reviews = data_Reviews(data_load_reviews)

            dash('reviews_like', 'Самый популярный отзыв', content=content_reviews['like'])

            dash('reviews_dislike', 'Самый непопулярный отзыв', content=content_reviews['dislike'])



if __name__ == '__main__':
    main()
