# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import scrapy
from scrapy.item import Item

class  JoesItems(Item):

   
    SKU =scrapy.Field()
    ProductName=scrapy.Field()
    Brand=scrapy.Field()
    ProductType=scrapy.Field()
    ProductCategory=scrapy.Field()
    Gender=scrapy.Field()
    LinkNavCategories=scrapy.Field()
    ProductLink=scrapy.Field()
    Image=scrapy.Field()
    ImageGallery=scrapy.Field()
    OriginalPrice=scrapy.Field()
    ActualPrice=scrapy.Field()
    Sizes=scrapy.Field()
    Color=scrapy.Field()
    Width=scrapy.Field()

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)  

def removeWords(string):
   
    string=string.replace("Women's",'')
    string=string.replace("WOMEN'S",'')
    string=string.replace("Men's",'')
    string=string.replace("Kid's",'')
    return string
   

class joesSpider(scrapy.Spider):
    name = "joes"
    start_urls =['https://www.joesnewbalanceoutlet.com/']
       
    def parse(self, response):
       
        href='.//a/@href'
        x='.//div[contains(@class,"menuOverflow")]/h3[1]/a/text()'
        y='.//div[contains(@class,"menuOverflow")]/h3[1]/span/text()'

       
        for NavCategories in response.css('div.subNavCat'):
           
               

               
            for link in NavCategories.xpath(href).getall():
               
                if str(NavCategories.xpath(x).extract_first()).strip()=='Shoes':

                    splitLink=link.split("/")
                    if len(splitLink)>3   :
                        print(link)
                        yield scrapy.Request('https://www.joesnewbalanceoutlet.com'+link, callback=self.details)
                else :
                    if (str(NavCategories.xpath(y).extract_first()).strip()=='Girls') or str(NavCategories.xpath(y).extract_first()).strip()=='Boys':
                        splitLink=link.split("/")
                        if len(splitLink)>3 and str(splitLink).find("shoes")!=-1  :
                            print(link)
                            yield scrapy.Request('https://www.joesnewbalanceoutlet.com'+link, callback=self.details)
            break
               
               

    def details(self,response):
       
       
       
        href='.//div[@class="figureWrapper"]/a[1]/@href'

#          מגיע לעמוד עם כל המוצרים
        urls=[]
        for link in response.xpath(href).getall():
           
            urls.append('https://www.joesnewbalanceoutlet.com'+link)
           
        for url in urls:
             
            item=JoesItems()
            item['LinkNavCategories']=response.url
            request= scrapy.Request(url, callback=self.productDetails)
            request.meta['LinkNavCategories'] =item
           
            yield request




        next_page_selector='a.fa.fa-chevron-right.pagingNext ::attr(href)'
        next_page=response.css(next_page_selector).get()
        if next_page :
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.details)
                       
                       
       
       
    def productDetails(self,response):        #        בשביל לראות את פרטי המוצר בצורה מפורטת יותר    


        item=response.meta['LinkNavCategories']

       
        indexofli=response.xpath('.//section[@id="Breadcrumbs"]/nav/ul/li').getall()
        item['Gender']=response.xpath('.//section[@id="Breadcrumbs"]/nav/ul/li[1]/a/text()').get()
        item['ProductType']='Shoes'

#        על מנת לקבל את המקום האחרון=לקבל את קטגוריית המוצר
        index=len(item['LinkNavCategories'].split('/'))
        ProductCategory=item['LinkNavCategories'].split('/')[index-1]
        if ProductCategory.find('?')!=-1:
            ind=ProductCategory.find('?')
            item['ProductCategory']=ProductCategory[:ind]
           
        else:    
           
            item['ProductCategory']=ProductCategory
       

        item['ProductLink']=response.url

        for res in response.xpath('.//section[@id="ProductDetailPage"]'):
       
            for img in response.xpath('.//span[@id="ProductImage"]') :    

                item['Image']=img.css('img::attr(src)').extract_first()
                   ##    בשביל המחירים
            for price in response.xpath('.//div[@id="Price"]'):
               
               
                char=price.xpath('.//span[contains(@class, "floatLeft") and contains(@class, "productPrice")]/span[1]/text()').extract_first()
                value=price.xpath('.//span[contains(@class, "floatLeft") and contains(@class, "productPrice")]/span[2]/text()').extract_first()
                item['ActualPrice']=value+char
               
                origp=price.xpath('.//div[contains(@class, "floatLeft") and contains(@class, "productPriceInfo")]/span/span/text()').extract_first()
                dot=price.xpath('.//div[contains(@class, "floatLeft") and contains(@class, "productPriceInfo")]/span/span/span/text()').extract_first()    
                item['OriginalPrice']=str(origp+dot).strip()
      #    בשביל הצבע והסטייל
            for color in response.css('div.pdpColorStyle'):
               
                item['Color']=color.xpath('.//span[@id="DisplayColor"]/text()').extract_first()
                item['SKU']=color.xpath('.//span[@id="Sku"]/text()').extract_first()
                          ##    בשביל המידות
            string=''
           
            for size in response.xpath('.//div[@id="AddToCartControls"]/div'):
               
                for s in size.xpath(".//span/a"):
#            קורא כאשר יש רק מידה אחת וזה עטוף בצורה שונה
                   
                    string=string+s.xpath("text()").extract_first()+','    
                   
                if string=='':
                   
                    string=size.xpath(".//h3/span/text()").extract_first()
   
            if hasNumbers(string)==True or string!='':
                item['Sizes']=string
            else:
                string=''
                for size in response.xpath('.//div[@id="AddToCartControls"]/div'):
                    for s in size.xpath(".//span/a"):
                        string=string+s.xpath("span[1]/text()").extract_first()+','
                        string=string+s.xpath("span[2]/text()").extract_first()+','
                item['Sizes']=string        
               
#            בשביל שאר התמונות
            imgString=' '
            for imageGallery in response.xpath('.//div[@id="Thumbnails"]/div/div/div[@class="swiper-slide"]'):
                for img in imageGallery.xpath('.//a'):
                   
                    imgString=imgString+img.css('img::attr(src)').extract_first()+','+' '
                   
            item['ImageGallery'] =imgString      
            for productDetails in response.xpath('.//div[@id="DetailsHeading"and contains(@class,"productDetails")]'):
                   
               
                productName=productDetails.xpath('h1/text()').extract_first()
                item['ProductName']=removeWords(productName)




            item['Brand']='New Balance'
            widthString=''    
            for WidthProduct in response.css('div.selfClearAfter.addToCartControl.RadioButton.WidthButton.selectorContainer') or response.css('div.selfClearAfter.addToCartControl.RadioButton.WidthButton'):
                for width in WidthProduct.xpath('.//span'):
                   
                   
                    if width.xpath('@data-name').extract_first()!=None:
                        widthString=str(widthString+width.xpath('@data-value').extract_first()).strip()
                   
                    if width.xpath('label/span/text()').extract_first()!=None:
                        widthString=widthString+str(width.xpath('label/span/text()').extract_first()).strip()+','
               
                item['Width']=widthString
                   
               
            #ftpURI = "ftp://football1::4uT%J*r84@s17.wpxhosting.com/domains/privatedeal.co.il/public_html/wp-content/uploads/wpallimport/files"
       
             
            yield  item