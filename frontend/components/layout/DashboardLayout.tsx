'use client';

import React from 'react';
import { useAuth } from '@/lib/auth/context';
import { Button } from '@/components/ui/Button';
import Link from 'next/link';

interface DashboardLayoutProps {
  children: React.ReactNode;
}

const DashboardLayout: React.FC<DashboardLayoutProps> = ({ children }) => {
  const { state, logout } = useAuth();

  const handleLogout = async () => {
    try {
      await logout();
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  return (
    <div className="min-h-screen bg-[#F9F6F3]">
      {/* Header */}
      <header className="bg-[#1C352D] text-white shadow-md">
        <div className="container mx-auto px-4 py-4 flex flex-col sm:flex-row justify-between items-center gap-4">
          <Link href="/dashboard" className="text-xl font-bold text-center sm:text-left">
            Todo App
          </Link>

          <div className="flex items-center space-x-2 sm:space-x-4">
            <span className="text-xs sm:text-sm text-center">
              Welcome, {state.user?.name || state.user?.email}
            </span>
            <Button
              variant="secondary"
              size="sm"
              onClick={handleLogout}
            >
              Logout
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-6 sm:py-8">
        {children}
      </main>

      {/* Footer */}
      <footer className="bg-[#1C352D] text-white py-4 mt-6 sm:mt-8">
        <div className="container mx-auto px-4 text-center">
          <p className="text-xs sm:text-sm">© {new Date().getFullYear()} Todo App. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default DashboardLayout;