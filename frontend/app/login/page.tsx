'use client';

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { LoginForm } from '@/components/auth/LoginForm';
import Link from 'next/link';

const LoginPage = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-[#F9F6F3] p-4">
      <div className="w-full max-w-md">
        <Card className="bg-white shadow-lg rounded-lg">
          <CardHeader className="text-center">
            <CardTitle className="text-2xl font-bold text-[#1C352D]">
              Welcome Back
            </CardTitle>
            <p className="text-sm text-gray-500 mt-2">
              Sign in to your account
            </p>
          </CardHeader>
          <CardContent>
            <LoginForm />
            <div className="mt-4 text-center text-sm text-gray-600">
              Don't have an account?{' '}
              <Link href="/signup" className="text-[#1C352D] hover:underline font-medium">
                Sign up
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default LoginPage;