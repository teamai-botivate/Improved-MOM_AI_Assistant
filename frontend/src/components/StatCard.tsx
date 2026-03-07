/* Reusable stat card for dashboard. */

interface Props {
  title: string;
  value: number | string;
  icon: React.ReactNode;
  color: string;          // tailwind color class like "bg-blue-500"
}

export default function StatCard({ title, value, icon, color }: Props) {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-5">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-500 dark:text-gray-400">{title}</p>
          <p className="text-2xl font-bold text-gray-900 dark:text-white mt-1">{value}</p>
        </div>
        <div className={`w-12 h-12 rounded-lg ${color} flex items-center justify-center text-white`}>
          {icon}
        </div>
      </div>
    </div>
  );
}
