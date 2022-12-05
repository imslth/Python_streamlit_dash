import scrapy
from page.backend.Databased import Base
from page.backend.Parsing_edit import EditParse
import json
from page.backend.Parsing_custom_setting import SETTING

# Паук scrapy для парсинга объектов недвижимости
class QuotesSpider(scrapy.Spider):
    name = "developer"
    func = Base()
    start_urls = func.read_url(table='yandex')
    custom_settings = SETTING

    def parse(self, response):
        all_data = response.css("script.state-view::text").getall()

        for data in all_data:
            data = json.loads(data)

        EditParse().Edit(content=data, project='yandex')

