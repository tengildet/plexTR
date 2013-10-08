# turkportal.org
NAME = 'cumhuriyet'
BASE_URL = 'http://www.cumhuriyet.com.tr/?im=galeri&t=v'
PRE_URL =  'http://www.cumhuriyet.com.tr/'
ART = 'bg.png'
ICON = 'logo.png'
SLOGAN = 'Bu ulkenin aydinlik insanlari. Size Cumhuriyet yakisir.'.encode('UTF-8')
####################################################################################################
def Start():
	Plugin.AddViewGroup('List', viewMode='List', mediaType='items')
	ObjectContainer.art = R(ART)
	ObjectContainer.title1 = NAME
	DirectoryObject.thumb = R(ICON)
####################################################################################################
@handler('/video/cumhuriyet', NAME, thumb=ICON, art=ART)
def MainMenu():
	oc = ObjectContainer(view_group='List')
	for category in HTML.ElementFromURL(BASE_URL).xpath("//div[@class='c500'][1]/div[contains (@class ,'album')]/div[@class='kategori']"):
		url =PRE_URL + str(category.xpath('./a/@href')[0])
		title=category.xpath('./a')[0].text
                oc.add(DirectoryObject(key = Callback(Tags, title=title, url=url),title = title, summary = SLOGAN))
	return oc
####################################################################################################
@route('/video/cumhuriyet/tags')
def Tags(title,url):
	oc = ObjectContainer(title2 = title, view_group='List')
	XHTML = HTML.ElementFromURL(url)
	for category in XHTML.xpath("//div[@class='s2']/div[2]/div[@class='c500']/div[contains (@class,'album')]"):
                url=PRE_URL + str(category.xpath('./a/@href')[0])
		title=category.xpath("./h2/a")[0].text
		thumb=category.xpath("./a/img[@class='foto170']/@src")[0]
                oc.add(VideoClipObject(url=url ,title = title, thumb=thumb))
        try:
                flink = XHTML.xpath("/html/body/div[4]/div[1]/div[2]/div[1]/div/div[2]/div[7]/span/a/@href")[0]
                fname = XHTML.xpath("/html/body/div[4]/div[1]/div[2]/div[1]/div/div[2]/div[7]/span/a")[0].text
                oc.add(DirectoryObject(key = Callback(Tags, title = fname, url = PRE_URL + flink),title = fname, summary = SLOGAN))
        except:
                no=None

        try:
                llink = XHTML.xpath("/html/body/div[4]/div[1]/div[2]/div[1]/div/div[2]/div[7]/span/a/@href")[1]
                lname = XHTML.xpath("/html/body/div[4]/div[1]/div[2]/div[1]/div/div[2]/div[7]/span/a")[1].text
                oc.add(DirectoryObject(key = Callback(Tags, title = lname, url = PRE_URL + llink),title = lname, summary = SLOGAN))
        except:
                no=None
	return oc
