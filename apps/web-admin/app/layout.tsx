export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-zinc-950 text-zinc-50 antialiased min-h-screen selection:bg-indigo-500/30">
        <div className="flex bg-zinc-950">
          <aside className="w-64 border-r border-zinc-800 h-screen sticky top-0 p-6 flex flex-col gap-8">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded bg-zinc-50 flex items-center justify-center">
                <div className="w-4 h-4 border-2 border-zinc-950 rounded-sm" />
              </div>
              <span className="font-semibold tracking-tight text-lg">VTE Control Plane</span>
            </div>

            <nav className="flex flex-col gap-2">
              <div className="text-xs font-semibold text-zinc-500 tracking-wider mb-2">GOVERNANCE</div>
              <a href="/workspaces" className="px-3 py-2 text-sm text-zinc-400 hover:text-zinc-50 hover:bg-zinc-900 rounded-md transition-all">Workspaces</a>
              <a href="/policies" className="px-3 py-2 text-sm text-zinc-400 hover:text-zinc-50 hover:bg-zinc-900 rounded-md transition-all">Policy Editor</a>
              <a href="/prompts" className="px-3 py-2 text-sm text-zinc-400 hover:text-zinc-50 hover:bg-zinc-900 rounded-md transition-all">Prompt Registry</a>
            </nav>
          </aside>

          <main className="flex-1 p-10 max-w-6xl mx-auto">
            {children}
          </main>
        </div>
      </body>
    </html>
  )
}
