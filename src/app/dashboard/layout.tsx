/**
 * Dashboard Layout -> Includes header with user profile dropdown.
 */

"use client";

import { useAuth } from "@/contexts/AuthContext";
import { useRouter } from "next/navigation";
import { useState } from "react";
import {
  AppBar,
  Toolbar,
  Container,
  Box,
  Typography,
  Avatar,
  Menu,
  MenuItem,
  ListItemIcon,
  ListItemText,
  IconButton,
} from "@mui/material";
import { Person as PersonIcon, Logout as LogoutIcon } from "@mui/icons-material";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { user, logout, isAuthenticated } = useAuth();
  const router = useRouter();
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);

  const handleMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleProfile = () => {
    handleMenuClose();
    const profilePath = user?.role === "Admin" ? "/dashboard/admin/profile" : 
                        user?.role === "HR" ? "/dashboard/hr/profile" : 
                        "/dashboard/employee/profile";
    router.push(profilePath);
  };

  const handleLogout = () => {
    handleMenuClose();
    logout();
    router.push("/login");
  };

  const getInitials = (name: string | null, email: string) => {
    if (name) {
      return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
    }
    return email.slice(0, 2).toUpperCase();
  };

  if (!isAuthenticated || !user) {
    return null; // Will redirect via ProtectedRoute
  }

  return (
    <Box sx={{ display: "flex", flexDirection: "column", minHeight: "100vh", backgroundColor: "#f9fafb" }}>
      {/* AppBar Header */}
      <AppBar position="static" sx={{ backgroundColor: "#ffffff", color: "#1f2937", boxShadow: 1 }}>
        <Toolbar>
          <Typography variant="h6" sx={{ fontWeight: "bold", color: "#1f2937", flex: 1 }}>
            DSPL Asset Pulse
          </Typography>
          
          <IconButton onClick={handleMenuOpen} sx={{ display: "flex", gap: 1, borderRadius: 2, px: 1 }}>
            <Avatar sx={{ bgcolor: "#4f46e5", width: 36, height: 36, fontSize: "0.875rem" }}>
              {getInitials(user.name, user.email)}
            </Avatar>
            <Typography sx={{ color: "#1f2937", fontWeight: 500, display: { xs: "none", sm: "block" } }}>
              {user.name || user.email}
            </Typography>
          </IconButton>

          <Menu
            anchorEl={anchorEl}
            open={Boolean(anchorEl)}
            onClose={handleMenuClose}
            transformOrigin={{ horizontal: "right", vertical: "top" }}
            anchorOrigin={{ horizontal: "right", vertical: "bottom" }}
            sx={{ mt: 1 }}
          >
            <MenuItem onClick={handleProfile}>
              <ListItemIcon>
                <PersonIcon fontSize="small" />
              </ListItemIcon>
              <ListItemText>My Profile</ListItemText>
            </MenuItem>
            <MenuItem onClick={handleLogout}>
              <ListItemIcon>
                <LogoutIcon fontSize="small" color="error" />
              </ListItemIcon>
              <ListItemText>Logout</ListItemText>
            </MenuItem>
          </Menu>
        </Toolbar>
      </AppBar>

      {/* Main Content */}
      <Container maxWidth="lg" sx={{ py: 6, flex: 1 }}>
        {children}
      </Container>
    </Box>
  );
}
