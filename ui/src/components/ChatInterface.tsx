import { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Send, User as UserIcon, Bot } from 'lucide-react';
import axios from 'axios';
import { useAuth } from '@/context/AuthContext';
import ReactMarkdown from 'react-markdown';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export default function ChatInterface() {
  const { user } = useAuth();
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', content: "Hello! I'm your Career Recovery Assistant. How can I help you today? Feel free to share your recent experiences or frustrations." }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);
  const [sessionId, setSessionId] = useState<string | null>(null);

  useEffect(() => {
     if (scrollRef.current) {
         scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
     }
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || !user) return;
    
    const userMsg = input;
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMsg }]);
    setLoading(true);

    try {
      const res = await axios.post('/api/v1/chat/message', {
        user_id: user.uid,
        session_id: sessionId,
        message: userMsg
      });
      
      setSessionId(res.data.session_id);
      setMessages(prev => [...prev, { role: 'assistant', content: res.data.response }]);
    } catch (e) {
      console.error(e);
      setMessages(prev => [...prev, { role: 'assistant', content: "Sorry, I'm having trouble connecting right now." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[600px] border rounded-lg bg-white shadow-sm">
      <div className="p-4 border-b bg-slate-50 rounded-t-lg">
        <h3 className="font-semibold text-slate-700 flex items-center gap-2">
            <Bot className="h-5 w-5 text-orange-600" /> AI Career Guide
        </h3>
      </div>
      
      <div className="flex-1 overflow-auto p-4 space-y-4" ref={scrollRef}>
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex gap-3 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            {msg.role === 'assistant' && (
                <div className="w-8 h-8 rounded-full bg-orange-100 flex items-center justify-center flex-shrink-0">
                    <Bot className="h-5 w-5 text-orange-600" />
                </div>
            )}
            <div className={`p-3 rounded-lg max-w-[80%] text-sm ${msg.role === 'user' ? 'bg-orange-600 text-white' : 'bg-slate-100 text-slate-800'}`}>
              <div className="prose prose-sm max-w-none break-words dark:prose-invert">
                <ReactMarkdown 
                    components={{
                        p: ({children}) => <p className="mb-2 last:mb-0">{children}</p>,
                        ul: ({children}) => <ul className="list-disc pl-4 mb-2">{children}</ul>,
                        ol: ({children}) => <ol className="list-decimal pl-4 mb-2">{children}</ol>,
                        li: ({children}) => <li className="mb-1">{children}</li>,
                        code: ({children}) => <code className="bg-black/10 px-1 py-0.5 rounded font-mono">{children}</code>
                    }}
                >
                    {msg.content}
                </ReactMarkdown>
              </div>
            </div>
            {msg.role === 'user' && (
                <div className="w-8 h-8 rounded-full bg-slate-200 flex items-center justify-center flex-shrink-0">
                    <UserIcon className="h-5 w-5 text-slate-500" />
                </div>
            )}
          </div>
        ))}
        {loading && <div className="text-xs text-slate-400 p-2">Thinking...</div>}
      </div>

      <div className="p-4 border-t bg-white rounded-b-lg flex gap-2">
        <Input 
            value={input} 
            onChange={(e) => setInput(e.target.value)} 
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Type your message..." 
            className="flex-1"
        />
        <Button onClick={handleSend} disabled={loading} size="icon">
            <Send className="h-4 w-4" />
        </Button>
      </div>
    </div>
  );
}
