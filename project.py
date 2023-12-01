# %%
import time
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
# %%
year = 2020
url = f"https://pageviews.wmcloud.org/topviews/?project=en.wikipedia.org&platform=all-access&date={year}&excludes="
driver = webdriver.Edge()
driver.get(url)
# %%
time.sleep(10) 
# %%
# Get the base XPath for the entries
base_xpath = '//*[@id="topview-entry-'
# %%
entry_list = []
# %%
# Loop through the range of numbers
for entry_number in range(2, 25):
    # Construct the full XPath for the current entry
    entry_xpath = f'{base_xpath}{entry_number}"]'

    if not driver.find_elements(By.XPATH, entry_xpath):
        continue

    # Find the entry element
    entry_info = driver.find_element(By.XPATH, entry_xpath)
    # Extract information for the current entry
    list_data = entry_info.text.split('\n')
    numbers = list_data[2].split()
    list_data.pop(2)
    list_data.extend(numbers)

    # Get the date information
    date_info = driver.find_element(By.ID, 'date-input')
    date_data = date_info.get_attribute('value')

    # Get the label href
    label_href = entry_info.find_element(By.XPATH, './/td[2]/div/a').get_attribute('href')

    # Create a dictionary with the extracted information
    entry_dict = {
        "Year": date_data,
        "Rank": list_data[0],
        "Label": list_data[1],
        "Edits": list_data[2],
        "Editors": list_data[3],
        "Views": list_data[4],
        "Mobile Percentage": list_data[5],
        "Link": label_href
    }
    
    entry_list.append(entry_dict)

    time.sleep(3)
# Append the dictionary to the DataFrame
df = pd.DataFrame(entry_list)

df
# %%