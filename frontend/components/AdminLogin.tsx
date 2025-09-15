import { useState } from 'react'
import { Button } from './ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { Input } from './ui/input'
import { apiClient } from '../lib/api-client'

interface AdminLoginProps {
  onLoginSuccess: () => void
  onBack: () => void
}

export default function AdminLogin({ onLoginSuccess, onBack }: AdminLoginProps) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!username.trim() || !password.trim()) {
      setError('Por favor ingresa usuario y contraseña')
      return
    }

    setLoading(true)
    setError('')

    try {
      await apiClient.login(username, password)
      onLoginSuccess()
    } catch (error: any) {
      setError(error.message || 'Error de autenticación')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <div className="text-6xl mb-4">🔐</div>
          <CardTitle className="text-2xl text-golf-green">
            Login Administrador
          </CardTitle>
          <CardDescription>
            Ingresa tus credenciales para gestionar torneos
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">
                Usuario
              </label>
              <Input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Ingresa tu usuario"
                disabled={loading}
                autoComplete="username"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">
                Contraseña
              </label>
              <Input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Ingresa tu contraseña"
                disabled={loading}
                autoComplete="current-password"
              />
            </div>

            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-3">
                <p className="text-sm text-red-700">{error}</p>
              </div>
            )}

            <Button
              type="submit"
              className="w-full"
              disabled={loading}
            >
              {loading ? '🔄 Iniciando sesión...' : '🔐 Iniciar Sesión'}
            </Button>

            <Button
              type="button"
              variant="outline"
              className="w-full"
              onClick={onBack}
              disabled={loading}
            >
              ← Volver
            </Button>
          </form>

          <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <p className="text-xs text-blue-700 font-semibold mb-2">
              Usuarios de prueba:
            </p>
            <div className="text-xs text-blue-600 space-y-1">
              <div><strong>admin</strong> / secret</div>
              <div><strong>juan</strong> / golf123</div>
              <div><strong>los_peligrosos</strong> / neiva2024</div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}