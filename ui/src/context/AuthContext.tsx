import { createContext, useContext, useEffect, useState } from 'react';
import { onAuthStateChanged, type User, signInWithPopup, GoogleAuthProvider, signOut } from 'firebase/auth';
import { auth } from '@/lib/firebase';
import axios from 'axios';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  signInWithGoogle: () => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType>({} as AuthContextType);

// API URL - Ensure this matches your backend
// API URL - Uses relative path for proxy
const API_URL = '';

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (firebaseUser) => {
      setUser(firebaseUser);
      if (firebaseUser) {
        // Sync with backend
        try {
            await axios.post(`${API_URL}/api/v1/auth/login`, {
                uid: firebaseUser.uid,
                email: firebaseUser.email,
                full_name: firebaseUser.displayName
            });
            console.log("User synced with backend");
        } catch (e) {
            console.error("Failed to sync user", e);
        }
      }
      setLoading(false);
    });
    return unsubscribe;
  }, []);

  const signInWithGoogle = async () => {
    const provider = new GoogleAuthProvider();
    await signInWithPopup(auth, provider);
  };

  const logout = () => signOut(auth);

  return (
    <AuthContext.Provider value={{ user, loading, signInWithGoogle, logout }}>
      {!loading && children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
