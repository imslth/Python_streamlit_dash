from .Highcharts import custom_grid


def main(content, project):
    Wordcloud = {
        'accessibility': {
            'screenReaderSection': {
                'beforeChartFormat': '<h5>{chartTitle}</h5>' +
                                     '<div>{chartSubtitle}</div>' +
                                     '<div>{chartLongdesc}</div>' +
                                     '<div>{viewTableButton}</div>'
            }
        },
        'series': [{
            'type': 'wordcloud',
            'data': content,
            'name': 'Кол-во упоминаний',
            'minFontSize': 8,
            'maxFontSize': 25,
            'placementStrategy': 'random',
            'spiral': 'archimedean'
        }],
        'title': {
            'text': f'Облако слов отзывов по проекту <b>{project}</b>'
        },
        'tooltip': {
            'headerFormat': '<span style="font-size: 16px"><b>{point.key}</b></span><br>'
        }
    }

    custom_grid(Wordcloud, 500)


if __name__ == '__main__':
    main()
