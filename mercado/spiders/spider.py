import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from mercado.items import MercadoItem
from scrapy.exceptions import CloseSpider

class MercadoSpider(CrawlSpider):
    name ='mercado' #aprenderlo para iniciarlo para la ejecucion en cmd
    item_count = 0

    #Dominio que deben de tener todas las paginas
    allowed_domain = ['www.mercadolibre.com.pe']
    
    #De donde se empezara la busqueda
    #Si se desea tomar la busqueda pero de celulares se toma el siguiente:
    start_urls =['https://listado.mercadolibre.com.pe/celulares#D[A:celulares]'] #que tambien fue probada y funciona
        #start_urls =['https://listado.mercadolibre.com.pe/impresiones#D[A:impresiones]']

    rules = {
        #Dos Reglas importantes, la primera se encargara de "presionar" el boton de siguiente que se encuentra en el listado de los productos
        #Mientras que la segunda se encargara de entrar a cada producto
        Rule(LinkExtractor(allow =(), restrict_xpaths = ('//li[@class="andes-pagination__button andes-pagination__button--next shops__pagination-button"]/a'))),
        Rule(LinkExtractor(allow =(), restrict_xpaths = ('//a[@class="ui-search-item__group__element shops__items-group-details ui-search-link"]')),
                            callback='parse_item', follow=False)
    }
    def parse_item(self, response):
        ml_item = MercadoItem()

        #info de producto
        ml_item['titulo'] = response.xpath('normalize-space(//h1[@class="ui-pdp-title"]/text())').extract()
        ml_item['folio'] = response.xpath('normalize-space(//span[@class="ui-pdp-color--BLACK ui-pdp-family--SEMIBOLD"]/text())').extract()
        ml_item['precio'] = response.xpath('normalize-space(//*[@id="ui-pdp-main-container"]/div[1]/div/div[1]/div[2]/div[2]/div[1]/div[1]/span[1]/span[3]/text())').extract()
        ml_item['condicion'] = response.xpath('normalize-space(//*[@id="ui-pdp-main-container"]/div[1]/div/div[1]/div[2]/div[1]/div/div[1]/span/text())').extract()
        ml_item['envio'] = response.xpath('normalize-space(//p [@class="ui-pdp-color--BLACK ui-pdp-family--REGULAR ui-pdp-media__title"]/text())').extract()
        ml_item['opiniones'] = response.xpath('normalize-space(//span[@class="ui-pdp-review__rating"]/text())').extract()

        #infor de vendedor
        ml_item['vendedor_url'] = response.xpath('normalize-space(//*[starts-with(@class, "ui-pdp-media__action ui-box-component__action")]/@href/text())').extract()
        ml_item['tipo_vendedor'] = response.xpath('normalize-space(//p[@class="ui-seller-info__status-info__title ui-pdp-seller__status-title"]/text())').extract()
        ml_item['ventas_vendedor'] = response.xpath('normalize-space(//strong[@class ="ui-pdp-seller__sales-description"]/text())').extract()
        self.item_count += 1
        if self.item_count > 200: #establecemos el limite que habrá de items
            raise CloseSpider('item_exceeded')
        yield ml_item