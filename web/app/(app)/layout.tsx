'use client';

import { Menu, X } from 'lucide-react';
import { type FC, type PropsWithChildren, useCallback } from 'react';

// components
import { Sidebar } from '@/components/builds/BuildSidebar';

// hooks
import useStore from '@/hooks/useStore';

// providers
import AuthenticatedRouteProvider from '@/providers/AuthenticatedRouteProvider';

const AppLayout: FC<PropsWithChildren> = ({ children }) => {
  // hooks
  const setSidebarAction = useStore(({ setSidebarAction }) => setSidebarAction);
  const sidebarOpen = useStore(({ sidebarOpen }) => sidebarOpen);
  // callbacks
  const handleSidebarToggleClick = useCallback(() => setSidebarAction(!sidebarOpen), [sidebarOpen, setSidebarAction]);
  const handleSidebarCloseClick = useCallback(() => setSidebarAction(false), [setSidebarAction]);

  return (
    <AuthenticatedRouteProvider>
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

            <button onClick={handleSidebarToggleClick} className="text-sidebar-foreground hover:opacity-75">
              {sidebarOpen ? <X size={20} /> : <Menu size={20} />}
            </button>
          </div>

          {/* Mobile Sidebar Overlay */}
          {sidebarOpen && (
            <div className="fixed inset-0 z-40 bg-black/50 md:hidden" onClick={handleSidebarCloseClick} />
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
    </AuthenticatedRouteProvider>
  );
};

AppLayout.displayName = 'AppLayout';

export default AppLayout;
