import random
from urllib.request import urlopen
from bs4 import BeautifulSoup as Soup
import re

#Function to generate the numbers for euromillions (from 1 - 50)
def generateNumbers():
    result = []
    count = 5
    while count != 0:
        randomnumber = random.randint(1,50)

        if randomnumber not in result:
            result.append(randomnumber)
            count -= 1

    return result

#Function to generate the stars for euromillions (from 1 - 12)
def generateStars():
    result = []
    count = 2

    while count != 0:
        randomstar = random.randint(1,12)

        if randomstar not in result:
            result.append(randomstar)
            count -= 1

    return result

#Quicksort

def sort(list):
    less = []
    equal = []
    greater = []
    if len(list) > 1:
        pivot = list[0]
        for x in list:
            if x < pivot:
                less.append(x)
            if x > pivot:
                greater.append(x)
            if x == pivot:
                equal.append(x)
        return sort(less) + equal + sort(greater)
    else:
        return list

#Function to generate sets of numbers based on number of bets (each bet is a combo of 5 numbers and 2 stars)
def playGame(apuestas):
    aps = int(apuestas)
    while aps != 0:
        print("Numbers:", *sort(generateNumbers()), "Stars:", *sort(generateStars()))
        aps -= 1

#public variables to store the winning combo of the last draw
winningnumbs = []
winningstars = []

#Function to scrape the spanish euromillons website to get latest result
def getdata():
    # open website and get data
    url = urlopen("https://www.loteriasyapuestas.es/es/euromillones")
    rawdata = url.read()
    url.close()

    # parse the data with BeautifulSoup
    parsed = Soup(rawdata, 'html.parser')

    for line in parsed.findAll('div', "cuerpoRegionIzq"):
        # Find the numbers
        nums = re.findall('<li> (.*?)</li>', str(line))
        for lines in nums:
            winningnumbs.append(int(lines))
    for line in parsed.findAll('div', "cuerpoRegionDerecha"):
        # Find the stars
        nums = re.findall('<li> (.*?)</li>', str(line))
        for lines in nums:
            winningstars.append(int(lines))

# check how many numbers of the inputed combo are in the winning combo
def check(numbers, stars):
    getdata()
    combnumb = 0
    combstar = 0
    for number in numbers:
        if number in winningnumbs:
            combnumb += 1
    for star in stars:
        if star in winningstars:
            combstar += 1
    print("You got: " + str(combnumb) + " numbers, and " + str(combstar) + " stars")
    print("The winning combination is:", *winningnumbs, "Stars:", *winningstars)

play = input("Want to generate numbers or check? (1 | 2): ")

if play == "1":
    apuestas = input("Number of bets? ")
    playGame(apuestas)
if play == "2":
    numbers = []
    stars = []
    numbercount: int = 1
    starcount = 1
    while numbercount != 6:
        userinput = input("Number " + str(numbercount) + ": ")
        try:
            if int(userinput) not in range(1,50):
                print("Please input a number between 1 and 50")
            if int(userinput) in numbers:
                print("Number already chosen. Numbers in Euromillions can't be repeated in the same bet.")
            else:
                numbers.append(int(userinput))
                numbercount += 1
        except ValueError:
            print("Please input a number")

    while starcount != 3:

        userinput = input("Star " + str(starcount) + ": ")

        try:
            if int(userinput) not in range(1,12):
                print("Please input a number between 1 and 12")
            if int(userinput) in stars:
                print("Number already chosen. Stars in Euromillions can't be repeated in the same bet.")
            else:
                stars.append(int(userinput))
                starcount += 1
        except ValueError:
            print("Please input a number")

    print("Your combo is:", *numbers, "Stars:", *stars)
    check(numbers, stars)
else:
    print("Invalid input, please write 1 or 2")