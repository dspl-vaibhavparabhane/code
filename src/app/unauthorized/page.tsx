

"use client";

import { useAuth } from "@/contexts/AuthContext";
import { useRouter } from "next/navigation";
import {
  Box,
  Container,
  Paper,
  Typography,
  Button,
  Stack,
} from "@mui/material";
import { Lock as LockIcon, Logout as LogoutIcon } from "@mui/icons-material";

export default function UnauthorizedPage() {
  const { logout } = useAuth();
  const router = useRouter();

  const handleLogout = () => {
    logout();
    router.push("/login");
  };

  return (
    <Box
      sx={{
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        background: "linear-gradient(to bottom right, #fef2f2, #fed7aa)",
      }}
    >
      <Container maxWidth="sm">
        <Paper elevation={3} sx={{ p: 4, textAlign: "center", borderRadius: 2 }}>
          {/* Icon */}
          <Box sx={{ mb: 2 }}>
            <LockIcon
              sx={{
                fontSize: "4rem",
                color: "#dc2626",
              }}
            />
          </Box>

          {/* Error Code */}
          <Typography
            variant="h3"
            sx={{
              fontWeight: "bold",
              color: "#dc2626",
              mb: 1,
            }}
          >
            403
          </Typography>

          {/* Error Title */}
          <Typography
            variant="h5"
            sx={{
              fontWeight: "bold",
              color: "#1f2937",
              mb: 2,
            }}
          >
            Access Denied
          </Typography>

          {/* Error Message */}
          <Typography
            color="textSecondary"
            sx={{ mb: 4 }}
          >
            You do not have permission to access this page. Please contact your
            administrator if you believe this is a mistake.
          </Typography>

          {/* Action Buttons */}
          <Stack spacing={2} sx={{ mt: 4 }}>
            <Button
              variant="contained"
              color="primary"
              fullWidth
              onClick={() => router.push("/dashboard")}
              sx={{
                fontWeight: 600,
                padding: "10px",
              }}
            >
              Go to Dashboard
            </Button>

            <Button
              variant="outlined"
              color="error"
              fullWidth
              startIcon={<LogoutIcon />}
              onClick={handleLogout}
              sx={{
                fontWeight: 600,
                padding: "10px",
              }}
            >
              Logout
            </Button>
          </Stack>
        </Paper>
      </Container>
    </Box>
  );
}
