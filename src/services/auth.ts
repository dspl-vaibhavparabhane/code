/**
 * Authentication Service
 *
 * Handles all authentication-related API calls.
 * Exports plain functions for login and token refresh.
 */

import { UserRole } from "@/contexts/AuthContext";
import apiClient from "./api";

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  message?: string;
  user: {
    id: number;
    email: string;
    name: string | null;
    role: UserRole | null;
    created_at: string;
    updated_at: string;
  };
}

export interface RefreshTokenResponse {
  access_token: string;
  message?: string;
}

/**
 * Login with email and password
 * @param email - User email
 * @param password - User password
 * @returns Login response with tokens and user data
 */
export async function login(
  email: string,
  password: string
): Promise<LoginResponse> {
  const response = await apiClient.post<LoginResponse>("/auth/login", {
    email,
    password,
  });
  return response.data;
}

/**
 * Refresh access token using refresh token
 * @param refreshToken - The refresh token
 * @returns New access token
 */
export async function refreshAccessToken(
  refreshToken: string
): Promise<RefreshTokenResponse> {
  const response = await apiClient.post<RefreshTokenResponse>(
    "/auth/refresh",
    { refresh_token: refreshToken }
  );
  return response.data;
}
