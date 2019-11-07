import scrapy
from crawlproduct_archiproducts.items import CrawlproductArchiproductsItem
import pymysql.cursors

class archispider(scrapy.Spider):
    name = "apforproduct"
    allowed_domains = ["archiproducts.com"]

    #global start_urls
    #start_urls=["https://www.archiproducts.com/en/3d-surface/products","https://www.archiproducts.com/en/3m-italia/products"]
    """
    def __init__(self):
        try:
            self.conn = pymysql.connect(host='localhost', user='root', password='1q2w3e4r', db='scrapy_db', charset='utf8mb4')
            self.cursor = self.conn.cursor()
        except pymysql.Error as e:
            print("Error %d: %s"%(e.args[0], e.args[1]))

    def start_requests(self):
        try:
            with self.conn.cursor() as cursor:
                sql = "select replace(link_url,'https://www.archiproducts.com/en/','') as link_url from archiproducts_brand where brand_id between 1 and 10 order by brand_id"
                cursor.execute(sql)
                result = cursor.fetchall()
        except pymysql.Error as e:
            print("Error %d: %s" % (e.args[0], e.args[1]))
        finally:
            self.conn.close()

        for k in result:
            for i in range(1, 6, 1):
                yield scrapy.Request('https://www.archiproducts.com/en/%s/products/%d' % (k[0],i), meta={'link_url':k[0]},
                                     callback=self.parse_brand)
    """

    global itype1
    global itype2
    itype1 = "furniture"
    itype2 = "sofas"

    def start_requests(self):
        for i in range(1, 103, 1):
            yield scrapy.Request('https://www.archiproducts.com/en/products/%s/%d'%(itype2, i),callback=self.parse_brand)

    def parse_brand(self, response):
        urls = response.xpath('//*[contains(@class,"_search-item-anchor")]/@href').extract()
        #urls=["/en/products/miniforms/upholstered-fabric-armchair-botera_409098"]

        for i in range(0, len(urls), 1):
            url = 'https://www.archiproducts.com%s' % urls[i]
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):

        item = CrawlproductArchiproductsItem()

        title = response.xpath('//*[contains(@class,"title-product-page")]/text()')[0].extract()
        description = response.xpath('//*[contains(@itemprop,"description")]')[0].extract().replace('<p itemprop="description">', "").replace('</p>',"")
        vendor = response.xpath('//*[contains(@itemprop,"manufacturer")]/a/text()')[0].extract()
        type1 = itype1
        type2 = itype2
        type3 = response.xpath('//*[contains(@class,"cell small-12 medium-9")]/h2/text()')[1].extract()
        #tags = response.xpath('//*[contains(@class,"cell small-12 medium-9")]/h2/a/text()').extract()
        #handle = vendor.replace(" ", "").replace("&","e") + "-" + type3.replace(" ", "-") + "-" + title.replace(" ", "").replace("|", "-")
        title = title.split("|")[0]
        published = "TRUE"
        producturl = response.xpath('//link[@hreflang and contains(@href, "en")]/@href')[0].extract()
        dimension=""
        if len(response.xpath('//*[@class="accordion-content"]/text()[preceding-sibling::br or following-sibling::br]').extract())>0:
            for i in range(0,len(response.xpath('//*[@class="accordion-content"]/text()[preceding-sibling::br or following-sibling::br]').extract()),1):
                #print(response.xpath('//*[@class="accordion-content"]/text()[preceding-sibling::br or following-sibling::br]')[i].extract().replace("\r\n",""))
                if response.xpath('//*[@class="accordion-content"]/text()[preceding-sibling::br or following-sibling::br]')[i].extract().replace("\r\n","").isspace()==False:
                    if i==0:
                        dimension = response.xpath('//*[@class="accordion-content"]/text()[preceding-sibling::br or following-sibling::br]')[i].extract().replace("\r\n","")
                    else:
                        dimension = dimension + "<br>" + response.xpath('//*[@class="accordion-content"]/text()[preceding-sibling::br or following-sibling::br]')[i].extract().replace("\r\n","")
        #print(dimension)
        item['title'] = title.strip()
        item['description'] = description.strip()
        item['vendor'] = vendor.strip()
        item['type1'] = type1
        item['type2'] = type2
        item['type3'] = type3
        item['published'] = published.strip()
        item['url'] = producturl
        item['dimension']=dimension

        yield item