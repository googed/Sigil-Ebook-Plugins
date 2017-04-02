#!/usr/bin/env python
#-*- coding: utf-8 -*-
import re
import sys
import sigil_bs4

# change ;:,?!. to full width
conversionDict={
                ";": "\N{FULLWIDTH SEMICOLON}",
                ":": "\N{FULLWIDTH COLON}",
                ",": "\N{FULLWIDTH COMMA}",
                "?": "\N{FULLWIDTH QUESTION MARK}",
                "!": "\N{FULLWIDTH EXCLAMATION MARK}",
                ".": "\N{FULLWIDTH FULL STOP}"
                }


def fixSelfCloseTags(html):
    return html.replace("></link>","/>").replace("<br></br>","<br/>").replace("></img>","/>")


def run(bk):
    print('start')
    for (id, href) in bk.text_iter():
        modified = False
        html = bk.readfile(id)
        # html = html.replace("<br/>","")
        soup = sigil_bs4.BeautifulSoup(html)
        ol = sigil_bs4.Tag(name="ol")
        ol['class'] = "sigil-footnote-content"
        # br tag  will cause p tag cannot be found
        for elem in soup.findAll(['p','div','span'], text=re.compile("["+"".join(conversionDict.keys())+"]")):
            modified = True
            text = elem.string
            for key in conversionDict:
                text = re.sub("["+key+"]", conversionDict[key], text)
            elem.string.replace_with(text)
            # print(elem.string)
        if modified:
            print("Modifed File -> ", id)
            bk.writefile(id, fixSelfCloseTags(str(soup)))
    return 0


def main():
    print("I reached main when I should not have\n")
    return -1

if __name__ == "__main__":
    sys.exit(main())