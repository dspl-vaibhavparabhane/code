

"use client";

import { useAuth, UserRole } from "@/contexts/AuthContext";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { Box, CircularProgress, Typography } from "@mui/material";

interface ProtectedRouteProps {
  children: React.ReactNode;
  requiredRole?: UserRole;
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
  children,
  requiredRole,
}) => {
  const { isAuthenticated, user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (loading) return; // Wait for auth state to load

    // Redirect if not authenticated
    if (!isAuthenticated) {
      router.push("/login");
      return;
    }

    // Redirect if role doesn't match (if required role is specified)
    if (requiredRole && user?.role !== requiredRole) {
      router.push("/unauthorized");
      return;
    }
  }, [isAuthenticated, user, loading, requiredRole, router]);

  // Show loading state
  if (loading) {
    return (
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          minHeight: "100vh",
        }}
      >
        <CircularProgress />
      </Box>
    );
  }

  // Show unauthorized if not authenticated or wrong role
  if (
    !isAuthenticated ||
    (requiredRole && user?.role !== requiredRole)
  ) {
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
            Access Denied
          </Typography>
          <Typography color="textSecondary">
            You do not have permission to access this page.
          </Typography>
        </Box>
      </Box>
    );
  }

  // Render protected content
  return <>{children}</>;
};
