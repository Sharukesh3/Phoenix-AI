import React, { memo } from 'react';
import { Handle, Position } from 'reactflow';
import type { NodeProps } from 'reactflow';
import { CheckCircle2, Circle, ExternalLink } from 'lucide-react';

const CheckableNode = ({ data, isConnectable }: NodeProps) => {
  // data.status can be 'completed' or 'pending'
  // data.onCheck is a function passed from the parent to toggle status
  // data.resource_query is the search query for the resource
  
  const isCompleted = data.status === 'completed';

  const handleLinkClick = (e: React.MouseEvent) => {
      e.stopPropagation();
      // Using a generic search or user-specified resource
      const query = encodeURIComponent(data.resource_query || data.label + " tutorial");
      window.open(`https://www.google.com/search?q=${query}`, '_blank');
  };

  return (
    <div className={`px-4 py-2 shadow-md rounded-md border-2 transition-colors min-w-[150px]
        ${isCompleted 
            ? 'bg-green-50 border-green-500 text-green-900' 
            : 'bg-white border-slate-200 text-slate-800 hover:border-blue-400'
        }
    `}>
      <Handle type="target" position={Position.Top} isConnectable={isConnectable} className="!bg-slate-400" />
      
      <div className="flex items-center gap-3">
        <button 
            onClick={(e) => {
                e.stopPropagation();
                data.onCheck(data.id);
            }}
            className="focus:outline-none hover:scale-110 transition-transform"
        >
            {isCompleted 
                ? <CheckCircle2 className="w-5 h-5 text-green-600" /> 
                : <Circle className="w-5 h-5 text-slate-300 hover:text-blue-500" />
            }
        </button>
        
        <div className="flex-1">
            <div 
                className={`font-semibold text-sm cursor-pointer hover:underline flex items-center gap-1 ${isCompleted ? 'line-through opacity-70' : ''}`}
                onClick={handleLinkClick}
                title="Click to find learning resources"
            >
                {data.label}
                <ExternalLink className="w-3 h-3 opacity-50" />
            </div>
        </div>
      </div>

      <Handle type="source" position={Position.Bottom} isConnectable={isConnectable} className="!bg-slate-400" />
    </div>
  );
};

export default memo(CheckableNode);
