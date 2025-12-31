import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { LayoutDashboard } from 'lucide-react';
import axios from 'axios';

export default function Login() {
  const { signInWithGoogle, user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    const checkProfile = async () => {
        if (user) {
            try {
                // Check if profile exists
                await axios.get(`/api/v1/agent/profile?user_id=${user.uid}`);
                // If success (200), go to dashboard
                navigate('/dashboard');
            } catch (e) {
                // If 404 or other error, go to onboarding
                navigate('/onboarding');
            }
        }
    }
    checkProfile();
  }, [user, navigate]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50">
      <Card className="w-[400px] shadow-lg">
        <CardHeader className="text-center">
          <div className="flex justify-center mb-4">
            <div className="h-12 w-12 bg-orange-600 rounded-lg flex items-center justify-center">
                <LayoutDashboard className="text-white h-6 w-6" />
            </div>
          </div>
          <CardTitle className="text-2xl font-bold text-slate-900">Welcome Back</CardTitle>
          <CardDescription>Sign in to access your Career Recovery Dashboard</CardDescription>
        </CardHeader>
        <CardContent>
          <Button onClick={signInWithGoogle} className="w-full bg-white text-slate-700 border hover:bg-slate-50" size="lg">
             <img src="https://www.google.com/favicon.ico" alt="Google" className="w-4 h-4 mr-2" />
             Sign in with Google
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
