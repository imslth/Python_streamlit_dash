import folium
import streamlit as st
from streamlit_folium import st_folium

# Функция отображения карты. Взято с https://github.com/randyzwitch/streamlit-folium
def main(content):

    # Для ЖК центральная точка - Москва
    if st.session_state.option == 'yandex':
        location = [55.76, 37.803]
        zoom = 10
    # Для дилеров нам надо показать всю Россию
    if st.session_state.option == 'dilers_yandex':
        location = [55.7522, 45.6156]
        zoom = 4

    m = folium.Map(location=location, zoom_start=zoom)
    # В этом цикле мы добавляем только наши проекты. Они имеют 3 цвета в зависимости от рейтинга.
    for i, row in content['all'].iterrows():
        html = f'''
                            <p>Проект: <b>{row["project"]}</b><p/>
                            <p>Адрес: <b>{row["address"]}</b><p/>
                            <p>Рейтинг: <b>{round(row["rating"], 1)}</b><p/>
                            '''
        if float(row['rating']) > 4.5:
            icon_color = 'green'
        elif float(row['rating']) < 3:
            icon_color = 'red'
        else:
            icon_color = 'blue'
        toolpit = folium.Tooltip(text=html)
        folium.Marker(location=row['coordinates'], tooltip=toolpit, c=row['project'],
                      icon=folium.Icon(color=icon_color, icon='home')).add_to(m)
    # В этом цикле мы добавляем на карту конкурентов. Они имеют один цвет всегда.
    for i, row in content['related'].iterrows():
        if row["related_project"] in content['all']['project']:
            pass
        else:
            html = f'''
                            <p>Проект: <b>{row["related_project"]}</b><p/>
                            <p>Рейтинг: <b>{round(row["related_rating"], 1)}</b><p/>
                            <p>Конкурент для: <b>{row['project']}</b><p/>
                            '''
            icon_color = 'cadetblue'
            toolpit = folium.Tooltip(text=html)
            folium.Marker(location=row['related_coordinates'], tooltip=toolpit, c=row['related_project'],
                          icon=folium.Icon(color=icon_color, icon='home')).add_to(m)
    # returned_objects говорит, что карта не должна обновляться при любых действиях с картой
    output = st_folium(
        m, width=700, height=600, returned_objects=["last_object_clicked"]
    )


if __name__ == '__main__':
    main()