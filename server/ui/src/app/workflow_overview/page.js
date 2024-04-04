'use client'

import ReactFlow, { 
    useNodesState, 
    useEdgesState, 
    ConnectionLineType,
    Controls,
    useOnSelectionChange
 } from 'reactflow';
import layoutElements from './graph';
import { useEffect } from 'react';
import 'reactflow/dist/style.css';


export default function WorkflowOverview({ datasets, processingSteps, setSelectedDatasets, setSelectedProcessingSteps }) {
    const [nodes, setNodes, onNodesChange] = useNodesState([]);
    const [edges, setEdges, onEdgesChange] = useEdgesState([]);

    useEffect(() => {
        const graph = layoutElements(datasets, processingSteps);
        setNodes(graph.nodes);
        setEdges(graph.edges);
    }, []);

    useOnSelectionChange({
        onChange: ({ nodes, edges }) => {
          setSelectedProcessingSteps(nodes.map((node) => node.id));
          setSelectedDatasets(edges.map((edge) => edge.id));
        },
      });

    if (nodes && nodes.length > 0){
        return (
            <div style={{height: 500, width: 1000}}> 
                <ReactFlow
                    nodes={nodes}
                    edges={edges}
                    onNodesChange={onNodesChange}
                    onEdgesChange={onEdgesChange}
                    connectionLineType={ConnectionLineType.SmoothStep}
                    fitView
                >
                    <Controls/>
                </ReactFlow>
            </div> 
        );
    }
    else{
        return <div></div>
    }
}