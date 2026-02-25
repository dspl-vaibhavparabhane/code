/**
 * Users API Service
 */

import apiClient from "./api";
import { User, UsersListResponse, CreateUserPayload, UpdateUserPayload } from "@/types/user";

export interface GetUsersParams {
  role?: string;
  name?: string;
  email?: string;
  offset?: number;
  limit?: number;
  sort_by?: string;
  order?: "asc" | "desc";
}

export async function getUsers(params?: GetUsersParams): Promise<UsersListResponse> {
  const response = await apiClient.get<UsersListResponse>("/users", { params });
  return response.data;
}

export async function getUserById(id: number): Promise<{ user: User }> {
  const response = await apiClient.get<{ user: User }>(`/users/${id}`);
  return response.data;
}

export async function createUser(payload: CreateUserPayload): Promise<{ message: string; user: User }> {
  const response = await apiClient.post<{ message: string; user: User }>("/users", payload);
  return response.data;
}

export async function updateUser(id: number, payload: UpdateUserPayload): Promise<{ message: string; user: User }> {
  const response = await apiClient.put<{ message: string; user: User }>(`/users/${id}`, payload);
  return response.data;
}

export async function deleteUser(id: number): Promise<{ message: string }> {
  const response = await apiClient.delete<{ message: string }>(`/users/${id}`);
  return response.data;
}
