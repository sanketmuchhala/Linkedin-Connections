'use client';

import { useEffect, useState } from 'react';
import { apiClient } from '@/lib/api-client';
import type { Connection } from '@/lib/types';

export default function RecruitersPage() {
  const [recruiters, setRecruiters] = useState<Connection[]>([]);
  const [loading, setLoading] = useState(true);
  const [total, setTotal] = useState(0);

  useEffect(() => {
    fetchRecruiters();
  }, []);

  async function fetchRecruiters() {
    try {
      const params = new URLSearchParams({
        is_recruiter: 'true',
        sort_by: 'total_score',
        sort_order: 'desc',
        limit: '200',
      });

      const data = await apiClient.get<any>(`/api/connections/?${params}`);
      setRecruiters(data.items);
      setTotal(data.total);
    } catch (err) {
      console.error('Failed to fetch recruiters:', err);
    } finally {
      setLoading(false);
    }
  }

  // Group by company
  const byCompany = recruiters.reduce((acc, recruiter) => {
    const company = recruiter.company_normalized || 'Unknown';
    if (!acc[company]) acc[company] = [];
    acc[company].push(recruiter);
    return acc;
  }, {} as Record<string, Connection[]>);

  const sortedCompanies = Object.entries(byCompany).sort((a, b) => b[1].length - a[1].length);

  if (loading) {
    return <div className="text-center py-12">Loading recruiters...</div>;
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Recruiters</h1>
        <p className="text-gray-600 mt-2">
          {total} recruiters across {sortedCompanies.length} companies
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-lg shadow p-6 text-white">
          <div className="text-3xl font-bold">{total}</div>
          <div className="text-green-100 mt-1">Total Recruiters</div>
        </div>
        <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg shadow p-6 text-white">
          <div className="text-3xl font-bold">{sortedCompanies.length}</div>
          <div className="text-blue-100 mt-1">Companies</div>
        </div>
        <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-lg shadow p-6 text-white">
          <div className="text-3xl font-bold">
            {Math.round(recruiters.filter(r => r.total_score >= 50).length / recruiters.length * 100)}%
          </div>
          <div className="text-purple-100 mt-1">High Priority</div>
        </div>
      </div>

      <div className="space-y-4">
        {sortedCompanies.map(([company, recs]) => (
          <div key={company} className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">
              {company}
              <span className="ml-2 text-sm font-normal text-gray-500">
                ({recs.length} recruiter{recs.length !== 1 ? 's' : ''})
              </span>
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {recs.map(recruiter => (
                <div key={recruiter.id} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                  <div>
                    <div className="font-medium text-gray-900">{recruiter.full_name_normalized}</div>
                    <div className="text-sm text-gray-600">{recruiter.position_normalized}</div>
                  </div>
                  <div className="text-right">
                    <div className="text-lg font-semibold text-gray-900">{recruiter.total_score.toFixed(0)}</div>
                    <div className="text-xs text-gray-500">Score</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
