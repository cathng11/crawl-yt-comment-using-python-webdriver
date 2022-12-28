from selenium import webdriver
import time
import csv
from selenium.webdriver.common.keys import Keys
import unidecode
import json
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def write_csv(filename, value):
    with open(filename, 'a', newline='', encoding='utf-8-sig') as csvfile:
        csvwriter = csv.writer(csvfile,delimiter=';')
        row = [value]
        # print(row)
        csvwriter.writerow(row)

def crawl():
    with open("./toxiccmt_en.csv", 'w', newline='', encoding='utf-8-sig') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Content'])
    with open("./toxiccmt_vn.csv", 'w', newline='', encoding='utf-8-sig') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Content'])
    with open("./toxiccmt_encode.csv", 'w', newline='', encoding='utf-8-sig') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Content'])

    driver = webdriver.Chrome(executable_path='E:/Downloads/ChromeDriver/chromedriver.exe')
    linkyoutube = [
        'https://www.youtube.com/watch?v=CqukoUj_4_s', #tục tiễu,
        'https://www.youtube.com/watch?v=VmSYymGcQOY', #tục tiễu
        'https://www.youtube.com/watch?v=O9g5n6KhKCk', #tích cực
        'https://www.youtube.com/watch?v=DSyJECeqxMA', #tiêu cực
        'https://www.youtube.com/watch?v=b1xnk59mMrU', #tiêu cực
        'https://www.youtube.com/watch?v=9wik86v_38I', #tiêu cực
        'https://www.youtube.com/watch?v=8uebEBO98V0', #tiêu cực
    ]
    driver.get('https://www.youtube.com/watch?v=IviYsgJXG5k')
    time.sleep(3)
    previous_height = driver.execute_script(
        'return document.documentElement.scrollHeight')
    new_height = 0
    step_scroll = 5
    old_height = 0

    while True:
        for i in range(1, step_scroll + 1):
            print(
                f"previous: {previous_height}, old_height: {old_height}, steps: {(previous_height - old_height) / step_scroll}")
            print(((previous_height - old_height) / step_scroll) * i + old_height)
            print("\n")
            driver.execute_script('window.scrollTo(0, arguments[0]);', ((
                previous_height - old_height) / step_scroll) * i + old_height)
            time.sleep(1)

        time.sleep(3)

        new_height = driver.execute_script(
            'return document.documentElement.scrollHeight')
        old_height = previous_height
        if previous_height == new_height:
            break
        previous_height = new_height
    print('end')

    # ele=driver.find_element_by_tag_name('body')
    # while True:
    #     ele.send_keys(Keys.PAGE_DOWN)
    #     print(Keys.PAGE_DOWN)
    #     time.sleep(1)

    time.sleep(3)
    element = driver.find_elements_by_id('content-text')
    for el in element:
        write_csv("./toxiccmt_en.csv",unidecode.unidecode(el.text))
        write_csv("./toxiccmt_vn.csv",el.text)
        write_csv("./toxiccmt_encode.csv",el.text.encode("utf-8"))
    print('exported')
    driver.close()

def csvToJson():
    csvFilePath = r'./comment_data.csv'
    jsonFilePath = r'./test.json'
    data = []
    with open(csvFilePath,'r', encoding='utf-8-sig')as csvFile:
        csvReader = csv.DictReader(csvFile)
        for rows in csvReader:
            content = rows['Content']
            negative = rows['Negative']
            data.append({
                'Content': content, 
                'Negative': negative
                })
    with open(jsonFilePath, 'w', encoding='utf-8-sig') as jsonFile:
        jsonFile.write(json.dumps(data, ensure_ascii=False))
    print("Done")

def txtToCsv():
    f = open('data.txt', encoding='utf-8-sig', errors='ignore')
    data = json.load(f)
    content = ''
    dataConvert = data
    newdata = []
    for i in range(0, len(data["Sheet1"])):
        try:

            content = data["Sheet1"][i]["Content"]
            regex = re.compile(r'[\n\r\t]')
            content = regex.sub("", content)
            dataConvert["Sheet1"][i]["Content"]=content
            newdata.append(dataConvert["Sheet1"][i])
        except:
            continue

    with open('comment_data.json', 'w',encoding='utf-8-sig', errors='ignore') as outfile:
        json.dump(newdata, outfile, ensure_ascii=False)
    # df = pd.read_json (r'comment_data.json',encoding='utf-8-sig')
    df=pd.DataFrame(newdata)
    df.to_csv (r'comment_data.csv', index = None,encoding='utf-8-sig')
    print('Done')

def plotChar(data):
    x_len = []
    for item in data:
        x_len.append(len(item['Content']))
    plt.hist(x_len, color='DarkGreen')
    plt.ylabel("Number of sentences")
    plt.xlabel("Number of characters")
    plt.show()


def plotNegative(data):
    comments = []
    for item in data:
        comments.append(item['Negative'])
    plt.hist(comments, color='DarkBlue')
    plt.ylabel("Number of sentences")
    plt.xlabel("Label")
    plt.show()

crawl()
csvToJson()
txtToCsv()
file = open('./comment_data.json', encoding='utf-8-sig', errors='ignore')
data = json.load(file)
plotNegative(data)
plotChar(data)