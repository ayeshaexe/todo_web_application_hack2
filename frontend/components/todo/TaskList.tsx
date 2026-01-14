'use client';

import React, { useEffect, useState, useCallback } from 'react';
import { TaskCard } from '@/components/todo/TaskCard';
import { Todo } from '@/lib/types';
import { apiClient } from '@/lib/api/client';
import { Button } from '@/components/ui/Button';

interface TaskListProps {
  onTaskUpdate?: (updatedTask: Todo) => void;
  onTaskDelete?: (taskId: string) => void;
  refreshTrigger?: number;
}

export const TaskList: React.FC<TaskListProps> = ({ onTaskUpdate, onTaskDelete, refreshTrigger }) => {
  const [tasks, setTasks] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchTasks();
  }, [refreshTrigger]);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiClient.getTodos();
      // Handle both API response formats (real API returns Todo[], mock API returns TodoResponse[])
      const extractedTodos = response.todos.map(item => {
        // Check if item has a 'todo' property (mock API format) or is a direct todo (real API format)
        const backendTodo = ('todo' in item && item.todo) ? item.todo : item;
        return {
          id: backendTodo.id || '',
          title: backendTodo.title || '',
          description: backendTodo.description || '',
          completed: Boolean(backendTodo.completed),
          userId: backendTodo.user_id || backendTodo.userId || '',
          createdAt: backendTodo.created_at || backendTodo.createdAt || new Date().toISOString(),
          updatedAt: backendTodo.updated_at || backendTodo.updatedAt || new Date().toISOString()
        };
      });
      // Sort tasks by creation date, newest first - optimized by precomputing timestamps
      const sortedTodos = extractedTodos.sort((a, b) => {
        const timeA = new Date(a.createdAt).getTime();
        const timeB = new Date(b.createdAt).getTime();
        return timeB - timeA; // Descending order (newest first)
      });
      setTasks(sortedTodos);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch tasks';
      setError(errorMessage);
      console.error('Error fetching tasks:', err);
      setTasks([]);
    } finally {
      setLoading(false);
    }
  };

  const handleTaskUpdate = (updatedTask: Todo | undefined) => {
    if (!updatedTask || !updatedTask.id) {
      console.error('Invalid updatedTask in handleTaskUpdate:', updatedTask);
      return;
    }

    // Update only the specific task without re-sorting if only completion status changed
    // This improves performance by avoiding unnecessary sorts
    const updatedTasks = tasks.map(task => task.id === updatedTask.id ? updatedTask : task);

    // Only re-sort if other fields changed (not just completion status)
    if (tasks.some(task => task.id === updatedTask.id &&
        (task.title !== updatedTask.title || task.description !== updatedTask.description))) {
      // Re-sort the tasks to maintain order by creation date (newest first)
      const sortedTasks = updatedTasks.sort((a, b) => {
        const timeA = new Date(a.createdAt).getTime();
        const timeB = new Date(b.createdAt).getTime();
        return timeB - timeA; // Descending order (newest first)
      });
      setTasks(sortedTasks);
    } else {
      // Just update the task without re-sorting for better performance
      setTasks(updatedTasks);
    }

    if (onTaskUpdate) {
      onTaskUpdate(updatedTask);
    }
  };

  const handleTaskDelete = (taskId: string) => {
    const filteredTasks = tasks.filter(task => task.id !== taskId);
    // Re-sort the tasks to maintain order by creation date (newest first) - optimized
    const sortedTasks = filteredTasks.sort((a, b) => {
      const timeA = new Date(a.createdAt).getTime();
      const timeB = new Date(b.createdAt).getTime();
      return timeB - timeA; // Descending order (newest first)
    });
    setTasks(sortedTasks);
    if (onTaskDelete) {
      onTaskDelete(taskId);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-32">
        <p className="text-gray-600">Loading tasks...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
        <span className="block sm:inline">{error}</span>
        <Button
          variant="secondary"
          size="sm"
          className="mt-2"
          onClick={fetchTasks}
        >
          Retry
        </Button>
      </div>
    );
  }

  if (tasks.length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-600">No tasks yet. Create your first task!</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {tasks.map(task => (
        <TaskCard
          key={task.id}
          task={task}
          onTaskUpdate={handleTaskUpdate}
          onTaskDelete={handleTaskDelete}
        />
      ))}
    </div>
  );
};