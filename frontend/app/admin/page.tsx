"use client"

import { useState, useEffect } from 'react'
import { Button } from '../../components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/card'
import { Input } from '../../components/ui/input'
import MainLayout from '../../components/layout/main-layout'
import { apiClient } from '../../lib/api-client'
import { useWebSocket, WebSocketMessage } from '../../hooks/useWebSocket'
import AdminLogin from '../../components/AdminLogin'
import { useRouter } from 'next/navigation'

export default function AdminPage() {
  const router = useRouter()
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [tournaments, setTournaments] = useState<any[]>([])
  const [selectedTournament, setSelectedTournament] = useState<any>(null)
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [loading, setLoading] = useState(false)
  const [liquidationData, setLiquidationData] = useState<any>(null)

  // Tournament creation form
  const [tournamentName, setTournamentName] = useState('')
  const [caseIndividual, setCaseIndividual] = useState(25000)
  const [multiplicador, setMultiplicador] = useState(1000)

  // Check authentication status on mount
  useEffect(() => {
    const authenticated = apiClient.isAuthenticated()
    setIsAuthenticated(authenticated)
    if (authenticated) {
      loadTournaments()
    }
  }, [])

  const loadTournaments = async () => {
    try {
      setLoading(true)
      const data = await apiClient.getTournaments()
      setTournaments(data)
    } catch (error) {
      console.error('Error loading tournaments:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateTournament = async () => {
    try {
      setLoading(true)
      const newTournament = await apiClient.createTournament({
        nombre: tournamentName,
        case_individual: caseIndividual,
        multiplicador: multiplicador
      })
      
      setTournaments([...tournaments, newTournament])
      setTournamentName('')
      setCaseIndividual(25000)
      setMultiplicador(1000)
      setShowCreateForm(false)
    } catch (error) {
      console.error('Error creating tournament:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleTournamentDetails = async (tournament: any) => {
    try {
      setLoading(true)
      const details = await apiClient.getTournamentDetails(tournament.id)
      const liquidation = await apiClient.getLiquidation(tournament.id)
      setSelectedTournament(details)
      setLiquidationData(liquidation)
    } catch (error) {
      console.error('Error loading tournament details:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleWebSocketMessage = (message: WebSocketMessage) => {
    if (message.type === 'liquidation_update') {
      setLiquidationData(message.data)
    }
  }

  const { connect, disconnect } = useWebSocket(selectedTournament?.id, handleWebSocketMessage)

  useEffect(() => {
    if (selectedTournament?.id) {
      connect()
      return () => disconnect()
    }
  }, [selectedTournament?.id])

  if (!isAuthenticated) {
    return (
      <MainLayout title="Acceso de Administrador" subtitle="Inicia sesión para continuar">
        <AdminLogin onLoginSuccess={() => {
          setIsAuthenticated(true)
          loadTournaments()
        }} />
      </MainLayout>
    )
  }

  if (selectedTournament) {
    return (
      <MainLayout 
        title={`Torneo: ${selectedTournament.nombre}`}
        subtitle={`Código: ${selectedTournament.codigo} | Jugadores: ${selectedTournament.jugadores?.length || 0}`}
      >
        <div className="space-y-6">
          <Button 
            onClick={() => setSelectedTournament(null)}
            variant="outline"
          >
            ← Volver a Torneos
          </Button>

          {/* Resumen General */}
          {liquidationData && (
            <Card>
              <CardHeader>
                <CardTitle>📊 Resumen General</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-golf-green">{liquidationData.total_jugadores}</div>
                    <div className="text-sm text-gray-600">Total Jugadores</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-golf-green">
                      ${liquidationData.total_recolectado?.toLocaleString()}
                    </div>
                    <div className="text-sm text-gray-600">Total Recolectado</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-golf-green">
                      ${liquidationData.total_premios?.toLocaleString()}
                    </div>
                    <div className="text-sm text-gray-600">Total Premios</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-golf-green">
                      ${liquidationData.ganancia_casa?.toLocaleString()}
                    </div>
                    <div className="text-sm text-gray-600">Ganancia Casa</div>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Premiación del Torneo */}
          {liquidationData.premiacion && liquidationData.premiacion.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle>🏆 Premiación del Torneo</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {liquidationData.premiacion.map((premio: any, index: number) => (
                    <div key={index} className={`flex items-center justify-between p-3 rounded-lg border ${
                      index === 0 ? 'bg-yellow-50 border-yellow-200' :
                      index === 1 ? 'bg-gray-50 border-gray-200' :
                      index === 2 ? 'bg-orange-50 border-orange-200' :
                      'bg-blue-50 border-blue-200'
                    }`}>
                      <div className="flex items-center gap-3">
                        <span className="text-2xl">
                          {index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : '🏅'}
                        </span>
                        <div>
                          <div className="font-semibold">{premio.jugador}</div>
                          <div className="text-sm text-gray-600">Posición #{premio.posicion}</div>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="font-bold text-lg">
                          ${premio.premio?.toLocaleString()}
                        </div>
                        <div className="text-sm text-gray-600">
                          {premio.porcentaje}%
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Lista de Jugadores */}
          <Card>
            <CardHeader>
              <CardTitle>👥 Jugadores del Torneo</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b">
                      <th className="text-left p-2">Pos</th>
                      <th className="text-left p-2">Jugador</th>
                      <th className="text-right p-2">Bruto</th>
                      <th className="text-right p-2">Hdcp</th>
                      <th className="text-right p-2">Neto</th>
                      <th className="text-right p-2">Putts</th>
                    </tr>
                  </thead>
                  <tbody>
                    {selectedTournament.jugadores?.map((player: any, index: number) => (
                      <tr key={player.id} className="border-b hover:bg-gray-50">
                        <td className="p-2 font-semibold">{index + 1}</td>
                        <td className="p-2">{player.nombre}</td>
                        <td className="p-2 text-right">{player.score_bruto || '-'}</td>
                        <td className="p-2 text-right">{player.handicap}</td>
                        <td className="p-2 text-right font-semibold">
                          {player.score_neto || '-'}
                        </td>
                        <td className="p-2 text-right">{player.putts || '-'}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </CardContent>
          </Card>
        </div>
      </MainLayout>
    )
  }

  return (
    <MainLayout 
      title="Panel de Administrador" 
      subtitle="Gestiona torneos y jugadores"
    >
      <div className="space-y-6">
        <Button onClick={() => router.push('/')}>
          ← Volver al Inicio
        </Button>

        {/* Crear Torneo */}
        <Card>
          <CardHeader>
            <CardTitle>🎯 Crear Nuevo Torneo</CardTitle>
            <CardDescription>
              Configura un nuevo torneo de golf
            </CardDescription>
          </CardHeader>
          <CardContent>
            {!showCreateForm ? (
              <Button 
                onClick={() => setShowCreateForm(true)}
                className="w-full"
                size="lg"
              >
                + Crear Torneo
              </Button>
            ) : (
              <div className="space-y-4">
                <Input
                  placeholder="Nombre del torneo"
                  value={tournamentName}
                  onChange={(e) => setTournamentName(e.target.value)}
                />
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-sm font-medium">Case Individual</label>
                    <Input
                      type="number"
                      value={caseIndividual}
                      onChange={(e) => setCaseIndividual(Number(e.target.value))}
                    />
                  </div>
                  <div>
                    <label className="text-sm font-medium">Multiplicador</label>
                    <Input
                      type="number"
                      value={multiplicador}
                      onChange={(e) => setMultiplicador(Number(e.target.value))}
                    />
                  </div>
                </div>
                <div className="flex gap-2">
                  <Button 
                    onClick={handleCreateTournament}
                    disabled={loading || !tournamentName}
                  >
                    {loading ? 'Creando...' : 'Crear'}
                  </Button>
                  <Button 
                    onClick={() => setShowCreateForm(false)}
                    variant="outline"
                  >
                    Cancelar
                  </Button>
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Lista de Torneos */}
        <Card>
          <CardHeader>
            <CardTitle>🏆 Torneos Existentes</CardTitle>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="text-center py-8">Cargando torneos...</div>
            ) : tournaments.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                No hay torneos creados
              </div>
            ) : (
              <div className="space-y-4">
                {tournaments.map((tournament) => (
                  <div key={tournament.id} className="flex items-center justify-between p-4 border rounded-lg">
                    <div>
                      <h3 className="font-semibold">{tournament.nombre}</h3>
                      <p className="text-sm text-gray-600">
                        Código: {tournament.codigo} | Jugadores: {tournament.jugadores_count || 0}
                      </p>
                    </div>
                    <Button 
                      onClick={() => handleTournamentDetails(tournament)}
                      disabled={loading}
                    >
                      Ver Detalles
                    </Button>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </MainLayout>
  )
}