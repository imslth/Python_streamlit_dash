import pandas
import streamlit as st
import re
from .Stopwords import stopwords
from .Load_Data import load_model
from rutermextract import TermExtractor


def data_foliumMap(data):
    content_all = pandas.DataFrame(data['all'], columns=['project', 'coordinates', 'address', 'rating'])
    content_related = pandas.DataFrame(data['related'],
                                       columns=['project', 'related_project', 'related_coordinates', 'related_rating'])

    for i in range(len(content_all)):
        temp_df = content_all['coordinates'][i][1:-1].replace(' ', '').split(',')
        content_all['coordinates'][i] = list(temp_df)
        content_all['coordinates'][i].reverse()

    for i in range(len(content_related)):
        temp_df = content_related['related_coordinates'][i][1:-1].replace(' ', '').split(',')
        content_related['related_coordinates'][i] = list(temp_df)
        content_related['related_coordinates'][i].reverse()

    content = {'all': content_all, 'related': content_related}

    return content


def data_Table(data):
    data_present = data['present']
    data_past = data['past']
    rows = list()
    col = [
        {"field": 'id', "headerName": 'ID', "width": 50},
        {"field": 'Проект', "headerName": 'Проект', "width": 120, "editable": True, },
        {"field": 'Адрес', "headerName": 'Адрес', "width": 250, "editable": True, },
        {"field": 'Изменение рейтинга', "headerName": 'Рейтинг', "width": 70, "editable": True, },
        {"field": 'Изменение кол-ва оценок', "headerName": 'Оценки', "type": 'number', "width": 70,
         "editable": True},
        {"field": 'Изменение кол-ва отзывов', "headerName": 'Отзывы', "type": 'number', "width": 70,
         "editable": True},
    ]

    for i, item in enumerate(data_present):
        rows.append({'id': i, 'Проект': item[0], 'Адрес': item[2],
                     f'Рейтинг на {st.session_state.date_present.strftime("%Y-%m-%d")}': item[5],
                     f'Оценок на {st.session_state.date_present.strftime("%Y-%m-%d")}': item[4],
                     f'Отзывов на {st.session_state.date_present.strftime("%Y-%m-%d")}': item[3]})

    for i, item in enumerate(data_past):
        for items in rows:
            if item[0] in items.values():
                items[f'Рейтинг на {st.session_state.date_past.strftime("%Y-%m-%d")}'] = item[5]
                items[f'Оценок на {st.session_state.date_past.strftime("%Y-%m-%d")}'] = item[4]
                items[f'Отзывов на {st.session_state.date_past.strftime("%Y-%m-%d")}'] = item[3]

    for item in rows:
        if f'Рейтинг на {st.session_state.date_past.strftime("%Y-%m-%d")}' in item.keys():
            pass
        else:
            item[f'Рейтинг на {st.session_state.date_past.strftime("%Y-%m-%d")}'] = 0
            item[f'Оценок на {st.session_state.date_past.strftime("%Y-%m-%d")}'] = 0
            item[f'Отзывов на {st.session_state.date_past.strftime("%Y-%m-%d")}'] = 0

    for item in rows:
        item['Изменение рейтинга'] = round(
            item[f'Рейтинг на {st.session_state.date_present.strftime("%Y-%m-%d")}'] - item[
                f'Рейтинг на {st.session_state.date_past.strftime("%Y-%m-%d")}'], 1)
        item['Изменение кол-ва оценок'] = item[f'Оценок на {st.session_state.date_present.strftime("%Y-%m-%d")}'] - \
                                          item[f'Оценок на {st.session_state.date_past.strftime("%Y-%m-%d")}']
        item['Изменение кол-ва отзывов'] = item[f'Отзывов на {st.session_state.date_present.strftime("%Y-%m-%d")}'] - \
                                           item[f'Отзывов на {st.session_state.date_past.strftime("%Y-%m-%d")}']
        item.pop(f'Рейтинг на {st.session_state.date_present.strftime("%Y-%m-%d")}')
        item.pop(f'Оценок на {st.session_state.date_present.strftime("%Y-%m-%d")}')
        item.pop(f'Отзывов на {st.session_state.date_present.strftime("%Y-%m-%d")}')
        item.pop(f'Рейтинг на {st.session_state.date_past.strftime("%Y-%m-%d")}')
        item.pop(f'Оценок на {st.session_state.date_past.strftime("%Y-%m-%d")}')
        item.pop(f'Отзывов на {st.session_state.date_past.strftime("%Y-%m-%d")}')

    content = {'col': col, 'rows': rows}

    return content


def data_BarRating(data):
    data = data['present']
    rat45 = dict()
    rat4 = dict()
    rat3 = dict()
    rat2 = dict()
    rat0 = dict()

    y = list()
    for item in data:
        project = f'{item[0]}, {item[2]}'
        y.append(project)
        if item[5] >= 4.5:
            rat45[project] = item[5]
        if 4.5 > item[5] >= 4:
            rat4[project] = item[5]
        if 4 > item[5] >= 3:
            rat3[project] = item[5]
        if 3 > item[5] >= 2:
            rat2[project] = item[5]
        if 2 > item[5] >= 0:
            rat0[project] = item[5]

    x = list()
    if rat45:
        rat45['country'] = 'Больше 4.5'
        x.append(rat45)
    if rat4:
        rat4['country'] = 'От 4 до 4.5'
        x.append(rat4)
    if rat3:
        rat3['country'] = 'От 3 до 4'
        x.append(rat3)
    if rat2:
        rat2['country'] = 'От 2 до 3'
        x.append(rat2)
    if rat0:
        rat0['country'] = 'От 0 до 2'
        x.append(rat0)

    content = {'x': x, 'y': y}

    return content


def data_BarReviews(data):
    data = data['present']
    rev100 = dict()
    rev300 = dict()
    rev600 = dict()
    rev = dict()
    y = list()
    for item in data:
        project = f'{item[0]}, {item[2]}'
        y.append(project)
        if item[3] >= 600:
            rev[project] = item[3]
        if 600 > item[3] >= 300:
            rev600[project] = item[3]
        if 300 > item[3] >= 100:
            rev300[project] = item[3]
        if 100 > item[3] >= 0:
            rev100[project] = item[3]

    x = list()
    if rev100:
        rev100['country'] = 'От 0 до 100'
        x.append(rev100)
    if rev300:
        rev300['country'] = 'От 100 до 300'
        x.append(rev300)
    if rev600:
        rev600['country'] = 'От 300 до 600'
        x.append(rev600)
    if rev:
        rev['country'] = 'Больше 600'
        x.append(rev)

    content = {'x': x, 'y': y}

    return content


def data_RadianBar(data):
    data = data['present']

    positive = list()
    neutral = list()
    negative = list()

    for item in data:
        positive.append({'x': item[0], 'y': item[2]})
        neutral.append({'x': item[0], 'y': item[3]})
        negative.append({'x': item[0], 'y': item[4]})

    content = [{'id': 'Позитив', 'data': positive}, {'id': 'Нейтрал', 'data': neutral},
               {'id': 'Негатив', 'data': negative}]

    return content


def data_LineReviews(data):
    data = data
    pos = list()
    neu = list()
    neg = list()
    df = pandas.DataFrame(data, columns=['positive', 'neutral', 'negative', 'now'])
    df_new = df.set_index('now', drop=False)
    for item in df_new['now'].unique():
        df_temp = df_new.loc[item]
        pos.append({
            "x": df_temp['now'][0],
            "y": int(df_temp['positive'].sum())
        })
        neu.append({
            "x": df_temp['now'][0],
            "y": int(df_temp['neutral'].sum())
        })
        neg.append({
            "x": df_temp['now'][0],
            "y": int(df_temp['negative'].sum())
        })

    content = [
        {
            "id": "Позитив",
            "color": "hsl(26, 70%, 50%)",
            "data": pos
        },
        {
            "id": "Нейтрал",
            "color": "hsl(81, 70%, 50%)",
            "data": neu
        },
        {
            "id": "Негатив",
            "color": "hsl(180, 70%, 50%)",
            "data": neg
        },
    ]

    return content


def data_LineRating(data):
    data_all = data['project']
    temp_all = list()
    for item in data_all:
        temp_all.append({'x': item[1], 'y': round(item[0], 1)})

    content = [{'id': st.session_state.select, 'data': temp_all}]

    return content


def data_Calendar(data):
    data = data
    content_votes = list()
    content_reviews = list()
    for i in range(1, len(data)):
        temp = data[i][0] - data[i - 1][0]
        if temp == 0:
            pass
        else:
            content_reviews.append({'value': temp, 'day': data[i][2]})

        temp = data[i][1] - data[i - 1][1]
        if temp == 0:
            pass
        else:
            content_votes.append({'value': temp, 'day': data[i][2]})

    content = {'reviews': content_reviews, 'votes': content_votes}

    return content


def data_Reviews(data):
    if data:
        item_like = list()
        item_dislike = list()
        max_like = 0
        max_dislike = 0

        for item in data:
            if item[3] > max_like:
                item_like = item
                max_like = item[3]
            if item[4] > max_dislike:
                item_dislike = item
                max_dislike = item[4]
        if item_like:
            pass
        else:
            item_like = data[0]

        if item_dislike:
            pass
        else:
            item_dislike = data[0]

        content_like = {'Reviews': item_like[0].replace('\n', ''), 'Rating': item_like[1],
                        'Date': item_like[2],
                        'Like': item_like[3], 'Dislike': item_like[4], 'OrgText': item_like[5]}
        content_dislike = {'Reviews': item_dislike[0].replace('\n', ''), 'Rating': item_dislike[1],
                           'Date': item_dislike[2], 'Like': item_dislike[3],
                           'Dislike': item_dislike[4], 'OrgText': item_dislike[5]}
    else:
        content_like = {'Reviews': 'Отзывы отсутствуют', 'Rating': '', 'Date': '',
                        'Like': '', 'Dislike': '', 'OrgText': ''}
        content_dislike = {'Reviews': 'Отзывы отсутствуют', 'Rating': '', 'Date': '',
                           'Like': '', 'Dislike': '', 'OrgText': ''}

    content = {'like': content_like, 'dislike': content_dislike}

    return content


def data_Wordcloud(data):
    data = data
    temp = list()
    for item in data:
        temp.append(item[0])
    words_first = ' '.join(temp)
    words_lower = words_first.lower()
    words_all = re.sub(r'[^\w\s]|[0-9]', '', words_lower)
    words = words_all.split(' ')

    words_list = list()
    temp = list()

    for item in words:
        if item in temp:
            pass
        else:
            words_list.append({"name": item, "weight": words.count(item)})
            temp.append(item)

    content = list()

    for item in words_list:
        if item['weight'] > 2 and item['name'] != '' and item['name'] not in stopwords: content.append(item)
    return content


def data_Bert(content):
    kw_model = load_model()
    keywords = kw_model.extract_keywords(
        content,
        keyphrase_ngram_range=(1, 1),
        use_mmr=True,
        stop_words=stopwords,
        top_n=5,
        diversity=0.5,
    )
    return keywords


def data_Pie(data):
    data_all = data['project']
    data_related = data['related']
    content = list()
    for item in data_related:
        content.append({'id': item[0], 'label': item[0], 'value': item[1]})
    content.append({'id': st.session_state.select, 'label': st.session_state.select, 'value': data_all[-1][0]})
    return content



