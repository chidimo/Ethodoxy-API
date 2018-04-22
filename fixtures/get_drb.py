
# coding: utf-8

# http://drbo.org/
# 
# {Book : {Chapter : [list of verses ]}}


import re
import json
import glob
from pywebber import Ripper

domain = "http://drbo.org/"

home = Ripper(domain)
home_links = list(home.links())

def get_book_links(raw_page_rip):
    nt = {}
    ot = {}
    OTIDS = []
    soup = raw_page_rip.soup   
    
    nt_soup = soup.find("td", class_="NT")
    ot1 = soup.find("td", class_="OT1")
    ot2 = soup.find("td", class_="OT2")
    
    for each in nt_soup.find_all("a", href=True):
        if 'class="b"' in str(each):
            href = each.get("href")
            name = each.text

            idd = re.search(r'\d{5}', href).group(0)
            nt[name] = [domain + href, idd]
            
    with open("new_test.json", "w+") as wh:
        json.dump(nt, wh)

    for each in ot1.find_all("a", href=True):
        if 'class="b"' in str(each):
            
            href = each.get("href")
            name = each.text
            idd = re.search(r'\d{5}', href).group(0)
                        
            if idd in OTIDS:
                ot[domain + href][0] = name + " or " + ot[domain + href][0]
                
            else:
                ot[domain + href] = [name, idd]
                OTIDS.append(idd)
                
    for each in ot2.find_all("a", href=True):
        if 'class="b"' in str(each):
            
            href = each.get("href")
            name = each.text
            idd = re.search(r'\d{5}', href).group(0)
                        
            if idd in OTIDS:
                ot[domain + href][0] = name + " or " + ot[domain + href][0]
                
            else:
                ot[domain + href] = [name, idd]
                OTIDS.append(idd)
                
    rev_old = {value[0] : [key, value[1]] for key, value in ot.items()}
    with open("old_test.json", "w+") as wh:
        json.dump(rev_old, wh)        

def normalize_filename(file_name):
    return "_".join([each.lower() for each in re.split(r"[\, *, \/]", file_name) if each != ''])

def get_chapters(book_name, book_link, idd):
    chapters = {"01" : book_link}
    home = Ripper(book_link)
    
    for each in home.raw_links:
        str_each = str(each)
        excludes = ["next" in str_each, "previous" in str_each, "chapter" in str_each, "statcounter" in str_each,
                    "/x/" in str_each, "DRBO.ORG" in str_each, "theologica" in str_each]
        
        if not any(excludes):
            chapters[each.text] = domain + "chapter/" + each.get("href")

    book_chaps = {book_name : chapters}

    with open("douay/chapters/" + normalize_filename(book_name) + ".json", "w+") as wh:
        json.dump(book_chaps, wh)
    return book_chaps

for each in ["new_test.json", "old_test.json"]:
    with open(each, "r+") as rh:
        books = json.load(rh)

    for name, link in books.items():
        link = link[0]
        idd = link[1]
        get_chapters(name, link, idd)

def join_chapter_text(chapter_content_list):
    chapter_content_list = [each for each in chapter_content_list if each != "\n"]
    chap_text = {}
    tracker = 0

    for each in chapter_content_list:
        each = str(each)
        if re.search(r'\/x\/d\?b=drb', each):
            tracker += 1
            verse = re.search(r'\[(\d+)\]', each).group(1)
            chap_text[tracker] = ""
        else:
            chap_text[tracker] = chap_text[tracker] + each
    return chap_text

def get_chapter_text(location):
    """Get text for single chapter"""
    chapter_output_dictionary = {}
    chapter_contents_list = []

    soup = Ripper(location, parser="html5lib").soup
    text = soup.find("table", class_="texttable")

    for each in text.find_all("p"):
        attributes = each.attrs
        if attributes:
            if "desc" in attributes["class"]:
                pass
            elif "note" in attributes["class"]:
                pass
        else:
            new_cont = each.contents
            chapter_contents_list.extend(new_cont)
    return join_chapter_text(chapter_contents_list)

def get_book_text(book_file_name):
    with open(book_file_name, "r+") as rh:
        book = json.load(rh)
    chapter_text = {}

    for name, chapters_dictionary in book.items():
        
        for chap, location in chapters_dictionary.items():
            chapter_text[name + "-" + chap] = get_chapter_text(location)
            norm = normalize_filename("{}_{}.json".format(name, chap))
            outfile = "douay/verses/{}.json".format(norm)
        
            with open(outfile, "w+") as wh:
                json.dump(chapter_text, wh)
            chapter_text = {}

all_books = glob.glob("douay/chapters/*.json")

for each in all_books:
    get_book_text(each)

