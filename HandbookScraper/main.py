from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up the browser (in this case, Chrome)
driver = webdriver.Chrome('path_to_chromedriver')

# Navigate to UNSW course booklet
driver.get('https://www.handbook.unsw.edu.au/search')

# Find and click the button that loads content
button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, 'react-tabs-12')))
button.click()



# Wait for content to load (if necessary)
# Scrape data after the content is loaded
# Example: data = driver.find_element_by_xpath('xpath_to_desired_data').text

# Close the browser
driver.quit()