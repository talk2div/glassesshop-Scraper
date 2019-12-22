# -*- coding: utf-8 -*-
import scrapy


class BestSellerSpider(scrapy.Spider):
    name = 'best_seller'
    allowed_domains = ['www.glassesshop.com']
    
    def start_requests(self):
        yield scrapy.Request(url='https://www.glassesshop.com/bestsellers',callback=self.parse,headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
        })

    def parse(self, response):
        row = response.xpath('//div[@class="prlist row"]/div[@class="col-sm-6 col-md-4 m-p-product"]')
        for eachGlass in row:
            product_url = eachGlass.xpath(".//div[1]/a/@href").get()
            product_image_link = eachGlass.xpath(".//div[1]/a/img/@src").getall()
            product_name = eachGlass.xpath('.//div[@class="row"]/p/a/text()').get() 
            product_price = eachGlass.xpath('.//div[@class="row"]/div/span/text()').get()
            yield {
                'product_url':product_url,
                'product_image_link':product_image_link, 
                'product_name':product_name,
                'product_price':product_price
            }

        next_page = response.xpath("//ul[@class='pagination']/li[position()=last()]/a[@rel='next']/@href").get()
        if next_page:
            yield scrapy.Request(url=next_page,callback=self.parse,headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
        })