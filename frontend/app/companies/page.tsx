'use client';

import { useEffect, useState } from 'react';
import { apiClient } from '@/lib/api-client';
import type { Company } from '@/lib/types';

export default function CompaniesPage() {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [loading, setLoading] = useState(true);
  const [total, setTotal] = useState(0);

  useEffect(() => {
    fetchCompanies();
  }, []);

  async function fetchCompanies() {
    try {
      const params = new URLSearchParams({
        sort_by: 'network_strength',
        sort_order: 'desc',
        limit: '100',
      });

      const data = await apiClient.get<any>(`/api/companies/?${params}`);
      setCompanies(data.items);
      setTotal(data.total);
    } catch (err) {
      console.error('Failed to fetch companies:', err);
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return <div className="text-center py-12">Loading companies...</div>;
  }

  const topCompanies = companies.slice(0, 10);
  const aiMlCompanies = companies.filter(c => c.ai_ml_count > 0).slice(0, 10);
  const highDensity = companies.filter(c => c.total_connections >= 5);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Companies</h1>
        <p className="text-gray-600 mt-2">
          {total} companies in your network • Ranked by network strength
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg shadow p-6 text-white">
          <div className="text-3xl font-bold">{total}</div>
          <div className="text-blue-100 mt-1">Total Companies</div>
        </div>
        <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-lg shadow p-6 text-white">
          <div className="text-3xl font-bold">{highDensity.length}</div>
          <div className="text-green-100 mt-1">High Density (5+ connections)</div>
        </div>
        <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-lg shadow p-6 text-white">
          <div className="text-3xl font-bold">{aiMlCompanies.length}</div>
          <div className="text-purple-100 mt-1">With AI/ML Talent</div>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          Top Companies by Network Strength
        </h2>
        <div className="space-y-3">
          {topCompanies.map(company => (
            <div key={company.id} className="p-4 bg-gray-50 rounded-lg">
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <h3 className="font-semibold text-gray-900 text-lg">
                    {company.name_normalized}
                  </h3>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-2 mt-2 text-sm">
                    <div>
                      <span className="text-gray-600">Total:</span>{' '}
                      <span className="font-medium text-gray-900">{company.total_connections}</span>
                    </div>
                    <div>
                      <span className="text-gray-600">Engineers:</span>{' '}
                      <span className="font-medium text-gray-900">{company.engineer_count}</span>
                    </div>
                    <div>
                      <span className="text-gray-600">AI/ML:</span>{' '}
                      <span className="font-medium text-gray-900">{company.ai_ml_count}</span>
                    </div>
                    <div>
                      <span className="text-gray-600">Founders:</span>{' '}
                      <span className="font-medium text-gray-900">{company.founder_count}</span>
                    </div>
                  </div>
                  <div className="flex gap-2 mt-2">
                    {company.company_type && (
                      <span className="px-2 py-1 text-xs rounded-full bg-blue-100 text-blue-800 capitalize">
                        {company.company_type.replace('_', ' ')}
                      </span>
                    )}
                    {company.top_seniority && (
                      <span className="px-2 py-1 text-xs rounded-full bg-purple-100 text-purple-800 capitalize">
                        Top: {company.top_seniority.replace('_', ' ')}
                      </span>
                    )}
                  </div>
                </div>
                <div className="text-right ml-4">
                  <div className="text-3xl font-bold text-blue-600">
                    {company.network_strength.toFixed(1)}
                  </div>
                  <div className="text-xs text-gray-500">Network Strength</div>
                  <div className="w-24 bg-gray-200 rounded-full h-2 mt-2">
                    <div
                      className="bg-blue-600 h-2 rounded-full"
                      style={{ width: `${company.network_strength}%` }}
                    />
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {aiMlCompanies.length > 0 && (
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Top AI/ML Companies
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {aiMlCompanies.map(company => (
              <div key={company.id} className="p-4 bg-purple-50 border border-purple-200 rounded-lg">
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="font-semibold text-gray-900">{company.name_normalized}</h3>
                    <div className="text-sm text-gray-600 mt-1">
                      {company.ai_ml_count} AI/ML • {company.total_connections} total
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-xl font-bold text-purple-600">
                      {company.network_strength.toFixed(1)}
                    </div>
                    <div className="text-xs text-gray-500">Strength</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
