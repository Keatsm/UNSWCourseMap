from createGraph import createGraph
import matplotlib.pyplot as plt
import networkx as nx

urls = [
    'https://www.handbook.unsw.edu.au/undergraduate/courses/2024/COMP1511?year=2024',
    'https://www.handbook.unsw.edu.au/undergraduate/courses/2024/COMP1521?year=2024',
    'https://www.handbook.unsw.edu.au/undergraduate/courses/2024/COMP1531?year=2024'
]

nx.draw(createGraph(urls), with_labels=True, font_weight='bold')
plt.show()