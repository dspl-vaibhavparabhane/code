/*
 * Provides global authentication state and utility functions.
 * Handles login, logout, token refresh, and user data management.
 */

"use client";

import React, { createContext, useContext, useState, useCallback, useEffect } from "react";
import * as authService from "@/services/auth";

export type UserRole = "Employee" | "HR" | "Admin";

export interface User {
  id: number;
  email: string;
  name: string | null;
  role: UserRole | null;
  created_at: string;
  updated_at: string;
}

export interface AuthContextType {
  // State
  isAuthenticated: boolean;
  user: User | null;
  loading: boolean;
  accessToken: string | null;
  refreshToken: string | null;

  // Methods
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  refreshAccessToken: () => Promise<void>;
  isSessionValid: () => boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [refreshToken, setRefreshToken] = useState<string | null>(null);

  // Initialize auth state from localStorage on mount
  useEffect(() => {
    const initAuthState = () => {
      const storedAccessToken = localStorage.getItem("accessToken");
      const storedRefreshToken = localStorage.getItem("refreshToken");
      const storedUser = localStorage.getItem("user");

      if (storedAccessToken && storedRefreshToken && storedUser) {
        setAccessToken(storedAccessToken);
        setRefreshToken(storedRefreshToken);
        setUser(JSON.parse(storedUser));
        setIsAuthenticated(true);
      }

      setLoading(false);
    };

    initAuthState();
  }, []);

  // Check if session is still valid
  const isSessionValid = useCallback((): boolean => {
    return isAuthenticated && accessToken !== null && user !== null;
  }, [isAuthenticated, accessToken, user]);

  // Login function
  const login = useCallback(async (email: string, password: string) => {
    try {
      const response = await authService.login(email, password);

      const { access_token, refresh_token, user: userData } = response;

      // Store tokens and user data
      localStorage.setItem("accessToken", access_token);
      localStorage.setItem("refreshToken", refresh_token);
      localStorage.setItem("user", JSON.stringify(userData));

      // Update state
      setAccessToken(access_token);
      setRefreshToken(refresh_token);
      setUser(userData);
      setIsAuthenticated(true);
    } catch (error) {
      // Don't update state on error - keep existing state
      throw error;
    }
  }, []);

  // Logout function
  const logout = useCallback(() => {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
    localStorage.removeItem("user");

    setIsAuthenticated(false);
    setAccessToken(null);
    setRefreshToken(null);
    setUser(null);
  }, []);

  // Refresh access token
  const refreshAccessToken = useCallback(async () => {
    if (!refreshToken) {
      logout();
      throw new Error("No refresh token available");
    }

    try {
      const response = await authService.refreshAccessToken(refreshToken);

      const { access_token } = response;

      // Update token in storage and state
      localStorage.setItem("accessToken", access_token);
      setAccessToken(access_token);
    } catch (error) {
      // If refresh fails, logout user
      logout();
      throw error;
    }
  }, [refreshToken, logout]);

  const value: AuthContextType = {
    isAuthenticated,
    user,
    loading,
    accessToken,
    refreshToken,
    login,
    logout,
    refreshAccessToken,
    isSessionValid,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

/**
 * Custom hook to use authentication context
 *
 * @throws {Error} If used outside of AuthProvider
 */
export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
