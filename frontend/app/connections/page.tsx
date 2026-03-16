'use client';

import { useEffect, useState } from 'react';
import { apiClient } from '@/lib/api-client';
import type { Connection } from '@/lib/types';

export default function ConnectionsPage() {
  const [connections, setConnections] = useState<Connection[]>([]);
  const [loading, setLoading] = useState(true);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(0);
  const [filters, setFilters] = useState({
    search: '',
    is_ai_ml: null as boolean | null,
    is_founder: null as boolean | null,
    is_recruiter: null as boolean | null,
    min_score: '',
  });

  const limit = 50;

  useEffect(() => {
    fetchConnections();
  }, [page, filters]);

  async function fetchConnections() {
    setLoading(true);
    try {
      const params = new URLSearchParams({
        skip: String(page * limit),
        limit: String(limit),
        sort_by: 'total_score',
        sort_order: 'desc',
      });

      if (filters.search) params.append('search', filters.search);
      if (filters.is_ai_ml !== null) params.append('is_ai_ml', String(filters.is_ai_ml));
      if (filters.is_founder !== null) params.append('is_founder', String(filters.is_founder));
      if (filters.is_recruiter !== null) params.append('is_recruiter', String(filters.is_recruiter));
      if (filters.min_score) params.append('min_score', filters.min_score);

      const data = await apiClient.get<any>(`/api/connections/?${params}`);
      setConnections(data.items);
      setTotal(data.total);
    } catch (err) {
      console.error('Failed to fetch connections:', err);
    } finally {
      setLoading(false);
    }
  }

  const handleFilterChange = (key: string, value: any) => {
    setFilters(prev => ({ ...prev, [key]: value }));
    setPage(0);
  };

  const toggleFilter = (key: 'is_ai_ml' | 'is_founder' | 'is_recruiter') => {
    setFilters(prev => ({
      ...prev,
      [key]: prev[key] === true ? null : true
    }));
    setPage(0);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Connections</h1>
        <p className="text-gray-600 mt-2">
          {total.toLocaleString()} connections • Sorted by priority score
        </p>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Filters</h2>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {/* Search */}
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Search by name, company, or position
            </label>
            <input
              type="text"
              value={filters.search}
              onChange={(e) => handleFilterChange('search', e.target.value)}
              placeholder="Search..."
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          {/* Min Score */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Min Score
            </label>
            <input
              type="number"
              value={filters.min_score}
              onChange={(e) => handleFilterChange('min_score', e.target.value)}
              placeholder="0-100"
              min="0"
              max="100"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          {/* Quick Filters */}
          <div className="md:col-span-4 flex gap-2 flex-wrap">
            <button
              onClick={() => toggleFilter('is_ai_ml')}
              className={`px-4 py-2 rounded-lg font-medium transition ${
                filters.is_ai_ml
                  ? 'bg-purple-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {filters.is_ai_ml ? '✓ ' : ''}AI/ML
            </button>
            <button
              onClick={() => toggleFilter('is_founder')}
              className={`px-4 py-2 rounded-lg font-medium transition ${
                filters.is_founder
                  ? 'bg-orange-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {filters.is_founder ? '✓ ' : ''}Founders
            </button>
            <button
              onClick={() => toggleFilter('is_recruiter')}
              className={`px-4 py-2 rounded-lg font-medium transition ${
                filters.is_recruiter
                  ? 'bg-green-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {filters.is_recruiter ? '✓ ' : ''}Recruiters
            </button>
            <button
              onClick={() => setFilters({
                search: '',
                is_ai_ml: null,
                is_founder: null,
                is_recruiter: null,
                min_score: '',
              })}
              className="px-4 py-2 rounded-lg font-medium bg-gray-100 text-gray-700 hover:bg-gray-200 transition"
            >
              Clear All
            </button>
          </div>
        </div>
      </div>

      {/* Results */}
      {loading ? (
        <div className="text-center py-12">
          <div className="text-gray-500">Loading connections...</div>
        </div>
      ) : (
        <>
          {/* Table */}
          <div className="bg-white rounded-lg shadow overflow-hidden">
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Name
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Company
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Position
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Tags
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Score
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {connections.map((connection) => (
                    <tr key={connection.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div>
                          <div className="text-sm font-medium text-gray-900">
                            {connection.full_name_normalized}
                          </div>
                          {connection.email_address && (
                            <div className="text-sm text-gray-500">
                              {connection.email_address}
                            </div>
                          )}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {connection.company_normalized || '-'}
                      </td>
                      <td className="px-6 py-4">
                        <div className="text-sm text-gray-900 max-w-xs truncate">
                          {connection.position_normalized || '-'}
                        </div>
                        {connection.seniority_level && (
                          <div className="text-xs text-gray-500 capitalize">
                            {connection.seniority_level.replace('_', ' ')}
                          </div>
                        )}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex gap-1 flex-wrap">
                          {connection.is_ai_ml && (
                            <span className="px-2 py-1 text-xs rounded-full bg-purple-100 text-purple-800">
                              AI/ML
                            </span>
                          )}
                          {connection.is_founder && (
                            <span className="px-2 py-1 text-xs rounded-full bg-orange-100 text-orange-800">
                              Founder
                            </span>
                          )}
                          {connection.is_cxo && (
                            <span className="px-2 py-1 text-xs rounded-full bg-blue-100 text-blue-800">
                              C-level
                            </span>
                          )}
                          {connection.is_recruiter && (
                            <span className="px-2 py-1 text-xs rounded-full bg-green-100 text-green-800">
                              Recruiter
                            </span>
                          )}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-semibold text-gray-900">
                          {connection.total_score.toFixed(1)}
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2 mt-1">
                          <div
                            className="bg-blue-600 h-2 rounded-full"
                            style={{ width: `${connection.total_score}%` }}
                          />
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Pagination */}
          <div className="flex items-center justify-between bg-white px-6 py-4 rounded-lg shadow">
            <div className="text-sm text-gray-700">
              Showing {page * limit + 1} to {Math.min((page + 1) * limit, total)} of{' '}
              {total.toLocaleString()} connections
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => setPage(p => Math.max(0, p - 1))}
                disabled={page === 0}
                className="px-4 py-2 border border-gray-300 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
              >
                Previous
              </button>
              <button
                onClick={() => setPage(p => p + 1)}
                disabled={(page + 1) * limit >= total}
                className="px-4 py-2 border border-gray-300 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
              >
                Next
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
