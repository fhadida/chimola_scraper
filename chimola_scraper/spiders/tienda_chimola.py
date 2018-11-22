# -*- coding: utf-8 -*-
import scrapy
from chimola_scraper.items import ChimolaScraperItemLoader, ChimolaScraperItem


class TiendaChimolaSpider(scrapy.spiders.SitemapSpider):
    name = 'tienda_chimola'
    allowed_domains = ['chimola.com.ar', 'cloudfront.net']
    sitemap_urls = ['https://www.tienda.chimola.com.ar/sitemap.xml']
    sitemap_rules = [(
            r'https://www\.tienda\.chimola\.com\.ar/productos/.+/',
            'parse_product'
    )]

    def parse_product(self, response):
        loader = ChimolaScraperItemLoader(
            item=ChimolaScraperItem(), response=response)
        product_loader = loader.nested_css('#prod-page')
        product_form_loader = product_loader.nested_css(
            '#single-product #product_form')
        product_form_loader.add_css(
            'id', 'input[name=add_to_cart]::attr(value)')
        product_loader.add_css('title', 'h1.product_name::text')
        product_form_loader.add_css('price', '#price_display::attr(content)')
        product_form_loader.add_css(
            'availability', 'meta[itemprop=availability]::attr(content)')
        product_loader.add_css(
            'description', 'div.user-content > p:first-of-type::text')
        loader.add_value('url', response.url)
        product_loader.add_css(
            'image_urls',
            'div.product-thumbs img.product-thumbs-img::attr(src)'
        )
        loader.add_css('category_path', 'div.breadcrumbs a::text')
        return loader.load_item()
