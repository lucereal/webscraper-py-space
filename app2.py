from logging import PlaceHolder
import os, time, sys
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get('OPENAI_API_KEY')
espn_key = os.environ.get('ESPN_KEY')

import re
from playwright.sync_api import Page, expect, TimeoutError 
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
    pwd = ""
    url = "https://www.espn.com/fantasy/"
    statsUrl = "https://www.espn.com/nfl/stats/player"
    
    page.goto(statsUrl)
    try:
        #user to select the option from the drop down 
        #page.get_by_label('Choose a color').select_option('blue')

        x = page.inner_html('.ResponsiveTable')
        
        soup = BeautifulSoup(x, "html.parser")
        tables = soup.findChildren('table')
        playerTable = tables[0]
        statsTable = tables[1]
        
        players = playerTable.findChildren(['tr'])
        
        # foo = players[1].get('data-idx')
        # print(foo)
        player_dict = {}
        # - get players from first table
        for player in players[1:]:
            pIndex = player.get('data-idx')
            pd = player.findChildren('td')
            pRank = pd[0].text
            pName = pd[1].findChildren('a')[0].text
            pTeam = pd[1].findChildren('span')[0].text
            player_dict[pIndex] = [pRank,pName,pTeam]
       
        
        # - get stats for each player from second table
        stats = statsTable.findChildren('tr')
        for stat in stats[1:]:          
            sIndex = stat.get('data-idx')          
            sdi = [i.text for i in stat.findChildren('td')]
            for sdix in sdi:
                player_dict[sIndex].append(sdix)

        
            
            #data-idx="0"
        # player1Data = players[1].findChildren(['td'])
        # player1Rank = player1Data[0].text
        # player1Name = player1Data[1].findChildren(['a'])[0].text
        # player1Team = player1Data[1].findChildren(['span'])[0].text
        # print(player1Rank)
        # print(player1Name)
        # print(player1Team)
    
        
    except Exception as error:
        print("An exception occurred:", error) # An exception occurred: division by zero
        
    # Keep the browser open for a few seconds to observe the result.
    # You can adjust this or remove it based on your needs.
    page.wait_for_timeout(5000)

    # Close the browser
    browser.close()
    
    
    

with sync_playwright() as playwright:
    run(playwright)

#url = "https://www.espn.com/fantasy/"
#select login then enter credentials
# login_button = page.wait_for_selector("text=Log In", timeout=10000)
# if login_button:
#     login_button.click()
#     page.wait_for_timeout(2000)
#     frame = page.frame(name="oneid-iframe")
#     if frame:
#         frame.locator("#InputIdentityFlowValue").fill(user)
#         frame.locator("#BtnSubmit").click()
#         page.wait_for_timeout(1000)
#         frame.locator("#InputPassword").fill(pwd)
#         frame.locator("#BtnSubmit").click()
#     else:
#         print("Could not find email address form")

# else:
#     print("Login button not found.")

# expect(page.get_by_role("heading", name="Sign up")).to_be_visible()

# page.get_by_role("checkbox", name="Subscribe").check()