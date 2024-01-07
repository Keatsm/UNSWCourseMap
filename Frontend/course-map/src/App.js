import React, { useState, useEffect } from 'react';
import GraphVisualization from './components/GraphVisualisation.js';
import axios from 'axios';

const App = () => {
  // Fetch graph data from Neo4j or mock data
  const [graphData, setGraphData] = useState({nodes: [], edges: []});

  // Fetch graph data from Neo4j or API on component mount
  useEffect(() => {
      axios.get('http://127.0.0.1:5000/graph')
      .then(response => {
        let newData = {
          nodes: [],
          edges: []
        }
        for (let node of response.data.nodes) {
          newData.nodes.push({id: node.id, label: node.properties.label})
        }
        for (let edge of response.data.relationships) {
          newData.edges.push({from: edge.startNode, to: edge.endNode})
        }
        console.log(newData)
        setGraphData(newData)
      })
      .catch(error => {
        // Handle error
        console.error('Error fetching data:', error);
      });
  }, []);

  return (
    <div>
      <h1>UNSW COMP Course Map</h1>
      <GraphVisualization graphData={graphData} />
    </div>
  );
};

export default App;
