import {
  BarChart3,
  CalendarDays,
  Library,
  Search,
  Settings,
  Telescope,
} from 'lucide-react';
import { NavLink, Outlet } from 'react-router-dom';
import type { NavigationItem } from '../types/navigation';
import { cn } from '../utils/cn';

const navigationItems: NavigationItem[] = [
  { label: 'Library', href: '/library', icon: Library },
  { label: 'Objects', href: '/objects', icon: Telescope },
  { label: 'Sessions', href: '/sessions', icon: CalendarDays },
  { label: 'Calendar', href: '/calendar', icon: CalendarDays },
  { label: 'Search', href: '/search', icon: Search },
  { label: 'Statistics', href: '/statistics', icon: BarChart3 },
];

const footerNavigationItems: NavigationItem[] = [
  { label: 'Settings', href: '/settings', icon: Settings },
];

export function AppShell() {
  return (
    <div className="min-h-screen bg-[#080d14] text-slate-100">
      <div className="pointer-events-none fixed inset-0 bg-[radial-gradient(circle_at_50%_-10%,rgba(37,99,235,0.12),transparent_35%)]" />
      <aside className="fixed inset-y-0 left-0 z-20 hidden w-56 border-r border-slate-800 bg-[#0b1119]/95 lg:flex lg:flex-col">
        <div className="flex h-16 items-center gap-3 border-b border-slate-800 px-5">
          <div className="grid size-8 place-items-center rounded-lg border border-slate-700 bg-slate-900 text-sky-300">
            <Telescope className="size-4" />
          </div>
          <span className="text-sm font-semibold text-white">
            Astro Library
          </span>
        </div>
        <nav className="flex-1 space-y-1 px-3 py-4">
          {navigationItems.map((item) => (
            <NavItem item={item} key={item.href} />
          ))}
        </nav>
        <nav className="space-y-1 px-3 py-4">
          {footerNavigationItems.map((item) => (
            <NavItem item={item} key={item.href} />
          ))}
        </nav>
      </aside>

      <div className="relative lg:pl-56">
        <header className="sticky top-0 z-10 border-b border-slate-800 bg-[#0b1119]/90 backdrop-blur lg:hidden">
          <div className="flex h-16 items-center justify-between px-4 sm:px-6 lg:px-8">
            <div className="flex items-center gap-3">
              <div className="grid size-8 place-items-center rounded-lg border border-slate-700 bg-slate-900 text-sky-300">
                <Telescope className="size-4" />
              </div>
              <p className="text-sm font-semibold text-white">Astro Library</p>
            </div>
            <nav className="flex items-center gap-1 lg:hidden">
              {[navigationItems[1], footerNavigationItems[0]].map((item) => (
                <NavItem compact item={item} key={item.href} />
              ))}
            </nav>
          </div>
        </header>

        <main className="px-4 py-6 sm:px-6 lg:px-8">
          <div className="mx-auto max-w-[1400px]">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
}

function NavItem({
  compact = false,
  item,
}: {
  compact?: boolean;
  item: NavigationItem;
}) {
  const Icon = item.icon;

  return (
    <NavLink
      aria-label={compact ? item.label : undefined}
      className={({ isActive }) =>
        cn(
          'flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition',
          isActive
            ? 'bg-slate-700/70 text-white'
            : 'text-slate-400 hover:bg-slate-800/80 hover:text-slate-100',
          compact && 'size-10 justify-center px-0',
        )
      }
      to={item.href}
    >
      {Icon ? <Icon className="size-4" /> : null}
      {compact ? <span className="sr-only">{item.label}</span> : item.label}
    </NavLink>
  );
}
