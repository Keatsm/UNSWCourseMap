from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--ignore-certificate-errors')
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

# Locate the subject area search bar
search_bar = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//div[@class='css-e2gxlx-SAccordionContentContainer e1450wuy10']/div/div[@class='css-e3eej2-SearchInputContainer eanr10p1']/input[1]"))
)

# Input text into the search bar
search_bar.send_keys('COMP')

# Click on COMP
button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[descendant::strong[text()='COMP']]")))
driver.execute_script("arguments[0].click();", button)

# Find the parent div for the search results
parent_div = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//div[@id='search-results']")))

# Set what the title is for the course that is initially at the search
prev_title = parent_div.find_element(By.XPATH, "//div[1]/a/span/span/span").text

# Check if search has changed
def check_for_search_changes(_):
    global prev_title, parent_div
    try:
        parent_div = driver.find_element(By.XPATH, "//div[@id='search-results']")
        title = parent_div.find_element(By.XPATH, "//div[1]/a/span/span/span")
    except Exception:
        print(Exception)
        return False
    check = prev_title != title.text
    print(prev_title, title.text)
    prev_title = title.text
    return check

# Wait for search results to update
WebDriverWait(driver, 30).until(check_for_search_changes)

morePages = True

# Repeat while there are more pages to go through
while morePages:
    # Find all child div elements of the parent div
    courses = parent_div.find_elements(By.XPATH, "./div")

    # Loop through each child div element
    for course in courses:
        # Find the <a> tag within each child div
        a_tag = course.find_element(By.XPATH, ".//a")
        
        # Get the href attribute value of the <a> tag
        href_value = a_tag.get_attribute("href")
        
        # Print the href value
        print(href_value)
        
    # Check if the right arrow to change page exists (which implies that there are more pages)
    morePages = len(driver.find_elements(By.XPATH, "//i[text()='keyboard_arrow_right']")) > 0
    if morePages:
        right_arrow = driver.find_element(By.XPATH, "//i[text()='keyboard_arrow_right']")
        # Click arrow
        driver.execute_script("arguments[0].click();", right_arrow)
        # Wait for update
        WebDriverWait(driver, 30).until(check_for_search_changes)

# Courses that won't appear on this list that we want to include
# Include SENG in the above search?
manual_courses = []


# Close the browser
driver.close()