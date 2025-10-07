'use client';

import { WagmiProvider, createConfig, http } from 'wagmi';
import { mainnet, polygon } from 'viem/chains';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactNode, useState } from 'react';
import { injected } from 'wagmi/connectors';
import { walletConnect } from 'wagmi/connectors';

const projectId = process.env.NEXT_PUBLIC_WALLETCONNECT_ID || 'demo';

const config = createConfig({
  chains: [mainnet, polygon],
  transports: {
    [mainnet.id]: http(),
    [polygon.id]: http()
  },
  connectors: [
    injected({
      target: 'metaMask'
    }),
    walletConnect({
      projectId,
      showQrModal: true
    })
  ]
});

export default function Providers({ children }: { children: ReactNode }) {
  const [queryClient] = useState(() => new QueryClient());

  return (
    <WagmiProvider config={config}>
      <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
    </WagmiProvider>
  );
}
