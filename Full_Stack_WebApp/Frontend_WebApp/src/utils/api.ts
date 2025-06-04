import { Team, Match } from "../types";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export const getTeams = async (): Promise<Team[]> => {
  const response = await fetch(`${API_BASE_URL}/teams/`);
  if (!response.ok) {
    throw new Error("Failed to fetch teams");
  }
  return response.json();
};

export const getTeam = async (id: number): Promise<Team> => {
  const response = await fetch(`${API_BASE_URL}/teams/${id}/`);
  if (!response.ok) {
    throw new Error("Failed to fetch team");
  }
  return response.json();
};

export const getMatches = async (queryParams?: string): Promise<Match[]> => {
  const url = queryParams
    ? `${API_BASE_URL}/matches/?${queryParams}`
    : `${API_BASE_URL}/matches/`;

  const response = await fetch(url);
  if (!response.ok) {
    throw new Error("Failed to fetch matches");
  }
  return response.json();
};

export const getMatch = async (id: number): Promise<Match> => {
  const response = await fetch(`${API_BASE_URL}/matches/${id}/`);
  if (!response.ok) {
    throw new Error("Failed to fetch match");
  }
  return response.json();
};
