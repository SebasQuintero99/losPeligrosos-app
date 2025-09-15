// ========== ENUMS ==========

export enum TournamentType {
  REGULAR = 'regular',
  PELIGROSO = 'peligroso'
}

export enum TournamentStatus {
  ACTIVE = 'active',
  COMPLETED = 'completed',
  CANCELLED = 'cancelled'
}

export enum UserRole {
  ADMIN = 'admin',
  PLAYER = 'player'
}

// ========== BASE INTERFACES ==========

export interface Tournament {
  id: number
  name: string
  code: string
  tournament_type: TournamentType
  status: TournamentStatus
  case_individual: number
  multiplicador: number
  created_at: string
  updated_at?: string
  completed_at?: string
  total_players?: number
  players_with_scores?: number
  players?: Player[]
}

export interface Player {
  id: number
  name: string
  handicap: number
  tournament_id: number
  gross1?: number
  gross2?: number
  gross_total?: number
  neto?: number
  putts?: number
  neto2?: number
  paga_neto: number
  paga_putts: number
  total_a_pagar: number
  scores_submitted: boolean
  is_active: boolean
  created_at: string
  scores_submitted_at?: string
}

// ========== FORM SCHEMAS ==========

export interface TournamentCreate {
  name: string
  tournament_type: TournamentType
}

export interface PlayerJoin {
  name: string
  handicap: number
  tournament_code: string
}

export interface PlayerScoreSubmission {
  gross1: number
  gross2: number
  putts: number
}

// ========== RANKING INTERFACES ==========

export interface PlayerRanking {
  position: number
  id: number
  name: string
  handicap: number
  neto?: number
  putts?: number
  gross_total?: number
  scores_submitted: boolean
}

export interface TournamentRankings {
  neto_ranking: PlayerRanking[]
  putts_ranking: PlayerRanking[]
}

// ========== LIQUIDATION INTERFACES ==========

export interface LiquidationSummary {
  total_jugadores: number
  total_case: number
  total_pagos: number
  total_recaudo: number
  atencion: number
  premios: number
  menor_neto: number
  menor_putts: number
  ganador_neto: string
  ganador_putts: string
}

export interface PrizeWinner {
  posicion: number
  nombre: string
  neto: number
  monto: number
}

export interface PrizeDistribution {
  regla: string
  ganadores: PrizeWinner[]
  top5?: Array<{
    posicion: number
    nombre: string
    neto: number
  }>
}

export interface TournamentLiquidation {
  players_liquidation: Player[]
  summary: LiquidationSummary
  premios_distribucion: PrizeDistribution
  rankings: {
    neto: Player[]
    putts: Player[]
  }
}

// ========== UI STATE INTERFACES ==========

export interface AppState {
  currentUser: {
    role: UserRole
    playerId?: number
    tournamentId?: number
  } | null
  isLoading: boolean
  error: string | null
}

export interface TournamentState {
  currentTournament: Tournament | null
  players: Player[]
  rankings: TournamentRankings | null
  liquidation: TournamentLiquidation | null
}

// ========== COMPONENT PROPS ==========

export interface LayoutProps {
  children: React.ReactNode
  title?: string
  showNavigation?: boolean
}

export interface CardProps {
  children: React.ReactNode
  className?: string
  title?: string
}

export interface ButtonProps {
  children: React.ReactNode
  onClick?: () => void
  variant?: 'primary' | 'secondary' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
  loading?: boolean
  className?: string
}

// ========== API RESPONSE TYPES ==========

export interface ApiResponse<T> {
  data: T
  message?: string
  success: boolean
}

export interface ApiError {
  detail: string
  status_code: number
}

export interface JoinTournamentResponse {
  success: boolean
  player: Player
  tournament: {
    id: number
    name: string
    type: TournamentType
  }
}

export interface SubmitScoresResponse {
  success: boolean
  player: Player
  message: string
}

// ========== FORM VALIDATION ==========

export interface FormErrors {
  [key: string]: string | undefined
}

export interface ValidationRule {
  required?: boolean
  min?: number
  max?: number
  pattern?: RegExp
  custom?: (value: any) => string | undefined
}