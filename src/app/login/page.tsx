/**
 * Login Page
 *
 * User authentication page with email and password login.
 * Handles form submission and redirects to appropriate dashboard on success.
 */

"use client";

import { useAuth } from "@/contexts/AuthContext";
import { useRouter } from "next/navigation";
import { useState } from "react";
import {
  Box,
  Container,
  Paper,
  TextField,
  Button,
  Typography,
  Alert,
  InputAdornment,
  IconButton,
  Stack,
} from "@mui/material";
import { Visibility, VisibilityOff } from "@mui/icons-material";

export default function LoginPage() {
  const { login } = useAuth();
  const router = useRouter();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      if (!email.trim()) {
        setError("Email is required");
        setLoading(false);
        return;
      }

      if (!password) {
        setError("Password is required");
        setLoading(false);
        return;
      }

      await login(email, password);
      
      // Success - redirect
      const storedUser = JSON.parse(localStorage.getItem("user") || "{}");
      if (storedUser.role === "Admin") {
        router.push("/dashboard/admin");
      } else if (storedUser.role === "HR") {
        router.push("/dashboard/hr");
      } else {
        router.push("/dashboard/employee");
      }
    } catch (err: any) {
      setLoading(false);
      const errorMessage = err?.response?.data?.error || err?.message || "Login failed. Please try again.";
      setError(errorMessage);
    }
  };

  const handleClickShowPassword = () => {
    setShowPassword(!showPassword);
  };

  const handleMouseDownPassword = (event: React.MouseEvent<HTMLButtonElement>) => {
    event.preventDefault();
  };

  return (
    <Box
      sx={{
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        background: "linear-gradient(to bottom right, #eff6ff, #e0e7ff)",
      }}
    >
      <Container maxWidth="sm">
        <Paper elevation={3} sx={{ p: 4, borderRadius: 2 }}>
          {/* Header */}
          <Box sx={{ mb: 4, textAlign: "center" }}>
            <Typography variant="h4" sx={{ fontWeight: "bold", mb: 1, color: "#1f2937" }}>
              DSPL Asset Pulse
            </Typography>
            <Typography variant="body1" color="textSecondary">
              Sign in to your account
            </Typography>
          </Box>

          {/* Error Message */}
          {error && (
            <Alert severity="error" sx={{ mb: 3 }}>
              {error}
            </Alert>
          )}

          {/* Login Form */}
          <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
            <Stack spacing={3}>
              {/* Email Field */}
              <TextField
                fullWidth
                label="Email Address"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@example.com"
                disabled={loading}
                variant="outlined"
              />

              {/* Password Field with Visibility Toggle */}
              <TextField
                fullWidth
                label="Password"
                type={showPassword ? "text" : "password"}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                disabled={loading}
                variant="outlined"
                InputProps={{
                  endAdornment: (
                    <InputAdornment position="end">
                      <IconButton
                        aria-label="toggle password visibility"
                        onClick={handleClickShowPassword}
                        onMouseDown={handleMouseDownPassword}
                        edge="end"
                        disabled={loading}
                      >
                        {showPassword ? <VisibilityOff /> : <Visibility />}
                      </IconButton>
                    </InputAdornment>
                  ),
                }}
              />

              {/* Submit Button */}
              <Button
                type="submit"
                fullWidth
                variant="contained"
                color="primary"
                disabled={loading}
                sx={{
                  fontWeight: 600,
                  fontSize: "1rem",
                  padding: "10px",
                }}
              >
                {loading ? "Signing in..." : "Sign In"}
              </Button>
            </Stack>
          </Box>

          {/* Demo Credentials */}
          <Alert severity="info" sx={{ mt: 4, mb: 2 }}>
            <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 1 }}>
              Demo Credentials:
            </Typography>
            <Typography variant="caption" display="block" sx={{ mb: 0.5 }}>
              <strong>Employee:</strong> employee@company.com / password123
            </Typography>
            <Typography variant="caption" display="block" sx={{ mb: 0.5 }}>
              <strong>HR:</strong> hr@company.com / password123
            </Typography>
            <Typography variant="caption" display="block">
              <strong>Admin:</strong> admin@company.com / password123
            </Typography>
          </Alert>

          {/* Footer */}
          <Typography
            variant="caption"
            sx={{
              display: "block",
              textAlign: "center",
              mt: 3,
              color: "#6b7280",
            }}
          >
            Development environment - SSO coming soon
          </Typography>
        </Paper>
      </Container>
    </Box>
  );
}
