import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import toast from 'react-hot-toast';
import api from '../api';
import type { Task, TaskStatus } from '../types';
import StatusBadge from '../components/StatusBadge';

export default function TasksPage() {
  const [filter, setFilter] = useState<TaskStatus | ''>('');
  const [search, setSearch] = useState('');
  const queryClient = useQueryClient();

  const { data: tasks = [], isLoading } = useQuery<Task[]>({
    queryKey: ['tasks', filter],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (filter) params.append('status', filter);
      return (await api.get(`/tasks/?${params}`)).data;
    },
  });

  const updateMutation = useMutation({
    mutationFn: async ({ id, status }: { id: number; status: TaskStatus }) =>
      api.put(`/tasks/${id}`, { status }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
      toast.success('Task updated');
    },
  });

  const filtered = tasks.filter(
    (t) =>
      t.title.toLowerCase().includes(search.toLowerCase()) ||
      (t.responsible_person || '').toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center gap-3">
        <h2 className="text-xl font-bold text-gray-900 dark:text-white">Tasks</h2>
        <div className="flex-1" />
        <input
          placeholder="Search tasks..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-sm text-gray-900 dark:text-white w-64"
        />
        <select
          value={filter}
          onChange={(e) => setFilter(e.target.value as TaskStatus | '')}
          className="px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-sm text-gray-900 dark:text-white"
        >
          <option value="">All Status</option>
          <option value="Pending">Pending</option>
          <option value="In Progress">In Progress</option>
          <option value="Completed">Completed</option>
        </select>
      </div>

      {isLoading ? (
        <div className="text-gray-400 text-center py-12">Loading tasks...</div>
      ) : (
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
          <table className="w-full text-sm text-left">
            <thead className="bg-gray-50 dark:bg-gray-700 text-gray-500 dark:text-gray-300 uppercase text-xs">
              <tr>
                <th className="px-6 py-3">Task</th>
                <th className="px-6 py-3">Responsible</th>
                <th className="px-6 py-3">Deadline</th>
                <th className="px-6 py-3">Status</th>
                <th className="px-6 py-3">Update</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
              {filtered.map((t) => (
                <tr key={t.id} className="hover:bg-gray-50 dark:hover:bg-gray-700/50">
                  <td className="px-6 py-4 font-medium text-gray-900 dark:text-white">{t.title}</td>
                  <td className="px-6 py-4 text-gray-500 dark:text-gray-400">{t.responsible_person || '—'}</td>
                  <td className="px-6 py-4 text-gray-500 dark:text-gray-400">{t.deadline || '—'}</td>
                  <td className="px-6 py-4"><StatusBadge status={t.status} /></td>
                  <td className="px-6 py-4">
                    <select
                      value={t.status}
                      onChange={(e) => updateMutation.mutate({ id: t.id, status: e.target.value as TaskStatus })}
                      className="px-2 py-1 rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-xs text-gray-900 dark:text-white"
                    >
                      <option value="Pending">Pending</option>
                      <option value="In Progress">In Progress</option>
                      <option value="Completed">Completed</option>
                    </select>
                  </td>
                </tr>
              ))}
              {filtered.length === 0 && (
                <tr>
                  <td colSpan={5} className="px-6 py-8 text-center text-gray-400">
                    No tasks found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
