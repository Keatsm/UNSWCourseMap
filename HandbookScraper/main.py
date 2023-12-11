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

# Locate the subject area search bar
searchBar = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//div[@class='css-e2gxlx-SAccordionContentContainer e1450wuy10']/div/div[@class='css-e3eej2-SearchInputContainer eanr10p1']/input[1]"))
)

# Input text into the search bar
searchBar.send_keys('COMP')

# Click on COMP
button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[descendant::strong[text()='COMP']]")))
driver.execute_script("arguments[0].click();", button)



# Clear search field
button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@id='closeMiniSearch']")))
driver.execute_script("arguments[0].click();", button)

# Input SENG into the search bar
searchBar.send_keys('SENG')

# Click on SENG
button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[descendant::strong[text()='SENG']]")))
driver.execute_script("arguments[0].click();", button)

# Find the parent div for the search results
parentDiv = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//div[@id='search-results']")))

prevTitle = None


# Check if search has changed
def check_for_search_changes(_):
    global prevTitle, parentDiv
    try:
        parentDiv = driver.find_element(By.XPATH, "//div[@id='search-results']")
        title = parentDiv.find_element(By.XPATH, "//div[1]/a/span/span/span")
    except Exception:
        print(Exception)
        return False
    check = prevTitle != title.text
    print(prevTitle, title.text)
    prevTitle = title.text
    return check

# Wait for search results to update
WebDriverWait(driver, 30).until(check_for_search_changes)

morePages = True

# Repeat while there are more pages to go through
while morePages:
    # Find all child div elements of the parent div
    courses = parentDiv.find_elements(By.XPATH, "./div")

    # Loop through each child div element
    for course in courses:
        # Find the <a> tag within each child div
        a_tag = course.find_element(By.XPATH, ".//a")
        
        # Get the href attribute value of the <a> tag
        hrefValue = a_tag.get_attribute("href")
        
        # Print the href value
        print(hrefValue)
        
    # Check if the right arrow to change page exists (which implies that there are more pages)
    morePages = driver.find_element(By.XPATH, "//button[@aria-label='Go forward 1 page in results']").is_enabled()
    if morePages:
        rightArrow = driver.find_element(By.XPATH, "//i[text()='keyboard_arrow_right']")
        # Click arrow
        driver.execute_script("arguments[0].click();", rightArrow)
        # Wait for update
        WebDriverWait(driver, 30).until(check_for_search_changes)

# Courses that won't appear on this list that we want to include
manualCourses = []


# Close the browser
driver.close()