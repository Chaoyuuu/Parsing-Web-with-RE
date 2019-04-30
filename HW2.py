import urllib.request
import re
import sys
import numpy as np
import matplotlib.pyplot as plt

author = input("input Author:")
x = author.split()
# print(x)
# input author name
# author = "Chao Wu"
# x = author.split()
name = "\""
for i in x:
    name = name + i + "+"

name = name + "\""

# pattern
find_total = "title is-clearfix\">[\s\S]*?</h1>"
find_warning = "<span class=\"is-warning\">author:"
pattern = "arxiv-result[\s\S]*?</li>"
find_authors = 'authors[\s\S]*?</p>'
find_author = '>' + author + '</a>'
find_submit = 'originally announced</span>[\s\S]*?\\n'

page = 0
count = 0
count_co = 0
aList = []
bList = []
find = 0

while (1):
    url = "https://arxiv.org/search/?query=" + name + "&searchtype=author&order=submitted_date&size=200&abstracts=show&start=" + str(page)
    content = urllib.request.urlopen(url)
    html_str = content.read().decode('utf-8')

    # if the end of page or not find
    result_warning = re.findall(find_warning, html_str)
    if result_warning:
        if page == 0:
            print("Sorry, your query for author: " + author + " produced no results.")
        else:
            find = 1
        break

    # find author
    result = re.findall(pattern, html_str)
    for i in result:
        # print(i)
        result_author = re.findall(find_author, i)
        # print(result_authors)
        if result_author:
            count = count + 1
            # print(result_authors)
            # find submitted time
            result_submit = re.findall(find_submit, i)
            tmp = result_submit[0].split("originally announced</span>")[1].split(".")[0].strip()
            year = tmp.split()
            aList.append(int(year[1]))
            # print(year[1])

            # find authors
            result_authors = re.findall(find_authors, i)
            tmp = result_authors[0].split(">")
            tmp.pop(0)
            tmp.pop(0)
            tmp.pop(0)
            for r in tmp[1::2]:
                r = r.split("</a")
                for m in r:
                    if m and m != author:  # get authors
                        bList.append(m)
                        count_co = count_co + 1
    page = page + 200

# print(count)
# print(len(aList))
# print(count_co)
bList = sorted(bList)
aList = sorted(aList)

#
if find == 1:
    # count co authors
    tmp = bList[0]
    num = 1
    for x in range(0, len(bList)):
        if x != len(bList)-1 and bList[x] == bList[x + 1]:
            num = num + 1
        elif x == len(bList)-1 and bList[x-1] != bList[x]:
            print("[ " + bList[x] + " ]: " + str(num) + " times")
        else:
            print("[ " + bList[x] + " ]: " + str(num) + " times")
            num = 1

    # show hist
    count_a = []
    no_repead = set(aList)
    no_repead = sorted(no_repead)

    # count the # of each year
    for y in range(aList[0], aList[len(aList)-1]+1):
        count_a.append(aList.count(y))

    # print(count_a)
    # print(no_repead)
    plt.bar(no_repead, count_a)

    plt.yticks(np.arange(0, max(count_a) + 1, 1))
    plt.xticks(np.arange(no_repead[0], max(no_repead)+1, 1))
    plt.title('Publications per year')
    plt.xlabel('Year')
    plt.ylabel('Publications')
    plt.show()


