import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import SidebarNav from "./sidebar-nav";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "LinkedIn Network Job Hunt Assistant",
  description: "Intelligence dashboard for LinkedIn networking and job hunting",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="flex min-h-screen bg-gray-50">
          {/* Sidebar */}
          <aside className="w-64 bg-white border-r border-gray-200 fixed h-full">
            <div className="p-6">
              <h1 className="text-xl font-bold text-gray-900">Network Intel</h1>
              <p className="text-sm text-gray-500 mt-1">Job Hunt Assistant</p>
            </div>

            <SidebarNav />
          </aside>

          {/* Main Content */}
          <main className="ml-64 flex-1 p-8">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
