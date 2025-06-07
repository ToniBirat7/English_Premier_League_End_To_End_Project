// Types for Premier League data
export interface Match {
  id: number;
  date: string;
  home_team: string;
  away_team: string;
  fthg: number;
  ftag: number;
  ftr: "H" | "A" | "D";
  season: string;
  matchweek: number;
}

export interface Team {
  id: number;
  name: string;
  short_name: string;
  logo_url?: string;
  stadium?: string;
  city?: string;
}

export interface TeamStats {
  team: Team;
  position: number;
  matches_played: number;
  wins: number;
  draws: number;
  losses: number;
  goals_for: number;
  goals_against: number;
  goal_difference: number;
  points: number;
}

export interface StatsOverview {
  total_matches: number;
  total_goals: number;
  average_goals_per_match: number;
  home_wins: number;
  away_wins: number;
  draws: number;
  home_win_percentage: number;
  away_win_percentage: number;
  draw_percentage: number;
  top_scoring_teams: Array<{
    team: string;
    goals: number;
  }>;
  season: string;
}

export interface ApiResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}
