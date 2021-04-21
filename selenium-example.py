from selenium import webdriver
import time
import pandas as pd

search_query = 'https://www.indeed.com/q-data-scientist-jobs.html'
driver = webdriver.Chrome()
job_details=[]

driver.get(search_query)
time.sleep(5)
job_list = driver.find_elements_by_xpath("//div[@data-tn-component='organicJob']")

for each_job in job_list:
    # Getting job info
    job_title = each_job.find_elements_by_xpath(".//h2[@class='title']/a")[0]
    job_company = each_job.find_elements_by_xpath(".//span[@class='company']")[0]
    job_location = each_job.find_elements_by_xpath(".//span[@class='location accessible-contrast-color-location']")[0]
    job_summary = each_job.find_elements_by_xpath(".//div[@class='summary']")[0]
    job_publish_date = each_job.find_elements_by_xpath(".//span[@class='date ']")[0]
    # Saving job info 
    job_info = [job_title.text, job_company.text, job_location.text, job_summary.text, job_publish_date.text]
    # Saving into job_details
    job_details.append(job_info)
driver.quit()

job_details_df = pd.DataFrame(job_details)
job_details_df.columns = ['title', 'company', 'location', 'summary', 'publish_date']
job_details_df.to_csv('job_details.csv', index=False)