'use client';

import { useEffect, useState } from 'react';
import { apiClient } from '@/lib/api-client';
import type { Connection } from '@/lib/types';

export default function FoundersPage() {
  const [founders, setFounders] = useState<Connection[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchFounders();
  }, []);

  async function fetchFounders() {
    try {
      const params = new URLSearchParams({
        is_founder: 'true',
        sort_by: 'total_score',
        sort_order: 'desc',
        limit: '200',
      });

      const data = await apiClient.get<any>(`/api/connections/?${params}`);
      setFounders(data.items);
    } catch (err) {
      console.error('Failed to fetch founders:', err);
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return <div className="text-center py-12">Loading founders...</div>;
  }

  const aiMlFounders = founders.filter(f => f.is_ai_ml);
  const cxoLeaders = founders.filter(f => f.is_cxo && !f.is_founder);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Founders & Leadership</h1>
        <p className="text-gray-600 mt-2">
          {founders.length} founders and {cxoLeaders.length} C-level executives
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-gradient-to-br from-orange-500 to-orange-600 rounded-lg shadow p-6 text-white">
          <div className="text-3xl font-bold">{founders.length}</div>
          <div className="text-orange-100 mt-1">Founders & Co-Founders</div>
        </div>
        <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-lg shadow p-6 text-white">
          <div className="text-3xl font-bold">{aiMlFounders.length}</div>
          <div className="text-purple-100 mt-1">AI/ML Founders</div>
        </div>
      </div>

      {aiMlFounders.length > 0 && (
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            AI/ML Founders ({aiMlFounders.length})
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {aiMlFounders.map(founder => (
              <div key={founder.id} className="p-4 bg-purple-50 border border-purple-200 rounded-lg">
                <div className="flex justify-between items-start">
                  <div>
                    <a href={founder.linkedin_url} target="_blank" rel="noopener noreferrer" className="font-semibold text-blue-600 hover:underline">{founder.full_name_normalized}</a>
                    <div className="text-sm text-gray-700 mt-1">{founder.position_normalized}</div>
                    <div className="text-sm text-gray-600">{founder.company_normalized}</div>
                  </div>
                  <div className="text-right">
                    <div className="text-xl font-bold text-purple-600">{founder.total_score.toFixed(0)}</div>
                    <div className="text-xs text-gray-500">Score</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          All Founders ({founders.length})
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {founders.map(founder => (
            <div key={founder.id} className="p-4 bg-orange-50 border border-orange-200 rounded-lg">
              <div className="flex justify-between items-start">
                <div>
                  <a href={founder.linkedin_url} target="_blank" rel="noopener noreferrer" className="font-semibold text-blue-600 hover:underline">{founder.full_name_normalized}</a>
                  <div className="text-sm text-gray-700 mt-1">{founder.position_normalized}</div>
                  <div className="text-sm text-gray-600">{founder.company_normalized}</div>
                  <div className="mt-2 flex gap-1">
                    {founder.is_ai_ml && (
                      <span className="px-2 py-1 text-xs rounded-full bg-purple-100 text-purple-800">
                        AI/ML
                      </span>
                    )}
                    <span className="px-2 py-1 text-xs rounded-full bg-gray-100 text-gray-700 capitalize">
                      {founder.seniority_level?.replace('_', ' ')}
                    </span>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-xl font-bold text-orange-600">{founder.total_score.toFixed(0)}</div>
                  <div className="text-xs text-gray-500">Score</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
