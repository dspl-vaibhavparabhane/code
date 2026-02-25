// HR Profile

"use client";

import { ProtectedRoute } from "@/components/ProtectedRoute";
import { useAuth } from "@/contexts/AuthContext";
import * as usersService from "@/services/users";
import { useEffect, useState } from "react";
import { Box, Stack, CircularProgress, Alert, Typography } from "@mui/material";
import { User } from "@/types/user";
import { UserProfileCard } from "@/components/users/UserProfileCard";

export default function HRProfilePage() {
  const { user: authUser } = useAuth();
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchUserProfile = async () => {
      if (!authUser?.id) return;

      try {
        const response = await usersService.getUserById(authUser.id);
        setUser(response.user);
      } catch (err: any) {
        setError(err.response?.data?.error || "Failed to fetch profile");
      } finally {
        setLoading(false);
      }
    };

    fetchUserProfile();
  }, [authUser]);

  return (
    <ProtectedRoute requiredRole="HR">
      <Stack spacing={3}>
        <Box>
          <Typography variant="h4" sx={{ fontWeight: "bold" }}>
            My Profile
          </Typography>
          <Typography color="textSecondary">View your profile information</Typography>
        </Box>

        {loading && (
          <Box sx={{ display: "flex", justifyContent: "center", py: 4 }}>
            <CircularProgress />
          </Box>
        )}

        {error && <Alert severity="error">{error}</Alert>}

        {user && <UserProfileCard user={user} />}
      </Stack>
    </ProtectedRoute>
  );
}
