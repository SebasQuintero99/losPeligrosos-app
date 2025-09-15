"use client"

import { useState } from 'react'
import { Button } from '../components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'
import { Input } from '../components/ui/input'
import MainLayout from '../components/layout/main-layout'
import { useRouter } from 'next/navigation'

export default function HomePage() {
  const router = useRouter()
  const [quickTournamentCode, setQuickTournamentCode] = useState('')

  const handleQuickJoin = () => {
    if (quickTournamentCode.trim()) {
      router.push(`/tournament/${quickTournamentCode.trim().toUpperCase()}`)
    }
  }

  return (
    <MainLayout 
      title="Los Peligrosos Neiva" 
      subtitle="Sistema de Torneos de Golf"
    >
      <div className="space-y-8 max-w-4xl mx-auto">
        
        {/* Quick Tournament Access */}
        <Card className="bg-gradient-to-r from-golf-green to-green-600 text-white">
          <CardHeader className="text-center">
            <div className="text-4xl mb-2">⚡</div>
            <CardTitle className="text-2xl">Acceso Rápido</CardTitle>
            <CardDescription className="text-green-100">
              Ingresa el código del torneo para ver resultados
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex gap-2">
              <Input
                placeholder="Código del torneo (ej: ABC123)"
                value={quickTournamentCode}
                onChange={(e) => setQuickTournamentCode(e.target.value.toUpperCase())}
                className="flex-1 text-center text-lg font-mono bg-white text-black"
              />
              <Button 
                onClick={handleQuickJoin}
                disabled={!quickTournamentCode.trim()}
                variant="secondary"
                size="lg"
              >
                Ver Torneo
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Role Selection */}
        <div className="grid md:grid-cols-2 gap-8">
          
          {/* Admin Card */}
          <Card 
            className="tournament-card cursor-pointer hover:border-golf-green hover:shadow-lg transition-all group"
            onClick={() => router.push('/admin')}
          >
            <CardHeader className="text-center">
              <div className="text-6xl mb-4 group-hover:scale-110 transition-transform">👨‍💼</div>
              <CardTitle className="text-2xl text-golf-green">
                Administrador
              </CardTitle>
              <CardDescription className="text-lg">
                Gestiona torneos, jugadores y liquidaciones
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-gray-600">
                <li>✅ Crear y gestionar torneos</li>
                <li>✅ Ver todos los jugadores</li>
                <li>✅ Calcular liquidaciones automáticas</li>
                <li>✅ Panel de administración completo</li>
                <li>✅ Actualizaciones en tiempo real</li>
              </ul>
              <Button className="w-full mt-4" size="lg">
                Acceder como Admin
              </Button>
            </CardContent>
          </Card>

          {/* Player Card */}
          <Card 
            className="tournament-card cursor-pointer hover:border-blue-500 hover:shadow-lg transition-all group"
            onClick={() => router.push('/player')}
          >
            <CardHeader className="text-center">
              <div className="text-6xl mb-4 group-hover:scale-110 transition-transform">⛳</div>
              <CardTitle className="text-2xl text-blue-600">
                Jugador
              </CardTitle>
              <CardDescription className="text-lg">
                Únete a torneos y carga tus scores
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-gray-600">
                <li>✅ Unirse con código de torneo</li>
                <li>✅ Cargar scores de golf</li>
                <li>✅ Ver ranking en tiempo real</li>
                <li>✅ Seguir el progreso del torneo</li>
                <li>✅ Notificaciones automáticas</li>
              </ul>
              <Button className="w-full mt-4 bg-blue-600 hover:bg-blue-700" size="lg">
                Unirse como Jugador
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Features Section */}
        <Card className="bg-gray-50">
          <CardHeader className="text-center">
            <CardTitle className="text-2xl">🏆 Características del Sistema</CardTitle>
            <CardDescription>
              Todo lo que necesitas para gestionar torneos de golf
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-3 gap-6">
              <div className="text-center">
                <div className="text-3xl mb-2">📊</div>
                <h3 className="font-semibold mb-2">Liquidaciones Automáticas</h3>
                <p className="text-sm text-gray-600">
                  Cálculo automático de premios y ganancias basado en la lógica original de Los Peligrosos
                </p>
              </div>
              <div className="text-center">
                <div className="text-3xl mb-2">⚡</div>
                <h3 className="font-semibold mb-2">Tiempo Real</h3>
                <p className="text-sm text-gray-600">
                  Actualizaciones instantáneas de scores, rankings y liquidaciones via WebSocket
                </p>
              </div>
              <div className="text-center">
                <div className="text-3xl mb-2">🔒</div>
                <h3 className="font-semibold mb-2">Seguro y Confiable</h3>
                <p className="text-sm text-gray-600">
                  Sistema de autenticación JWT y base de datos persistent SQLite
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Instructions */}
        <Card className="border-2 border-dashed border-gray-300">
          <CardHeader>
            <CardTitle className="text-center">💡 ¿Cómo empezar?</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <h3 className="font-semibold text-golf-green mb-2">Para Administradores:</h3>
                <ol className="text-sm space-y-1">
                  <li>1. Accede con tus credenciales de administrador</li>
                  <li>2. Crea un nuevo torneo con la configuración deseada</li>
                  <li>3. Comparte el código de 6 caracteres con los jugadores</li>
                  <li>4. Monitorea el progreso y liquidación en tiempo real</li>
                </ol>
              </div>
              <div>
                <h3 className="font-semibold text-blue-600 mb-2">Para Jugadores:</h3>
                <ol className="text-sm space-y-1">
                  <li>1. Obtén el código del torneo del administrador</li>
                  <li>2. Regístrate con tu nombre y handicap</li>
                  <li>3. Carga tu score bruto y putts al terminar</li>
                  <li>4. Ve tu posición y premios potenciales</li>
                </ol>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Footer */}
        <div className="text-center text-gray-500 text-sm py-8">
          <div className="mb-2">🏌️‍♂️ Sistema de Torneos Los Peligrosos Neiva 🏌️‍♀️</div>
          <div>Modernizado con Next.js + FastAPI</div>
        </div>
      </div>
    </MainLayout>
  )
}