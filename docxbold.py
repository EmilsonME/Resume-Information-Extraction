from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import pdfminer
import re
from Cryptodome import Cipher

def createPDFDoc(fpath):
	fp = open(fpath, 'rb')
	parser = PDFParser(fp)
	document = PDFDocument(parser, password='')
	if not document.is_extractable:
		raise "Not extractable"
	else:
		return document


def createDeviceInterpreter():
	rsrcmgr = PDFResourceManager()
	laparams = LAParams()
	device = PDFPageAggregator(rsrcmgr, laparams=laparams)
	interpreter = PDFPageInterpreter(rsrcmgr, device)
	return device, interpreter

def remove_non_ascii_2(text):
	return ''.join([i if ord(i) < 128 else ' ' for i in text])


def parse_obj(objs):
	list1 = []
	for obj in objs:
		if isinstance(obj, pdfminer.layout.LTTextBox):
			for o in obj._objs:
				if isinstance(o,pdfminer.layout.LTTextLine):
					text=o.get_text()
					text = remove_non_ascii_2(text)
					text = re.sub('\'', '', text)
					if text.strip():
						for c in  o._objs:
							if isinstance(c, pdfminer.layout.LTChar):
								if("Bold" in c.fontname ):
									# print text + " fontname %s"%c.fontname
									list1.append(text)
		elif isinstance(obj, pdfminer.layout.LTFigure):
			parse_obj(obj._objs)
		else:
			pass

	return list(set(list1))

def extractThis(directory):
	document=createPDFDoc(directory)
	device,interpreter=createDeviceInterpreter()
	pages=PDFPage.create_pages(document)
	password = ""
	maxpages = 0
	caching = True
	pagenos=set()
	list1 = []

	fp = open(directory, 'rb')
	for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
		interpreter.process_page(page)
		layout = device.get_result()
		list1 = list1 + parse_obj(layout._objs)


	# interpreter.process_page(pages.next())
	
	return list1