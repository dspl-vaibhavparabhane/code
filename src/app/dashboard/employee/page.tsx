// Employee Dashboard Landing

"use client";

import { ProtectedRoute } from "@/components/ProtectedRoute";
import { Box, Typography, Grid } from "@mui/material";
import { DashboardCard } from "@/components/dashboard/DashboardCard";
import { Inventory as InventoryIcon, MeetingRoom as MeetingRoomIcon } from "@mui/icons-material";

export default function EmployeeDashboardPage() {
  return (
    <ProtectedRoute requiredRole="Employee">
      <Box>
        <Typography variant="h4" sx={{ fontWeight: "bold", mb: 1 }}>
          Employee Dashboard
        </Typography>
        <Typography color="textSecondary" sx={{ mb: 4 }}>
          View your assigned assets and information
        </Typography>

        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <DashboardCard
              title="Assigned Assets"
              description="View all assets assigned to you"
              icon={<InventoryIcon sx={{ fontSize: 28 }} />}
              path="/dashboard/employee/assets"
              color="#10b981"
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <DashboardCard
              title="Room Bookings"
              description="Book conference rooms and view your bookings"
              icon={<MeetingRoomIcon sx={{ fontSize: 28 }} />}
              path="/dashboard/employee/bookings"
              color="#f59e0b"
            />
          </Grid>
        </Grid>
      </Box>
    </ProtectedRoute>
  );
}
