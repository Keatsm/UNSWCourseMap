import networkx as nx
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time, re, requests

specialNodes = 0

def getCapacity(timetableLink):
    response = requests.get(timetableLink)
    htmlContent = response.content
    print(timetableLink)
    soup = BeautifulSoup(htmlContent, 'html.parser')
    tds = soup.find_all('td', class_='formBody')
    total = 0
    for td in tds:
        if not td.find('td', class_='data', text='Undergraduate'):
            continue
        subTds = td.find_all('td', class_='formBody')
        for i, subTd in enumerate(subTds):
            if i == 0:
                continue
            if not subTd.find('tr', class_='rowLowlight') and not subTd.find('tr', class_='rowHighlight'):
                continue
            try:
                enrollments = subTd.find_all('table')[2]
                rows =  enrollments.find_all('tr', class_='rowHighlight') + enrollments.find_all('tr', class_='rowLowlight')
                for row in rows:
                    activity = row.find_all('td')[0].find('a').text
                    if (not re.search('[lL]ecture', activity) and not re.search('[eE]nrolment', activity)) or re.search('Sequence [^1]+ of [0-9]', activity):
                        continue
                    match = re.search('([0-9]+)/([0-9]+)', row.find_all('td', class_='data')[5].text)
                    total += int(match.group(1))
            except:
                continue
                
    return total
                
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
        try:
            capacity = getCapacity(driver.find_element(By.XPATH, "//div[child::h4[text()='Timetable']]/div/div/a").get_attribute("href"))
        except:
            capacity = 0
        # Not all courses have prerequisites; if the conditions box is not found, assume empty
        try:
            prereqs = re.sub('Pre-?requisites?:', '', driver.find_element(By.XPATH, "//div[@id='ConditionsforEnrolment']/div[2]/div").text)
            print(prereqs)
        except:
            prereqs = ''
        print(courseCode, courseTitle, prereqs, offeringTerms, field)
        graph.add_node(courseCode, attr={'specialNode' : False, 'courseTitle' : courseTitle, 'prereqs' : prereqs, 'offeringTerms' : offeringTerms, 'field' : field, 'url': url, 'capacity' : capacity})
        driver.close()
    except Exception as e:
        print(str(e))
        # If we get blocked, try again after 5 seconds
        driver.close()
        time.sleep(5)
        initNode(graph, url)



# node -> the current node we are adding edges to
# At the top level this is the node for the course
# Go down a level for every parentheses
# Go down a level for every or. This is harder than parentheses as we need to scan forward?
# The different seperators are 'OR', ',' and 'AND'
# Don't create the OR if there ends up being only one valud link into it (same for parenthesis)
def createEdges(graph, node):
    global lastNode, lastEdge
    lastNode = None
    lastEdge = None
    prereqString = node[1]['attr']['prereqs']
    
    # Clean up the string a bunch to make parsing easier
    prereqString = re.sub(r'\[', r'(', prereqString)
    prereqString = re.sub(r'\]', r')', prereqString)
    prereqString = re.sub(r'\(', r'( ', prereqString)
    prereqString = re.sub(r'\)', r' )', prereqString)
    prereqString = re.sub(r',', r' ,', prereqString)
    prereqString = re.sub('/', ' or ', prereqString)
    
    if prereqString.startswith('Exclusion') or prereqString == '':
        return
    words = prereqString.split(' ')
    res = analysePrereq(graph, words, None, node[0])
    # graph.nodes[res[0]]['attr'] = node[1]['attr']
    # graph.remove_node(node[0])
    # nx.relabel_nodes(graph, {res[0] : node[0]})

# Variables needed for 'or' nodes as we need to be able to add them into the or (which would precede the last node)
# and delete the original edge that was created for it
lastNode = None
lastEdge = None
def analysePrereq(graph, words, label, node=None):
    global specialNodes, lastNode, lastEdge
    if node == None:
        graph.add_node(label + str(specialNodes), attr={'specialNode' : True, 'label': label})
        node = label + str(specialNodes)
        specialNodes += 1
    if label == 'or':
        if lastNode:
            words = [lastNode] + words
            graph.remove_edge(*lastEdge)
            lastNode = None
            lastEdge = None
    print(node, words)
    i = 0
    while i < len(words):
        word = words[i]
        if word == '(':
            res = analysePrereq(graph, words[i + 1:], 'group')
            i += res[1]
            if res[0] is not None:
                lastNode = res[0]
                lastEdge = (res[0], node)
                graph.add_edge(*lastEdge)
        elif word.lower() == 'or' and label != 'or':
            res = analysePrereq(graph, words[i + 1:], 'or')
            i += res[1]
            if res[0] is not None:
                lastNode = res[0]
                lastEdge = (res[0], node)
                graph.add_edge(*lastEdge)
        elif label is not None and word == ')':
            if label == 'or':
                i -= 1
            break
        elif label == 'or' and (word.lower() == 'and' or word == ','):
            break
        else:
            codeMatch = re.search(r'(?:COMP|MATH|SENG)[0-9]{4}', word)
            numberMatch = re.search(r'[0-9]{4}', word)
            if (codeMatch and (graph.has_node(codeMatch.group()))) and codeMatch.group() != node:
                lastNode = codeMatch.group()
                lastEdge = (codeMatch.group(), node)
                graph.add_edge(*lastEdge)
            # Edge case where only the number (not the full code) is given
            elif numberMatch and (graph.has_node('COMP' + numberMatch.group())) and 'COMP' + numberMatch.group() != node:
                lastNode = 'COMP' + numberMatch.group()
                lastEdge = ('COMP' + numberMatch.group(), node)
                graph.add_edge(*lastEdge)
            # This is for the case where we have added in a previous group node (for example) into the list of words
            # for an or node and this wouldn't be matched using the above regex pattern
            elif graph.has_node(word) and word != node:
                lastNode = word
                lastEdge = (word, node)
                graph.add_edge(*lastEdge)
        i += 1
    # Need to check if we should collapse a group/or node (eg if such node only has one indegree)
    # In that situation, it may as well just link that one node directly to the parent
    if graph.nodes[node]['attr']['specialNode'] == True:
        if graph.in_degree(node) == 0:
            print(f'Deleting {node}')
            graph.remove_node(node)
            node = None
            
        elif graph.in_degree(node) == 1:
            prev = node
            node = list(graph.predecessors(node))[0]
            graph.remove_node(prev)
            print(f'Collapsing {prev} into {node}')
    if node is not None:
        print(f'Returning {node} with preds: {list(graph.predecessors(node))}')
    return (node, i + 1 if label != 'or' else i) 

def createGraph(urls):
    graph = nx.DiGraph()
    for url in urls:
        initNode(graph, url)

    # Create a copy so we don't iterate over newly created special nodes
    for node in list(graph.nodes(data=True)).copy():
        createEdges(graph, node)

    
    return graph