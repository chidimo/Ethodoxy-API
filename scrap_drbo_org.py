
# coding: utf-8

# http://drbo.org/

# In[ ]:

import re
import os
import json
import glob
from django.template.defaultfilters import slugify
from pywebber import Ripper


# In[ ]:

domain = "http://drbo.org/"
BASE_DIR = os.path.dirname(os.path.abspath("__file__"))
save_path = os.path.join(BASE_DIR, "drbo_org_scrap")
data_store = os.path.join(BASE_DIR, "drbo_data")
chapter_store = os.path.join(BASE_DIR, "drbo_data", "chapters")
verse_store = os.path.join(BASE_DIR, "drbo_data", "verses")
challoner_store = os.path.join(BASE_DIR, "drbo_data", "challoner")


# In[ ]:

def normalize_filename(file_name):
    return "_".join([each.lower() for each in re.split(r"[\, *, \/]", file_name) if each != ''])

# home = Ripper(domain, save_path="D:\git\ethodoxy\drbo_org_scrap")
# home_links = list(home.links())

# In[ ]:

def get_all_books_page_links(raw_page_rip):
    """Get page links for each book"""
    nt = {}
    ot = {}
    OTIDS = []
    soup = raw_page_rip.soup
    if not os.path.exists(data_store):
        os.mkdir(data_store)
    
    nt_soup = soup.find("td", class_="NT")
    ot1 = soup.find("td", class_="OT1")
    ot2 = soup.find("td", class_="OT2")
    
    for each in nt_soup.find_all("a", href=True):
        if 'class="b"' in str(each):
            href = each.get("href")
            name = each.text

            idd = re.search(r'\d{5}', href).group(0)
            nt[name] = [domain + href, idd]
            
    with open(os.path.join(data_store, "new_test.json"), "w+") as wh:
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
    with open(os.path.join(data_store, "old_test.json"), "w+") as wh:
        json.dump(rev_old, wh)


# In[ ]:

def export_chapter_links_to_json(book_name, book_link, idd):
    """Get all chapters and write to json"""
    chapters = {"01" : book_link}
    home = Ripper(book_link, save_path=save_path)
    
    if not os.path.exists(chapter_store):
        os.mkdir(chapter_store)
    
    for each in home.raw_links:
        str_each = str(each)
        excludes = ["next" in str_each, "previous" in str_each, "chapter" in str_each, "statcounter" in str_each,
                    "/x/" in str_each, "DRBO.ORG" in str_each, "theologica" in str_each]
        
        if not any(excludes):
            chapters[each.text] = domain + "chapter/" + each.get("href")

    book_chaps = {book_name : chapters}
    
    book_save_name = "{}.json".format(os.path.join(chapter_store, normalize_filename(book_name)))

    with open(book_save_name, "w+") as wh:
        json.dump(book_chaps, wh)
    return book_chaps


# In[ ]:




# In[ ]:

def join_chapter_text(chapter_content_list):
    """Join paragraphs of a chapter"""
    cleaned_chapter_content_list = [each for each in chapter_content_list if each != "\n"]
    chap_text = {0 : ""}
    tracker = 0

    for each in chapter_content_list:
        each = str(each)
        if re.search(r'\/x\/d\?b=drb', each):
            tracker += 1
            verse = re.search(r'\[(\d+)\]', each).group(1)
            chap_text[tracker] = ""
        else:
            chap_text[tracker] = chap_text[tracker] + each.strip()
    
    chap_text.pop(0, None)
    return chap_text

def get_chapter_text(location):
    """Get text content for a single chapter"""
    chapter_output_dictionary = {}
    chapter_contents_list = []

    soup = Ripper(location, parser="html5lib", save_path=save_path).soup
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

def get_all_text_for_book(book_file_name):
    """Get text for a single book, all chapters"""
    if not os.path.exists(verse_store):
        os.mkdir(verse_store)
    with open(book_file_name, "r+") as rh:
        book = json.load(rh)
    chapter_text = {}

    for name, chapters_dictionary in book.items():
        for chap, location in chapters_dictionary.items():
            outfile = "{}/{}_{}.json".format(verse_store, normalize_filename(name), chap)
            
            if os.path.exists(outfile):
                continue
            else:
                chapter_text[name + "__" + chap] = get_chapter_text(location)
                with open(outfile, "w+") as wh:
                    json.dump(chapter_text, wh)
                chapter_text = {}


# In[ ]:

def export_commentary_text_as_dictionary(commentary_parts_list):
    """Make a dictionary from each commentary text.
    Input is a list consisting of a 3 items.
    [verse, underlined text from bible, commentary text]
    """
    verse_string = str(commentary_parts_list[0])
    header_string = str(commentary_parts_list[1])
        
    verse = re.search(r"\[(\d+)\]", verse_string).group(1)
    header = re.search(r'\<u\>\s*"(.+)"\s*\<\/u\>', header_string).group(1)

    commentary_text = commentary_parts_list[2].replace(": ", "")
    key = verse + "__" + header
    
    return key, commentary_text.strip()

def get_commentary_for_chapter(location):
    """Get commentary text for single chapter"""
    chapter_commentary_dictionary = {}

    soup = Ripper(location, parser="html5lib", save_path=save_path).soup
    text = soup.find("table", class_="texttable")

    for each in text.find_all("p"):
        attributes = each.attrs
        if attributes:
            if "desc" in attributes["class"]:
                pass
            elif "note" in attributes["class"]:
                new_content = each.contents
                verse_header, text = export_commentary_text_as_dictionary(new_content)
                chapter_commentary_dictionary[verse_header] = text
        else:
            continue
    return chapter_commentary_dictionary

def get_commentary_for_book_chapters(book_file_name):
    """Get commentary for all chapters of all books"""
    if not os.path.exists(challoner_store):
        os.mkdir(challoner_store)
    with open(book_file_name, "r+") as rh:
        book = json.load(rh)
    chapter_text = {}

    for name, chapters_dictionary in book.items():
        
        for chap, location in chapters_dictionary.items():
            norm = normalize_filename("{}_{}".format(name, chap))
            
            outfile = "{}/{}.json".format(challoner_store, norm)
            
            if os.path.exists(outfile):
                continue
            else:
                chapter_text[name + "__" + chap] = get_commentary_for_chapter(location)
                with open(outfile, "w+") as wh:
                    json.dump(chapter_text, wh)
                chapter_text = {}


# ## Gateway

# get_all_books_page_links(Ripper(url=domain, save_path=save_path))

# for each in [os.path.join(data_store, "new_test.json"), os.path.join(data_store, "old_test.json")]:
#     with open(each, "r+") as rh:
#         books = json.load(rh)
#     for name, link in books.items():
#         link = link[0]
#         idd = link[1]
#         export_chapter_links_to_json(name, link, idd)

# all_books = glob.glob("{}/*.json".format(chapter_store))

# for each in all_books:
#     get_all_text_for_book(each)

# for each in all_books:
#     get_commentary_for_book_chapters(each)

# In[ ]:



