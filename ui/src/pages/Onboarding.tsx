import { useNavigate } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import ResumeUpload from '@/components/ResumeUpload';
import { analyzeProfile } from '@/api/client';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { UserCheck } from 'lucide-react';
import { useState } from 'react';

export default function Onboarding() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const handleAnalysis = async (file: File | null, github: string) => {
    if (!user) return;
    setLoading(true);
    try {
        const formData = new FormData();
        if (file) formData.append('resume', file);
        if (github) formData.append('github_username', github);
        formData.append('user_id', user.uid);
        
        // This analyzes AND saves to DB
        await analyzeProfile(formData);
        
        // Redirect to dashboard on success
        navigate('/dashboard');
    } catch (e) {
        console.error(e);
        alert("Setup failed. Please try again.");
    } finally {
        setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50 p-4">
      <Card className="max-w-2xl w-full shadow-lg">
        <CardHeader className="text-center">
            <div className="flex justify-center mb-4">
                <div className="h-16 w-16 bg-orange-100 rounded-full flex items-center justify-center">
                    <UserCheck className="h-8 w-8 text-orange-600" />
                </div>
            </div>
            <CardTitle className="text-2xl font-bold text-slate-900">Let's Get You Set Up</CardTitle>
            <CardDescription className="text-lg">
                We need your details to personalize your career recovery plan. <br/>
                Please upload your resume and Github profile.
            </CardDescription>
        </CardHeader>
        <CardContent>
            {loading ? (
                <div className="text-center py-10">
                    <p className="text-lg font-medium text-slate-700">Analyzing your profile...</p>
                    <p className="text-sm text-slate-500">This might take a minute.</p>
                </div>
            ) : (
                <ResumeUpload onSubmit={handleAnalysis} />
            )}
        </CardContent>
      </Card>
    </div>
  );
}
