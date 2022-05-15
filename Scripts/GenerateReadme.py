# -*- coding: utf-8 -*-

import sys
from os import listdir
from os.path import isfile, join

def get_file_path_list(dir_path):
    onlyfiles = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
    return onlyfiles


def generate_title_from_file(dir_path, file_name):
    date = ""
    title = ""
    url = ""

    # with open(dir_path + "/" + file_name, 'r', encoding="utf-8") as f:
    with open(dir_path + "/" + file_name, 'r') as f:
        content_lines = f.readlines()
        for line in content_lines:
            if line.startswith("draft: true"):
                return None
            if line.startswith("title: "):
                title = line[7:].strip().strip("\"")
            elif line.startswith("date: "):
                date = line[6:].strip()[:10]
            url = "https://github.com/lightjiao/lightjiao.github.io/blob/master/Blogs/" + file_name

    title_template = "- {0}: [{1}]({2})".format(date, title, url)
    return title_template


README_Template = """# Lightjiao的博客  
👨‍💻电子游戏开发者  🎮电子游戏爱好者  🏊‍♂️游泳爱好者"

## [关于我](https://github.com/lightjiao/lightjiao.github.io/blob/master/Blogs/000.About-me.md)  

"""

if __name__ == '__main__':
    str_list = []
    dir_path = sys.argv[1]

    title_list = []
    for file_name in get_file_path_list(dir_path):
        title = generate_title_from_file(dir_path, file_name)
        if title == None:
            continue
        if (title.find("000.") != -1):
            continue
        title_list.append(title)
    title_list.reverse()

   
    old_year_str = ""
    for title in title_list:
        the_year = title[2:6]
        if the_year != old_year_str:
            README_Template += "## " + the_year + "\n"
            old_year_str = the_year
        README_Template += title + "\n"

    print(README_Template)