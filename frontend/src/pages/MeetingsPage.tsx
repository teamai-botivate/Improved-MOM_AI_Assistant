import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import api from '../api';
import type { MeetingListItem } from '../types';

export default function MeetingsPage() {
  const { data: meetings = [], isLoading } = useQuery<MeetingListItem[]>({
    queryKey: ['meetings'],
    queryFn: async () => (await api.get('/meetings/')).data,
  });

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-bold text-gray-900 dark:text-white">All Meetings</h2>
        <div className="flex gap-2">
          <Link to="/upload" className="px-4 py-2 bg-primary-600 text-white rounded-lg text-sm hover:bg-primary-700 transition">
            Upload MOM
          </Link>
          <Link to="/create-mom" className="px-4 py-2 bg-green-600 text-white rounded-lg text-sm hover:bg-green-700 transition">
            Create MOM
          </Link>
        </div>
      </div>

      {isLoading ? (
        <div className="text-gray-400 text-center py-12">Loading meetings...</div>
      ) : meetings.length === 0 ? (
        <div className="text-center py-12 text-gray-400">No meetings found. Upload or create one.</div>
      ) : (
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
          <table className="w-full text-sm text-left">
            <thead className="bg-gray-50 dark:bg-gray-700 text-gray-500 dark:text-gray-300 uppercase text-xs">
              <tr>
                <th className="px-6 py-3">Title</th>
                <th className="px-6 py-3">Organization</th>
                <th className="px-6 py-3">Date</th>
                <th className="px-6 py-3">Venue</th>
                <th className="px-6 py-3">Tasks</th>
                <th className="px-6 py-3">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
              {meetings.map((m) => (
                <tr key={m.id} className="hover:bg-gray-50 dark:hover:bg-gray-700/50">
                  <td className="px-6 py-4 font-medium text-gray-900 dark:text-white">{m.title}</td>
                  <td className="px-6 py-4 text-gray-500 dark:text-gray-400">{m.organization || '—'}</td>
                  <td className="px-6 py-4 text-gray-500 dark:text-gray-400">{m.date || '—'}</td>
                  <td className="px-6 py-4 text-gray-500 dark:text-gray-400">{m.venue || '—'}</td>
                  <td className="px-6 py-4">
                    <span className="px-2 py-0.5 bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 rounded-full text-xs font-medium">
                      {m.task_count}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <Link to={`/meetings/${m.id}`} className="text-primary-600 hover:underline text-sm">
                      View
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
