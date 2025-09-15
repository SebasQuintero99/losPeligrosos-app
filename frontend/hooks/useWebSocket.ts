import { useEffect, useRef, useCallback } from 'react'

export interface WebSocketMessage {
  type: 'tournament_created' | 'player_joined' | 'scores_updated' | 'liquidation_calculated' | 'liquidation_auto_calculated'
  tournament_id?: number
  tournament?: any
  player?: any
  liquidation?: any
}

export function useWebSocket(
  tournamentId: number | null, 
  onMessage: (message: WebSocketMessage) => void
) {
  const ws = useRef<WebSocket | null>(null)
  const reconnectTimeoutRef = useRef<NodeJS.Timeout>()
  
  const connect = useCallback(() => {
    if (!tournamentId) return
    
    try {
      // Close existing connection
      if (ws.current) {
        ws.current.close()
      }
      
      // Create new connection
      ws.current = new WebSocket(`ws://localhost:8001/ws/tournament/${tournamentId}`)
      
      ws.current.onopen = () => {
        console.log(`🔗 WebSocket connected to tournament ${tournamentId}`)
      }
      
      ws.current.onmessage = (event) => {
        try {
          const message: WebSocketMessage = JSON.parse(event.data)
          console.log('📨 WebSocket message received:', message)
          onMessage(message)
        } catch (error) {
          console.error('❌ Error parsing WebSocket message:', error)
        }
      }
      
      ws.current.onclose = () => {
        console.log(`❌ WebSocket disconnected from tournament ${tournamentId}`)
        // Auto-reconnect after 3 seconds
        reconnectTimeoutRef.current = setTimeout(() => {
          console.log('🔄 Attempting to reconnect WebSocket...')
          connect()
        }, 3000)
      }
      
      ws.current.onerror = (error) => {
        console.error('❌ WebSocket error:', error)
      }
    } catch (error) {
      console.error('❌ Failed to create WebSocket connection:', error)
    }
  }, [tournamentId, onMessage])
  
  const disconnect = useCallback(() => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current)
    }
    
    if (ws.current) {
      ws.current.close()
      ws.current = null
    }
  }, [])
  
  const sendMessage = useCallback((message: any) => {
    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify(message))
    }
  }, [])
  
  useEffect(() => {
    if (tournamentId) {
      connect()
    }
    
    return () => {
      disconnect()
    }
  }, [tournamentId, connect, disconnect])
  
  return {
    sendMessage,
    disconnect,
    isConnected: ws.current?.readyState === WebSocket.OPEN
  }
}