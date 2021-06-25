# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
# ##  Google Colab ##
# # Requirements
# !pip install psycopg2
# !pip install scrapy

# # Go to DeepREI Project Folder
# %cd gdrive/My Drive/DeepREI-Project/DeepREI/Scraper


# %%
from config import DB_HOST, DB_DATABASE, DB_USER, DB_PASSWORD, DB_PORT, SCRAPY_API
from scrapy.crawler import CrawlerProcess
import psycopg2
import scrapy

# Declare packages as global, GCP error workaround
global scrapy, CrawlerProcess


# %%
# Instantiate DB Connection
connection = psycopg2.connect(
    host=DB_HOST,
    database=DB_DATABASE,
    user=DB_USER,
    password=DB_PASSWORD,
    port=DB_PORT
)
cur = connection.cursor()

if connection is not None:
    print('Connection established to PostgreSQL.')
else:
    print('Connection not established to PostgreSQL.')

# Import Zipcode
global postcodes
filezip = open('counties.txt', 'r')
zipcode = filezip.read().split('\n')
postcodes = [z.strip() for z in zipcode if z.strip()]
print(postcodes)


# %%


class RealtorScraper(scrapy.Spider):
    name = 'realtor'
    custom_settings = {
        'DOWNLOAD_TIMEOUT': 600,
        'DOWNLOADER_MIDDLEWARES': {'scrapy_crawlera.CrawleraMiddleware': 610},
        'CRAWLERA_ENABLED': True,
        'CRAWLERA_APIKEY': SCRAPY_API,
        'CONCURRENT_REQUESTS': 16,
        'AUTOTHROTTLE_ENABLED': False,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 32}
    
    print(SCRAPY_API)

    # Function: For Each Zipcode,
    def start_requests(self):
        for pc in postcodes:
            # urlsold = f'https://www.realtor.com/soldhomeprices/{pc}/type-single-family-home'
            # yield scrapy.Request(url=urlsold, meta={'listingtype': 'sold'}, dont_filter=False)
            urlbuy = f'https://www.realtor.com/realestateandhomes-search/{pc}/type-single-family-home/price-250000-500000'
            yield scrapy.Request(url=urlbuy, meta={'listingtype': 'buy'}, dont_filter=False)

    def parse(self, response, **kwargs):
        if 'Pardon Our Interruption' in response.css('body > div > h1::text').extract_first(''):
            yield scrapy.Request(url=response.url, dont_filter=False, callback=self.parse, meta={'listingtype': response.meta['listingtype']})
        else:
            try:
                total_pages = int(response.css(
                    '.pagination span.page')[-1].css('a::text').extract_first())
                i = 1
                while i <= total_pages:
                    link = response.url + f'/pg-{i}/'
                    yield scrapy.Request(url=link, dont_filter=False, callback=self.parse_props, meta={'listingtype': response.meta['listingtype']})
                    i += 1
            except:
                try:
                    total_pages = int(
                        response.css('div[data-testid="pagination"] .item')[-2].css('::text').extract_first())
                    i = 1
                    while i <= total_pages:
                        link = response.url + f'/pg-{i}/'
                        yield scrapy.Request(url=link, dont_filter=False, callback=self.parse_props, meta={'listingtype': response.meta['listingtype']})
                        i += 1
                except:
                    yield scrapy.Request(url=response.url, dont_filter=False, callback=self.parse, meta={'listingtype': response.meta['listingtype']})

    def parse_props(self, response):
        if 'Pardon Our Interruption' in response.css('body > div > h1::text').extract_first(''):
            yield scrapy.Request(url=response.url, dont_filter=False, callback=self.parse_props, meta={'listingtype': response.meta['listingtype']})
        else:
            if len(response.css('ul[data-testid="property-list-container"] li[data-testid="result-card"]')) == 0:
                for res in response.css(
                        'ul.srp-list-marginless.list-unstyled.prop-list li.component_property-card.js-component_property-card'):
                    link = 'https://www.realtor.com' + \
                        res.css('::attr(href)').extract_first()
                    yield scrapy.Request(url=link, dont_filter=False, callback=self.parse_data, meta={'listingtype': response.meta['listingtype']})
            else:
                for res in response.css('ul[data-testid="property-list-container"] li[data-testid="result-card"]'):
                    link = 'https://www.realtor.com' + \
                        res.css('::attr(href)').extract_first()
                    yield scrapy.Request(url=link, dont_filter=False, callback=self.parse_data, meta={'listingtype': response.meta['listingtype']})

    def parse_data(self, response):
        if 'Pardon Our Interruption' in response.css('body > div > h1::text').extract_first(''):
            yield scrapy.Request(url=response.url, dont_filter=False, callback=self.parse_data, meta={'listingtype': response.meta['listingtype']})
        else:
            LastSoldPrice = None
            ForSalePrice = None

            bedroom = None
            TotalBathrooms = None
            FullBathrooms = None
            HalfBathrooms = None
            BathroomDescription = None
            GarageSpaces = None
            CoolingFeatures = None
            InteriorFeatures = None
            HeatingFeatures = None
            DiningRoomDescription = None
            ExteriorandLotFeatures = None
            WaterFeatures = None
            WaterfrontDescription = None
            PoolFeatures = None
            PoolDescription = None
            Mode = None
            ParkingFeatures = None
            View = None
            OtherEquipment = None
            ElementarySchool = None
            HighSchool = None
            MiddleSchool = None
            AssociationFeeAmenitie = None
            Association = None
            AssociationAmenities = None
            AssociationFee = None
            AssociationFeeFrequency = None
            CalculatedTotalMonthlyAssociation = None
            MaintenanceDescription = None
            PetDescription = None
            AnnualTaxAmount = None
            SourceListingStatus = None
            County = None
            Directions = None
            TaxYear = None
            Restrictions = None
            SourcePropertyType = None
            Area = None
            SourceNeighborhood = None
            PostalCode = None
            PublicSurveySection = None
            Subdivision = None
            Zoning = None
            SourceSystemName = None
            TotalSquareFeetLiving = None
            YearBuilt = None
            ConstructionMaterials = None
            DirectionFaces = None
            PropertyAge = None
            Roof = None
            LevelsorStories = None
            StructureType = None
            HouseStyle = None
            TotalAreaSqft = None
            YearBuiltDetails = None
            ArchitecturalStyle = None
            Sewer = None
            WaterSource = None

            if 'Property Details' in ''.join(response.css('section[data-label="Property Details"] h2::text').extract()).strip():
                link = response.url
                ListingType = response.meta['listingtype']

                if ListingType == 'buy':
                    try:
                        ForSalePrice =response.xpath("/html[1]/body[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/main[1]/div[4]/span[1]/div[1]/div[1]/div[1]/h2[1]/div[1]/div[1]/div[1]").get()
                        # if ForSalePrice is None:
                        #     ForSalePrice=response.xpath("//div[@data-testid='property-meta-sqft']/span/text()").get()
                        try:
                            ForSalePrice = ForSalePrice.strip()
                        except:
                            ForSalePrice = ForSalePrice

                        ForSalePrice = ForSalePrice.replace('$', '')
                        ForSalePrice = ForSalePrice.replace(',', '')
                        print(ForSalePrice)

                    except:
                        ForSalePrice = 'None'

                if ListingType == 'sold':
                    try:
                        LastSoldPrice = response.xpath(
                            "//div[@class='ldp-header-price']/div[@class='display-inline']/span[position()=last()]/text()").get()
                        try:
                            LastSoldPrice = LastSoldPrice.strip()
                        except:
                            LastSoldPrice = LastSoldPrice

                        LastSoldPrice = LastSoldPrice.replace('$', '')
                        LastSoldPrice = LastSoldPrice.replace(',', '')
                        print(LastSoldPrice)

                    except:
                        LastSoldPrice = 'None'

                try:
                    description = response.css(
                        'section[data-label="Property Details"] div.desc::text').extract_first().strip().replace("'", "")
                except:
                    description = 'None'
                for res in response.css('section[data-label="Property Details"] div.feature-item'):

                    if 'Bedrooms' in res.css('h4::text').extract_first():
                        for re in res.css('ul li'):
                            bedroom = re.css('::text').extract_first().split(
                                ':')[-1].strip().replace("'", "")
                    if 'Bathrooms' in res.css('h4::text').extract_first():
                        for r in res.css('ul li'):
                            if 'Total Bathrooms' in r.css('::text').extract_first():
                                TotalBathrooms = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                            if 'Full Bathrooms' in r.css('::text').extract_first():
                                FullBathrooms = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                            if '1/2 Bathrooms' in r.css('::text').extract_first():
                                HalfBathrooms = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                            if 'Bathroom Description' in r.css('::text').extract_first():
                                BathroomDescription = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                    if 'Interior Features' in res.css('h4::text').extract_first():
                        for r in res.css('ul li'):
                            InteriorFeatures = ''.join(
                                r.css('::text').extract_first()).replace("'", "")
                    if 'Heating and Cooling' in res.css('h4::text').extract_first():
                        for r in res.css('ul li'):
                            if 'Cooling Features' in r.css('::text').extract_first():
                                CoolingFeatures = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                            if 'Heating Features' in r.css('::text').extract_first():
                                HeatingFeatures = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                    if 'Kitchen and Dining' in res.css('h4::text').extract_first():
                        for r in res.css('ul li'):
                            if 'Dining Room Description' in r.css('::text').extract_first():
                                DiningRoomDescription = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                    if 'Exterior and Lot Features' in res.css('h4::text').extract_first():
                        for r in res.css('ul li'):
                            ExteriorandLotFeatures = ''.join(
                                r.css('::text').extract_first()).replace("'", "")
                    if 'Waterfront and Water Access' in res.css('h4::text').extract_first():
                        for r in res.css('ul li'):
                            if 'Water Features' in r.css('::text').extract_first():
                                WaterFeatures = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                            if 'Waterfront Description' in r.css('::text').extract_first():
                                WaterfrontDescription = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                    if 'Pool and Spa' in res.css('h4::text').extract_first():
                        for r in res.css('ul li'):
                            if 'Pool Features: Pool YN' in r.css('::text').extract_first():
                                PoolFeatures = r.css('::text').extract_first().split('YN:')[-1].split(',')[
                                    0].strip().replace("'", "")
                            if 'Pool Description' in r.css('::text').extract_first():
                                PoolDescription = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                    if 'Manufactured and Mobile Info' in res.css('h4::text').extract_first():
                        for r in res.css('ul li'):
                            if 'Mode' in r.css('::text').extract_first():
                                Mode = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                    if 'Garage and Parking' in res.css('h4::text').extract_first():
                        for r in res.css('ul li'):
                            if 'Garage Spaces' in r.css('::text').extract_first():
                                GarageSpaces = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                            if 'Parking Features' in r.css('::text').extract_first():
                                ParkingFeatures = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                    if 'Home Features' in res.css('h4::text').extract_first():
                        for r in res.css('ul li'):
                            if 'Garage Spaces' in r.css('::text').extract_first():
                                GarageSpaces = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                            if 'Parking Features' in r.css('::text').extract_first():
                                ParkingFeatures = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                    if 'School Information' in res.css('h4::text').extract_first():
                        for r in res.css('ul li'):
                            if 'Elementary School' in r.css('::text').extract_first():
                                ElementarySchool = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                            if 'High School' in r.css('::text').extract_first():
                                HighSchool = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                            if 'Middle School' in r.css('::text').extract_first():
                                MiddleSchool = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                    if 'Homeowners Association' in res.css('h4::text').extract_first():
                        for r in res.css('ul li'):
                            if 'Association Fee Amenitie' in r.css('::text').extract_first():
                                AssociationFeeAmenitie = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                            if 'Association:' in r.css('::text').extract_first():
                                Association = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                            if 'Association Amenities:' in r.css('::text').extract_first():
                                AssociationAmenities = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                            if 'Association Fee:' in r.css('::text').extract_first():
                                AssociationFee = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                            if 'Association Fee Frequency:' in r.css('::text').extract_first():
                                AssociationFeeFrequency = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                            if 'Calculated Total Monthly Association' in r.css('::text').extract_first():
                                CalculatedTotalMonthlyAssociation = r.css('::text').extract_first().split(':')[
                                    -1].strip().replace("'", "")
                            if 'Maintenance Description' in r.css('::text').extract_first():
                                MaintenanceDescription = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                            if 'Pet Description' in r.css('::text').extract_first():
                                PetDescription = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                    if 'Other Property Info' in res.css('h4::text').extract_first():
                        for r in res.css('ul li'):
                            if 'Annual Tax Amount' in r.css('::text').extract_first():
                                AnnualTaxAmount = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                            if 'Source Listing Status' in r.css('::text').extract_first():
                                SourceListingStatus = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                            if 'County' in r.css('::text').extract_first():
                                County = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                            if 'Directions' in r.css('::text').extract_first():
                                Directions = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                            if 'Tax Year' in r.css('::text').extract_first():
                                TaxYear = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                            if 'Restrictions' in r.css('::text').extract_first():
                                Restrictions = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                            if 'Source Property Type' in r.css('::text').extract_first():
                                SourcePropertyType = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                            if 'Area' in r.css('::text').extract_first():
                                Area = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                            if 'Source Neighborhood' in r.css('::text').extract_first():
                                SourceNeighborhood = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                            if 'Postal Code' in r.css('::text').extract_first():
                                PostalCode = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                            if 'Public Survey Section' in r.css('::text').extract_first():
                                PublicSurveySection = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                            if 'Subdivision' in r.css('::text').extract_first():
                                Subdivision = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                            if 'Zoning' in r.css('::text').extract_first():
                                Zoning = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                            if 'Source System Name' in r.css('::text').extract_first():
                                SourceSystemName = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                    if 'Building and Construction' in res.css('h4::text').extract_first():
                        for r in res.css('ul li'):
                            if 'Total Square Feet Living' in r.css('::text').extract_first():
                                TotalSquareFeetLiving = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                            if 'Year Built' in r.css('::text').extract_first():
                                YearBuilt = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                            if 'Construction Materials' in r.css('::text').extract_first():
                                ConstructionMaterials = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                            if 'Direction Faces' in r.css('::text').extract_first():
                                DirectionFaces = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                            if 'Property Age' in r.css('::text').extract_first():
                                PropertyAge = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                            if 'Roof' in r.css('::text').extract_first():
                                Roof = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                            if 'Levels or Stories' in r.css('::text').extract_first():
                                LevelsorStories = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                            if 'Structure Type' in r.css('::text').extract_first():
                                StructureType = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                            if 'House Style' in r.css('::text').extract_first():
                                HouseStyle = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                            if 'Total Area Sqft' in r.css('::text').extract_first():
                                TotalAreaSqft = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                            if 'Year Built Details' in r.css('::text').extract_first():
                                YearBuiltDetails = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                            if 'Architectural Style' in r.css('::text').extract_first():
                                ArchitecturalStyle = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                    if 'Utilities' in res.css('h4::text').extract_first():
                        for r in res.css('ul li'):
                            if 'Sewer' in r.css('::text').extract_first():
                                Sewer = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")
                            if 'Water Source' in r.css('::text').extract_first():
                                WaterSource = r.css('::text').extract_first().split(
                                    ':')[-1].strip().replace("'", "")


                cur.execute(
                    'INSERT INTO public.county_forsale_properties(PropertyUrl, ListingType, ForSalePrice, LastSoldPrice, description, bedroom, TotalBathrooms, FullBathrooms, HalfBathrooms, BathroomDescription, InteriorFeatures, CoolingFeatures, HeatingFeatures, DiningRoomDescription, ExteriorandLotFeatures, WaterFeatures, WaterfrontDescription, PoolFeatures, PoolDescription, ManufacturedMode, GarageSpaces, ParkingFeatures, HomeFeaturesView, OtherEquipment, ElementarySchool,  HighSchool, MiddleSchool, AssociationFeeAmenitie, Association, AssociationAmenities, AssociationFee, AssociationFeeFrequency, CalculatedTotalMonthlyAssociation, MaintenanceDescription, PetDescription, AnnualTaxAmount, SourceListingStatus, County, Directions, TaxYear, Restrictions, SourcePropertyType, Area, SourceNeighborhood, PostalCode, PublicSurveySection, Subdivision, Zoning, SourceSystemName, TotalSquareFeetLiving, YearBuilt, ConstructionMaterials, DirectionFaces, PropertyAge, Roof, LevelsorStories, StructureType, HouseStyle, TotalAreaSqft, YearBuiltDetails, ArchitecturalStyle, Sewer, WaterSource)' + f"VALUES ('{link}', '{ListingType}', '{ForSalePrice}', '{LastSoldPrice}', '{description}', '{bedroom}', '{TotalBathrooms}', '{FullBathrooms}', '{HalfBathrooms}', '{BathroomDescription}', '{InteriorFeatures}', '{CoolingFeatures}', '{HeatingFeatures}', '{DiningRoomDescription}', '{ExteriorandLotFeatures}', '{WaterFeatures}', '{WaterfrontDescription}', '{PoolFeatures}', '{PoolDescription}', '{Mode}', '{GarageSpaces}', '{ParkingFeatures}', '{View}', '{OtherEquipment}', '{ElementarySchool}', '{HighSchool}', '{MiddleSchool}', '{AssociationFeeAmenitie}', '{Association}', '{AssociationAmenities}', '{AssociationFee}', '{AssociationFeeFrequency}', '{CalculatedTotalMonthlyAssociation}', '{MaintenanceDescription}', '{PetDescription}', '{AnnualTaxAmount}', '{SourceListingStatus}', '{County}', '{Directions}', '{TaxYear}', '{Restrictions}', '{SourcePropertyType}', '{Area}', '{SourceNeighborhood}', '{PostalCode}', '{PublicSurveySection}', '{Subdivision}', '{Zoning}', '{SourceSystemName}', '{TotalSquareFeetLiving}', '{YearBuilt}', '{ConstructionMaterials}', '{DirectionFaces}', '{PropertyAge}', '{Roof}', '{LevelsorStories}', '{StructureType}', '{HouseStyle}', '{TotalAreaSqft}', '{YearBuiltDetails}', '{ArchitecturalStyle}', '{Sewer}', '{WaterSource}')")
                connection.commit()
            
            elif 'Property Details' in ''.join(response.css('#ldp-collapsed-property-details h2::text').extract()).strip():
                link = response.url
                ListingType = response.meta['listingtype']

                if ListingType == 'buy':
                    try:
                        ForSalePrice = response.xpath(
                            "//div[@data-testid='price-section']/span[contains(@class,'price')]/text()").get()
                        try:
                            ForSalePrice = ForSalePrice.strip()
                        except:
                            ForSalePrice = ForSalePrice

                        ForSalePrice = ForSalePrice.replace('$', '')
                        ForSalePrice = ForSalePrice.replace(',', '')
                        print(ForSalePrice)

                    except:
                        ForSalePrice = 'None'


                if ListingType == 'sold':
                    try:
                        LastSoldPrice = response.xpath(
                            "//div[@class='ldp-header-price']/div[@class='display-inline']/span[position()=last()]/text()").get()
                        try:
                            LastSoldPrice = LastSoldPrice.strip()
                        except:
                            LastSoldPrice = LastSoldPrice

                        LastSoldPrice = LastSoldPrice.replace('$', '')
                        LastSoldPrice = LastSoldPrice.replace(',', '')
                        print(LastSoldPrice)

                    except:
                        LastSoldPrice = 'None'

                try:
                    description = ''.join(response.css('#ldp-detail-overview ::text').extract(
                    )).strip().replace('\n', '').replace(' ', '').replace("'", "")
                except:
                    description = 'null'
                j = 0
                for i, res in enumerate(response.css('#load-more-features .row')):
                    for re in res.css('.col-lg-3.col-sm-6.col-xs-6.col-xxs-12.ldp-features-image-tag'):

                        if 'Bedrooms' in re.css('h4::text').extract_first():
                            bedroom = re.css('ul li::text').extract_first().split(
                                ':')[-1].strip().replace("'", "")
                        if 'Bathrooms' in re.css('h4::text').extract_first():
                            for r in re.css('ul li'):
                                if 'Total Bathrooms' in r.css('::text').extract_first():
                                    TotalBathrooms = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")
                                if 'Full Bathrooms' in r.css('::text').extract_first():
                                    FullBathrooms = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")
                                if '1/2 Bathrooms' in r.css('::text').extract_first():
                                    HalfBathrooms = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")
                                if 'Bathroom Description' in r.css('::text').extract_first():
                                    BathroomDescription = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")
                    if i == 0:
                        continue

                    if 'Interior Features' in response.css('#load-more-features h4.title-subsection-sm.font-bold')[
                            j].css('::text').extract_first():
                        InteriorFeatures = ''.join(
                            res.css(' ::text').extract()).strip().replace("'", "")

                    if 'Heating and Cooling' in response.css('#load-more-features h4.title-subsection-sm.font-bold')[
                            j].css('::text').extract_first():
                        for re in res.css('.list-default'):
                            for r in re.css('li'):
                                if 'Cooling Features' in r.css('::text').extract_first():
                                    CoolingFeatures = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")
                                if 'Heating Features' in r.css('::text').extract_first():
                                    HeatingFeatures = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")

                    if 'Kitchen and Dining' in response.css('#load-more-features h4.title-subsection-sm.font-bold')[
                            j].css('::text').extract_first():
                        for re in res.css('.list-default'):
                            for r in re.css('li'):
                                if 'Dining Room Description' in r.css('::text').extract_first():
                                    DiningRoomDescription = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")

                    if 'Exterior and Lot Features' in response.css('#load-more-features h4.title-subsection-sm.font-bold')[j].css('::text').extract_first():
                        ExteriorandLotFeatures = ''.join(
                            res.css(' ::text').extract()).strip().replace("'", "")

                    if 'Waterfront and Water Access' in response.css('#load-more-features h4.title-subsection-sm.font-bold')[j].css('::text').extract_first():
                        for re in res.css('.list-default'):
                            for r in re.css('li'):
                                if 'Water Features' in r.css('::text').extract_first():
                                    WaterFeatures = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")
                                if 'Waterfront Description' in r.css('::text').extract_first():
                                    WaterfrontDescription = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")

                    if 'Pool and Spa' in response.css('#load-more-features h4.title-subsection-sm.font-bold')[j].css('::text').extract_first():
                        for re in res.css('.list-default'):
                            for r in re.css('li'):
                                if 'Pool Features: Pool YN' in r.css('::text').extract_first():
                                    PoolFeatures = r.css('::text').extract_first().split('YN:')[-1].split(',')[
                                        0].strip().replace("'", "")
                                if 'Pool Description' in r.css('::text').extract_first():
                                    PoolDescription = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")

                    if 'Manufactured and Mobile Info' in response.css('#load-more-features h4.title-subsection-sm.font-bold')[j].css('::text').extract_first():
                        for re in res.css('.list-default'):
                            for r in re.css('li'):
                                if 'Mode' in r.css('::text').extract_first():
                                    Mode = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")

                    if 'Garage and Parking' in response.css('#load-more-features h4.title-subsection-sm.font-bold')[j].css('::text').extract_first():
                        for re in res.css('.list-default'):
                            for r in re.css('li'):
                                if 'Garage Spaces' in r.css('::text').extract_first():
                                    GarageSpaces = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")
                                if 'Parking Features' in r.css('::text').extract_first():
                                    ParkingFeatures = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")

                    if 'Home Features' in response.css('#load-more-features h4.title-subsection-sm.font-bold')[j].css('::text').extract_first():
                        for re in res.css('.list-default'):
                            for r in re.css('li'):
                                if 'View' in r.css('::text').extract_first():
                                    View = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")
                                if 'Other Equipment' in r.css('::text').extract_first():
                                    OtherEquipment = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")

                    if 'School Information' in response.css('#load-more-features h4.title-subsection-sm.font-bold')[j].css('::text').extract_first():
                        for re in res.css('.list-default'):
                            for r in re.css('li'):
                                if 'Elementary School' in r.css('::text').extract_first():
                                    ElementarySchool = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")
                                if 'High School' in r.css('::text').extract_first():
                                    HighSchool = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")
                                if 'Middle School' in r.css('::text').extract_first():
                                    MiddleSchool = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")

                    if 'Homeowners Association' in response.css('#load-more-features h4.title-subsection-sm.font-bold')[j].css('::text').extract_first():
                        for re in res.css('.list-default'):
                            for r in re.css('li'):
                                if 'Association Fee Amenitie' in r.css('::text').extract_first():
                                    AssociationFeeAmenitie = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")
                                if 'Association:' in r.css('::text').extract_first():
                                    Association = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")
                                if 'Association Amenities:' in r.css('::text').extract_first():
                                    AssociationAmenities = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")
                                if 'Association Fee:' in r.css('::text').extract_first():
                                    AssociationFee = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")
                                if 'Association Fee Frequency:' in r.css('::text').extract_first():
                                    AssociationFeeFrequency = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")
                                if 'Calculated Total Monthly Association' in r.css('::text').extract_first():
                                    CalculatedTotalMonthlyAssociation = r.css(
                                        '::text').extract_first().split(':')[-1].strip().replace("'", "")
                                if 'Maintenance Description' in r.css('::text').extract_first():
                                    MaintenanceDescription = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")
                                if 'Pet Description' in r.css('::text').extract_first():
                                    PetDescription = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")

                    if 'Other Property Info' in response.css('#load-more-features h4.title-subsection-sm.font-bold')[j].css('::text').extract_first():
                        for re in res.css('.list-default'):
                            for r in re.css('li'):
                                if 'Annual Tax Amount' in r.css('::text').extract_first():
                                    AnnualTaxAmount = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")
                                if 'Source Listing Status' in r.css('::text').extract_first():
                                    SourceListingStatus = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")
                                if 'County' in r.css('::text').extract_first():
                                    County = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")
                                if 'Directions' in r.css('::text').extract_first():
                                    Directions = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")
                                if 'Tax Year' in r.css('::text').extract_first():
                                    TaxYear = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")
                                if 'Restrictions' in r.css('::text').extract_first():
                                    Restrictions = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")
                                if 'Source Property Type' in r.css('::text').extract_first():
                                    SourcePropertyType = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")
                                if 'Area' in r.css('::text').extract_first():
                                    Area = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")
                                if 'Source Neighborhood' in r.css('::text').extract_first():
                                    SourceNeighborhood = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")
                                if 'Postal Code' in r.css('::text').extract_first():
                                    PostalCode = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")
                                if 'Public Survey Section' in r.css('::text').extract_first():
                                    PublicSurveySection = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")
                                if 'Subdivision' in r.css('::text').extract_first():
                                    Subdivision = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")
                                if 'Zoning' in r.css('::text').extract_first():
                                    Zoning = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")
                                if 'Source System Name' in r.css('::text').extract_first():
                                    SourceSystemName = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")

                    if 'Building and Construction' in response.css('#load-more-features h4.title-subsection-sm.font-bold')[j].css('::text').extract_first():
                        for re in res.css('.list-default'):
                            for r in re.css('li'):
                                if 'Total Square Feet Living' in r.css('::text').extract_first():
                                    TotalSquareFeetLiving = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")
                                if 'Year Built' in r.css('::text').extract_first():
                                    YearBuilt = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")
                                if 'Construction Materials' in r.css('::text').extract_first():
                                    ConstructionMaterials = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")
                                if 'Direction Faces' in r.css('::text').extract_first():
                                    DirectionFaces = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")
                                if 'Property Age' in r.css('::text').extract_first():
                                    PropertyAge = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")
                                if 'Roof' in r.css('::text').extract_first():
                                    Roof = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")
                                if 'Levels or Stories' in r.css('::text').extract_first():
                                    LevelsorStories = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")
                                if 'Structure Type' in r.css('::text').extract_first():
                                    StructureType = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")
                                if 'House Style' in r.css('::text').extract_first():
                                    HouseStyle = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")
                                if 'Total Area Sqft' in r.css('::text').extract_first():
                                    TotalAreaSqft = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")
                                if 'Year Built Details' in r.css('::text').extract_first():
                                    YearBuiltDetails = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")
                                if 'Architectural Style' in r.css('::text').extract_first():
                                    ArchitecturalStyle = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")

                    if 'Utilities' in response.css('#load-more-features h4.title-subsection-sm.font-bold')[j].css('::text').extract_first():
                        for re in res.css('.list-default'):
                            for r in re.css('li'):
                                if 'Sewer' in r.css('::text').extract_first():
                                    Sewer = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")
                                if 'Water Source' in r.css('::text').extract_first():
                                    WaterSource = r.css('::text').extract_first().split(
                                        ':')[-1].strip().replace("'", "")

                    j += 1
                cur.execute(
                    'INSERT INTO public.county_forsale_properties(PropertyUrl, ListingType, ForSalePrice, LastSoldPrice, description, bedroom, TotalBathrooms, FullBathrooms, HalfBathrooms, BathroomDescription, InteriorFeatures, CoolingFeatures, HeatingFeatures, DiningRoomDescription, ExteriorandLotFeatures, WaterFeatures, WaterfrontDescription, PoolFeatures, PoolDescription, ManufacturedMode, GarageSpaces, ParkingFeatures, HomeFeaturesView, OtherEquipment, ElementarySchool, HighSchool, MiddleSchool, AssociationFeeAmenitie, Association, AssociationAmenities, AssociationFee, AssociationFeeFrequency, CalculatedTotalMonthlyAssociation, MaintenanceDescription, PetDescription, AnnualTaxAmount, SourceListingStatus, County, Directions, TaxYear, Restrictions, SourcePropertyType, Area, SourceNeighborhood, PostalCode, PublicSurveySection, Subdivision, Zoning, SourceSystemName, TotalSquareFeetLiving, YearBuilt, ConstructionMaterials, DirectionFaces, PropertyAge, Roof, LevelsorStories, StructureType, HouseStyle, TotalAreaSqft, YearBuiltDetails, ArchitecturalStyle, Sewer, WaterSource)' + f"VALUES ('{link}', '{ListingType}', '{ForSalePrice}', '{LastSoldPrice}', '{description}', '{bedroom}', '{TotalBathrooms}', '{FullBathrooms}', '{HalfBathrooms}', '{BathroomDescription}', '{InteriorFeatures}', '{CoolingFeatures}', '{HeatingFeatures}', '{DiningRoomDescription}', '{ExteriorandLotFeatures}', '{WaterFeatures}', '{WaterfrontDescription}', '{PoolFeatures}', '{PoolDescription}', '{Mode}', '{GarageSpaces}', '{ParkingFeatures}', '{View}', '{OtherEquipment}', '{ElementarySchool}', '{HighSchool}', '{MiddleSchool}', '{AssociationFeeAmenitie}', '{Association}', '{AssociationAmenities}', '{AssociationFee}', '{AssociationFeeFrequency}', '{CalculatedTotalMonthlyAssociation}', '{MaintenanceDescription}', '{PetDescription}', '{AnnualTaxAmount}', '{SourceListingStatus}', '{County}', '{Directions}', '{TaxYear}', '{Restrictions}', '{SourcePropertyType}', '{Area}', '{SourceNeighborhood}', '{PostalCode}', '{PublicSurveySection}', '{Subdivision}', '{Zoning}', '{SourceSystemName}', '{TotalSquareFeetLiving}', '{YearBuilt}', '{ConstructionMaterials}', '{DirectionFaces}', '{PropertyAge}', '{Roof}', '{LevelsorStories}', '{StructureType}', '{HouseStyle}', '{TotalAreaSqft}', '{YearBuiltDetails}', '{ArchitecturalStyle}', '{Sewer}', '{WaterSource}')")
                connection.commit()

    def close(spider, reason):
        connection.close()


# %%
# Run Scraper
process = CrawlerProcess({
    'USER_AGENT': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36"})

process.crawl(RealtorScraper)
process.start()
