import axios from "axios";

const API_BASE_URL = "http://localhost:8000/api";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Types based on your Django API
export interface Team {
  id: number;
  name: string;
  short_name: string;
  founded?: number;
  stadium?: string;
  city?: string;
  logo_url?: string;
}

export interface Match {
  id: number;
  date: string;
  home_team: string;
  away_team: string;
  fthg: number;
  ftag: number;
  ftr: string;
  season: string;
  matchweek: number;
}

export interface DetailedMatch {
  id: number;
  date: string;
  home_team_name: string;
  away_team_name: string;
  fthg: number;
  ftag: number;
  ftr: string;
  season: string;
  matchweek: number;
}

export interface StandingsTeam extends Team {
  matches_played: number;
  wins: number;
  draws: number;
  losses: number;
  goals_for: number;
  goals_against: number;
  goal_difference: number;
  points: number;
  position: number;
}

export interface MatchStatistics {
  possession: { home: number; away: number };
  shots: { home: number; away: number };
  shots_on_target: { home: number; away: number };
  corners: { home: number; away: number };
  fouls: { home: number; away: number };
  yellow_cards: { home: number; away: number };
  red_cards: { home: number; away: number };
}

export interface MatchDetails {
  match: DetailedMatch;
  statistics: MatchStatistics;
}

export interface ApiResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

// API Functions
export const teamsApi = {
  // Get all teams
  getTeams: async (): Promise<ApiResponse<Team>> => {
    const response = await api.get("/teams/");
    return response.data;
  },

  // Get league standings
  getStandings: async (season?: string): Promise<StandingsTeam[]> => {
    const params = season ? { season } : {};
    const response = await api.get("/teams/standings/", { params });
    return response.data;
  },

  // Get team matches
  getTeamMatches: async (
    teamId: number,
    season?: string
  ): Promise<ApiResponse<Match>> => {
    const params = season ? { season } : {};
    const response = await api.get(`/teams/${teamId}/matches/`, { params });
    return response.data;
  },

  // Get available seasons
  getSeasons: async (): Promise<string[]> => {
    const response = await api.get("/matches/seasons/");
    return response.data;
  },
};

export const matchesApi = {
  // Get all matches with pagination
  getMatches: async (
    page?: number,
    season?: string,
    team?: string
  ): Promise<ApiResponse<Match>> => {
    const params: any = {};
    if (page) params.page = page;
    if (season) params.season = season;
    if (team) params.team = team;

    const response = await api.get("/matches/", { params });
    return response.data;
  },

  // Get recent matches
  getRecentMatches: async (): Promise<Match[]> => {
    const response = await api.get("/matches/recent/");
    return response.data;
  },

  // Get match details with statistics
  getMatchDetails: async (matchId: number): Promise<MatchDetails> => {
    const response = await api.get("/matches/match_detail/", {
      params: { match_id: matchId },
    });
    return response.data;
  },
};

// Helper functions
export const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleDateString("en-GB", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  });
};

export const formatTime = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleTimeString("en-GB", {
    hour: "2-digit",
    minute: "2-digit",
  });
};

export const getResultClass = (result: string): "green" | "red" | "yellow" => {
  switch (result) {
    case "H":
      return "green"; // Home win
    case "A":
      return "red"; // Away win
    case "D":
      return "yellow"; // Draw
    default:
      return "yellow";
  }
};

export const getTeamLogo = (teamName: string): string => {
  // You can replace this with actual team logo URLs
  const teamLogos: { [key: string]: string } = {
    Arsenal: "/logos/arsenal.png",
    Chelsea: "/logos/chelsea.png",
    Liverpool: "/logos/liverpool.png",
    "Man City": "/logos/man-city.png",
    "Man United": "/logos/man-united.png",
    Tottenham: "/logos/tottenham.png",
    Brighton: "/logos/brighton.png",
    Newcastle: "/logos/newcastle.png",
    "West Ham": "/logos/west-ham.png",
    "Aston Villa": "/logos/aston-villa.png",
    // Add more teams as needed
  };

  return teamLogos[teamName] || "/logos/default-team.png";
};
