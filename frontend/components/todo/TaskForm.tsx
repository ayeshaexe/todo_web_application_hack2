'use client';

import React, { useState } from 'react';
import { Input } from '@/components/ui/Input';
import { Button } from '@/components/ui/Button';
import { apiClient } from '@/lib/api/client';
import { Todo, TodoForm } from '@/lib/types';

interface TaskFormProps {
  onTaskCreated?: (newTask: Todo) => void;
  onCancel?: () => void;
}

export const TaskForm: React.FC<TaskFormProps> = ({ onTaskCreated, onCancel }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!title.trim()) {
      setError('Title is required');
      return;
    }

    setLoading(true);

    try {
      const response = await apiClient.createTodo({ title, description, completed: false });
      setTitle('');
      setDescription('');

      // Use the response from the backend which contains the correct timestamps
      const newTask = {
        id: response.todo?.id || '',
        title: response.todo?.title || title,
        description: response.todo?.description || description || '',
        completed: response.todo?.completed || false,
        userId: response.todo?.userId || '',
        createdAt: response.todo?.created_at || response.todo?.createdAt || '', // Handle both snake_case and camelCase from backend
        updatedAt: response.todo?.updated_at || response.todo?.updatedAt || '' // Handle both snake_case and camelCase from backend
      };

      if (onTaskCreated) {
        onTaskCreated(newTask);
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to create task';
      setError(errorMessage);
      console.error('Error creating task:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 sm:space-y-5 p-3 sm:p-4 bg-gray-50 rounded-lg">
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg text-sm" role="alert">
          <span className="block sm:inline">{error}</span>
        </div>
      )}

      <div className="w-full">
        <Input
          label="Task Title"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="What needs to be done?"
          required
          className="text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm sm:text-base w-full"
        />
      </div>

      <div className="w-full">
        <Input
          label="Description (Optional)"
          type="text"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Add details..."
          className="text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm sm:text-base w-full"
        />
      </div>

      <div className="flex flex-col sm:flex-row sm:space-x-3 space-y-2 sm:space-y-0 pt-2">
        <Button
          type="submit"
          className="bg-gradient-to-r from-[#1C352D] to-[#2A4D3D] hover:from-[#2A4D3D] hover:to-[#1C352D] w-full sm:w-auto text-sm py-2"
          disabled={loading}
        >
          {loading ? (
            <span className="flex items-center justify-center sm:justify-start">
              <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Creating...
            </span>
          ) : 'Add Task'}
        </Button>
        {onCancel && (
          <Button
            type="button"
            variant="outline"
            onClick={onCancel}
            className="w-full sm:w-auto text-sm py-2"
          >
            Cancel
          </Button>
        )}
      </div>
    </form>
  );
};