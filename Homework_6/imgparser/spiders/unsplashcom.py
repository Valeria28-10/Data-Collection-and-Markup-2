import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from imgparser.items import ImgparserItem


class UnsplashcomSpider(scrapy.Spider):

    name = "unsplashcom"
    allowed_domains = ["unsplash.com"]
    start_urls = ["https://unsplash.com"]

    def parse(self, response:HtmlResponse):
        # Загружаем ссылки на категорию изображений
        categories = response.xpath("(//ul)[last()]//a[not(text()='Unsplash+') and not(text()='Editorial')]/@href")

        for category in categories:
            # Посылаем запросы на страницу категории
            yield response.follow(url=category, callback=self.img_parse)

    def img_parse(self, response:HtmlResponse):
        # Вычисляем обЩее количество картинок в категории
        list_url = response.xpath("//img[@data-test]")
        for item in list_url:
            # Создаем элемент loader
            loader = ItemLoader(item=ImgparserItem(), response=response)
            # Записываем в loader имя категории
            loader.add_xpath('category', '//h1/text()')
            # Записываем в переменные название и ссылку на картинку
            url = item.xpath('./@src').get()
            name = item.xpath('./@alt').get()
            # Записываем в loader ссылку на картинку и название
            loader.add_value('url', url)
            loader.add_value('name', name)
            # Посылаем loader в Pipeline
            yield loader.load_item()

