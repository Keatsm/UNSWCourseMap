import networkx as nx
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def initNode(graph, url):
    try:
        print(url)
        driver = webdriver.Chrome()
        driver.get(url)
        courseCode = driver.find_element(By.XPATH, "//div[@class='css-u09y4s-Box-Flex-StyledFlex e3iudi70']/div[1]/h5").text
        courseTitle = driver.find_element(By.XPATH, "//h2").text
        # Not all courses have prerequisites; if the conditions box is not found, assume empty
        try:
            prereqs = driver.find_element(By.XPATH, "//div[@id='ConditionsforEnrolment']/div[2]/div").text
        except:
            prereqs = ''
        print(courseCode, courseTitle, prereqs)
        graph.add_node(courseCode)
        driver.close()
    except:
        # If we get blocked, try again after 5 seconds
        time.sleep(5)
        initNode(graph, url)

def createGraph(urls):
    graph = nx.Graph()
    for url in urls:
        initNode(graph, url)
    
    return graph