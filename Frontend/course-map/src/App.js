import React, { useState, useEffect } from 'react';
import GraphVisualization from './components/GraphVisualisation.js';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css'

const colorList = [
  '#e8b2b2',
  '#cadfc2',
  '#e8d8c2',
  '#cdc0e6',
  '#b2c6e8',
  '#e3b2e8',
  '#4aaeff',
  '#804aff',
  '#ff4ae7',
  '#ff4a4a',
  '#ffb14a',
  '#4affb7',
  '#8cff4a',
  '#954aff'
];


const hexValue = {}

let i = 0

function cleanCourseField(courseField) {
  // Remove numbers at the beginning
  const withoutNumbers = courseField.replace(/^\d+\s*/, '');
  // Remove 'not elsewhere classified' from the end
  const withoutNEC = withoutNumbers.replace(/\s*not\selsewhere\sclassified*$/, '');

  return withoutNEC.trim();
}

const App = () => {
  // Fetch graph data from Neo4j or mock data
  const [graphData, setGraphData] = useState({nodes: [], edges: []});
  

  // Fetch graph data from Neo4j or API on component mount
  useEffect(() => {
      axios.get('unswcoursemap-production.up.railway.app/graph')
      .then(response => {
        let newData = {
          nodes: [],
          edges: []
        }
        for (let node of response.data.nodes) {
          if (node.properties.field !== undefined){
            let field = cleanCourseField(node.properties.field);
            if (!hexValue.hasOwnProperty(field)) {
              hexValue[field] = colorList[i]
              i += 1
            }
            node.properties.field = field
          }
          
          newData.nodes.push({id: node.id, label: node.properties.label, data: node.properties});
          
        }
        for (let edge of response.data.relationships) {
          newData.edges.push({from: edge.startNode, to: edge.endNode});
        }
        setGraphData(newData);
      })
      .catch(error => {
        // Handle error
        console.error('Error fetching data:', error);
      });
  }, []);

  return (
    <div style={{
      display : 'flex',
      flexDirection : 'column',
      alignItems : 'center'
    }}>
      <h1>UNSW COMP Course Map</h1>
      <GraphVisualization 
        graphData={graphData} 
        titleHeight={document.querySelector('h1') == null ? 10 : document.querySelector('h1').offsetHeight}
        hexMap={hexValue}
      />
    </div>
  );
};

export default App;
