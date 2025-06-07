import axios from "axios";
import { Match, Team, TeamStats, StatsOverview, ApiResponse } from "./types";

// Configure axios with base URL
const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
  timeout: 10000,
});

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("API Error:", error);
    return Promise.reject(error);
  }
);

export class PremierLeagueAPI {
  // Matches endpoints
  static async getMatches(params?: {
    page?: number;
    page_size?: number;
    season?: string;
    team?: string;
    date_from?: string;
    date_to?: string;
  }): Promise<ApiResponse<Match>> {
    const response = await api.get("/matches/", { params });
    return response.data;
  }

  static async getRecentMatches(): Promise<Match[]> {
    const response = await api.get("/matches/recent/");
    return response.data;
  }

  static async getMatchesBySeason(season: string): Promise<Match[]> {
    const response = await api.get("/matches/by_season/", {
      params: { season },
    });
    return response.data;
  }

  static async getFixtures(): Promise<Match[]> {
    const response = await api.get("/matches/fixtures/");
    return response.data;
  }

  // Teams endpoints
  static async getTeams(): Promise<Team[]> {
    const response = await api.get("/teams/");
    return response.data;
  }

  static async getTeamStats(
    teamId: number,
    season?: string
  ): Promise<TeamStats> {
    const params = season ? { season } : {};
    const response = await api.get(`/teams/${teamId}/stats/`, { params });
    return response.data;
  }

  static async getTeamMatches(
    teamId: number,
    season?: string,
    page?: number
  ): Promise<ApiResponse<Match>> {
    const params = { ...(season && { season }), ...(page && { page }) };
    const response = await api.get(`/teams/${teamId}/matches/`, { params });
    return response.data;
  }

  static async getLeagueTable(season?: string): Promise<TeamStats[]> {
    const params = season ? { season } : {};
    const response = await api.get("/teams/league_table/", { params });
    return response.data;
  }

  // Stats endpoints
  static async getStatsOverview(season?: string): Promise<StatsOverview> {
    const params = season ? { season } : {};
    const response = await api.get("/stats/overview/", { params });
    return response.data;
  }

  static async getSeasons(): Promise<string[]> {
    const response = await api.get("/stats/seasons/");
    return response.data;
  }
}

export default PremierLeagueAPI;
