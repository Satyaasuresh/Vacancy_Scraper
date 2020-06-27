from selenium import webdriver
import selenium
import pandas as pd
from bs4 import BeautifulSoup
import xlrd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(executable_path='C:\webdrivers\chromedriver.exe')

#Get soc_list file from local machine
path = r'C:\Users\Satyaa\Desktop\soc_list.xlsx'
inputWorkbook = xlrd.open_workbook(path)
inputWorksheet = inputWorkbook.sheet_by_index(0)



# Set up data frame
df = pd.DataFrame(columns=["Title", "Location", "Company", "Salary"])

#Reading Excel rows 487-767, where the SOC Jobs lie.
for i in range(500,750):
    #Read in cells values from SOC List, input them into the Indeed URL to search
    name = inputWorksheet.cell_value(i+1,1)
    soc_number = str(inputWorksheet.cell_value(i+1,0))
    #Approximate number of scraped listings desired per SOC job.
    for i in range(0,100,10):
        driver.get('https://www.indeed.com/jobs?q=%s&l=' % name)
        jobs = []
        driver.implicitly_wait(4)

        for job in driver.find_elements_by_class_name('result'):

            soup = BeautifulSoup(job.get_attribute('innerHTML'), 'html.parser')

            try:
                 title = soup.find("a", class_="jobtitle").text.replace("\n", "").strip()

            except:
                 title = 'None'

            try:
                 location = soup.find(class_="location").text
            except:
                 location = 'None'

            try:
                 company = soup.find(class_="company").text.replace("\n", "").strip()
            except:
                 company = 'None'

            try:
                 salary = soup.find(class_="salary").text.replace("\n", "").strip()
            except:
                 salary = 'None'

            sum_div = job.find_element_by_xpath('./div[3]')

            try:
                driver.execute_script("arguments[0].click();", sum_div)

            except:
                if driver.find_elements_by_class_name('popover-x-button-close'):
                    close_button = driver.find_elements_by_class_name('popover-x-button-close')[0]
                    close_button.click()
                    sum_div.click()
                else:
                    break
            #Attempt to get job description. However, only yields a sentence.
            job_desc = soup.find(class_="summary").text.replace("\n", "").strip()


            df = df.append({'SOC Number': soc_number, 'SOC Title': name, 'Listing Title': title, 'Location': location, "Company": company, "Salary": salary,
                'Description/Requirements': job_desc}, ignore_index=True)

            print("Got these many results:", df.shape)
            df.to_csv("ai.csv", index=False)

#Place results into new spreadsheet
