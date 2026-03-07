import { Link, useLocation } from 'react-router-dom';
import { useThemeStore } from '../store';
import {
  HomeIcon,
  CalendarDaysIcon,
  ArrowUpTrayIcon,
  DocumentPlusIcon,
  ClipboardDocumentListIcon,
  UserGroupIcon,
  UsersIcon,
  BellIcon,
  SunIcon,
  MoonIcon,
} from '@heroicons/react/24/outline';

const navItems = [
  { path: '/', label: 'Dashboard', icon: HomeIcon },
  { path: '/meetings', label: 'Meetings', icon: CalendarDaysIcon },
  { path: '/upload', label: 'Upload MOM', icon: ArrowUpTrayIcon },
  { path: '/create-mom', label: 'Create MOM', icon: DocumentPlusIcon },
  { path: '/tasks', label: 'Tasks', icon: ClipboardDocumentListIcon },
  { path: '/attendance', label: 'Attendance', icon: UserGroupIcon },
  { path: '/users', label: 'Users', icon: UsersIcon },
  { path: '/notifications', label: 'Notifications', icon: BellIcon },
];

export default function Layout({ children }: { children: React.ReactNode }) {
  const location = useLocation();
  const { dark, toggle } = useThemeStore();

  return (
    <div className="flex h-screen overflow-hidden bg-gray-50 dark:bg-gray-900">
      {/* Sidebar */}
      <aside className="hidden md:flex md:flex-col w-64 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700">
        <div className="flex items-center gap-2 px-6 py-5 border-b border-gray-200 dark:border-gray-700">
          <div className="w-8 h-8 rounded-lg bg-primary-600 flex items-center justify-center text-white font-bold text-sm">
            M
          </div>
          <span className="text-lg font-bold text-gray-900 dark:text-white">MOM Assistant</span>
        </div>
        <nav className="flex-1 overflow-y-auto py-4 px-3 space-y-1">
          {navItems.map(({ path, label, icon: Icon }) => {
            const active = location.pathname === path;
            return (
              <Link
                key={path}
                to={path}
                className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                  active
                    ? 'bg-primary-50 text-primary-700 dark:bg-primary-900/30 dark:text-primary-400'
                    : 'text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700'
                }`}
              >
                <Icon className="w-5 h-5" />
                {label}
              </Link>
            );
          })}
        </nav>
        <div className="px-4 py-4 border-t border-gray-200 dark:border-gray-700">
          <div className="font-medium text-sm text-gray-900 dark:text-white truncate">
            MOM AI Assistant
          </div>
          <div className="text-xs text-gray-500 dark:text-gray-400">v1.0</div>
        </div>
      </aside>

      {/* Main content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top bar */}
        <header className="flex items-center justify-between h-16 px-6 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
          <h1 className="text-lg font-semibold text-gray-900 dark:text-white">
            {navItems.find((n) => n.path === location.pathname)?.label ?? 'MOM AI Assistant'}
          </h1>
          <div className="flex items-center gap-3">
            <button
              onClick={toggle}
              className="p-2 rounded-lg text-gray-500 hover:bg-gray-100 dark:text-gray-400 dark:hover:bg-gray-700"
            >
              {dark ? <SunIcon className="w-5 h-5" /> : <MoonIcon className="w-5 h-5" />}
            </button>
            <Link
              to="/notifications"
              className="p-2 rounded-lg text-gray-500 hover:bg-gray-100 dark:text-gray-400 dark:hover:bg-gray-700"
            >
              <BellIcon className="w-5 h-5" />
            </Link>

          </div>
        </header>

        {/* Page content */}
        <main className="flex-1 overflow-y-auto p-6">{children}</main>
      </div>
    </div>
  );
}
