"use client"

import { useState, useEffect } from 'react'
import { Button } from '../../../components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../../components/ui/card'
import MainLayout from '../../../components/layout/main-layout'
import { apiClient } from '../../../lib/api-client'
import { useParams, useRouter } from 'next/navigation'

export default function TournamentPublicPage() {
  const params = useParams()
  const router = useRouter()
  const tournamentCode = params.code as string
  
  const [tournament, setTournament] = useState<any>(null)
  const [liquidation, setLiquidation] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    if (tournamentCode) {
      loadTournamentByCode()
    }
  }, [tournamentCode])

  const loadTournamentByCode = async () => {
    try {
      setLoading(true)
      setError('')
      
      // Find tournament by code (we'll need to get all tournaments and filter)
      const tournaments = await apiClient.getTournaments()
      const foundTournament = tournaments.find((t: any) => 
        t.codigo.toUpperCase() === tournamentCode.toUpperCase()
      )
      
      if (!foundTournament) {
        setError('Torneo no encontrado')
        return
      }
      
      const details = await apiClient.getTournamentDetails(foundTournament.id)
      const liquidationData = await apiClient.getLiquidation(foundTournament.id)
      
      setTournament(details)
      setLiquidation(liquidationData)
      
    } catch (error: any) {
      setError(error.message || 'Error al cargar el torneo')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <MainLayout title="Cargando Torneo..." subtitle="Obteniendo información del torneo">
        <div className="flex justify-center items-center py-12">
          <div className="text-center">
            <div className="text-6xl mb-4">⏳</div>
            <div>Cargando datos del torneo...</div>
          </div>
        </div>
      </MainLayout>
    )
  }

  if (error) {
    return (
      <MainLayout title="Error" subtitle="No se pudo cargar el torneo">
        <div className="max-w-md mx-auto space-y-4">
          <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
            <div className="text-6xl mb-4">❌</div>
            <div className="text-red-700 font-semibold mb-2">
              {error}
            </div>
            <div className="text-red-600 text-sm">
              Código de torneo: {tournamentCode}
            </div>
          </div>
          
          <div className="flex flex-col gap-2">
            <Button onClick={() => router.push('/player')}>
              🎯 Ir a Panel de Jugador
            </Button>
            <Button onClick={() => router.push('/')} variant="outline">
              ← Volver al Inicio
            </Button>
          </div>
        </div>
      </MainLayout>
    )
  }

  if (!tournament) {
    return (
      <MainLayout title="Torneo No Encontrado" subtitle="El código proporcionado no existe">
        <div className="max-w-md mx-auto text-center space-y-4">
          <div className="text-6xl mb-4">🔍</div>
          <p>No se encontró ningún torneo con el código: <strong>{tournamentCode}</strong></p>
          <Button onClick={() => router.push('/player')}>
            🎯 Ir a Panel de Jugador
          </Button>
        </div>
      </MainLayout>
    )
  }

  return (
    <MainLayout 
      title={`Torneo: ${tournament.nombre}`}
      subtitle={`Código: ${tournament.codigo} | Vista Pública`}
    >
      <div className="space-y-6">
        <div className="flex gap-2">
          <Button onClick={() => router.push('/')}>
            ← Inicio
          </Button>
          <Button onClick={() => router.push('/player')}>
            🎯 Unirse como Jugador
          </Button>
        </div>

        {/* Tournament Info */}
        <Card>
          <CardHeader>
            <CardTitle>ℹ️ Información del Torneo</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div>
                <div className="text-sm text-gray-600">Código</div>
                <div className="font-semibold text-lg font-mono">{tournament.codigo}</div>
              </div>
              <div>
                <div className="text-sm text-gray-600">Jugadores</div>
                <div className="font-semibold text-lg">{tournament.jugadores?.length || 0}</div>
              </div>
              <div>
                <div className="text-sm text-gray-600">Case Individual</div>
                <div className="font-semibold text-lg">${tournament.case_individual?.toLocaleString()}</div>
              </div>
              <div>
                <div className="text-sm text-gray-600">Con Scores</div>
                <div className="font-semibold text-lg">
                  {tournament.jugadores?.filter((p: any) => p.score_neto !== null).length || 0}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Resumen General (si hay liquidación) */}
        {liquidation && liquidation.total_jugadores > 0 && (
          <Card>
            <CardHeader>
              <CardTitle>📊 Resumen General</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-golf-green">{liquidation.total_jugadores}</div>
                  <div className="text-sm text-gray-600">Total Jugadores</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-golf-green">
                    ${liquidation.total_recolectado?.toLocaleString()}
                  </div>
                  <div className="text-sm text-gray-600">Total Recolectado</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-golf-green">
                    ${liquidation.total_premios?.toLocaleString()}
                  </div>
                  <div className="text-sm text-gray-600">Total Premios</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-golf-green">
                    ${liquidation.ganancia_casa?.toLocaleString()}
                  </div>
                  <div className="text-sm text-gray-600">Ganancia Casa</div>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Premiación (si existe) */}
        {liquidation?.premiacion && liquidation.premiacion.length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle>🏆 Premiación del Torneo</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {liquidation.premiacion.map((premio: any, index: number) => (
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

        {/* Ranking de Jugadores */}
        <Card>
          <CardHeader>
            <CardTitle>🏆 Ranking del Torneo</CardTitle>
            <CardDescription>
              Posiciones actuales ordenadas por score neto
            </CardDescription>
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
                  {tournament.jugadores
                    ?.filter((p: any) => p.score_neto !== null)
                    .sort((a: any, b: any) => (a.score_neto || 999) - (b.score_neto || 999))
                    .map((player: any, index: number) => (
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
            
            {tournament.jugadores?.filter((p: any) => p.score_neto === null).length > 0 && (
              <div className="mt-4 pt-4 border-t">
                <h4 className="font-semibold text-sm text-gray-600 mb-2">
                  Jugadores pendientes: {tournament.jugadores.filter((p: any) => p.score_neto === null).length}
                </h4>
                <div className="text-xs text-gray-500 space-y-1">
                  {tournament.jugadores
                    ?.filter((p: any) => p.score_neto === null)
                    .map((p: any, index: number) => (
                      <div key={p.id} className="inline-block mr-3">
                        {p.nombre} (Hdcp: {p.handicap})
                      </div>
                    ))}
                </div>
              </div>
            )}

            {tournament.jugadores?.length === 0 && (
              <div className="text-center py-8 text-gray-500">
                <div className="text-4xl mb-4">👥</div>
                <div>Aún no hay jugadores registrados en este torneo</div>
                <Button 
                  onClick={() => router.push('/player')} 
                  className="mt-4"
                >
                  🎯 Ser el Primer Jugador
                </Button>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Call to Action */}
        <Card className="bg-golf-green bg-opacity-10 border-golf-green">
          <CardContent className="pt-6 text-center">
            <div className="text-4xl mb-4">🎯</div>
            <h3 className="font-semibold text-lg mb-2">¿Quieres participar?</h3>
            <p className="text-gray-600 mb-4">
              Usa el código <strong className="font-mono bg-gray-100 px-2 py-1 rounded">{tournament.codigo}</strong> para unirte a este torneo
            </p>
            <Button 
              onClick={() => router.push('/player')}
              size="lg"
            >
              🎯 Unirse al Torneo
            </Button>
          </CardContent>
        </Card>
      </div>
    </MainLayout>
  )
}