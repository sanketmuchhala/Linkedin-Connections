'use client';

import { usePathname } from 'next/navigation';

const navItems = [
  { href: '/', label: 'Overview' },
  { href: '/connections', label: 'Connections' },
  { href: '/companies', label: 'Companies' },
  { href: '/priority-outreach', label: 'Priority Outreach' },
  { href: '/recruiters', label: 'Recruiters' },
  { href: '/founders', label: 'Founders' },
  { href: '/ai-ml', label: 'AI/ML Matches' },
];

export default function SidebarNav() {
  const pathname = usePathname();

  return (
    <nav className="mt-6">
      {navItems.map(({ href, label }) => {
        const isActive = href === '/' ? pathname === '/' : pathname.startsWith(href);
        return (
          <a
            key={href}
            href={href}
            className={`block px-6 py-3 text-sm font-medium transition ${
              isActive
                ? 'text-blue-600 bg-blue-50 border-l-4 border-blue-600'
                : 'text-gray-700 hover:bg-gray-50 border-l-4 border-transparent'
            }`}
          >
            {label}
          </a>
        );
      })}
    </nav>
  );
}
