import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { History, ChevronLeft, ChevronRight, Plus, Trash2 } from 'lucide-react';
import { useState } from 'react';

interface HistoryListProps {
  history: any[];
  onSelect: (plan: any) => void;
  onNew: () => void;
  onDelete: (id: string, e: React.MouseEvent) => void;
  activeId: number | null;
}

export default function RecoveryHistoryList({ history, onSelect, onNew, onDelete, activeId }: HistoryListProps) {
  const [collapsed, setCollapsed] = useState(false);

  if (collapsed) {
      return (
          <div className="border-r pr-2 pt-4 pl-2 h-full hidden lg:block bg-slate-50/50">
              <Button variant="ghost" size="icon" onClick={() => setCollapsed(false)}>
                  <ChevronRight className="h-4 w-4" />
              </Button>
              <div className="mt-4 flex flex-col gap-4 items-center">
                  <Button variant="outline" size="icon" onClick={onNew} title="New Analysis">
                      <Plus className="h-4 w-4" />
                  </Button>
                  <History className="h-4 w-4 text-slate-400" />
              </div>
          </div>
      )
  }

  return (
    <div className="w-64 border-r pr-4 pt-4 pl-4 hidden lg:block h-full flex flex-col bg-slate-50/50">
        <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold text-slate-700 flex items-center gap-2">
                <History className="h-4 w-4"/> Previous Plans
            </h3>
            <Button variant="ghost" size="icon" className="h-6 w-6" onClick={() => setCollapsed(true)}>
                <ChevronLeft className="h-3 w-3" />
            </Button>
        </div>
        <Button onClick={onNew} className="w-full mb-4" variant="outline">+ New Analysis</Button>
        
        <ScrollArea className="flex-1 -mr-2 pr-2">
            <div className="space-y-2 pb-4">
                {Array.isArray(history) && history.length > 0 ? (
                    history.map((item) => (
                    <div 
                        key={item.id}
                        onClick={() => onSelect(item)}
                        className={`group p-3 rounded-md text-sm cursor-pointer transition-colors border flex items-start justify-between gap-2 ${activeId === item.id ? 'bg-orange-50 border-orange-200' : 'hover:bg-slate-50 border-transparent'}`}
                    >
                        <button 
                            onClick={(e) => onDelete(item.id, e)}
                            className="p-1.5 hover:bg-red-100 rounded-md text-slate-400 hover:text-red-500 transition-colors shrink-0 mt-1"
                            title="Delete Plan"
                        >
                            <Trash2 className="w-4 h-4" />
                        </button>

                        <div className="flex-1 min-w-0">
                            <p className="font-medium truncate text-slate-800">
                               {item.diagnosis?.root_cause || "Analysis"}
                            </p>
                            <p className="text-xs text-slate-500 mt-1">
                                {new Date(item.created_at).toLocaleDateString()}
                            </p>
                        </div>
                    </div>
                ))
                ) : (
                    <div className="text-center py-8 text-slate-400 text-sm">
                        {Array.isArray(history) ? "No history yet" : "Failed to load history"}
                    </div>
                )}
            </div>
        </ScrollArea>
    </div>
  );
}
