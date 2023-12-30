import networkx as nx
from selenium import webdriver
from selenium.webdriver.common.by import By
import time, re

specialNodes = 0

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
        graph.add_node(courseCode, attr={'specialNode' : False, 'courseTitle' : courseTitle, 'prereqs' : prereqs, 'offeringTerms' : offeringTerms, 'field' : field})
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
    prereqString = re.sub(r'\[', r'(', prereqString)
    prereqString = re.sub(r'\]', r')', prereqString)
    prereqString = re.sub(r'\(', r'( ', prereqString)
    prereqString = re.sub(r'\)', r' )', prereqString)
    prereqString = re.sub(r',', r' ,', prereqString)
    prereqString = re.sub('/', ' or ', prereqString)
    print('PREREQS:', prereqString)
    if prereqString.startswith('Exlusion') or prereqString == '':
        return
    words = prereqString.split(' ')
    res = analysePrereq(graph, words, None, node[0])
    # graph.nodes[res[0]]['attr'] = node[1]['attr']
    # graph.remove_node(node[0])
    # nx.relabel_nodes(graph, {res[0] : node[0]})


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
                # print(match.group())
                lastNode = codeMatch.group()
                lastEdge = (codeMatch.group(), node)
                graph.add_edge(*lastEdge)
            elif numberMatch and (graph.has_node('COMP' + numberMatch.group())) and 'COMP' + numberMatch.group() != node:
                lastNode = 'COMP' + numberMatch.group()
                lastEdge = ('COMP' + numberMatch.group(), node)
                graph.add_edge(*lastEdge)
            elif graph.has_node(word) and word != node:
                lastNode = word
                lastEdge = (word, node)
                graph.add_edge(*lastEdge)
        i += 1
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
    
    # specialNodes to be added to graph after we have looped through existing nodes
    # tuple with unique ID and then actual label
    # specialNodes = []

    # Create a copy so we don't iterate over newly created special nodes
    for node in list(graph.nodes(data=True)).copy():
        createEdges(graph, node)
    
    # for node in specialNodes:
    #     graph.add_edge(node[0], attr={'label': node[1]})
    
    return graph