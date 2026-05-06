import axios from 'axios';

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1';
const ENABLE_API_LOGS = import.meta.env.DEV || import.meta.env.VITE_ENABLE_API_LOGS === 'true';
const ENABLE_BACKEND_LOG_MIRROR = import.meta.env.VITE_ENABLE_BACKEND_LOG_MIRROR !== 'false';

const api = axios.create({
  baseURL: API_BASE_URL,
});

type SilentAxiosConfig = {
  _silent?: boolean;
};

// Request interceptor for debugging
api.interceptors.request.use((config) => {
  const silentConfig = config as typeof config & SilentAxiosConfig;
  silentConfig._silent = Boolean(config.url?.includes('/logs/'));

  if (ENABLE_API_LOGS && !silentConfig._silent) {
    console.log(`[API Request] ${config.method?.toUpperCase()} ${config.url}`, config.data || '');
  }
  return config;
});

// Response interceptor for debugging
api.interceptors.response.use(
  (response) => {
    const silentConfig = response.config as typeof response.config & SilentAxiosConfig;
    if (ENABLE_API_LOGS && !silentConfig._silent) {
      console.log(`[API Response] ${response.config.method?.toUpperCase()} ${response.config.url}`, response.status);
    }
    return response;
  },
  (error) => {
    const silentConfig = error.config as typeof error.config & SilentAxiosConfig | undefined;
    if (ENABLE_API_LOGS && !silentConfig?._silent) {
      console.error(`[API Error] ${error.config?.method?.toUpperCase()} ${error.config?.url}`, error.response?.status, error.response?.data);
    }
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
  if (!ENABLE_BACKEND_LOG_MIRROR) return;
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

  void tick();
  setInterval(tick, intervalMs);
};

export default api;
