'use client';

import React, { useState, useCallback } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { TaskList } from '@/components/todo/TaskList';
import { TaskForm } from '@/components/todo/TaskForm';
import { Button } from '@/components/ui/Button';

export const TaskDashboard: React.FC = () => {
  const [showForm, setShowForm] = useState(false);

  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleTaskCreated = useCallback(() => {
    setShowForm(false);
    // Trigger a refresh of the task list
    setRefreshTrigger(prev => prev + 1);
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-[#1C352D]">My Tasks</h1>
        <Button
          variant="primary"
          onClick={() => setShowForm(!showForm)}
        >
          {showForm ? 'Cancel' : 'Add New Task'}
        </Button>
      </div>

      {showForm && (
        <Card>
          <CardHeader>
            <CardTitle>Create New Task</CardTitle>
          </CardHeader>
          <CardContent>
            <TaskForm
              onTaskCreated={handleTaskCreated}
              onCancel={() => setShowForm(false)}
            />
          </CardContent>
        </Card>
      )}

      <Card>
        <CardHeader>
          <CardTitle>Your Tasks</CardTitle>
        </CardHeader>
        <CardContent>
          <TaskList key={refreshTrigger} />
        </CardContent>
      </Card>
    </div>
  );
};