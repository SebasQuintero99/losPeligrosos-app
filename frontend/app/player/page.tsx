"use client"

import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import MainLayout from '@/components/layout/main-layout'
import { apiClient } from '@/lib/api-client'
import { useRouter } from 'next/navigation'

export default function PlayerPage() {
  const router = useRouter()
  const [tournamentCode, setTournamentCode] = useState('')
  const [joinedTournament, setJoinedTournament] = useState<any>(null)
  const [currentPlayer, setCurrentPlayer] = useState<any>(null)
  const [showScoreForm, setShowScoreForm] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  // Player join form
  const [playerName, setPlayerName] = useState('')
  const [handicap, setHandicap] = useState('')

  // Score form
  const [scoreBruto, setScoreBruto] = useState('')
  const [putts, setPutts] = useState('')

  const handleJoinTournament = async () => {
    try {
      setLoading(true)
      setError('')
      
      const result = await apiClient.joinTournament({
        codigo_torneo: tournamentCode,
        nombre_jugador: playerName,
        handicap: Number(handicap)
      })
      
      setJoinedTournament(result.tournament)
      setCurrentPlayer(result.player)
      setTournamentCode('')
      setPlayerName('')
      setHandicap('')
      
    } catch (error: any) {
      setError(error.message || 'Error al unirse al torneo')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmitScore = async () => {
    try {
      setLoading(true)
      setError('')
      
      await apiClient.submitScore({
        jugador_id: currentPlayer.id,
        score_bruto: Number(scoreBruto),
        putts: Number(putts)
      })
      
      // Reload tournament details to get updated data
      const tournamentDetails = await apiClient.getTournamentDetails(joinedTournament.id)
      const updatedPlayer = tournamentDetails.jugadores.find((p: any) => p.id === currentPlayer.id)
      
      setCurrentPlayer(updatedPlayer)
      setJoinedTournament(tournamentDetails)
      setScoreBruto('')
      setPutts('')
      setShowScoreForm(false)
      
    } catch (error: any) {
      setError(error.message || 'Error al enviar el score')
    } finally {
      setLoading(false)
    }
  }

  if (joinedTournament && currentPlayer) {
    return (
      <MainLayout 
        title={`Torneo: ${joinedTournament.nombre}`}
        subtitle={`¡Bienvenido, ${currentPlayer.nombre}!`}
      >
        <div className="space-y-6">
          <Button onClick={() => router.push('/')}>
            ← Volver al Inicio
          </Button>

          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
              {error}
            </div>
          )}

          {/* Player Info */}
          <Card>
            <CardHeader>
              <CardTitle>👤 Tu Información</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div>
                  <div className="text-sm text-gray-600">Jugador</div>
                  <div className="font-semibold">{currentPlayer.nombre}</div>
                </div>
                <div>
                  <div className="text-sm text-gray-600">Handicap</div>
                  <div className="font-semibold">{currentPlayer.handicap}</div>
                </div>
                <div>
                  <div className="text-sm text-gray-600">Score Bruto</div>
                  <div className="font-semibold text-golf-green">
                    {currentPlayer.score_bruto || 'Pendiente'}
                  </div>
                </div>
                <div>
                  <div className="text-sm text-gray-600">Score Neto</div>
                  <div className="font-semibold text-golf-green">
                    {currentPlayer.score_neto || 'Pendiente'}
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Score Form */}
          <Card>
            <CardHeader>
              <CardTitle>⛳ Cargar Score</CardTitle>
              <CardDescription>
                {currentPlayer.score_bruto ? 
                  'Actualiza tu score del torneo' : 
                  'Ingresa tu score del torneo'
                }
              </CardDescription>
            </CardHeader>
            <CardContent>
              {!showScoreForm ? (
                <Button 
                  onClick={() => setShowScoreForm(true)}
                  className="w-full"
                  size="lg"
                >
                  {currentPlayer.score_bruto ? 
                    '📝 Actualizar Score' : 
                    '📝 Cargar Score'
                  }
                </Button>
              ) : (
                <div className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="text-sm font-medium">Score Bruto</label>
                      <Input
                        type="number"
                        placeholder="72"
                        value={scoreBruto}
                        onChange={(e) => setScoreBruto(e.target.value)}
                      />
                    </div>
                    <div>
                      <label className="text-sm font-medium">Putts</label>
                      <Input
                        type="number"
                        placeholder="28"
                        value={putts}
                        onChange={(e) => setPutts(e.target.value)}
                      />
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <Button 
                      onClick={handleSubmitScore}
                      disabled={loading || !scoreBruto || !putts}
                    >
                      {loading ? 'Enviando...' : 'Enviar Score'}
                    </Button>
                    <Button 
                      onClick={() => setShowScoreForm(false)}
                      variant="outline"
                    >
                      Cancelar
                    </Button>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Tournament Ranking */}
          <Card>
            <CardHeader>
              <CardTitle>🏆 Ranking del Torneo</CardTitle>
              <CardDescription>
                Posiciones actuales (ordenado por score neto)
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
                    {joinedTournament.jugadores
                      ?.filter((p: any) => p.score_neto !== null)
                      .sort((a: any, b: any) => (a.score_neto || 999) - (b.score_neto || 999))
                      .map((player: any, index: number) => (
                        <tr 
                          key={player.id} 
                          className={`border-b hover:bg-gray-50 ${
                            player.id === currentPlayer.id ? 'bg-golf-green bg-opacity-10' : ''
                          }`}
                        >
                          <td className="p-2 font-semibold">
                            {index + 1}
                            {player.id === currentPlayer.id && <span className="ml-1">👤</span>}
                          </td>
                          <td className="p-2">
                            {player.nombre}
                            {player.id === currentPlayer.id && <span className="text-xs text-golf-green ml-1">(Tú)</span>}
                          </td>
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
              
              {joinedTournament.jugadores?.filter((p: any) => p.score_neto === null).length > 0 && (
                <div className="mt-4 pt-4 border-t">
                  <h4 className="font-semibold text-sm text-gray-600 mb-2">
                    Jugadores sin score: {joinedTournament.jugadores.filter((p: any) => p.score_neto === null).length}
                  </h4>
                  <div className="text-xs text-gray-500">
                    {joinedTournament.jugadores
                      ?.filter((p: any) => p.score_neto === null)
                      .map((p: any) => p.nombre)
                      .join(', ')}
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Tournament Info */}
          <Card>
            <CardHeader>
              <CardTitle>ℹ️ Información del Torneo</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="text-gray-600">Código:</span> {joinedTournament.codigo}
                </div>
                <div>
                  <span className="text-gray-600">Total Jugadores:</span> {joinedTournament.jugadores?.length || 0}
                </div>
                <div>
                  <span className="text-gray-600">Case Individual:</span> ${joinedTournament.case_individual?.toLocaleString()}
                </div>
                <div>
                  <span className="text-gray-600">Multiplicador:</span> {joinedTournament.multiplicador}
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </MainLayout>
    )
  }

  return (
    <MainLayout 
      title="Panel de Jugador" 
      subtitle="Únete a un torneo con tu código"
    >
      <div className="space-y-6 max-w-md mx-auto">
        <Button onClick={() => router.push('/')}>
          ← Volver al Inicio
        </Button>

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
            {error}
          </div>
        )}

        <Card>
          <CardHeader className="text-center">
            <div className="text-6xl mb-4">🎯</div>
            <CardTitle className="text-2xl text-golf-green">
              Únete al Torneo
            </CardTitle>
            <CardDescription>
              Ingresa el código del torneo y tus datos
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="text-sm font-medium">Código del Torneo</label>
              <Input
                placeholder="Ej: ABC123"
                value={tournamentCode}
                onChange={(e) => setTournamentCode(e.target.value.toUpperCase())}
                className="text-center text-lg font-mono"
              />
            </div>
            
            <div>
              <label className="text-sm font-medium">Tu Nombre</label>
              <Input
                placeholder="Nombre completo"
                value={playerName}
                onChange={(e) => setPlayerName(e.target.value)}
              />
            </div>
            
            <div>
              <label className="text-sm font-medium">Tu Handicap</label>
              <Input
                type="number"
                placeholder="18"
                value={handicap}
                onChange={(e) => setHandicap(e.target.value)}
              />
            </div>
            
            <Button 
              onClick={handleJoinTournament}
              disabled={loading || !tournamentCode || !playerName || !handicap}
              className="w-full"
              size="lg"
            >
              {loading ? 'Uniéndose...' : 'Unirse al Torneo'}
            </Button>
          </CardContent>
        </Card>

        <Card className="bg-blue-50 border-blue-200">
          <CardContent className="pt-6">
            <div className="text-center text-sm text-blue-700">
              <div className="font-semibold mb-2">💡 ¿Cómo funciona?</div>
              <ol className="text-left space-y-1">
                <li>1. El administrador te dará un código de 6 caracteres</li>
                <li>2. Ingresa el código y tus datos</li>
                <li>3. Carga tu score cuando termines de jugar</li>
                <li>4. Ve el ranking en tiempo real</li>
              </ol>
            </div>
          </CardContent>
        </Card>
      </div>
    </MainLayout>
  )
}