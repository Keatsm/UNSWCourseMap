from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

# Navigate to UNSW course booklet
driver.get('https://www.handbook.unsw.edu.au/search')

# Press 'Course'
button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, 'react-tabs-6')))
button.click()

# Press 'Subject Area'
button = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, "//div[@style='overflow: hidden;']/div[6]/div[1]")))
button.click()


search_bar = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//div[@class='css-e2gxlx-SAccordionContentContainer e1450wuy10']/div/div[@class='css-e3eej2-SearchInputContainer eanr10p1']/input[1]"))
)

# Input text into the search bar
search_bar.send_keys('COMP')

button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//ul[@class='css-zia84r-StyledOptionsList e15kvt300']/li[2]")))
button.click()



# Close the browser
driver.close()