// Admin Dashboard Landing

"use client";

import { ProtectedRoute } from "@/components/ProtectedRoute";
import { Box, Typography, Grid } from "@mui/material";
import { DashboardCard } from "@/components/dashboard/DashboardCard";
import { People as PeopleIcon, SupervisorAccount as SupervisorIcon, MeetingRoom as MeetingRoomIcon, RoomPreferences as RoomIcon } from "@mui/icons-material";

export default function AdminDashboardPage() {
  return (
    <ProtectedRoute requiredRole="Admin">
      <Box>
        <Typography variant="h4" sx={{ fontWeight: "bold", mb: 1 }}>
          Admin Dashboard
        </Typography>
        <Typography color="textSecondary" sx={{ mb: 4 }}>
          Manage employees and HR personnel
        </Typography>

        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <DashboardCard
              title="Employee Management"
              description="View and manage all employee records"
              icon={<PeopleIcon sx={{ fontSize: 28 }} />}
              path="/dashboard/admin/employees"
              color="#4f46e5"
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <DashboardCard
              title="HR Management"
              description="View and manage HR personnel"
              icon={<SupervisorIcon sx={{ fontSize: 28 }} />}
              path="/dashboard/admin/hr"
              color="#ec4899"
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <DashboardCard
              title="Admin Management"
              description="View and manage admin users"
              icon={<SupervisorIcon sx={{ fontSize: 28 }} />}
              path="/dashboard/admin/admins"
              color="#10b981"
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <DashboardCard
              title="Room Bookings"
              description="View and manage all conference room bookings"
              icon={<MeetingRoomIcon sx={{ fontSize: 28 }} />}
              path="/dashboard/admin/bookings"
              color="#f59e0b"
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <DashboardCard
              title="Conference Rooms"
              description="Manage conference rooms"
              icon={<RoomIcon sx={{ fontSize: 28 }} />}
              path="/dashboard/admin/conference-rooms"
              color="#8b5cf6"
            />
          </Grid>
        </Grid>
      </Box>
    </ProtectedRoute>
  );
}
