/**
 * User Types
 */

export type UserRole = "Employee" | "HR" | "Admin";
export type UserStatus = "active" | "separated";

export interface User {
  id: number;
  email: string;
  name: string | null;
  role: UserRole | null;
  join_date: string | null;
  separation_date: string | null;
  status: UserStatus | null;
  created_at: string;
  updated_at: string;
}

export interface UsersListResponse {
  total: number;
  offset: number;
  limit: number;
  users: User[];
}

export interface CreateUserPayload {
  email: string;
  password: string;
  name: string;
  role: UserRole;
  join_date: string;
  separation_date?: string;
  status: UserStatus;
}

export interface UpdateUserPayload {
  name?: string;
  email?: string;
  role?: UserRole;
  join_date?: string;
  separation_date?: string;
  status?: UserStatus;
}
