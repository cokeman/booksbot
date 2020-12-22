# -*- coding: utf-8 -*-
import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["www.idealista.com"]
    start_urls = [
        'https://www.idealista.com/pro/century21-capital-las-palmas/',
    ]

    def parse(self, response):
        for book_url in response.css("article.item-multimedia-container > a.item-link ::attr(href)").extract():
            yield scrapy.Request(response.urljoin(book_url), callback=self.parse_book_page)
        next_page = response.css("li.next > a ::attr(href)").extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_book_page(self, response):
        item = {}
        product = response.css("div.detail-container")
        item["title"] = product.css("h1 ::text").extract_first()
        item['category'] = response.css('span.main-info__title-minor ::text').extract_first()
        item['description'] = response.xpath(
            "//div[@class='details-property_features'] > ul/following-sibling::li/text()"
        ).extract_first()
        item['price'] = response.css('span.info-data-price ::text').extract_first()
        yield item
