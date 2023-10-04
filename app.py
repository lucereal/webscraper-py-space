from logging import PlaceHolder
import os, time, sys
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get('OPENAI_API_KEY')

import re
from playwright.sync_api import Page, expect
from bs4 import BeautifulSoup
from langchain.llms import OpenAI 
import json 

MAX_MONTHS = 3
MAX_AVAILABILITY_COUNT = 3

# test code
#llm = OpenAI(openai_api_key=api_key, temperature=0.9)
#x = llm(prompt='What would be a good company name for a company that makes colorful socks?')
#print(x)

#TODO: move console logging to text

from playwright.sync_api import Playwright, sync_playwright, expect

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()


    # set a default for testing
    user = "lucerodavid1010@gmail.com"
    pwd = "Fluffy44$"
    url = "https://www.espn.com/fantasy/"

    page.goto(url)

    page.frame_locator("iframe").locator("div").filter(has_text=re.compile(r"^Email \*$")).click()
    page.frame_locator("iframe").get_by_label("Email *").fill(user)
    page.frame_locator("iframe").get_by_label("Password *").click()
    page.frame_locator("iframe").get_by_label("Password *").click()
    page.frame_locator("iframe").get_by_label("Password *").fill(pwd)
    page.frame_locator("iframe").get_by_role("button", name="LOG IN").click()
    #page.wait_for_load_state()
    page.frame_locator("iframe").get_by_text("Calendarkeyboard_arrow_right").click()
    page.frame_locator("iframe").get_by_role("link", name="Show Availability").click()

    page.frame_locator("iframe").get_by_role("combobox", name="Select Division * Bowman, John B. (02)").locator("div").nth(3).click()

    #page.frame_locator("iframe").locator("div").filter(has_text=re.compile(r"^Select Division \*$")).nth(2).click()

    page.frame_locator("iframe").get_by_placeholder("Search Division").fill(judge_text)
    page.frame_locator("iframe").get_by_placeholder("Search Division").press("Enter")

    page.frame_locator("iframe").get_by_text("Select the Category Type", exact=True).click()
    page.frame_locator("iframe").get_by_text("Motion Calendar").click()

    page.frame_locator("iframe").get_by_role("button", name="Month").click()
    page.frame_locator("iframe").get_by_role("button", name="Search").click()
    page.wait_for_load_state() 
    time.sleep(30)
            
    content = page.frame_locator("iframe").locator("div:nth-child(4) > div").first.inner_html()
    parent_content = page.frame_locator("iframe").locator("div:nth-child(4) > div").locator("..").locator("..").first.inner_html()
    
    monthCount = 0
    availabilityCount = 0
    availability = ""
    
    soup = BeautifulSoup(content, "html.parser")
    parent_soup = BeautifulSoup(parent_content, "html.parser")
    dates = list()

    while monthCount < MAX_MONTHS :

        monthDiv = parent_soup.find_all("div", {"class": "title font-weight-900"})
        dateParts = monthDiv[0].text.split()
        monthName = dateParts[0]
        year = dateParts[1]

        #print("Checking month " + str(monthCount) + "...")
        #availableCells = soup.find_all("div", string = "Available")
        availableSmalls = soup.find_all(lambda tag:tag.name=="small" and "Available" in tag.text)
        #print("Found " + str(len(availableCells)) + " available dates.")

        for small in availableSmalls :

            text = str(small.text)

            # parent div has a span that contains the day number
            parentDiv = small.previous_sibling()
            dateNumber = parentDiv[0].text 
            availability = monthName + " " + dateNumber + ", " + year + " " + text 

            if ("Available" in text) :
                dates.append(availability.replace("Available", "").strip())        
            
        if monthCount < MAX_MONTHS :
            #print("Loading the next month into the Soup.")
            page.frame_locator("iframe").get_by_role("button", name="Next").click()
            page.wait_for_load_state() 
            time.sleep(30)
            #content = page.content()
            content = page.frame_locator("iframe").locator("div:nth-child(4) > div").first.inner_html()
            parent_content = page.frame_locator("iframe").locator("div:nth-child(4) > div").locator("..").locator("..").first.inner_html()

            monthCount = monthCount + 1
            soup = BeautifulSoup(content, "html.parser")
            parent_soup = BeautifulSoup(parent_content, "html.parser")

    #print(dates)
    print(json.dumps(dates))
    #text_file = open("availability.txt", "w")
    #dtstring = ""
    #for dt in dates :
    #    dtstring = dtstring + dt + "\n"
        
    #n = text_file.write(dtstring)
    #text_file.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)


