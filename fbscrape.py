from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from shutil import which
from bs4 import BeautifulSoup
from lxml import etree
import time
import json
import os
import argparse


class GetUserData():
    def __init__(self, username, password, name):
        self.username = username
        self.password = password
        self.name = name

    def fblogin(self, headless=True):
        user_details = {}
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument("--disable-extensions")

        prefs = {"profile.default_content_setting_values.notifications" : 2}
        chrome_options.add_experimental_option("prefs",prefs)

        chrome_path = which("chromedriver_linux64/chromedriver")

        global driver
        driver = webdriver.Chrome(executable_path=chrome_path \
            ,options=chrome_options)
        driver.get("https://www.facebook.com")

        search_email = driver.find_element(By.ID, "email")
        search_email.clear()

        search_email.send_keys(self.username)

        search_pass = driver.find_element(By.ID, "pass")
        search_pass.clear()

        search_pass.send_keys(self.password)
        search_pass.send_keys(Keys.ENTER)


        search_btn = driver.find_element(By.XPATH, "//label[contains(@class, 'lzcic4wl gs1a9yip br7hx15l h2jyy9rg n3ddgdk9 owxd89k7 rq0escxv j83agx80 a5nuqjux l9j0dhe7 k4urcfbm kbf60n1y b3i9ofy5')]")
        search_btn.click() 

        search_inp = driver.find_element(By.XPATH, "//input[contains(@class, 'oajrlxb2 f1sip0of hidtqoto e70eycc3 hzawbc8m ijkhr0an pvl4gcvk sgqwj88q b1f16np4 hdh3q7d8 dwo3fsh8 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz br7hx15l h2jyy9rg n3ddgdk9 owxd89k7 rq0escxv oo9gr5id mg4g778l buofh1pr g5gj957u ihxqhq3m jq4qci2q hpfvmrgz lzcic4wl l9j0dhe7 iu8raji3 l60d2q6s dflh9lhu hwnh5xvq scb9dxdr qypqp5cg aj8hi1zk kd8v7px7 r4fl40cc m07ooulj mzan44vs')]")
        search_inp.clear()
        search_inp.send_keys(self.name)
        search_inp.send_keys(Keys.ENTER)

        try:

            enter_people = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.LINK_TEXT, "People"))
            )

            enter_people.click()
            driver.implicitly_wait(10)
            print("clicked people button")
            print(driver.current_url)
            time.sleep(3)
            search_page = driver.page_source
            soup = BeautifulSoup(search_page, 'html.parser')
            search_page = etree.HTML(str(soup))
            name = search_page.xpath("(//a[@class = 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gpro0wi8 oo9gr5id lrazzd5p dkezsu63']/span)[1]/text()")[0]
            print(name)
            user_details['name'] = name
            try:   
                enter_person = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.LINK_TEXT, name))
                )
                enter_person.click()
            except:
                enter_person = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/h3[1]/span[1]/span[1]/span[1]/a[1]/span[1]"))
                )
                enter_person.click()

            print("clicked on first person")

            print(driver.current_url)
            time.sleep(1)
            user_url = driver.current_url
            user_details['url'] = user_url
            user_page = driver.page_source
            user_soup = BeautifulSoup(user_page, 'html.parser')
            user_page = etree.HTML(str(user_soup))
            last_10_posts = user_page.xpath("(//a[@class='oajrlxb2 gs1a9yip g5ia77u1 mtkw9kbi tlpljxtp qensuy8j ppp5ayq2 goun2846 ccm00jje s44p3ltw mk2mc5f4 rt8b4zig n8ej3o3l agehan2d sk4xxmp2 rq0escxv nhd2j8a9 mg4g778l pfnyh3mw p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x tgvbjcpo hpfvmrgz jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso l9j0dhe7 i1ao9s8h esuyzwwr f1sip0of du4w35lb n00je7tq arfg74bv qs9ysxi8 k77z8yql btwxx1t3 abiwlrkh p8dawk7l lzcic4wl a8c37x1j tm8avpzi'])[position()<11]/@href")
            user_details['last_10_posts'] = last_10_posts
            try:
                locked = user_page.xpath("//div[@class='a5q79mjw a6zn2dtd oo9gr5id']/text()")
            except:
                print('profile is not locked')
            print(locked)

            if len(locked) !=0:
                return print('Account is Locked')



            try:
                about_person = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.LINK_TEXT, 'About'))
                )
                about_person.click()
            except:
                driver.get(str(driver.current_url)+'/about')

            time.sleep(1)
            print(driver.current_url)
            about_page = driver.page_source
            about_soup = BeautifulSoup(about_page, 'html.parser')
            about_page = etree.HTML(str(about_soup))
            missing_details = about_page.xpath("//span[@class='d2edcug0 hpfvmrgz qv66sw1b c1et5uql b0tq1wua a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d9wwppkn hrzyx87i jq4qci2q a3bd9o3v ekzkrbhg m9osqain']/text()")
            print(missing_details)
            available_details = about_page.xpath("//span[@class='d2edcug0 hpfvmrgz qv66sw1b c1et5uql b0tq1wua a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d9wwppkn hrzyx87i jq4qci2q a3bd9o3v b1v8xokw oo9gr5id']/text()")
            print(available_details)
            available_details_full = about_page.xpath("//span[contains(@class, 'd2edcug0 hpfvmrgz qv66sw1b c1et5uql b0tq1wua a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d9wwppkn hrzyx87i jq4qci2q a3bd9o3v b1v8xokw ')]/a/span/span/text()")
            print(available_details_full)
            user_details['intro'] = available_details_full

            try:
                about_person = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.LINK_TEXT, 'Work and education'))
                )
                about_person.click()
            except:
                driver.get(str(user_url)+'/about_work_and_education')

            time.sleep(1)
            print(driver.current_url)
            wae_page = driver.page_source
            wae_soup = BeautifulSoup(wae_page, 'html.parser')
            wae_page = etree.HTML(str(wae_soup))
            work_unavaliable = wae_page.xpath("//span[@class ='d2edcug0 hpfvmrgz qv66sw1b c1et5uql b0tq1wua a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d9wwppkn hrzyx87i jq4qci2q a3bd9o3v ekzkrbhg m9osqain']/text()")
            print(work_unavaliable)
            university = wae_page.xpath("//span[@class = 'd2edcug0 hpfvmrgz qv66sw1b c1et5uql b0tq1wua a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d9wwppkn hrzyx87i jq4qci2q a3bd9o3v b1v8xokw oo9gr5id']/text()")
            print(university)
            university_name = wae_page.xpath("//a[@class='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gpro0wi8 oo9gr5id lrazzd5p']/span/span/text()")
            print(university_name)
            user_details['education'] = university_name

            try:
                about_person = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.LINK_TEXT, 'Places lived'))
                )
                about_person.click()
            except:
                driver.get(str(user_url)+'/about_places')

            time.sleep(1)
            print(driver.current_url)
            places_page = driver.page_source
            places_soup = BeautifulSoup(places_page, 'html.parser')
            places_page = etree.HTML(str(places_soup))
            places = places_page.xpath("//a[@class='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gpro0wi8 oo9gr5id lrazzd5p']/span/span/text()")
            print(places)
            user_details['places'] = places
            try:
                about_person = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.LINK_TEXT, 'Contact and basic info'))
                )
                about_person.click()
            except:
                driver.get(str(user_url)+'/about_contact_and_basic_info')

            time.sleep(1)
            print(driver.current_url)
            contact_page = driver.page_source
            contact_soup = BeautifulSoup(contact_page, 'html.parser')
            contact_page = etree.HTML(str(contact_soup))
            contact_info_ua = contact_page.xpath("//span[@class='d2edcug0 hpfvmrgz qv66sw1b c1et5uql b0tq1wua a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d9wwppkn hrzyx87i jq4qci2q a3bd9o3v ekzkrbhg m9osqain']/text()")
            print(contact_info_ua)
            contact_info= contact_page.xpath("//span[@class='d2edcug0 hpfvmrgz qv66sw1b c1et5uql b0tq1wua a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d9wwppkn hrzyx87i jq4qci2q a3bd9o3v b1v8xokw oo9gr5id hzawbc8m']/text()")
            print(contact_info)
            user_details['info'] = contact_info
            contact_info_cat = contact_page.xpath("//span[@class='d2edcug0 hpfvmrgz qv66sw1b c1et5uql b0tq1wua sq6gx45u a3bd9o3v b1v8xokw m9osqain hzawbc8m']/div/text()")
            print(contact_info_cat)


            try:
                about_person = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.LINK_TEXT, 'Life events'))
                )
                about_person.click()
            except:
                driver.get(str(user_url)+'/about_life_events')

            time.sleep(1)
            print(driver.current_url)
            life_page = driver.page_source
            life_soup = BeautifulSoup(life_page, 'html.parser')
            life_page = etree.HTML(str(life_soup))
            years = life_page.xpath("//span[@class='d2edcug0 hpfvmrgz qv66sw1b c1et5uql b0tq1wua a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d9wwppkn hrzyx87i jq4qci2q a3bd9o3v ekzkrbhg oo9gr5id']/text()")
            print(years)
            events = life_page.xpath("//span[@class='d2edcug0 hpfvmrgz qv66sw1b c1et5uql b0tq1wua a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d9wwppkn hrzyx87i jq4qci2q a3bd9o3v b1v8xokw oo9gr5id hzawbc8m']/text()")
            print(events)
            user_details['events'] = events

            try:
                photos_person = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.LINK_TEXT, 'Photos'))
                )
                photos_person.click()
            except:
                driver.get(str(user_url)+'/photos')

            time.sleep(1)
            print(driver.current_url)
            photos_page = driver.page_source
            photos_soup = BeautifulSoup(photos_page, 'html.parser')
            photos_page = etree.HTML(str(photos_soup))
            photos_url = photos_page.xpath("//a[@class='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8 a8c37x1j datstx6m l9j0dhe7 k4urcfbm']/@href")
            print(photos_url)
            user_details['photos_url']=photos_url

            
        except:
            driver.quit()
        
        driver.close()
        user_details_json = json.dumps(user_details)
        return user_details_json, user_page

    def save_json(self, headless=True):
        json_file = GetUserData(self.username, self.password, self.name).fblogin(headless)[0]
        try:
            os.mkdir("jsonFiles")
        except:
            pass
        try:
            with open(f"jsonFiles/{self.name}.json", "w") as outfile:
                outfile.write(json_file)
        except:
            print("json file already exists")

        print(f"json file saved at location {os.getcwd()}")

    def save_page_source(self):
        page_source = GetUserData(self.username, self.password, self.name).fblogin()[1]
        try:
            os.mkdir("pagesources")
        except:
            pass
        try:
            with open(f"pagesources/{self.name}.html", "w") as text_file:
                text_file.write(page_source)
        except:
            print("page source file already exists")

        print(f"page source file saved at location {os.getcwd()}")



if __name__ == "__main__":
    username = input("Enter Facebook username")
    password = input("enter Facebook password")
    search_name = input("enter author name")
    search = GetUserData(username, password, search_name)
    json_file = search.save_json()

