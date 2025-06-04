export interface Team {
  id: number;
  name: string;
  shortName: string;
  logo?: string;
  stadium: string;
  city: string;
  founded: number;
  website?: string;
}

export interface Match {
  id: number;
  homeTeam: Team;
  awayTeam: Team;
  homeScore: number | null;
  awayScore: number | null;
  date: string;
  status: "scheduled" | "in_progress" | "completed" | "cancelled";
  competition: string;
  season: string;
  round: string;
  venue: string;
}

export interface Prediction {
  id: number;
  match: Match;
  homeScore: number;
  awayScore: number;
  confidence: number;
  createdAt: string;
  updatedAt: string;
}
