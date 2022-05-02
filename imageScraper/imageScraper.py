from bs4 import BeautifulSoup
import sys
import requests
import re
import os
import urllib.request

def validateInput():
    if len(sys.argv) < 2:
        print("Not enough arguments provided")
        return False

    return True

def searchGalleryPage(page, baseUrl, parentDir):
    first = False

    for aTag in page.find_all('a'):
        if not first:
            first = True
            continue

        link = str(aTag.get('href'))

        if link.startswith(".", 0, 1):
            # concatenate link
            link = link.replace("./", "")
            link = parentDir + link

            # GET
            r = requests.get(link)

            subPage = BeautifulSoup(r.text, 'html.parser')

            # find cloud type
            bTags = subPage.find_all('b')
            # search for type ..(type)</b>.. or ..(type</b>..
            cat = re.search('\(.+\\n*\</b\>', str(bTags))
            if cat is None:
                print(bTags)
            cat = cat.group(0)
            # filter ( and ) and </b> and \n
            cat = cat.replace('(', '')
            cat = cat.replace(')', '')
            cat = cat.replace('</b>', '')
            cat = cat.replace('\n', '')
            # check for multiple categorys
            #catList = cat.split(',')
            #if len(catList) > 1:
            #    print('multiple cat')

            # check if category has a directory
            if not os.path.isdir(cat):
                os.mkdir(cat)
                print('Created new directory: %s' % cat)

            #print(cat)

            # find images
            images = subPage.find_all('img')
            # every second img
            # or filter like .jpg
            for img in images:
                if (img.has_attr('src') and str(img['src']).endswith('.jpg') and
                str(img['src']).startswith('..', 0, 2)):
                    # concatenate image link
                    img_link = baseUrl + str(img['src']).replace('../', '')
                    # get image title
                    img_title = img_link.split('/')[-1]
                    # save image on hard drive
                    urllib.request.urlretrieve(img_link, cat + '/' + img_title)
                    print('Saved %s in %s' % (img_title, cat))

def soupDocument(link):
    # get html document
    r = requests.get(link)

    # return souped html document
    return BeautifulSoup(r.text, 'html.parser')

def main():
    if not validateInput():
        return

    inputLink = sys.argv[1]

    soup = soupDocument(inputLink)
    # engineer better
    baseUrl = re.search('http://.+.de/', inputLink).group(0)
    parentDir = re.search('http://.+/', inputLink).group(0)

    # first gallery page
    searchGalleryPage(soup, baseUrl, parentDir)

    # scrape other gallerys
    selects = soup.find('select')
    options = selects.find_all('option')

    # loop through gallerys
    for option in options:
        rawLink = option.get('value')
        if rawLink is not None:
            rawLink = rawLink.replace('./', '')
            # filter verzeichnis
            if rawLink.startswith('l'):
                continue
            # concatenate gallery link
            galleryLink = parentDir + rawLink
            # output link
            print(galleryLink)

            soup = soupDocument(galleryLink)
            searchGalleryPage(soup, baseUrl, parentDir)


main()
