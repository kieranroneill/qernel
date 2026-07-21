'use client';

import React, { ReactNode, useState } from 'react';
import { Sidebar } from '@/components/builds/BuildSidebar';
import { Menu, X } from 'lucide-react';

interface AppLayoutProps {
  children: ReactNode;
}

export function AppLayout({ children }: AppLayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="flex h-screen bg-background">
      {/* Desktop Sidebar */}
      <div className="hidden w-64 border-r border-border bg-sidebar md:flex md:flex-col">
        <Sidebar />
      </div>

      {/* Main Content */}
      <div className="flex flex-1 flex-col">
        {/* Mobile Header */}
        <div className="flex items-center justify-between border-b border-border bg-sidebar px-4 py-3 md:hidden">
          <h1 className="font-light text-sidebar-foreground">Qernel</h1>
          <button onClick={() => setSidebarOpen(!sidebarOpen)} className="text-sidebar-foreground hover:opacity-75">
            {sidebarOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>

        {/* Mobile Sidebar Overlay */}
        {sidebarOpen && (
          <div className="fixed inset-0 z-40 bg-black/50 md:hidden" onClick={() => setSidebarOpen(false)} />
        )}

        {/* Mobile Sidebar */}
        {sidebarOpen && (
          <div className="fixed inset-y-12 left-0 z-50 w-64 border-r border-border bg-sidebar md:hidden">
            <Sidebar />
          </div>
        )}

        {/* Main Content Area */}
        <main className="flex-1 overflow-auto">{children}</main>
      </div>
    </div>
  );
}
