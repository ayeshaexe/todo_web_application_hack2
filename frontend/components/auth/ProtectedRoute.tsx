'use client';

import React from 'react';
import { useAuth } from '@/lib/auth/context';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

interface ProtectedRouteProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
  children,
  fallback = <div>Loading...</div>
}) => {
  const { state } = useAuth();
  const router = useRouter();

  useEffect(() => {
    // Wait for auth state to load before checking authentication
    if (!state.loading && !state.isAuthenticated) {
      // Redirect to login if not authenticated
      router.push('/login');
    }
  }, [state.isAuthenticated, state.loading, router]);

  // Show fallback while checking authentication status
  if (state.loading) {
    return fallback;
  }

  // Show fallback if not authenticated
  if (!state.isAuthenticated) {
    return fallback;
  }

  // Render children if authenticated
  return <>{children}</>;
};

export default ProtectedRoute;