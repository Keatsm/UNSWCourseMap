from createGraph import createGraph
import matplotlib.pyplot as plt
import networkx as nx

urls = [
    'https://www.handbook.unsw.edu.au/undergraduate/courses/2024/COMP1511?year=2024',
    'https://www.handbook.unsw.edu.au/undergraduate/courses/2024/COMP1521?year=2024',
    'https://www.handbook.unsw.edu.au/undergraduate/courses/2024/COMP1531?year=2024',
    'https://www.handbook.unsw.edu.au/undergraduate/courses/2024/COMP9417/?year=2024',
    'https://www.handbook.unsw.edu.au/undergraduate/courses/2024/COMP3142/?year=2024',
    'https://www.handbook.unsw.edu.au/undergraduate/courses/2024/MATH1081/?year=2024',
    'https://www.handbook.unsw.edu.au/undergraduate/courses/2024/COMP2521/?year=2024',
    'https://www.handbook.unsw.edu.au/undergraduate/courses/2024/COMP2041/?year=2024',
    'https://www.handbook.unsw.edu.au/undergraduate/courses/2024/COMP2511/?year=2024'
]

urlsWeird = [
    'https://www.handbook.unsw.edu.au/undergraduate/courses/2024/COMP9491?year=2024',
    'https://www.handbook.unsw.edu.au/undergraduate/courses/2024/COMP3411?year=2024',
    'https://www.handbook.unsw.edu.au/undergraduate/courses/2024/COMP9444?year=2024',
    'https://www.handbook.unsw.edu.au/undergraduate/courses/2024/COMP9417?year=2024',
    'https://www.handbook.unsw.edu.au/undergraduate/courses/2024/COMP9517?year=2024',
    'https://www.handbook.unsw.edu.au/undergraduate/courses/2024/COMP4418?year=2024'
]

urlsSquare = [
    'https://www.handbook.unsw.edu.au/undergraduate/courses/2024/COMP9243?year=2024',
    'https://www.handbook.unsw.edu.au/undergraduate/courses/2024/COMP3331?year=2024',
    'https://www.handbook.unsw.edu.au/undergraduate/courses/2024/COMP3231?year=2024',
    'https://www.handbook.unsw.edu.au/undergraduate/courses/2024/COMP3891?year=2024'
]

properCollapse = [
    'https://www.handbook.unsw.edu.au/undergraduate/courses/2024/COMP3151?year=2024'
]

nx.draw(createGraph(urlsWeird), with_labels=True, font_weight='bold')
plt.show()