import React, { useEffect, useRef } from 'react';
import { Network } from "vis-network/peer/esm/vis-network";
import { DataSet } from "vis-data/peer/esm/vis-data"

const GraphVisualisation = ({ graphData }) => {
  const networkRef = useRef(null);

  useEffect(() => {
    const nodes = new DataSet(graphData.nodes);
    const edges = new DataSet(graphData.edges);

    const container = networkRef.current;
    const data = { nodes, edges };
    const options = {
      edges: {
        arrows: {
          to: {
            enabled: true
          }
        }
      }
    };

    const network = new Network(container, data, options);

    return () => {
      network.destroy(); // Clean up network on component unmount
    };
  }, [graphData]);

  return <div ref={networkRef} style={{ width: '100%', height: '100vh' }} />;
};

export default GraphVisualisation;
