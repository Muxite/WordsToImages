# by Muk
# updated on 2022/12/25 Merry Christmas!
# make sure to update the xpaths along with changing the chrome driver version
# this is an update to "wordsToPictures" which I made a video about
from selenium import webdriver
from selenium.webdriver import ActionChains
import time
browser = webdriver.Chrome("D:\Google Drive\Code\Python\chromedriver 108.exe")


words = []
images = []


def process_input():
    global words
    user_input = str(input("Input your sentence to be converted into pictures: "))
    words = sentence_to_words(user_input)
    search_for_words()


def sentence_to_words(inputted_sentence):
    word_list = list(inputted_sentence.split())  # split the long string into a list of words

    # replace every "_" with a space
    for i in range(0, len(word_list)):
        word_list[i] = word_list[i].replace("_", " ")
        print(word_list[i])
        # at the same time append all the image spaces with None
        images.append(None)

    return word_list


search_bar_xpath = '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input'
thumbnail_jsname = 'Q4LuWd'

def search_for_words():
    for i in range(0, len(words)):
        browser.get("https://www.google.com/imghp?hl=EN")  # open google images search
        browser.maximize_window()
        search_bar = browser.find_element_by_xpath(search_bar_xpath)  # get the search bar
        search_bar.send_keys(words[i])  # input the word
        search_bar.send_keys(u'\ue007')  # press enter
        time.sleep(1)  # wait a bit for the page to load
        grab_image(i)  # download the first image found that meets requirements
        browser.close


def grab_image(number):
    searched_images = browser.find_elements_by_xpath('//img[contains(@src,"data:image")]')
    find_to_click(searched_images, number)


def find_to_click(found_images,  number):
    # width and height = 50 means it is not usable(it is a button)
    num_selector = 0
    while int(found_images[num_selector].get_attribute('height')) <= 50 and\
            int(found_images[num_selector].get_attribute('width')) <= 50 or \
            found_images[num_selector].get_attribute('jsname') != thumbnail_jsname:
        num_selector += 1
    action = ActionChains(browser)
    action.click(on_element=found_images[num_selector])  # click on the correct image//
    action.perform()

    find_to_use(number)  # search the page for the click result image


def find_to_use(number):
    # must be enlarged(selected), not a small rectangle
    # if less than requirements then do not take it either
    time.sleep(0.5)  # wait a bit for the page to load again
    element = browser.find_element_by_xpath('//img[contains(@jsaction, "load:XAeZkd;")]')
    # download the big image "num_to_use"
    with open(str(number) + '.png', 'wb') as images[number]:
        # downloads the image to project folder
        images[number].write(element.screenshot_as_png)


process_input()
