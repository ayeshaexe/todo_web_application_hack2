'use client';

import React from 'react';
import { Card, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { apiClient } from '@/lib/api/client';
import { Todo } from '@/lib/types';
import { useState } from 'react';
import { formatDateTimeForDisplay } from '@/lib/utils/date';

interface TaskCardProps {
  task: Todo;
  onTaskUpdate?: (updatedTask: Todo) => void;
  onTaskDelete?: (taskId: string) => void;
}

const TaskCardComponent: React.FC<TaskCardProps> = ({ task, onTaskUpdate, onTaskDelete }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(task.title);
  const [editDescription, setEditDescription] = useState(task.description || '');

  const handleToggleCompletion = async () => {
    if (loading) return;

    setLoading(true);
    setError(null);

    try {
      const response = await apiClient.toggleTodoCompletion(task.id);
      if (onTaskUpdate) {
        // Extract the todo from the response and map it to the expected format
        const backendTodo = response.todo;
        const mappedTodo = {
          id: backendTodo.id || task.id || '',
          title: backendTodo.title || task.title || '',
          description: backendTodo.description || task.description || '',
          completed: Boolean(backendTodo.completed),
          userId: backendTodo.user_id || backendTodo.userId || task.userId || '',
          createdAt: backendTodo.created_at || backendTodo.createdAt || task.createdAt || new Date().toISOString(),
          updatedAt: backendTodo.updated_at || backendTodo.updatedAt || new Date().toISOString()
        };
        onTaskUpdate(mappedTodo);
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to update task';
      setError(errorMessage);
      console.error('Error toggling task completion:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (loading) return;

    setLoading(true);
    setError(null);

    try {
      await apiClient.deleteTodo(task.id);
      if (onTaskDelete) {
        onTaskDelete(task.id);
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to delete task';
      setError(errorMessage);
      console.error('Error deleting task:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSaveEdit = async () => {
    if (loading) return;

    setLoading(true);
    setError(null);

    try {
      const response = await apiClient.updateTodo(task.id, {
        title: editTitle,
        description: editDescription,
      });
      if (onTaskUpdate) {
        // Extract the todo from the response and map it to the expected format
        const backendTodo = response.todo;
        const mappedTodo = {
          id: backendTodo.id || task.id || '',
          title: backendTodo.title || editTitle || '',
          description: backendTodo.description || editDescription || '',
          completed: Boolean(backendTodo.completed),
          userId: backendTodo.user_id || backendTodo.userId || task.userId || '',
          createdAt: backendTodo.created_at || backendTodo.createdAt || task.createdAt || new Date().toISOString(),
          updatedAt: backendTodo.updated_at || backendTodo.updatedAt || new Date().toISOString()
        };
        onTaskUpdate(mappedTodo);
      }
      setIsEditing(false);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to update task';
      setError(errorMessage);
      console.error('Error updating task:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCancelEdit = () => {
    setEditTitle(task.title);
    setEditDescription(task.description || '');
    setIsEditing(false);
  };

  return (
    <Card
      className={`vintage-card transition-all duration-200 ${task.completed ? 'bg-[#F9F6F3] opacity-80' : 'bg-white'} font-sans`}
      role="listitem"
    >
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-2 text-sm rounded-t-lg">
          {error}
        </div>
      )}
      <CardContent className="p-4">
        <div className="flex items-start justify-between">
          <div className="flex items-start space-x-3 flex-1">
            <input
              type="checkbox"
              checked={task.completed}
              onChange={handleToggleCompletion}
              disabled={loading}
              className="mt-1 h-5 w-5 rounded border-gray-300 text-[#1C352D] focus:ring-[#1C352D] focus:ring-offset-2"
              aria-label={`Mark task "${task.title}" as ${task.completed ? 'incomplete' : 'complete'}`}
            />
            <div className="flex-1">
              {isEditing ? (
                <div className="space-y-2">
                  <input
                    type="text"
                    value={editTitle}
                    onChange={(e) => setEditTitle(e.target.value)}
                    className="w-full p-2 border border-gray-300 rounded mb-2 font-sans"
                    disabled={loading}
                    autoFocus
                  />
                  <textarea
                    value={editDescription}
                    onChange={(e) => setEditDescription(e.target.value)}
                    className="w-full p-2 border border-gray-300 rounded font-sans"
                    rows={2}
                    disabled={loading}
                  />
                  <div className="flex space-x-2 mt-2">
                    <Button
                      variant="primary"
                      size="sm"
                      onClick={handleSaveEdit}
                      disabled={loading}
                    >
                      Save
                    </Button>
                    <Button
                      variant="secondary"
                      size="sm"
                      onClick={handleCancelEdit}
                      disabled={loading}
                    >
                      Cancel
                    </Button>
                  </div>
                </div>
              ) : (
                <>
                  <h3
                    className={`font-medium text-lg ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}
                    tabIndex={0}
                  >
                    {task.title}
                  </h3>
                  {task.description && (
                    <p
                      className={`mt-1 text-base ${task.completed ? 'text-gray-400' : 'text-gray-600'}`}
                      tabIndex={0}
                    >
                      {task.description}
                    </p>
                  )}
                  <div className="flex justify-between items-center mt-2">
                    <p className="text-xs text-gray-500 italic" tabIndex={0}>
                      Created: {formatDateTimeForDisplay(task.createdAt).date} at {formatDateTimeForDisplay(task.createdAt).time}
                    </p>
                    <div className="flex space-x-2">
                      <Button
                        variant="secondary"
                        size="sm"
                        onClick={() => setIsEditing(true)}
                        disabled={loading}
                        className="font-sans"
                      >
                        Edit
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={handleDelete}
                        disabled={loading}
                        className="delete-btn text-red-500 hover:text-white"
                        aria-label={`Delete task "${task.title}"`}
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                          <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                        </svg>
                      </Button>
                    </div>
                  </div>
                </>
              )}
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

// Export memoized component to prevent unnecessary re-renders
export const TaskCard = React.memo(TaskCardComponent);