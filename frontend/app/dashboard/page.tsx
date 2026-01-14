'use client';

import React from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import { TaskDashboard } from '@/components/todo/TaskDashboard';
import DashboardLayout from '@/components/layout/DashboardLayout';

const DashboardPage = () => {
  return (
    <ProtectedRoute>
      <DashboardLayout>
        <TaskDashboard />
      </DashboardLayout>
    </ProtectedRoute>
  );
};

export default DashboardPage;