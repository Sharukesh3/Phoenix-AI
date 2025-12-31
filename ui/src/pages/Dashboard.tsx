import { useState, useEffect } from 'react';
import { useAuth } from '@/context/AuthContext';
import { Button } from '@/components/ui/button';
import { LogOut, MessageSquare, LayoutDashboard, FileText, Activity, Trash2 } from 'lucide-react';
import ChatInterface from '@/components/ChatInterface';
import ResumeUpload from '@/components/ResumeUpload';
import AnalysisResult from '@/components/AnalysisResult';
import RecoveryStrategyResult from '@/components/RecoveryStrategyResult';
import RejectionInput from '@/components/RejectionInput';
import RecoveryHistoryList from '@/components/RecoveryHistoryList';
import { analyzeProfile } from '@/api/client';
import axios from 'axios';

export default function Dashboard() {
  const { user, logout } = useAuth();
  const [activeTab, setActiveTab] = useState<'chat' | 'profile' | 'recovery'>('chat');
  
  const [analysisData, setAnalysisData] = useState<any>(null);
  const [recoveryData, setRecoveryData] = useState<any>(null);
  const [history, setHistory] = useState<any[]>([]); 
  const [loading, setLoading] = useState(false);

  // Fetch profile on load (omitted for brevity, assume same) ...

  const handleRecovery = async (context: string, jobDesc: string) => {
    if (!user) return;
    setLoading(true);
    try {
        const formData = new FormData();
        formData.append('context', context);
        formData.append('job_description', jobDesc);
        formData.append('user_id', user.uid);
        
        const res = await axios.post('/api/v1/agent/recover', formData);
        const newData = res.data;
        setRecoveryData(newData);
        
        // Refresh history immediately
        const historyRes = await axios.get(`/api/v1/agent/history?user_id=${user.uid}`);
        setHistory(historyRes.data);

    } catch (e) {
        console.error(e);
        alert("Failed to generate recovery plan");
    } finally {
        setLoading(false);
    }
  };

  // ... (handleAnalysis)
  useEffect(() => {
    if (user?.uid) {
        axios.get(`/api/v1/agent/profile?user_id=${user.uid}`)
             .then(res => setAnalysisData(res.data))
             .catch(err => console.log("No existing profile found."));
        
        // Fetch history
        axios.get(`/api/v1/agent/history?user_id=${user.uid}`)
             .then(res => setHistory(res.data))
             .catch(err => console.log("Failed to fetch history"));
    }
  }, [user]);

  const handleAnalysis = async (file: File | null, github: string) => {
    setLoading(true);
    try {
        const formData = new FormData();
        if (file) formData.append('resume', file);
        if (github) formData.append('github_username', github);
        if (user?.uid) formData.append('user_id', user.uid);
        
        const data = await analyzeProfile(formData);
        setAnalysisData(data);
        setActiveTab('profile'); 
    } catch (e) {
        console.error(e);
        alert("Analysis failed");
    } finally {
        setLoading(false);
    }
  };

  // Delete Plan Handler
  const handleDeletePlan = async (planId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (!confirm("Are you sure you want to delete this recovery plan?")) return;
    
    try {
        await axios.delete(`/api/v1/agent/recovery/plan/${planId}`);
        // Remove from local state
        setHistory(prev => prev.filter(p => p.id !== planId));
        // If active, clear it
        if (recoveryData?.id === planId) {
            setRecoveryData(null);
        }
    } catch (err) {
        alert("Failed to delete plan");
    }
  };

  // Delete Account Handler
  const handleDeleteAccount = async () => {
      if (!user?.uid) return;
      const confirmText = prompt("Type 'DELETE' to confirm deleting your account and all data. This cannot be undone.");
      if (confirmText !== 'DELETE') return;

      try {
          await axios.delete(`/api/v1/auth/user/${user.uid}`);
          await logout();
      } catch (err) {
          alert("Failed to delete account");
          console.error(err);
      }
  };

  return (
    <div className="flex h-screen bg-slate-50">
      {/* Sidebar */}
      <div className="w-64 bg-white border-r flex flex-col">
        <div className="p-6 border-b">
          <h1 className="text-xl font-bold text-slate-800 flex items-center gap-2">
             <LayoutDashboard className="text-orange-600"/> Phoenix AI
          </h1>
          <p className="text-xs text-slate-500 mt-1">Welcome, {user?.displayName?.split(' ')[0]}</p>
        </div>
        
        <nav className="flex-1 p-4 space-y-2">
          <Button variant={activeTab === 'chat' ? 'secondary' : 'ghost'} className={`w-full justify-start ${activeTab === 'chat' ? 'text-orange-700 bg-orange-50' : ''}`} onClick={() => setActiveTab('chat')}>
             <MessageSquare className="mr-2 h-4 w-4" /> AI Assistant
          </Button>
          <Button variant={activeTab === 'profile' ? 'secondary' : 'ghost'} className={`w-full justify-start ${activeTab === 'profile' ? 'text-orange-700 bg-orange-50' : ''}`} onClick={() => setActiveTab('profile')}>
             <FileText className="mr-2 h-4 w-4" /> Profile & Skills
          </Button>
          <Button variant={activeTab === 'recovery' ? 'secondary' : 'ghost'} className={`w-full justify-start ${activeTab === 'recovery' ? 'text-orange-700 bg-orange-50' : ''}`} onClick={() => setActiveTab('recovery')}>
             <Activity className="mr-2 h-4 w-4" /> Recovery Plan
          </Button>
        </nav>

        <div className="p-4 border-t space-y-2">
          <Button variant="ghost" className="w-full text-slate-500 hover:text-red-600 hover:bg-red-50 justify-start" onClick={handleDeleteAccount}>
             <Trash2 className="mr-2 h-4 w-4" /> Delete Account
          </Button>
          <Button variant="outline" className="w-full text-red-600 hover:text-red-700 hover:bg-red-50" onClick={logout}>
            <LogOut className="mr-2 h-4 w-4" /> Sign Out
          </Button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
            {activeTab === 'chat' && (
                <div className="flex-1 overflow-auto">
                    <div className="max-w-5xl mx-auto p-8 space-y-6">
                        <div>
                            <h2 className="text-2xl font-bold text-slate-900">Chat & Griefing</h2>
                            <p className="text-slate-500">Vent your frustrations or ask for advice. Our AI is here to listen.</p>
                        </div>
                        <ChatInterface />
                    </div>
                </div>
            )}

            {activeTab === 'profile' && (
                <div className="flex-1 overflow-auto">
                    <div className="max-w-5xl mx-auto p-8 space-y-6">
                        <h2 className="text-2xl font-bold text-slate-900">Profile Analysis</h2>
                        {!analysisData ? (
                            <div className="max-w-xl">
                                <p className="mb-4 text-slate-600">Upload your resume once to get started.</p>
                                <ResumeUpload onSubmit={handleAnalysis} />
                                {loading && <p>Analyzing...</p>}
                            </div>
                        ) : (
                            <AnalysisResult data={analysisData} />
                        )}
                    </div>
                </div>
            )}

            {activeTab === 'recovery' && (
                <div className="flex h-full"> 
                    {/* History Sidebar - Rigid height, internal scroll */}
                    <RecoveryHistoryList 
                        history={history} 
                        onSelect={(plan) => setRecoveryData({ 
                            diagnosis: plan.diagnosis, 
                            recovery_strategy: plan.strategy,
                            id: plan.id // track active
                        })}
                        onNew={() => setRecoveryData(null)}
                        onDelete={handleDeletePlan}
                        activeId={recoveryData?.id} 
                    />

                    {/* Right Content - Independent Scroll */}
                    <div className="flex-1 overflow-auto h-full p-8">
                        <div className="max-w-5xl space-y-6">
                            <h2 className="text-2xl font-bold text-slate-900">Recovery Roadmap</h2>
                             {!recoveryData ? (
                                <div className="max-w-3xl mx-auto">
                                    <RejectionInput onSubmit={handleRecovery} loading={loading} />
                                </div>
                            ) : (
                                <RecoveryStrategyResult 
                                    data={recoveryData} 
                                    onRestart={() => setRecoveryData(null)} 
                                />
                            )}
                        </div>
                    </div>
                </div>
            )}
      </div>
    </div>
  );
}
