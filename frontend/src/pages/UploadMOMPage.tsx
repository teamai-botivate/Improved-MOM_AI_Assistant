import { useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDropzone } from 'react-dropzone';
import toast from 'react-hot-toast';
import { ArrowUpTrayIcon, DocumentIcon } from '@heroicons/react/24/outline';
import api from '../api';

export default function UploadMOMPage() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const onDrop = useCallback((files: File[]) => {
    if (files.length > 0) setFile(files[0]);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'application/pdf': ['.pdf'], 'text/plain': ['.txt'] },
    maxFiles: 1,
    maxSize: 10 * 1024 * 1024,
  });

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('file', file);
      const { data } = await api.post('/upload/mom', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      toast.success('MOM processed successfully!');
      navigate(`/meetings/${data.id}`);
    } catch (err: any) {
      toast.error(err.response?.data?.detail || 'Upload failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <h2 className="text-xl font-bold text-gray-900 dark:text-white">Upload MOM Document</h2>

      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-colors ${
          isDragActive
            ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
            : 'border-gray-300 dark:border-gray-600 hover:border-primary-400'
        }`}
      >
        <input {...getInputProps()} />
        <ArrowUpTrayIcon className="w-12 h-12 mx-auto text-gray-400 mb-4" />
        {isDragActive ? (
          <p className="text-primary-600 font-medium">Drop the file here...</p>
        ) : (
          <>
            <p className="text-gray-600 dark:text-gray-300 font-medium">Drag & drop a PDF or TXT file here</p>
            <p className="text-sm text-gray-400 mt-1">or click to browse (max 10MB)</p>
          </>
        )}
      </div>

      {file && (
        <div className="flex items-center gap-3 p-4 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700">
          <DocumentIcon className="w-8 h-8 text-primary-500" />
          <div className="flex-1">
            <p className="font-medium text-gray-900 dark:text-white">{file.name}</p>
            <p className="text-xs text-gray-500">{(file.size / 1024).toFixed(1)} KB</p>
          </div>
          <button
            onClick={() => setFile(null)}
            className="text-sm text-red-500 hover:underline"
          >
            Remove
          </button>
        </div>
      )}

      <button
        onClick={handleUpload}
        disabled={!file || loading}
        className="w-full py-3 rounded-lg bg-primary-600 hover:bg-primary-700 text-white font-medium transition disabled:opacity-50"
      >
        {loading ? 'Processing with AI...' : 'Upload & Process'}
      </button>

      <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-xl p-4">
        <h3 className="font-medium text-blue-800 dark:text-blue-300 mb-1">How it works</h3>
        <ol className="text-sm text-blue-700 dark:text-blue-400 space-y-1 list-decimal list-inside">
          <li>Upload your MOM document (PDF or TXT)</li>
          <li>AI extracts meeting details, attendees, agenda, and action items</li>
          <li>Data is saved and tasks are automatically created</li>
          <li>Notifications are sent to responsible persons</li>
        </ol>
      </div>
    </div>
  );
}
