# coding: utf-8

# In[ ]:

# all the function and librarys I need to run
from urllib.request import urlopen
import re
from bs4 import BeautifulSoup
import csv
from collections import Counter

# In[ ]:

# I am trying to scrape the herb website and save the herb name, common name, as well as herb function into a dictionary
herbs_page = urlopen("http://www.herbaltransitions.com/BotanCom.html")
soup = BeautifulSoup(herbs_page, 'html.parser')
# get all herb links on the herbs_page
herb_links = soup.body.p.find_all('a')[2:]

# In[ ]:

# since I have all the links, I am going to parse the website again for each link
cout = 1
# this is just a placeholder, later I am going to add the herb details in the list
result = []
# Loop through the list of links I built
for herb_link in herb_links:
    # try/except funtion here to make sure we don't have a invalid link
    try:
        href = herb_link.get('href')
        if not href:
            continue
        ref = "http://www.herbaltransitions.com/" + href
        # Once again I'll use beautiful soup to process it the html of my links.
        herb_page = urlopen(ref)
        link_soup = BeautifulSoup(herb_page, 'html.parser')
        names = link_soup.head.title.string.split('-')

        # based on the html format, we are going to use re.search function to find name, common name, and use and get rid of those unneccsary info
        m = re.search('(.+?) \((.+?)\)', str(names[-1]))
        if not m:
            continue
        # name
        # From looking at the HTML source (using View Source in our browser)
        # we see that name is the first one of m group
        name = m.group(1)
        # use is in the body part of the link
        use = link_soup.body.p
        # because each herb might have few uses,we need to seperate them using ',' and as well as get rid of the a), b), c), etc. in for future use
        m = re.search('<b>Use:</b>(.+?)<br/>', str(use))
        # if/else function here to identify the use section
        if not m:
            m = re.search('<b>Use: </b>(.+?)<br/>', str(use))
        if not m:
            m = re.search('<b>Use</b>:(.+?)<br/>', str(use))
        if m:
            use = m.group(1).split(',')
            use = ' '.join(list(map(lambda x: x[5:], use)))
        else:
            use = ''
        # append everything into the result list
        result.append([name.strip(' '), use.strip(' ').rstrip('.')])
    except Exception as err:
        print(herb_link)
        print(err)

with open('herbs.csv', 'w') as outcsv:
    writer = csv.DictWriter(outcsv, fieldnames = ["Name", "Use"])
    writer.writeheader()
    writer.writerows({'Name': row[0], 'Use': row[1]} for row in result)

# I want to create dictionary with key=name, value=use
mydict = {t[0]:t[1:] for t in result}
print(mydict)

# print menu, you can look up a herb, add an herb, delete an herb, look up an herb, and print their funtions
def print_menu():
    print('1. Print Herbs')
    print('2. Add a herb')
    print('3. Remove a herb')
    print('4. Lookup a herb')
    print('5. count')
    print('6. Quit')
    print()
# setup counter to store menu choice
menu_choice = 0
# display your menu
print_menu()
# as long as the menu choice isn't "quit" get user options
while menu_choice != 6:
    # get menu choice from user
    menu_choice = int(input("Type in a number (1-6): "))
    # view current entries
    if menu_choice == 1:
        print("All Herbs:")
        for x, y in mydict.items():
            print("Name: {} \tFunction: {} \n".format(x, y))
    # add an herb
    elif menu_choice == 2:
        print("Add herb")
        name = input("Name: ")
        function = input("Function: ")
        mydict[name] = function
    # remove an herb
    elif menu_choice == 3:
        # what do i do here?
        print("Remove herb")
        # get the name of the herb they want to delete
        input_name = input("Name: ")
        # check if input name in dictionary
        if input_name in mydict:
            del mydict[input_name]
    # look up use
    elif menu_choice == 4:
        print("Lookup herb")
        name = input("Name or use: ")
        for key, value in mydict.items():
            if (name == key):
                print(mydict[name])
            if (name == value):
                print([item[0] for item in mydict.items() if item[1] == name])
            else:
                print("Herb not found.")

    # count how many herbs with each function
    elif menu_choice == 5:
        print("count herb")
        use = input("use: ")
        c = Counter(result)
        # print(c)
        print("there are {} herbs with {}".format(c[use], use))
    else:
        print_menu()