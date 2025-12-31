import React, { useCallback, useMemo } from 'react';
import ReactFlow, { 
  MiniMap, 
  Controls, 
  Background, 
  useNodesState, 
  useEdgesState, 
  addEdge,
  useReactFlow,
  ReactFlowProvider,
  MarkerType
} from 'reactflow';
import type { Connection, Edge, Node } from 'reactflow';
import 'reactflow/dist/style.css';
import dagre from 'dagre';
import CheckableNode from './CheckableNode';

const nodeTypes = {
  checkable: CheckableNode,
};

interface RoadmapProps {
  data: {
    nodes: any[];
    edges: any[];
  }
}

const getLayoutedElements = (nodes: any[], edges: any[], direction = 'TB') => {
  const dagreGraph = new dagre.graphlib.Graph();
  dagreGraph.setDefaultEdgeLabel(() => ({}));

  const isHorizontal = direction === 'LR';
  dagreGraph.setGraph({ rankdir: direction });

  nodes.forEach((node) => {
    // Estimating node dimensions for layout
    dagreGraph.setNode(node.id, { width: 180, height: 60 });
  });

  edges.forEach((edge) => {
    dagreGraph.setEdge(edge.source, edge.target);
  });

  dagre.layout(dagreGraph);

  const newNodes = nodes.map((node) => {
    const nodeWithPosition = dagreGraph.node(node.id);
    return {
      ...node,
      targetPosition: isHorizontal ? 'left' : 'top',
      sourcePosition: isHorizontal ? 'right' : 'bottom',
      position: {
        x: nodeWithPosition.x - 90, // center offset
        y: nodeWithPosition.y - 30,
      },
      type: 'checkable', // Force custom type
    };
  });

  return { nodes: newNodes, edges };
};

const Flow = ({ data }: RoadmapProps) => {
    const { fitView } = useReactFlow();

    // Initial Layout Calculation
    const layouted = useMemo(() => {
       if (!data?.nodes || !data.nodes.length) return { nodes: [], edges: [] };
       // Ensure edges have IDs
       const safeEdges = (data.edges || []).map((e: any) => ({
           ...e, id: e.id || `e${e.source}-${e.target}`, animated: true, markerEnd: { type: MarkerType.ArrowClosed }
       }));
       const safeNodes = data.nodes.map((n: any) => ({ ...n, data: { ...n, onCheck: () => {} } })); // placeholder onCheck
       
       return getLayoutedElements(safeNodes, safeEdges);
    }, [data]);

    const [nodes, setNodes, onNodesChange] = useNodesState(layouted.nodes);
    const [edges, setEdges, onEdgesChange] = useEdgesState(layouted.edges);

    // Handle Check Action
    const handleCheck = useCallback((nodeId: string) => {
        setNodes((nds) => 
            nds.map((node) => {
                if (node.id === nodeId) {
                    const newStatus = node.data.status === 'completed' ? 'pending' : 'completed';
                    return { ...node, data: { ...node.data, status: newStatus } };
                }
                return node;
            })
        );
    }, [setNodes]);

    // Inject handleCheck into nodes
    const nodesWithHandler = useMemo(() => {
        return nodes.map(n => ({
            ...n,
            data: { ...n.data, onCheck: handleCheck }
        }));
    }, [nodes, handleCheck]);

    const onConnect = useCallback((params: Connection | Edge) => setEdges((eds) => addEdge(params, eds)), [setEdges]);

    return (
        <div className="h-[600px] w-full border rounded-lg bg-slate-50">
            <ReactFlow
                nodes={nodesWithHandler}
                edges={edges}
                onNodesChange={onNodesChange}
                onEdgesChange={onEdgesChange}
                onConnect={onConnect}
                nodeTypes={nodeTypes}
                fitView
            >
                <Controls />
                <MiniMap />
                <Background gap={12} size={1} />
            </ReactFlow>
        </div>
    );
};

const InteractiveRoadmap = (props: RoadmapProps) => (
    <ReactFlowProvider>
        <Flow {...props} />
    </ReactFlowProvider>
);

export default InteractiveRoadmap;
