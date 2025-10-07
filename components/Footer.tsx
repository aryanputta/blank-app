import Link from 'next/link';

const links = [
  {
    title: 'Explore',
    items: [
      { href: '/', label: 'Home' },
      { href: '/token', label: 'Token' },
      { href: '/impact', label: 'Impact' },
      { href: '/learn', label: 'Learn' }
    ]
  },
  {
    title: 'Community',
    items: [
      { href: '/join', label: 'Join' },
      { href: '/contact', label: 'Contact' },
      { href: 'https://impact.kind.earth', label: 'Impact Dashboard', external: true }
    ]
  },
  {
    title: 'Legal',
    items: [
      { href: '/terms', label: 'Terms of Use', external: true },
      { href: '/privacy', label: 'Privacy Policy', external: true },
      { href: '/risk', label: 'Risk Disclosure', external: true }
    ]
  }
];

export default function Footer() {
  return (
    <footer className="bg-white border-t border-brand-100/60">
      <div className="section-shell pt-12 pb-8 grid gap-12 lg:grid-cols-4">
        <div className="space-y-4">
          <div className="flex items-center gap-3">
            <span className="h-10 w-10 rounded-full bg-gradient-to-br from-brand-400 via-ocean to-brand-600 flex items-center justify-center text-white font-semibold shadow-soft">
              K
            </span>
            <div>
              <p className="font-semibold text-lg text-dusk">KIND Token</p>
              <p className="text-sm text-dusk/60">Finance with empathy.</p>
            </div>
          </div>
          <p className="text-sm text-dusk/70">
            A nonprofit blockchain foundation reinvesting every surplus into climate and humanitarian progress.
          </p>
          <div className="flex gap-3">
            {['Twitter', 'Discord', 'Telegram', 'YouTube', 'LinkedIn'].map((network) => (
              <a
                key={network}
                href="#"
                className="h-9 w-9 rounded-full border border-brand-200 flex items-center justify-center text-ocean hover:bg-brand-50 transition"
                aria-label={network}
              >
                {network.slice(0, 2)}
              </a>
            ))}
          </div>
        </div>
        {links.map((group) => (
          <div key={group.title} className="space-y-4">
            <p className="text-sm font-semibold text-dusk/80 uppercase tracking-widest">{group.title}</p>
            <ul className="space-y-2">
              {group.items.map((item) => (
                <li key={item.href}>
                  {item.external ? (
                    <a href={item.href} className="text-sm text-dusk/70 hover:text-brand-600">
                      {item.label}
                    </a>
                  ) : (
                    <Link href={item.href} className="text-sm text-dusk/70 hover:text-brand-600">
                      {item.label}
                    </Link>
                  )}
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
      <div className="border-t border-brand-100/60 py-6 text-center text-xs text-dusk/60">
        © {new Date().getFullYear()} KIND Foundation. All rights reserved.
      </div>
    </footer>
  );
}
