import dagre from "dagre";

export default function layoutElements(nodes, edges){
    const graph = new dagre.graphlib.Graph();
    graph.setDefaultEdgeLabel(() => ({}));
    graph.setGraph({rankdir: "LR"});

    const nodeWidth = 100;
    const nodeHeight = 30;  

    nodes.forEach(node => {
        graph.setNode(node.id, { width: nodeWidth, height: nodeHeight});
    });
    edges.forEach(edge => {
        graph.setEdge(edge);
    });
    dagre.layout(graph);

    nodes.forEach(node => {
        const nodeWithPosition = graph.node(node.id);
        node.targetPosition = 'left';
        node.sourcePosition = 'right';
    
        // Shifting the dagre node position (anchor=center center) to the top left
        // so it matches the React Flow node anchor point (top left).
        node.position = {
          x: nodeWithPosition.x - nodeWidth / 2,
          y: nodeWithPosition.y - nodeHeight / 2,
        };
    
        return node;
    });

    return { nodes, edges }
}

