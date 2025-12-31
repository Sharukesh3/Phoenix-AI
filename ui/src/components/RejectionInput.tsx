import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { AlertTriangle, ArrowRight } from 'lucide-react';

interface RejectionInputProps {
  onSubmit: (context: string, jobDesc: string) => void;
  loading: boolean;
}

export default function RejectionInput({ onSubmit, loading }: RejectionInputProps) {
  const [context, setContext] = useState('');
  const [jobDesc, setJobDesc] = useState('');

  const handleSubmit = () => {
    if (context && jobDesc) {
      onSubmit(context, jobDesc);
    }
  };

  return (
    <Card className="w-full max-w-2xl mx-auto shadow-sm border-orange-100">
      <CardHeader className="bg-orange-50/50 rounded-t-lg">
        <div className="flex items-center gap-2 text-orange-600 mb-2">
           <AlertTriangle className="h-5 w-5" />
           <span className="font-semibold text-sm uppercase tracking-wider">Recovery Mode</span>
        </div>
        <CardTitle className="text-xl font-bold text-slate-800">Analyze Rejection</CardTitle>
        <CardDescription>
          Paste the rejection email/feedback and the job description. <br/>
          Our Agent will cross-reference this with your profile to find specific gaps.
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4 pt-6">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Rejection Context (Email/Feedback)</label>
          <Textarea 
            placeholder="e.g. 'We decided to move forward with candidates who have more experience in System Design...'"
            className="h-24 bg-slate-50 border-slate-200 focus:border-orange-500 focus:ring-orange-500"
            value={context}
            onChange={(e) => setContext(e.target.value)}
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Target Job Description</label>
          <Textarea 
            placeholder="Paste the JD here..."
            className="h-32 bg-slate-50 border-slate-200 focus:border-orange-500 focus:ring-orange-500"
            value={jobDesc}
            onChange={(e) => setJobDesc(e.target.value)}
          />
        </div>
        <Button 
            onClick={handleSubmit} 
            disabled={loading || !context || !jobDesc}
            className="w-full bg-orange-600 hover:bg-orange-700 text-white font-medium py-6"
        >
            {loading ? 'Analyzing Application Gap...' : (
                <span className="flex items-center">
                    Generate Recovery Plan <ArrowRight className="ml-2 h-4 w-4" />
                </span>
            )}
        </Button>
      </CardContent>
    </Card>
  );
}
