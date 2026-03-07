import { useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import api from '../api';
import type { Meeting } from '../types';
import StatusBadge from '../components/StatusBadge';

export default function MeetingDetailPage() {
  const { id } = useParams<{ id: string }>();

  const handleDownloadPDF = () => {
    if (!id) return;
    // Use window.location.origin for API base URL
    const url = `${window.location.origin}/api/v1/meetings/${id}/pdf`;
    window.open(url, '_blank');
  };

  const { data: meeting, isLoading } = useQuery<Meeting>({
    queryKey: ['meeting', id],
    queryFn: async () => (await api.get(`/meetings/${id}`)).data,
  });

  if (isLoading || !meeting) {
    return <div className="text-gray-400 text-center py-12">Loading meeting details...</div>;
  }

  return (
    <div className="space-y-6 max-w-4xl">
      {/* Download PDF Button */}
      <div className="flex justify-end mb-2">
        <button
          onClick={handleDownloadPDF}
          className="bg-primary-600 hover:bg-primary-700 text-white font-semibold py-2 px-4 rounded-lg shadow-sm transition"
        >
          Download MOM PDF
        </button>
      </div>
      {/* Header */}
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">{meeting.title}</h2>
        <div className="mt-3 grid grid-cols-2 md:grid-cols-3 gap-3 text-sm">
          <div><span className="text-gray-500">Organization:</span> <span className="text-gray-900 dark:text-white">{meeting.organization || '—'}</span></div>
          <div><span className="text-gray-500">Type:</span> <span className="text-gray-900 dark:text-white">{meeting.meeting_type || '—'}</span></div>
          <div><span className="text-gray-500">Date:</span> <span className="text-gray-900 dark:text-white">{meeting.date || '—'}</span></div>
          <div><span className="text-gray-500">Time:</span> <span className="text-gray-900 dark:text-white">{meeting.time || '—'}</span></div>
          <div><span className="text-gray-500">Venue:</span> <span className="text-gray-900 dark:text-white">{meeting.venue || '—'}</span></div>
          <div><span className="text-gray-500">Called By:</span> <span className="text-gray-900 dark:text-white">{meeting.called_by || '—'}</span></div>
          <div><span className="text-gray-500">Prepared By:</span> <span className="text-gray-900 dark:text-white">{meeting.prepared_by || '—'}</span></div>
        </div>
      </div>

      {/* Attendees */}
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">Attendees</h3>
        {meeting.attendees.length === 0 ? (
          <p className="text-gray-400 text-sm">No attendees recorded.</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
            {meeting.attendees.map((a) => (
              <div key={a.id} className="flex items-center gap-3 p-2 rounded-lg bg-gray-50 dark:bg-gray-700/50">
                <div className="w-8 h-8 rounded-full bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center text-primary-700 dark:text-primary-400 text-sm font-medium">
                  {a.user_name.charAt(0)}
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-900 dark:text-white">{a.user_name}</p>
                  <p className="text-xs text-gray-500">{a.email || 'N/A'}</p>
                </div>
                <span className={`ml-auto text-xs px-2 py-0.5 rounded-full ${
                  a.attendance_status === 'Present'
                    ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400'
                    : 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'
                }`}>
                  {a.attendance_status}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Agenda */}
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">Agenda</h3>
        {meeting.agenda_items.length === 0 ? (
          <p className="text-gray-400 text-sm">No agenda items.</p>
        ) : (
          <ul className="space-y-2">
            {meeting.agenda_items.map((a, i) => (
              <li key={a.id} className="pl-4 border-l-2 border-primary-500">
                <p className="font-medium text-gray-900 dark:text-white">{i + 1}. {a.topic}</p>
                {a.description && <p className="text-sm text-gray-500 mt-0.5">{a.description}</p>}
              </li>
            ))}
          </ul>
        )}
      </div>

      {/* Discussion */}
      {meeting.discussion && (
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">Discussion Summary</h3>
          <p className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap">{meeting.discussion.summary_text}</p>
        </div>
      )}

      {/* Tasks */}
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">Action Items / Tasks</h3>
        {meeting.tasks.length === 0 ? (
          <p className="text-gray-400 text-sm">No tasks recorded.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="text-xs uppercase text-gray-500 dark:text-gray-400">
                <tr>
                  <th className="py-2 pr-4">Task</th>
                  <th className="py-2 pr-4">Responsible</th>
                  <th className="py-2 pr-4">Deadline</th>
                  <th className="py-2">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100 dark:divide-gray-700">
                {meeting.tasks.map((t) => (
                  <tr key={t.id}>
                    <td className="py-2 pr-4 text-gray-900 dark:text-white">{t.title}</td>
                    <td className="py-2 pr-4 text-gray-500">{t.responsible_person || '—'}</td>
                    <td className="py-2 pr-4 text-gray-500">{t.deadline || '—'}</td>
                    <td className="py-2"><StatusBadge status={t.status} /></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Next Meeting */}
      {meeting.next_meeting && (
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Next Meeting</h3>
          <p className="text-gray-700 dark:text-gray-300">
            {meeting.next_meeting.next_date || 'TBD'} at {meeting.next_meeting.next_time || 'TBD'}
          </p>
        </div>
      )}
    </div>
  );
}
