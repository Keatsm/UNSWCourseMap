import React, { useEffect, useRef, useState } from 'react';
import { Network } from "vis-network/peer/esm/vis-network";
import { DataSet } from "vis-data/peer/esm/vis-data";
import NodeModal from './NodeModal.js';
import Spinner from 'react-bootstrap/Spinner';


const GraphVisualisation = ({ graphData, titleHeight }) => {
  const [selectedNode, setSelectedNode] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [loadingGraph, setLoadingGraph] = useState(true);

  const windowSize = useRef([window.innerWidth, window.innerHeight]);

  const handleClose = () => {
    setShowModal(false);
    setSelectedNode(null);
  };

  
  
  const container = useRef(null);
  useEffect(() => {
    const handleNodeClick = (event) => {
      const { nodes } = event;
      if (nodes.length === 1) {
        const clickedNode = graphData.nodes.find((node) => node.id === nodes[0]);
        if (!clickedNode.data.specialNode) {
          setSelectedNode(clickedNode);
          setShowModal(true);
        }
      }
    };
    const nodes = new DataSet(graphData.nodes);
    const edges = new DataSet(graphData.edges);
    const scaledNodes = graphData.nodes.map(node => ({
      ...node,
      font: {
        size: Math.max(15, Math.sqrt(Math.sqrt(node.data.capacity === undefined ? 100 : node.data.capacity)) * 5)
      }

    }));

    nodes.update(scaledNodes);
    const data = { nodes, edges };
    const options = {
      edges: {
        arrows: {
          to: {
            enabled: true
          }
        }
      },
      interaction: {
        // Enable node selection
        selectConnectedEdges: false,
      },
      physics: {
        barnesHut: {
            "gravitationalConstant": -10000,
            "centralGravity": 1,
            avoidOverlap: 0.1
        },
        minVelocity: 1,
        repulsion: {
          nodeDistance: 375
        },
        solver: 'repulsion'
      }
    };

    const network = new Network(container.current, data, options);
    network.on('click', handleNodeClick);
    network.on('afterDrawing', () => {if (graphData.nodes.length > 0) setLoadingGraph(false)});
    return () => {
      network.destroy(); // Clean up network on component unmount
    };
  }, [graphData]);

  return (
    <div style={{
      display : 'flex',
      flexDirection : 'column',
      alignItems : 'center',
      justifyContent : 'center',
      width: '100%'
    }}>
      {loadingGraph && 
      <Spinner animation="border" role="status">
        <span className="visually-hidden">Loading...</span>
      </Spinner>}
      <div ref={container} style={{ width: '100%', height: windowSize.current[1] - titleHeight}} />
      <NodeModal showModal={showModal} handleClose={handleClose} node={selectedNode} />
    </div>
  );
};

export default GraphVisualisation;
