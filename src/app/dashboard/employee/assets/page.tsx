// Employee Assigned Assets

"use client";

import { ProtectedRoute } from "@/components/ProtectedRoute";
import { Box, Typography, Paper, Alert } from "@mui/material";
import { Inventory as InventoryIcon } from "@mui/icons-material";

export default function EmployeeAssetsPage() {
  return (
    <ProtectedRoute requiredRole="Employee">
      <Box>
        <Typography variant="h4" sx={{ fontWeight: "bold", mb: 1 }}>
          Assigned Assets
        </Typography>
        <Typography color="textSecondary" sx={{ mb: 4 }}>
          View all assets assigned to you
        </Typography>

        <Alert severity="info" sx={{ mb: 3 }}>
          Asset management feature is coming soon!
        </Alert>

        <Paper sx={{ p: 6, textAlign: "center" }}>
          <InventoryIcon sx={{ fontSize: 64, color: "#9ca3af", mb: 2 }} />
          <Typography variant="h6" color="textSecondary">
            No assets assigned yet
          </Typography>
          <Typography color="textSecondary" sx={{ mt: 1 }}>
            Your assigned assets will appear here once the feature is implemented.
          </Typography>
        </Paper>
      </Box>
    </ProtectedRoute>
  );
}
