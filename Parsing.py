import scrapy
from page.backend.Databased import Base
from page.backend.Parsing_edit import EditParse
import json
from page.backend.Parsing_custom_setting import SETTING
from page.backend.Types_parsing import types_auto
import pandas as pd


url_lst = list()
index_lst = list()

# Сначала получаем список тех объектов, которые необходимо просмотреть. В цикле собираем ссылки всех объектов в базе,
# во второй список сохраняем название этих элементов. Т.е. url_lst[0]=http:/.... , index_lst[0]='yandex'
for item in types_auto:
    func = Base()
    url = func.read_url(table=item)
    index = [item] * len(url)
    url_lst.extend(url)
    index_lst.extend(index)

# В фрейме объединяем два списка
df = pd.DataFrame(url_lst, columns=['url'])
df.insert(1, 'item', index_lst)


# Паук scrapy для парсинга
class QuotesSpider(scrapy.Spider):
    name = "parsing"
    # Устанавливаем наши кастомные настройки
    custom_settings = SETTING
    # Стартовые ссылки это наши все ссылки из базы по всем таблицам
    start_urls = df['url'].tolist()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, kwargs)
        self.df_filter = None
        self.all_data = None
        self.data = None
        self.item = None

    def parse(self, response):
        self.all_data = response.css("script.state-view::text").getall()

        for self.data in self.all_data:
            self.data = json.loads(self.data)

        # Тут мы узнаем из нашего фрейма какому объекту соответствует ссылка
        self.df_filter = df.loc[(df['url'] == response.url)]

        self.item = self.df_filter['item'].values[0]

        EditParse().Edit(content=self.data, project=self.item)

















