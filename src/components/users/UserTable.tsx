import { useState } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  IconButton,
  TablePagination,
  TextField,
  Box,
  Stack,
  MenuItem,
  CircularProgress,
  Typography,
} from "@mui/material";
import { Edit as EditIcon, Delete as DeleteIcon } from "@mui/icons-material";
import { User, UserRole } from "@/types/user";
import { RoleChip } from "@/components/common/RoleChip";
import { StatusChip } from "@/components/common/StatusChip";

interface UserTableProps {
  users: User[];
  total: number;
  loading: boolean;
  page: number;
  rowsPerPage: number;
  onPageChange: (page: number) => void;
  onRowsPerPageChange: (rowsPerPage: number) => void;
  onEdit: (user: User) => void;
  onDelete?: (user: User) => void;
  onFilterChange: (filters: { role?: string; name?: string; email?: string }) => void;
  showDeleteAction?: boolean;
}

export function UserTable({
  users,
  total,
  loading,
  page,
  rowsPerPage,
  onPageChange,
  onRowsPerPageChange,
  onEdit,
  onDelete,
  onFilterChange,
  showDeleteAction = false,
}: UserTableProps) {
  const [filters, setFilters] = useState({ role: "", name: "", email: "" });

  const handleFilterChange = (field: string, value: string) => {
    const newFilters = { ...filters, [field]: value };
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  const formatDate = (date: string | null) => {
    if (!date) return "N/A";
    return new Date(date).toLocaleDateString();
  };

  return (
    <Paper sx={{ width: "100%" }}>
      <Box sx={{ p: 2 }}>
        <Stack direction={{ xs: "column", sm: "row" }} spacing={2}>
          <TextField
            size="small"
            label="Filter by Name"
            value={filters.name}
            onChange={(e) => handleFilterChange("name", e.target.value)}
            sx={{ flex: 1 }}
          />
          <TextField
            size="small"
            label="Filter by Email"
            value={filters.email}
            onChange={(e) => handleFilterChange("email", e.target.value)}
            sx={{ flex: 1 }}
          />
          {/* <TextField
            select
            size="small"
            label="Filter by Role"
            value={filters.role}
            onChange={(e) => handleFilterChange("role", e.target.value)}
            sx={{ flex: 1, minWidth: 150 }}
          >
            <MenuItem value="">All Roles</MenuItem>
            <MenuItem value="Employee">Employee</MenuItem>
            <MenuItem value="HR">HR</MenuItem>
            <MenuItem value="Admin">Admin</MenuItem>
          </TextField> */}
        </Stack>
      </Box>

      <TableContainer>
        <Table>
          <TableHead>
            <TableRow sx={{ backgroundColor: "#f9fafb" }}>
              <TableCell sx={{ fontWeight: 600 }}>Name</TableCell>
              <TableCell sx={{ fontWeight: 600 }}>Email</TableCell>
              <TableCell sx={{ fontWeight: 600 }}>Role</TableCell>
              <TableCell sx={{ fontWeight: 600 }}>Join Date</TableCell>
              <TableCell sx={{ fontWeight: 600 }}>Separation Date</TableCell>
              <TableCell sx={{ fontWeight: 600 }}>Status</TableCell>
              <TableCell sx={{ fontWeight: 600 }}>Created At</TableCell>
              <TableCell sx={{ fontWeight: 600 }} align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell colSpan={8} align="center" sx={{ py: 4 }}>
                  <CircularProgress />
                </TableCell>
              </TableRow>
            ) : users.length === 0 ? (
              <TableRow>
                <TableCell colSpan={8} align="center" sx={{ py: 4 }}>
                  <Typography color="textSecondary">No users found</Typography>
                </TableCell>
              </TableRow>
            ) : (
              users.map((user) => (
                <TableRow key={user.id} hover>
                  <TableCell>{user.name || "N/A"}</TableCell>
                  <TableCell>{user.email}</TableCell>
                  <TableCell>
                    <RoleChip role={user.role} />
                  </TableCell>
                  <TableCell>{formatDate(user.join_date)}</TableCell>
                  <TableCell>{formatDate(user.separation_date)}</TableCell>
                  <TableCell>
                    <StatusChip status={user.status} />
                  </TableCell>
                  <TableCell>{formatDate(user.created_at)}</TableCell>
                  <TableCell align="right">
                    <IconButton size="small" color="primary" onClick={() => onEdit(user)}>
                      <EditIcon fontSize="small" />
                    </IconButton>
                    {showDeleteAction && onDelete && (
                      <IconButton size="small" color="error" onClick={() => onDelete(user)}>
                        <DeleteIcon fontSize="small" />
                      </IconButton>
                    )}
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </TableContainer>

      <TablePagination
        component="div"
        count={total}
        page={page}
        onPageChange={(_, newPage) => onPageChange(newPage)}
        rowsPerPage={rowsPerPage}
        onRowsPerPageChange={(e) => onRowsPerPageChange(parseInt(e.target.value, 10))}
        rowsPerPageOptions={[5, 10, 25, 50]}
        labelRowsPerPage="Users per page:"
        labelDisplayedRows={({ page }) => `Page ${page + 1} of ${Math.ceil(total / rowsPerPage)}`}
      />
    </Paper>
  );
}
