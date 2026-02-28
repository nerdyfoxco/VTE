import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'VTE Data Plane | Operator Queue',
  description: 'Deterministic Workflow Execution',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-zinc-950 text-zinc-50 antialiased min-h-screen selection:bg-rose-500/30">
        <div className="flex bg-zinc-950 min-h-screen">
          <aside className="w-16 border-r border-zinc-800 h-screen sticky top-0 flex flex-col items-center py-6 gap-8 bg-zinc-900/30">
            <div className="w-8 h-8 rounded-full bg-zinc-800 flex items-center justify-center border border-zinc-700">
              <div className="w-3 h-3 bg-zinc-400 rounded-sm" />
            </div>

            <nav className="flex flex-col gap-6 w-full items-center">
              <a href="/queue" className="w-10 h-10 rounded-xl flex items-center justify-center text-zinc-400 hover:text-zinc-50 hover:bg-zinc-800 transition-all" title="Execution Queue">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="8" y1="6" x2="21" y2="6"></line><line x1="8" y1="12" x2="21" y2="12"></line><line x1="8" y1="18" x2="21" y2="18"></line><line x1="3" y1="6" x2="3.01" y2="6"></line><line x1="3" y1="12" x2="3.01" y2="12"></line><line x1="3" y1="18" x2="3.01" y2="18"></line></svg>
              </a>
              <a href="/holds" className="w-10 h-10 rounded-xl flex items-center justify-center text-amber-500 hover:text-amber-400 hover:bg-amber-500/10 transition-all border border-transparent hover:border-amber-500/20" title="Hold Queue">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
              </a>
              <a href="/integrations" className="w-10 h-10 rounded-xl flex items-center justify-center text-zinc-400 hover:text-zinc-50 hover:bg-zinc-800 transition-all" title="Integrations & Ingestion">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>
              </a>
            </nav>
          </aside>

          <main className="flex-1 overflow-x-hidden">
            {children}
          </main>
        </div>
      </body>
    </html>
  )
}
