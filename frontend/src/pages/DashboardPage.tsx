import { useQuery } from '@tanstack/react-query';
import {
  CalendarDaysIcon,
  ClipboardDocumentListIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  ClockIcon,
  UsersIcon,
} from '@heroicons/react/24/outline';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, Legend,
} from 'recharts';

import api from '../api';
import type { AnalyticsData } from '../types';
import StatCard from '../components/StatCard';
import StatusBadge from '../components/StatusBadge';
import { Link } from 'react-router-dom';

const PIE_COLORS = ['#facc15', '#3b82f6', '#22c55e'];

export default function DashboardPage() {
  const { data, isLoading } = useQuery<AnalyticsData>({
    queryKey: ['dashboard'],
    queryFn: async () => (await api.get('/dashboard/')).data,
  });

  if (isLoading || !data) {
    return <div className="flex items-center justify-center h-64 text-gray-400">Loading dashboard...</div>;
  }

  const { stats, task_distribution, meeting_trends, recent_meetings, overdue_tasks } = data;

  return (
    <div className="space-y-6">
      {/* Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard title="Total Meetings" value={stats.total_meetings} color="bg-blue-500" icon={<CalendarDaysIcon className="w-6 h-6" />} />
        <StatCard title="Pending Tasks" value={stats.pending_tasks} color="bg-yellow-500" icon={<ClockIcon className="w-6 h-6" />} />
        <StatCard title="Completed Tasks" value={stats.completed_tasks} color="bg-green-500" icon={<CheckCircleIcon className="w-6 h-6" />} />
        <StatCard title="Overdue Tasks" value={stats.overdue_tasks} color="bg-red-500" icon={<ExclamationTriangleIcon className="w-6 h-6" />} />
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard title="Total Tasks" value={stats.total_tasks} color="bg-indigo-500" icon={<ClipboardDocumentListIcon className="w-6 h-6" />} />
        <StatCard title="In Progress" value={stats.in_progress_tasks} color="bg-blue-400" icon={<ClockIcon className="w-6 h-6" />} />
        <StatCard title="Upcoming Meetings" value={stats.upcoming_meetings} color="bg-purple-500" icon={<CalendarDaysIcon className="w-6 h-6" />} />
        <StatCard title="Total Users" value={stats.total_users} color="bg-teal-500" icon={<UsersIcon className="w-6 h-6" />} />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Meeting Trends */}
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-5">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Meeting Trends</h2>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={meeting_trends}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" tick={{ fontSize: 12 }} />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Bar dataKey="count" fill="#3b82f6" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Task Distribution */}
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-5">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Task Distribution</h2>
          <ResponsiveContainer width="100%" height={280}>
            <PieChart>
              <Pie
                data={task_distribution}
                dataKey="count"
                nameKey="status"
                cx="50%"
                cy="50%"
                outerRadius={100}
                label={({ status, count }) => `${status}: ${count}`}
              >
                {task_distribution.map((_, idx) => (
                  <Cell key={idx} fill={PIE_COLORS[idx % PIE_COLORS.length]} />
                ))}
              </Pie>
              <Legend />
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Recent Meetings & Overdue Tasks */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Meetings */}
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-5">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Recent Meetings</h2>
          {recent_meetings.length === 0 ? (
            <p className="text-gray-400 text-sm">No meetings yet.</p>
          ) : (
            <div className="space-y-3">
              {recent_meetings.map((m) => (
                <Link
                  key={m.id}
                  to={`/meetings/${m.id}`}
                  className="block p-3 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition"
                >
                  <div className="flex justify-between items-start">
                    <div>
                      <p className="font-medium text-gray-900 dark:text-white">{m.title}</p>
                      <p className="text-xs text-gray-500">{m.date || 'No date'} &middot; {m.venue || 'N/A'}</p>
                    </div>
                    <span className="text-xs bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 px-2 py-1 rounded-full">
                      {m.task_count} tasks
                    </span>
                  </div>
                </Link>
              ))}
            </div>
          )}
        </div>

        {/* Overdue Tasks */}
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-5">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Overdue Tasks</h2>
          {overdue_tasks.length === 0 ? (
            <p className="text-gray-400 text-sm">No overdue tasks.</p>
          ) : (
            <div className="space-y-3">
              {overdue_tasks.map((t) => (
                <div key={t.id} className="p-3 rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800">
                  <p className="font-medium text-gray-900 dark:text-white">{t.title}</p>
                  <p className="text-xs text-gray-500 mt-1">
                    Assigned to: {t.responsible_person || 'Unassigned'} &middot; Due: {t.deadline}
                  </p>
                  <StatusBadge status={t.status} />
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
