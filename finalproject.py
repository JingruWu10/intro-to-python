# Final Project
#Objective:
#1. get all the herb information with name, as well as use function from a website a) try/except statement b) if/else statement c) write output to a file
#2. then save all the information into a dictionary. a) at least one dictionary
#3. Create menu options to add herb, delete herb, look up herb by use, look up use by herb, and count herb. a)a calculation on a list
#4. create a class to print histagram of each use with number of herbs a) function that takes two user arguments from command line b) class
#5. include docstrings telling us how to run your script
#6. comments on the purpose of the function as well as inputs and outputs

# all the resources and libraries I need to run
from urllib.request import urlopen
# this is the request library use to scrape html
from bs4 import BeautifulSoup
import re
# my page source involve regular expression therefore using this package
import csv
# this is the csv library use to write my output into csv file
from collections import Counter
# this is use for count function

mydict = {}
#create a class to print histagram of each use with number of herbs and involve two arguments from command line
class Histogram(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "There are %s herbs with %s use" % (self.x, self.y)


# scrape the herb website and save the herb name, common name, as well as herb function into a dictionary
herbs_page = urlopen("http://www.herbaltransitions.com/BotanCom.html")
soup = BeautifulSoup(herbs_page, 'html.parser')
# using Beautiful soup here to parse the url
# get all herb links on the herbs_page
herb_links = soup.body.p.find_all('a')[2:]

# show the output of all links
# since I have all the links, I am going to parse the website again for each link
count = 1
# this is just a placeholder, later I am going to add the herb details in the list
result = []

cnt = Counter()
lcount = 0
# Loop through the list of links I built
for herb_link in herb_links:
    # try/except funtion here to make sure we don't have a invalid link
    try:
        href = herb_link.get('href')
        if not href:
            continue
        ref = "http://www.herbaltransitions.com/" + href
        # Once again I'll use beautiful soup to process the html of my links.
        herb_page = urlopen(ref)
        link_soup = BeautifulSoup(herb_page, 'html.parser')
        names = link_soup.head.title.string.split('-')

        # based on the html format, we are going to use re.search function to find name, common name, use and get rid of unnecessary info
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
            use = list(map(lambda x: x[5:], use))
            for i in use:
                cnt[i.strip(' ').rstrip('.')] += 1
            use = ' '.join(use)
            # get rid of the (a),(b) """
        else:
            use = ''

        # append everything into the result list
        result.append([name.strip(' '),use.strip(' ').rstrip('.')])
    # some of the herbs have error links
    except Exception as err:
        print(herb_link)
        print(err)

# I want to write all info into a csv file
with open('herbs.csv', 'w') as outcsv:
    writer = csv.DictWriter(outcsv, fieldnames=["Name", "Use"])
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
        found_herb = []
        for key, value in mydict.items():
            if (name == key):
                found_herb.append(key)
            else:
                if value[0].find(name) != -1:
                    found_herb.append(key)
        if found_herb:
            print(found_herb)
        else:
            print("Herb not found.")

    # count how many herbs with each function
    elif menu_choice == 5:
        print("count herb")
        use = input("use: ")
        print("there are {} herbs with {}".format(cnt[use], use))
    else:
        print_menu()