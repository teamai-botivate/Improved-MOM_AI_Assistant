import axios from 'axios';

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Request interceptor for debugging
api.interceptors.request.use((config) => {
  console.log(`[API Request] ${config.method?.toUpperCase()} ${config.url}`, config.data || '');
  return config;
});

// Response interceptor for debugging
api.interceptors.response.use(
  (response) => {
    console.log(`[API Response] ${response.config.method?.toUpperCase()} ${response.config.url}`, response.status);
    return response;
  },
  (error) => {
    console.error(`[API Error] ${error.config?.method?.toUpperCase()} ${error.config?.url}`, error.response?.status, error.response?.data);
    return Promise.reject(error);
  }
);

// ---------------------------------------------------------------------------
// Backend log mirror: polls /logs and prints entries in the browser console.
// ---------------------------------------------------------------------------
let _lastLogId = 0;
let _logPollerStarted = false;

const _levelToConsole = (level: string): ((...args: unknown[]) => void) => {
  switch (level) {
    case 'ERROR':
    case 'CRITICAL':
      return console.error.bind(console);
    case 'WARNING':
      return console.warn.bind(console);
    case 'DEBUG':
      return console.debug.bind(console);
    default:
      return console.log.bind(console);
  }
};

export const startBackendLogMirror = (intervalMs = 2000): void => {
  if (_logPollerStarted) return;
  _logPollerStarted = true;

  const tick = async () => {
    try {
      const res = await api.get('/logs/', {
        params: { since: _lastLogId, limit: 500 },
      });
      const data = res.data as {
        last_id: number;
        logs: Array<{ id: number; ts: number; level: string; logger: string; message: string }>;
      };
      if (data.logs && data.logs.length > 0) {
        for (const entry of data.logs) {
          _levelToConsole(entry.level)(
            `[BACKEND ${entry.level}] ${entry.logger} | ${entry.message}`
          );
        }
      }
      if (typeof data.last_id === 'number') {
        _lastLogId = data.last_id;
      }
    } catch {
      // Swallow errors silently to avoid console noise from CORS/preflight on cold start.
    }
  };

  // Suppress the request/response interceptor logs for /logs/ to avoid feedback spam.
  api.interceptors.request.use((config) => {
    if (config.url?.includes('/logs/')) {
      (config as unknown as { _silent?: boolean })._silent = true;
    }
    return config;
  });

  void tick();
  setInterval(tick, intervalMs);
};

export default api;
