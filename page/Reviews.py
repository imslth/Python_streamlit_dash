import streamlit as st
from .backend import Session_state
from .backend.Graphs_Data import data_Wordcloud, data_Bert
from .backend.Load_Data import load_reviews_wordcloud, load_reviews
from .frontend import Wordcloud, Bert, Dostoevsky

# Отображение страницы с отзывами
def main():
    Session_state()

    st.subheader('Информация об отзывах на ресурсе')

    # Здесь логика работы selectbox такая же, как и на странице дашборда с одиночным select. Показывается проект и адрес
    project = list()
    for i in range(len(st.session_state.selectlist) - 1):
        # Мы в selectbox загружаем только те проекты, у которых есть отзывы. Но это не спасает т.к. чаще всего
        # сталкиваемся с ситуацией - по данным общей таблицы у проекта есть отзывы, но по факту они или не спарсились,
        # или что еще. В общем текстов в базе по ним нет.
        if int(st.session_state.count_text[i]) > 0:
            project.append(f'{st.session_state.selectlist[i]}, {st.session_state.selectaddress[i]}')

    col1, col2 = st.columns([1, 3])
    with col1:
        word_project = st.selectbox(
            'Выберете проект', project)
        st.markdown('')
        st.markdown(
            f'Справа отображено облако наиболее часто используемых слов, используемых в отзывах по проекту {word_project}')
    with col2:
        chooise_project = ''
        for i, item in enumerate(st.session_state.selectaddress):
            if item in word_project:
                chooise_project = word_project.replace(item, '')[:-2]
                chooise_coordinates = st.session_state.selectcoordinates[i]
                chooise_address = item
                st.session_state.number = 0

        content = data_Wordcloud(load_reviews_wordcloud(project=chooise_project, coordinates=chooise_coordinates))

        # Проверка - существуют ли отзывы в БД по проекту. Если да - грузим облако слов, если нет - заглушка.
        if content:
            Wordcloud(content, chooise_project)
        else:
            st.markdown(f'По проекту {chooise_project}, {chooise_address} отзывов не обнаружено')

    # Проверка - существуют ли отзывы в БД по проекту. Если да - грузим отзывы и ключи, если нет - заглушка.
    if content:
        st.markdown(
            f'Ниже отображен отзыв с выделением положительных и негативных слов, характеризующих текст. Фразы получены с помощью библиотеки обработки естественного языка Dostoevsky.')
        st.markdown(
            f'Также ниже отображены ключевые слова, описывающие выбранный отзыв. Фразы получены с помощью нейросети Bert.')

        content_Bert = load_reviews(table=f'{st.session_state.option}_reviews',
                                    project=chooise_project, coordinates=chooise_coordinates)
        text = list()

        for item in content_Bert:
            text.append(item[0])

        st.text('')

        # Здесь мы отображаем отзывы в зависимости от их номера в базе (каждый отзыв идет с аннотацией негатива и
        # позитива). Каждый новый отзыв отправляется в Bert для поиска ключевиков.
        col1, col2, col3 = st.columns([5, 1, 1])
        with col2:
            if st.button('Предыдущий'):
                if st.session_state.number == 0:
                    st.session_state.number = len(text) - 1
                else:
                    st.session_state.number -= 1
        with col3:
            if st.button('Следующий'):
                if st.session_state.number == len(text) - 1:
                    st.session_state.number = 0
                else:
                    st.session_state.number += 1

        with col1:
            Dostoevsky(text[st.session_state.number])

        st.text('')

        content = data_Bert(text[st.session_state.number])
        st.header("")
        Bert(content)
    else:
        pass


if __name__ == '__main__':
    main()
