'use client';

import { useEffect, useState } from 'react';
import { apiClient } from '@/lib/api-client';
import type { Connection } from '@/lib/types';

export default function AiMlPage() {
  const [connections, setConnections] = useState<Connection[]>([]);
  const [loading, setLoading] = useState(true);
  const [total, setTotal] = useState(0);

  useEffect(() => {
    fetchAiMlConnections();
  }, []);

  async function fetchAiMlConnections() {
    try {
      const params = new URLSearchParams({
        is_ai_ml: 'true',
        sort_by: 'total_score',
        sort_order: 'desc',
        limit: '200',
      });

      const data = await apiClient.get<any>(`/api/connections/?${params}`);
      setConnections(data.items);
      setTotal(data.total);
    } catch (err) {
      console.error('Failed to fetch AI/ML connections:', err);
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return <div className="text-center py-12">Loading AI/ML connections...</div>;
  }

  const highPriority = connections.filter(c => c.total_score >= 70);
  const engineers = connections.filter(c => c.is_engineer);
  const seniors = connections.filter(c =>
    c.seniority_level && ['senior', 'lead', 'manager', 'director', 'vp', 'c_level', 'founder'].includes(c.seniority_level)
  );

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">AI/ML Connections</h1>
        <p className="text-gray-600 mt-2">
          {total} connections relevant to AI/ML roles
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-lg shadow p-6 text-white">
          <div className="text-3xl font-bold">{total}</div>
          <div className="text-purple-100 mt-1">AI/ML Connections</div>
        </div>
        <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg shadow p-6 text-white">
          <div className="text-3xl font-bold">{highPriority.length}</div>
          <div className="text-blue-100 mt-1">High Priority (70+)</div>
        </div>
        <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-lg shadow p-6 text-white">
          <div className="text-3xl font-bold">{seniors.length}</div>
          <div className="text-green-100 mt-1">Senior+ Level</div>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          Top AI/ML Connections
        </h2>
        <div className="space-y-3">
          {connections.slice(0, 50).map(connection => (
            <div key={connection.id} className="p-4 bg-purple-50 border border-purple-200 rounded-lg">
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <h3 className="font-semibold text-gray-900">{connection.full_name_normalized}</h3>
                  <p className="text-sm text-gray-700 mt-1">{connection.position_normalized}</p>
                  <p className="text-sm text-gray-600">{connection.company_normalized}</p>
                  <div className="flex gap-2 mt-2">
                    {connection.is_engineer && (
                      <span className="px-2 py-1 text-xs rounded-full bg-blue-100 text-blue-800">
                        Engineer
                      </span>
                    )}
                    {connection.is_founder && (
                      <span className="px-2 py-1 text-xs rounded-full bg-orange-100 text-orange-800">
                        Founder
                      </span>
                    )}
                    {connection.seniority_level && (
                      <span className="px-2 py-1 text-xs rounded-full bg-gray-100 text-gray-700 capitalize">
                        {connection.seniority_level.replace('_', ' ')}
                      </span>
                    )}
                  </div>
                </div>
                <div className="text-right ml-4">
                  <div className="text-2xl font-bold text-purple-600">
                    {connection.total_score.toFixed(0)}
                  </div>
                  <div className="text-xs text-gray-500 mb-2">Priority Score</div>
                  <a
                    href={connection.linkedin_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-block px-3 py-1 text-xs bg-purple-600 text-white rounded-lg hover:bg-purple-700"
                  >
                    LinkedIn →
                  </a>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
