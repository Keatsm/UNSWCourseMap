import networkx as nx
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

orNodes = 0

def initNode(graph, url):
    try:
        print(url)
        driver = webdriver.Chrome()
        driver.get(url)
        courseCode = driver.find_element(By.XPATH, "//div[@class='css-u09y4s-Box-Flex-StyledFlex e3iudi70']/div[1]/h5").text
        courseTitle = driver.find_element(By.XPATH, "//h2").text
        try:
            offeringTerms = driver.find_element(By.XPATH, "//div[child::h4[text()='Offering Terms']]/div/div").text
        except:
            offeringTerms = ''
        try:
            field = driver.find_element(By.XPATH, "//div[child::h4[text()='Field of Education']]/div/div").text
        except:
            field = ''
        # Not all courses have prerequisites; if the conditions box is not found, assume empty
        try:
            prereqs = driver.find_element(By.XPATH, "//div[@id='ConditionsforEnrolment']/div[2]/div").text
        except:
            prereqs = ''
        print(courseCode, courseTitle, prereqs, offeringTerms, field)
        graph.add_node(courseCode, attr={'courseTitle' : courseTitle, 'prereqs' : prereqs, 'offeringTerms' : offeringTerms, 'field' : field})
        driver.close()
    except Exception as e:
        print(str(e))
        # If we get blocked, try again after 5 seconds
        driver.close()
        time.sleep(5)
        initNode(graph, url)
        
def createEdges(graph, node, orNodes):
    prereqString = node['attr']['prereqs']
    if prereqString.startswith('Exlusion') or prereqString == '':
        return

def createGraph(urls):
    graph = nx.Graph()
    for url in urls:
        initNode(graph, url)
    # orNodes to be added to graph after we have looped through existing nodes
    orNodes = []
    
    return graph