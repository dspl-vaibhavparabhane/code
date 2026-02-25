// Admin HR Management

"use client";

import { ProtectedRoute } from "@/components/ProtectedRoute";
import { useAuth } from "@/contexts/AuthContext";
import * as usersService from "@/services/users";
import { useEffect, useState, useCallback } from "react";
import { Box, Button, Stack, Snackbar, Alert, Typography } from "@mui/material";
import { Add as AddIcon } from "@mui/icons-material";
import { User } from "@/types/user";
import { UserTable } from "@/components/users/UserTable";
import { CreateUserDialog } from "@/components/users/CreateUserDialog";
import { EditUserDialog } from "@/components/users/EditUserDialog";
import { DeleteConfirmDialog } from "@/components/users/DeleteConfirmDialog";

export default function AdminHRPage() {
  const { user } = useAuth();
  const [users, setUsers] = useState<User[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [filters, setFilters] = useState({ role: "HR", name: "", email: "" });
  const [createDialogOpen, setCreateDialogOpen] = useState(false);
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [snackbar, setSnackbar] = useState({ open: false, message: "", severity: "success" as "success" | "error" });

  const fetchUsers = useCallback(async () => {
    setLoading(true);
    try {
      const params: any = {
        offset: page * rowsPerPage,
        limit: rowsPerPage,
        role: "HR",
      };
      if (filters.name) params.name = filters.name;
      if (filters.email) params.email = filters.email;

      const response = await usersService.getUsers(params);
      setUsers(response.users);
      setTotal(response.total);
    } catch (err) {
      setSnackbar({ open: true, message: "Failed to fetch HR users", severity: "error" });
    } finally {
      setLoading(false);
    }
  }, [page, rowsPerPage, filters]);

  useEffect(() => {
    fetchUsers();
  }, [fetchUsers]);

  const handleCreateUser = async (payload: any) => {
    await usersService.createUser(payload);
    setSnackbar({ open: true, message: "HR user created successfully", severity: "success" });
    fetchUsers();
  };

  const handleEditUser = async (id: number, payload: any) => {
    await usersService.updateUser(id, payload);
    setSnackbar({ open: true, message: "HR user updated successfully", severity: "success" });
    fetchUsers();
  };

  const handleDeleteUser = async (id: number) => {
    await usersService.deleteUser(id);
    setSnackbar({ open: true, message: "HR user deleted successfully", severity: "success" });
    fetchUsers();
  };

  return (
    <ProtectedRoute requiredRole="Admin">
      <Stack spacing={3}>
        <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <Box>
            <Typography variant="h4" sx={{ fontWeight: "bold" }}>
              HR Management
            </Typography>
            <Typography color="textSecondary">Manage all HR personnel</Typography>
          </Box>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => setCreateDialogOpen(true)}
          >
            Create HR User
          </Button>
        </Box>

        <UserTable
          users={users}
          total={total}
          loading={loading}
          page={page}
          rowsPerPage={rowsPerPage}
          onPageChange={setPage}
          onRowsPerPageChange={(rows) => {
            setRowsPerPage(rows);
            setPage(0);
          }}
          onEdit={(user) => {
            setSelectedUser(user);
            setEditDialogOpen(true);
          }}
          onDelete={(user) => {
            setSelectedUser(user);
            setDeleteDialogOpen(true);
          }}
          onFilterChange={(newFilters) => {
            setFilters({
              role: "HR",
              name: newFilters.name || "",
              email: newFilters.email || ""
            });
            setPage(0);
          }}

          showDeleteAction
        />

        <CreateUserDialog
          open={createDialogOpen}
          onClose={() => setCreateDialogOpen(false)}
          onSubmit={handleCreateUser}
          currentUserRole={user?.role || null}
        />

        <EditUserDialog
          open={editDialogOpen}
          user={selectedUser}
          onClose={() => {
            setEditDialogOpen(false);
            setSelectedUser(null);
          }}
          onSubmit={handleEditUser}
          currentUserRole={user?.role || null}
        />

        <DeleteConfirmDialog
          open={deleteDialogOpen}
          user={selectedUser}
          onClose={() => {
            setDeleteDialogOpen(false);
            setSelectedUser(null);
          }}
          onConfirm={handleDeleteUser}
        />

        <Snackbar
          open={snackbar.open}
          autoHideDuration={4000}
          onClose={() => setSnackbar({ ...snackbar, open: false })}
          anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
        >
          <Alert onClose={() => setSnackbar({ ...snackbar, open: false })} severity={snackbar.severity}>{snackbar.message}</Alert>
        </Snackbar>
      </Stack>
    </ProtectedRoute>
  );
}
