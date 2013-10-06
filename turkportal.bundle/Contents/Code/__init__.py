import urllib
NAME = 'turkportal'
SECTION_URL = 'http://smartsmart.pusku.com/enigma/proxy.php?kim='
ART = 'backdrop.png'
ICON = 'turkportal.png'
####################################################################################################
def Start():
	Plugin.AddViewGroup('List', viewMode='List', mediaType='items')
	ObjectContainer.art = R(ART)
	ObjectContainer.title1 = NAME
	DirectoryObject.thumb = R(ICON)
####################################################################################################
@handler('/video/turkportal', NAME, thumb=ICON, art=ART)
def MainMenu(url='http://smartsmart.pusku.com/enigma/proxy.php'):
	oc = ObjectContainer(view_group='List')
	for category in XML.ElementFromURL(url).xpath('//AnaPortal'):
		baslik = category.xpath('./Baslik')[0].text.upper()
		resim =category.xpath('./Resim')[0].text
		bak = category.xpath('./PlayOrStream')[0].text
		stream = category.xpath('./Streamlink')[0].text
		if bak=='xor': 
			url=SECTION_URL + urllib.quote(category.xpath('./PlayList')[0].text)
			oc.add(DirectoryObject(key = Callback(MainMenu,url=url),title =baslik,thumb=resim))
		else:
			oc.add(VideoClipObject(title=baslik, thumb=resim, url=stream, summary='TURKPORTAL'))		
	return oc
