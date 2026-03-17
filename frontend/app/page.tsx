'use client';

import { useEffect, useState } from 'react';
import { apiClient } from '@/lib/api-client';
import type { OverviewAnalytics } from '@/lib/types';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';

export default function OverviewPage() {
  const [analytics, setAnalytics] = useState<OverviewAnalytics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchAnalytics() {
      try {
        const data = await apiClient.get<OverviewAnalytics>('/api/analytics/overview');
        setAnalytics(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load analytics');
      } finally {
        setLoading(false);
      }
    }

    fetchAnalytics();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Loading analytics...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <p className="text-red-800">Error: {error}</p>
        <p className="text-sm text-red-600 mt-2">Make sure the backend API is running on port 8000</p>
      </div>
    );
  }

  if (!analytics) {
    return null;
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Network Overview</h1>
        <p className="text-gray-600 mt-2">Your LinkedIn network intelligence dashboard</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total Connections"
          value={analytics.total_connections.toLocaleString()}
          subtitle="LinkedIn connections"
          color="blue"
        />
        <StatCard
          title="Companies"
          value={analytics.total_companies.toLocaleString()}
          subtitle="Unique companies"
          color="green"
        />
        <StatCard
          title="AI/ML Connections"
          value={analytics.ai_ml_count.toLocaleString()}
          subtitle="Relevant to AI/ML roles"
          color="purple"
        />
        <StatCard
          title="Founders & Leaders"
          value={analytics.founder_count.toLocaleString()}
          subtitle="Founders and executives"
          color="orange"
        />
      </div>

      {/* Connection Growth Over Time */}
      {analytics.connection_growth.length > 0 && (
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Connections Growth Over Time</h2>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart
                data={analytics.connection_growth}
                margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
              >
                <defs>
                  <linearGradient id="colorCount" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis
                  dataKey="month"
                  tick={{ fontSize: 12, fill: '#6b7280' }}
                  tickLine={false}
                  axisLine={{ stroke: '#e5e7eb' }}
                />
                <YAxis
                  tick={{ fontSize: 12, fill: '#6b7280' }}
                  tickLine={false}
                  axisLine={{ stroke: '#e5e7eb' }}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#fff',
                    border: '1px solid #e5e7eb',
                    borderRadius: '8px',
                    fontSize: '14px',
                  }}
                  formatter={((value: any) => [Number(value).toLocaleString(), 'New Connections']) as any}
                  labelFormatter={((label: any) => {
                    const [year, month] = String(label).split('-');
                    const date = new Date(Number(year), Number(month) - 1);
                    return date.toLocaleDateString('en-US', { year: 'numeric', month: 'long' });
                  }) as any}
                />
                <Area
                  type="monotone"
                  dataKey="count"
                  stroke="#3b82f6"
                  strokeWidth={2}
                  fillOpacity={1}
                  fill="url(#colorCount)"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {/* Top Companies */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Top Companies by Network Strength</h2>
        <div className="space-y-3">
          {analytics.top_companies.slice(0, 10).map((company: any, idx: number) => (
            <a
              key={idx}
              href={`/connections?search=${encodeURIComponent(company.name)}`}
              className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-blue-50 transition cursor-pointer"
            >
              <div className="flex-1">
                <p className="font-medium text-gray-900">{company.name}</p>
                <p className="text-sm text-gray-500">
                  {company.total_connections} connections
                  {company.ai_ml_count > 0 && ` • ${company.ai_ml_count} AI/ML`}
                </p>
              </div>
              <div className="text-right">
                <p className="text-lg font-semibold text-blue-600">
                  {company.network_strength.toFixed(1)}
                </p>
                <p className="text-xs text-gray-500">Strength</p>
              </div>
            </a>
          ))}
        </div>
      </div>

      {/* Seniority Distribution */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Seniority Distribution</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {analytics.seniority_distribution.map((item: any, idx: number) => (
            <div key={idx} className="bg-gray-50 rounded-lg p-4 text-center">
              <p className="text-2xl font-bold text-gray-900">{item.count}</p>
              <p className="text-sm text-gray-600 capitalize mt-1">
                {item.seniority.replace('_', ' ')}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg shadow p-6 text-white">
        <h2 className="text-xl font-semibold mb-2">Ready to Start Your Outreach?</h2>
        <p className="text-blue-100 mb-4">
          You have {analytics.ai_ml_count} AI/ML connections and {analytics.founder_count} founders in your network
        </p>
        <div className="flex gap-3">
          <a
            href="/priority-outreach"
            className="bg-white text-blue-600 px-4 py-2 rounded-lg font-medium hover:bg-blue-50 transition"
          >
            View Priority Contacts
          </a>
          <a
            href="/connections"
            className="bg-blue-700 text-white px-4 py-2 rounded-lg font-medium hover:bg-blue-800 transition"
          >
            Browse All Connections
          </a>
        </div>
      </div>
    </div>
  );
}

interface StatCardProps {
  title: string;
  value: string;
  subtitle: string;
  color: 'blue' | 'green' | 'purple' | 'orange';
}

function StatCard({ title, value, subtitle, color }: StatCardProps) {
  const colorClasses = {
    blue: 'bg-blue-50 border-blue-200 text-blue-600',
    green: 'bg-green-50 border-green-200 text-green-600',
    purple: 'bg-purple-50 border-purple-200 text-purple-600',
    orange: 'bg-orange-50 border-orange-200 text-orange-600',
  };

  return (
    <div className={`rounded-lg border p-6 ${colorClasses[color]}`}>
      <p className="text-sm font-medium opacity-75">{title}</p>
      <p className="text-3xl font-bold mt-2">{value}</p>
      <p className="text-sm opacity-75 mt-1">{subtitle}</p>
    </div>
  );
}
