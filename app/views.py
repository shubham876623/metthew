from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import View
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import  Options
from random import expovariate, seed
from random import random
from time import sleep, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys
import pandas as pd
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import logging
from loguru import logger
from app.models import FinalData
import csv
# Create your views here.


class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')


class CreateCSVFILE(View):
    def get(self, request):
        df = pd.read_excel("/home/hp/workspace/sanjeevupwork/matthew/master-address-list.xlsx")

        print(df)

        list_update = []

        for i in range(20000, 30000):
            address = df['Address'][i]
            list_update.append(address)

            city = df['City'][i]
            list_update.append(city)

            state = df['State'][i]
            list_update.append(state)

            zip_code = df['ZIP Code'][i]
            list_update.append(zip_code)

            country = df['Country'][i]
            list_update.append(country)

            print(list_update)
            c0=pd.Series(data=[list_update[0]])
            c1=pd.Series(data=[list_update[1]])
            c2=pd.Series(data=[list_update[2]])
            c3=pd.Series(data=[list_update[3]])     
            c4=pd.Series(data=[list_update[4]])     
            data = pd.concat([c0, c1, c2, c3, c4], axis=1)
            data_frame = pd.DataFrame(data)
            print(data_frame)
            data_frame.to_csv('dataforserver2.csv',index=False,mode='a',header=False, sep =',')
            list_update.clear()
        
        return HttpResponse("Created!!")


def getdata(request):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('start-maximized')
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    
    df = pd.read_excel("master-address-list.xlsx", engine='openpyxl')
    
    # total_records = int(df.shape[0])
    # print(f"Total Records : {total_records}")

    list_of_fields = ["fire department","police department",
                "gun range","whole foods near",
                "dollar store near","pawn shop near",
                "homeless shleter near","bike path near","army recruiter near","chinese restaurant near",
                "equestrian path near","golf course near","country club near","starbucks near"]

    
    address_list=[]
    name_list=[]
    id_list=[]


    for i in range (98927, 103927+1):
        try:
            if str(df['City'][i])!="nan":
                address=str(df["Address"][i])+ " " + str(df["City"][i])
            else:
                address=str(df["Address"][i])
            addresss=address
            id_list.append(i)
        
            if not FinalData.objects.filter(address=address).exists():
                address_list.append(addresss)
                # print("ZIP Code => ", df["ZIP Code"][i])
                zip = df["ZIP Code"][i]
                driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
    
                driver.get('https://www.google.co.in/maps/@30.7396608,76.7328256,13z')
                driver.delete_all_cookies()            
                WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="searchboxinput"]'))).send_keys(addresss)
                driver.find_element_by_xpath('//*[@id="searchboxinput"]').send_keys(Keys.ENTER)
                time.sleep(5)

                try:
                    WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,'/html/body/jsl/div[3]/div[10]/div[8]/div/div[1]/div/div/div[4]/div[1]/div/button'))).click()
                except Exception as e:
                    pass
                try:
                    #click on the direction button
                    driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[4]/div[1]/button').click()
                except Exception as e:
                    pass  
                
                # Button click for the change direction.
                WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="omnibox-directions"]/div/div[3]/div[2]/button/div'))).click()

                list_output=[]

                # Search keyword 
                for i in list_of_fields:
                                                                            
                    # Clear input field for the search next keyword.
                    driver.find_element_by_xpath('//*[@id="sb_ifc52"]/input').clear()            
                    print(i+" "+addresss)
                    WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="sb_ifc52"]/input'))).send_keys(i + " " +  addresss)

                    driver.find_element_by_xpath('//*[@id="sb_ifc52"]/input').send_keys(Keys.ENTER)
                    time.sleep(7)
                    # res = driver.page_source
                    try:
                        a = driver.find_element_by_xpath('/html/body/jsl/div[3]/div[10]/div[8]/div/div[1]/div/div/div[5]/div[1]/div/div[1]/div[1]/div[2]')
                        print("a 1=> ", a.text)
                    except Exception as e:
                        pass

                    try:
                        a = driver.find_element_by_xpath('//*[@id="section-directions-trip-0"]/div/div[3]/div[1]/div[2]')
                        print("a 2=> ", a.text)
                    except Exception as e:
                        pass

                    try:
                        a = driver.find_element_by_xpath('//*[@id="section-directions-trip-0"]/div/div[1]/div[1]/div[2]/div')
                    except Exception as e:
                        pass            
                    if a:
                        try:
                            list_output.append(a.text)
                            print(a.text)
                        except:
                            
                            list_output.append("NA")
                    else:
                        list_output.append("NA")
        
                # save to database
                saveRecords(addresss, list_output, zip)
                
                logger.success("Record Created Done!")
                print("Save to database => ", addresss, list_output, zip)

                list_output.clear()
                id_list.clear()
                name_list.clear()
                address_list.clear()
                driver.close()

        except Exception as e:
            print("Error :", e)
            logger.warning(e)
            pass
    # else:
    #     print("not get")
    #     id_list.clear()
    #     name_list.clear()
    #     address_list.clear()
    #     logger.warning("Already exist")


    return redirect('home')


def saveRecords(addresss, list_output, zip):
    """ save records in database """
    if not FinalData.objects.filter(address=addresss).exists():
        FinalData.objects.create(
            address=addresss, zip_code=zip, \
            fire_depart=list_output[0], police_depart=list_output[1], \
            gun_range=list_output[2], food_near=list_output[3], \
            dollar_stor_near=list_output[4], pawn_shop=list_output[5],\
            homeless_shleter=list_output[6], bike_path=list_output[7], \
            army_recruiter=list_output[8], chinese_restaurant=list_output[9],\
            equestrian_path=list_output[10], golf_course=list_output[11],\
            country_club=list_output[12], starbucks=list_output[13])

    return True


def get_csv(request):
    """
    function to get csv
    """
    
    response = HttpResponse(
        content_type='csv',
        headers={'Content-Disposition': 'attachment; filename="export.csv"'},
    )
    obj = FinalData.objects.all()

    for s in obj:
        # check duplicates
        duplicates = FinalData.objects.filter(address=s.address).order_by('id')[1:]
        # if check duplcate and delete record
        if len(duplicates) > 0:
          duplicates[0].delete()
    
        writer = csv.writer(response)
        writer.writerow([
            s.address, s.zip_code, s.fire_depart, 
            s.police_depart, s.gun_range, s.food_near, 
            s.dollar_stor_near, s.pawn_shop, s.homeless_shleter, 
            s.bike_path, s.army_recruiter, s.chinese_restaurant, 
            s.equestrian_path, s.golf_course, s.country_club, s.starbucks])

    return response