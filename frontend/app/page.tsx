'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/auth/context';

export default function Home() {
  const router = useRouter();
  const { state } = useAuth();

  useEffect(() => {
    // Wait for authentication state to be loaded
    if (!state.loading) {
      // If user is authenticated, redirect to dashboard
      if (state.isAuthenticated) {
        router.push('/dashboard');
      } else {
        // If not authenticated, redirect to login
        router.push('/login');
      }
    }
  }, [state.isAuthenticated, state.loading, router]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#F9F6F3]">
      <p className="text-lg text-[#1C352D]">
        {state.loading ? 'Loading...' : 'Redirecting...'}
      </p>
    </div>
  );
}
