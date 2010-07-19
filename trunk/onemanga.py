import urllib
import urllib2
import os

import lxml.html as html

DIR = 'http://www.onemanga.com/directory/'
URI = 'http://www.onemanga.com'

def getMangas():
	root = html.parse(DIR)
	mangas = root.xpath('//td[@class="ch-subject"]')
	return [manga[0].text for manga in mangas]

def getChapters(manga):
	url = URI + '/' + manga
	root = html.parse(url)
	chapters = root.xpath('//td[@class="ch-subject"]')
	chapters.reverse()
	return [chapter[0].text.split()[-1] for chapter in chapters]


def getPages(manga, chapter):
	url = URI + '/' +  manga + '/' + chapter + '/'
	root = html.parse(url)
	soup = root.xpath('//li')
	url = URI + soup[0][0].get('href')
	root = html.parse(url)
	pages = root.xpath('//select[@class="page-select"]')
	return [page.text for page in pages[0].getchildren()]
	

def getImage(manga, chapter, page):
	url = URI + '/' + manga + '/' + chapter + '/' +  page+ '/'
	root = html.parse(url)
	img = root.xpath('//img[@class="manga-page"]')
	return img[0].get('src')

def downloadChapter(manga, chapter):
	pages = getPages(manga, chapter)
	folder = os.path.join('.', manga + ' ' + chapter)
	if not os.path.exists(folder):
		os.makedirs(folder)
	
	for page in pages:
		print 'page', page, 'of',  manga, chapter
		image = getImage(manga, chapter, page)
		filename = image.split('/')[-1]
		outpath = os.path.join(folder, filename)
		urllib.urlretrieve(image, outpath)


def downloadManga(manga):
	chapters = getChapters(manga)
	if not os.path.exists(manga):
		os.makedirs(manga)
	os.chdir(manga)

	for chapter in chapters:
		print 'chapter', chapter
		downloadChapter(manga, chapter)


