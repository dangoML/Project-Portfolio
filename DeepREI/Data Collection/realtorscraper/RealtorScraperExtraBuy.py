import scrapy
import csv
from scrapy import signals
from datetime import date
from scrapy import Spider
from scrapy.crawler import CrawlerProcess

User_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
FileName=str(date.today())
filee = open(FileName+'.csv','w',newline='',encoding='utf-8-sig')
csvw = csv.writer(filee)
csvw.writerow(['','PropertyUrl','sq ft','sqft lot','acres lot','FoodFactor'])

class FileSpider(scrapy.Spider):
    name = 'Main'
    allowed_domains = ['www.realtor.com']

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {'scrapy_crawlera.CrawleraMiddleware': 610},
        'CRAWLERA_ENABLED': True,
        'CRAWLERA_APIKEY': 'cbff43406ca546f89ffa0d195e5c19ab', }
       
            
    
    def start_requests(self):
        with open('Urls.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                Url=row["propertyurl"]
                num=row['']
                yield scrapy.Request(url=Url,callback=self.parse,headers={"User-Agent":User_agent},meta={"Num":num},dont_filter=False)
                

    def parse(self, response):
        Number=response.request.meta['Num']
        SQFT=response.xpath("//li[@data-label='property-meta-sqft']/span/text()").get()
        if SQFT is None:
            SQFT=response.xpath("//li[@data-testid='property-meta-sqft']/span/text()").get()

        SqftLot=response.xpath("//li[@data-label='property-meta-lotsize']/span/following-sibling::text()[contains(.,'sqft lot')]/parent::node()/span/text()").get()
        if SqftLot is None:
            SqftLot=response.xpath("//li[@data-testid='property-meta-lot-size']/span/following-sibling::text()[contains(.,'sqft lot')]/parent::node()/span/text()").get()

        ACRESLOT=response.xpath('//li[@data-label="property-meta-lotsize"]/span/following-sibling::text()[contains(.,"acres")]/parent::node()/span/text()').get()
        if ACRESLOT is None:
            ACRESLOT=response.xpath('//li[@data-testid="property-meta-lot-size"]/span/following-sibling::text()[contains(.,"acres")]/parent::node()/span/text()').get()
        
        try:
            FoodFactor=str(response.xpath("//span[@class='ldp-flood-score']/b/text()").get())+str(response.xpath("//span[@class='ldp-flood-score']/b/following-sibling::text()").get())
            if 'None' in FoodFactor: FoodFactor=''
        except:pass

        csvw.writerow([Number,response.url,SQFT,SqftLot,ACRESLOT,"  "+FoodFactor])

        yield{
            '':Number,
            'PropertyUrl':response.url,
            'sq ft':SQFT,
            'sqft lot':SqftLot,
            'acres lot':ACRESLOT,
            "FoodFactor":FoodFactor}
   
        
process = CrawlerProcess()
process.crawl(FileSpider) 
process.start()

# sqft = pd.read_csv('sqft.csv')
# sqft['sqft lot'] = sqft['sqft lot'].fillna(sqft['acres lot']*43560)
# sqft['sqft lot'] = [round(float(x.replace(',','')),2) if isinstance(x, str) else round(x,2) for x in sqft['sqft lot']]
# sqft['sq ft'] = [round(float(x.replace(',','')),2) if isinstance(x, str) else round(x,2) for x in sqft['sq ft']]
# sqft = sqft.drop('acres lot',axis=1)
# sqft = sqft.drop('Unnamed: 0',axis=1)
# sqft.columns = ['propertyurl', 'sqft Inside', 'sqft Outside', 'floodfactor']
# sqft = sqft.dropna()

# south_florida = pd.merge(sqft,south_florida,
#                         on='propertyurl',
#                         how='inner')
# south_florida = south_florida.drop('index',axis=1)

# south_florida.to_sql('south_florida_data3',engine)