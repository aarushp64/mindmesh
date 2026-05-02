import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { Providers } from './providers'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'MindMesh - Your AI Digital Twin',
  description: 'An AI reflection engine that grows from your thoughts, mirrors your personality, and helps you think, plan, and act like a second consciousness.',
  keywords: ['AI', 'digital twin', 'reflection', 'consciousness', 'mindmesh'],
  authors: [{ name: 'MindMesh Team' }],
  viewport: 'width=device-width, initial-scale=1',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.className} bg-gray-900 text-white min-h-screen`}>
        <div className="fixed inset-0 bg-neural-pattern opacity-20"></div>
        <Providers>
          <div className="relative z-10">
            {children}
          </div>
        </Providers>
      </body>
    </html>
  )
}