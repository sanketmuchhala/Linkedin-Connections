'use client';

import { useEffect, useState } from 'react';
import { apiClient } from '@/lib/api-client';
import type { Connection } from '@/lib/types';

export default function PriorityOutreachPage() {
  const [connections, setConnections] = useState<Connection[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchPriorityContacts();
  }, []);

  async function fetchPriorityContacts() {
    try {
      const params = new URLSearchParams({
        min_score: '70',
        sort_by: 'total_score',
        sort_order: 'desc',
        limit: '100',
      });

      const data = await apiClient.get<any>(`/api/connections/?${params}`);
      setConnections(data.items);
    } catch (err) {
      console.error('Failed to fetch priority contacts:', err);
    } finally {
      setLoading(false);
    }
  }

  // Group connections by suggested outreach type
  const referralAsks = connections.filter(c =>
    c.total_score >= 80 && (c.is_engineer || c.is_ai_ml) && !c.is_recruiter
  );
  const founderNetwork = connections.filter(c => c.is_founder || c.is_cxo);
  const recruiterOutreach = connections.filter(c => c.is_recruiter && c.total_score >= 70);
  const informational = connections.filter(c =>
    c.total_score >= 70 && !c.is_recruiter && !founderNetwork.includes(c) && !referralAsks.includes(c)
  );

  if (loading) {
    return <div className="text-center py-12">Loading priority contacts...</div>;
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Priority Outreach</h1>
        <p className="text-gray-600 mt-2">
          High-value contacts ranked by priority score (≥70)
        </p>
      </div>

      {connections.length === 0 ? (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6 text-center">
          <p className="text-yellow-800 font-medium">No high-priority contacts found</p>
          <p className="text-yellow-600 text-sm mt-2">Try lowering the score threshold or check your filters</p>
        </div>
      ) : (
        <>
          {/* Referral Asks */}
          {referralAsks.length > 0 && (
            <OutreachGroup
              title="Referral Asks"
              subtitle="High-scoring technical contacts at target companies"
              connections={referralAsks}
              badgeColor="blue"
            />
          )}

          {/* Founder/Executive Networking */}
          {founderNetwork.length > 0 && (
            <OutreachGroup
              title="Startup Networking"
              subtitle="Founders and executives for strategic connections"
              connections={founderNetwork}
              badgeColor="orange"
            />
          )}

          {/* Recruiter Outreach */}
          {recruiterOutreach.length > 0 && (
            <OutreachGroup
              title="Recruiter Messages"
              subtitle="Recruiters at relevant companies"
              connections={recruiterOutreach}
              badgeColor="green"
            />
          )}

          {/* Informational Chats */}
          {informational.length > 0 && (
            <OutreachGroup
              title="Informational Chats"
              subtitle="Other high-value connections worth reaching out to"
              connections={informational}
              badgeColor="purple"
            />
          )}
        </>
      )}
    </div>
  );
}

function OutreachGroup({
  title,
  subtitle,
  connections,
  badgeColor
}: {
  title: string;
  subtitle: string;
  connections: Connection[];
  badgeColor: string;
}) {
  const colorClasses = {
    blue: 'bg-blue-50 border-blue-200',
    orange: 'bg-orange-50 border-orange-200',
    green: 'bg-green-50 border-green-200',
    purple: 'bg-purple-50 border-purple-200',
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="mb-4">
        <h2 className="text-xl font-semibold text-gray-900">{title}</h2>
        <p className="text-sm text-gray-600 mt-1">
          {subtitle} • {connections.length} contacts
        </p>
      </div>

      <div className="space-y-3">
        {connections.slice(0, 20).map((connection) => (
          <div
            key={connection.id}
            className={`p-4 rounded-lg border ${colorClasses[badgeColor as keyof typeof colorClasses]}`}
          >
            <div className="flex justify-between items-start">
              <div className="flex-1">
                <h3 className="font-semibold text-gray-900">
                  {connection.full_name_normalized}
                </h3>
                <p className="text-sm text-gray-700 mt-1">
                  {connection.position_normalized}
                </p>
                <p className="text-sm text-gray-600">
                  {connection.company_normalized}
                </p>
                <div className="flex gap-2 mt-2">
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
                  {connection.seniority_level && (
                    <span className="px-2 py-1 text-xs rounded-full bg-gray-100 text-gray-700 capitalize">
                      {connection.seniority_level.replace('_', ' ')}
                    </span>
                  )}
                </div>
              </div>
              <div className="text-right ml-4">
                <div className="text-2xl font-bold text-gray-900">
                  {connection.total_score.toFixed(0)}
                </div>
                <div className="text-xs text-gray-500">Score</div>
                <a
                  href={connection.linkedin_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="mt-2 inline-block px-3 py-1 text-xs bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  LinkedIn →
                </a>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
