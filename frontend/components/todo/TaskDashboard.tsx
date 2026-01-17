'use client';

import React, { useState, useCallback } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { TaskList } from '@/components/todo/TaskList';
import { TaskForm } from '@/components/todo/TaskForm';
import { Button } from '@/components/ui/Button';

export const TaskDashboard: React.FC = () => {
  const [showForm, setShowForm] = useState(false);

  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleTaskCreated = useCallback((newTask) => {
    setShowForm(false);
    // Trigger a refresh of the task list
    setRefreshTrigger(prev => prev + 1);
  }, []);

  return (
    <div className="space-y-4 sm:space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-center gap-4">
        <h1 className="text-2xl font-bold text-[#1C352D] text-center sm:text-left w-full sm:w-auto">
          My Tasks
        </h1>
        <Button
          variant="primary"
          className="w-full sm:w-auto"
          onClick={() => setShowForm(!showForm)}
        >
          {showForm ? 'Cancel' : 'Add New Task'}
        </Button>
      </div>

      {showForm && (
        <Card className="animate-fadeIn">
          <CardHeader>
            <CardTitle className="text-center sm:text-left">Create New Task</CardTitle>
          </CardHeader>
          <CardContent>
            <TaskForm
              onTaskCreated={handleTaskCreated}
              onCancel={() => setShowForm(false)}
            />
          </CardContent>
        </Card>
      )}

      <Card className="animate-fadeIn">
        <CardHeader>
          <CardTitle className="text-center sm:text-left">Your Tasks</CardTitle>
        </CardHeader>
        <CardContent>
          <TaskList key={refreshTrigger} />
        </CardContent>
      </Card>
    </div>
  );
};