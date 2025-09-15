"use client"

import { ReactNode } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card'

interface MainLayoutProps {
  children: ReactNode
  title?: string
  subtitle?: string
}

export default function MainLayout({ children, title, subtitle }: MainLayoutProps) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-golf-green/10 to-golf-fairway/10">
      {/* Header */}
      <header className="bg-gradient-to-r from-golf-green to-golf-fairway text-white shadow-lg">
        <div className="container mx-auto px-4 py-8">
          <div className="text-center">
            <h1 className="text-5xl font-bold mb-2">
              🏌️‍♂️ TORNEO GOLF ⛳
            </h1>
            <p className="text-xl opacity-90">
              Sistema de Liquidación - "Los Peligrosos Neiva"
            </p>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {title && (
          <Card className="mb-8 golf-card">
            <CardHeader className="text-center">
              <CardTitle className="text-3xl text-golf-green mb-2">
                {title}
              </CardTitle>
              {subtitle && (
                <p className="text-muted-foreground text-lg">{subtitle}</p>
              )}
            </CardHeader>
          </Card>
        )}
        
        <div className="fade-in">
          {children}
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-100 mt-16">
        <div className="container mx-auto px-4 py-6 text-center text-gray-600">
          <p>© 2024 Los Peligrosos Neiva - Sistema Moderno de Torneos</p>
        </div>
      </footer>
    </div>
  )
}