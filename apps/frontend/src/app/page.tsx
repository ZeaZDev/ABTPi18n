// ZeaZDev [Frontend Root Page Redirect] //
// Project: Auto Bot Trader i18n //
// Version: 1.0.0 (Omega Scaffolding) //
// Author: ZeaZDev Meta-Intelligence (Generated) //
// --- DO NOT EDIT HEADER --- //
"use client";

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function RootPage() {
  const router = useRouter();
  
  useEffect(() => {
    router.push('/en/dashboard');
  }, [router]);

  return (
    <div style={{ padding: '2rem', textAlign: 'center' }}>
      <p>Redirecting to dashboard...</p>
    </div>
  );
}
