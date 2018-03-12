#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 17:21:20 2017

@author: radhikakalaiselvan
"""
import urllib.request  as urllib2
import urllib.parse as urlparse
import os
import sys
import nltk


from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

#RequiresBeautifulSoup
try:
        from bs4 import BeautifulSoup  
except ImportError:
            print("Please download and install beautiful soup first!")
            sys.exit(0)
            
            
downloaded_files=[]
count=[]

#return the text content of pdf file
def read_pdf(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)
    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)
    infile = open(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
        text = output.getvalue()
        output.flush
        
    infile.close()
    converter.close()
    output.close
    return text 

#Downloads all pdfs from any web page
def download_pdfs():
    url="Your URL"
    website=urllib2.urlopen(url)
    soup=BeautifulSoup(website.read(),"lxml")
    i=0
    # A set which stores all the links of pdf. Used to avoid accidentally downloading the same pdf files again. 
    url_set=set()
    #Find all a tags in the page
    for tag in soup.findAll('a',href=True):
        tag['href']=urlparse.urljoin(url,tag['href'])
        url_split=os.path.splitext(os.path.basename(tag['href']))
        #get the last part of href and check if it is .pdf file
        if url_split[1].lower() == '.pdf' :
            #if the link is in url_set then it is already downloaded else download the file now
            found=tag['href'] in url_set
            if not found:
                parsed = urlparse.urlparse(tag['href'])
                file_name=urlparse.parse_qs(parsed.query)['filename'][0]
                with open(file_name,'wb') as f:
                    current=urllib2.urlopen(tag['href'])
                    f.write(current.read())
                downloaded_files.append(file_name)
                print("Downloaded ",file_name," ...")
                url_set.add(tag['href'])
                i+=1
    print("Downloaded ",i," files.")

if __name__ =='__main__':
    download_pdfs()
    for file in downloaded_files:
        print("Reading file ",file)
        text_content=read_pdf(file)
        print("Counting 'travel' ...")
        words = nltk.word_tokenize(text_content.lower())
        fdist = nltk.FreqDist(words)
        count_p=fdist['YOUR WORD TO SEARCH']
        count.append(count_p)
        print("Count = ",count_p)
    for i in range(len(downloaded_files)):
        print(downloaded_files[i],"  ",count[i])

            