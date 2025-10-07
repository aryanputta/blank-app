'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useState } from 'react';
import { Bars3Icon, XMarkIcon } from '@heroicons/react/24/outline';

const links = [
  { href: '/', label: 'Home' },
  { href: '/token', label: 'Token' },
  { href: '/dashboard', label: 'Dashboard' },
  { href: '/impact', label: 'Impact' },
  { href: '/learn', label: 'Learn' },
  { href: '/join', label: 'Join' },
  { href: '/contact', label: 'Contact' }
];

export default function Navbar() {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);

  return (
    <header className="sticky top-0 z-40 backdrop-blur bg-white/80 border-b border-brand-100/40">
      <div className="mx-auto flex items-center justify-between px-6 md:px-12 lg:px-24 xl:px-36 py-4">
        <Link href="/" className="flex items-center gap-3">
          <span className="h-10 w-10 rounded-full bg-gradient-to-br from-brand-400 via-ocean to-brand-600 flex items-center justify-center text-white font-semibold shadow-soft">
            K
          </span>
          <div>
            <p className="text-lg font-semibold text-dusk">KIND Token</p>
            <p className="text-xs text-ocean/70">Carbon-Negative Impact Network</p>
          </div>
        </Link>
        <nav className="hidden lg:flex items-center gap-6">
          {links.map(({ href, label }) => (
            <Link
              key={href}
              href={href}
              className={`text-sm font-semibold transition-colors ${
                pathname === href ? 'text-brand-600' : 'text-dusk/70 hover:text-brand-600'
              }`}
            >
              {label}
            </Link>
          ))}
        </nav>
        <div className="hidden lg:flex items-center gap-3">
          <Link href="/dashboard" className="btn-secondary text-sm">
            View Dashboard
          </Link>
          <Link href="/join" className="btn-primary text-sm">
            Join the Movement
          </Link>
        </div>
        <button
          className="lg:hidden inline-flex items-center justify-center rounded-full border border-brand-200 p-2 text-brand-700"
          onClick={() => setOpen((prev) => !prev)}
          aria-label="Toggle navigation"
        >
          {open ? <XMarkIcon className="h-6 w-6" /> : <Bars3Icon className="h-6 w-6" />}
        </button>
      </div>
      {open && (
        <div className="lg:hidden bg-white border-t border-brand-100/60 px-6 pb-6 space-y-4">
          {links.map(({ href, label }) => (
            <Link
              key={href}
              href={href}
              onClick={() => setOpen(false)}
              className={`block text-base font-semibold ${
                pathname === href ? 'text-brand-600' : 'text-dusk/80'
              }`}
            >
              {label}
            </Link>
          ))}
          <div className="flex flex-col gap-3 pt-4">
            <Link href="/dashboard" className="btn-secondary text-center">
              View Dashboard
            </Link>
            <Link href="/join" className="btn-primary text-center">
              Join the Movement
            </Link>
          </div>
        </div>
      )}
    </header>
  );
}
