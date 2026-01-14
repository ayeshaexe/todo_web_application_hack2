'use client';

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { SignupForm } from '@/components/auth/SignupForm';
import Link from 'next/link';

const SignupPage = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-[#F9F6F3] p-4">
      <div className="w-full max-w-md">
        <Card className="bg-white shadow-lg rounded-lg">
          <CardHeader className="text-center">
            <CardTitle className="text-2xl font-bold text-[#1C352D]">
              Create Account
            </CardTitle>
            <p className="text-sm text-gray-500 mt-2">
              Sign up for a new account
            </p>
          </CardHeader>
          <CardContent>
            <SignupForm />
            <div className="mt-4 text-center text-sm text-gray-600">
              Already have an account?{' '}
              <Link href="/login" className="text-[#1C352D] hover:underline font-medium">
                Sign in
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default SignupPage;