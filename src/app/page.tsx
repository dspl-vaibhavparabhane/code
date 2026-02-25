
//Root Page ->Redirects based on authentication status.


"use client";

import { useAuth } from "@/contexts/AuthContext";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { Box, Typography, CircularProgress } from "@mui/material";

export default function Home() {
  const { isAuthenticated, user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (loading) return;

    if (isAuthenticated && user) {
      // Redirect to appropriate dashboard based on role
      if (user.role === "Admin") {
        router.push("/dashboard/admin");
      } else if (user.role === "HR") {
        router.push("/dashboard/hr");
      } else {
        router.push("/dashboard/employee");
      }
    } else {
      // Redirect to login
      router.push("/login");
    }
  }, [isAuthenticated, user, loading, router]);

  return (
    <Box
      sx={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        minHeight: "100vh",
      }}
    >
      <Box sx={{ textAlign: "center" }}>
        <Typography variant="h5" sx={{ fontWeight: "bold", mb: 2 }}>
          Loading...
        </Typography>
        <Typography color="textSecondary" sx={{ mb: 2 }}>
          Redirecting to dashboard...
        </Typography>
        <CircularProgress />
      </Box>
    </Box>
  );
}
