// HR Dashboard Landing

"use client";

import { ProtectedRoute } from "@/components/ProtectedRoute";
import { Box, Typography, Grid } from "@mui/material";
import { DashboardCard } from "@/components/dashboard/DashboardCard";
import { People as PeopleIcon, MeetingRoom as MeetingRoomIcon, RoomPreferences as RoomIcon } from "@mui/icons-material";

export default function HRDashboardPage() {
  return (
    <ProtectedRoute requiredRole="HR">
      <Box>
        <Typography variant="h4" sx={{ fontWeight: "bold", mb: 1 }}>
          HR Dashboard
        </Typography>
        <Typography color="textSecondary" sx={{ mb: 4 }}>
          Manage employee records and information
        </Typography>

        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <DashboardCard
              title="Employee Management"
              description="View and manage all employee records"
              icon={<PeopleIcon sx={{ fontSize: 28 }} />}
              path="/dashboard/hr/employees"
              color="#4f46e5"
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <DashboardCard
              title="Room Bookings"
              description="View and manage all conference room bookings"
              icon={<MeetingRoomIcon sx={{ fontSize: 28 }} />}
              path="/dashboard/hr/bookings"
              color="#f59e0b"
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <DashboardCard
              title="Conference Rooms"
              description="Manage conference rooms"
              icon={<RoomIcon sx={{ fontSize: 28 }} />}
              path="/dashboard/hr/conference-rooms"
              color="#8b5cf6"
            />
          </Grid>
        </Grid>
      </Box>
    </ProtectedRoute>
  );
}
