"use client";

import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  TableSortLabel,
  Paper,
  TextField,
  Box,
  Chip,
  IconButton,
  Tooltip,
  CircularProgress,
  MenuItem,
} from "@mui/material";
import { Edit, Delete } from "@mui/icons-material";
import { ConferenceRoom } from "@/types/booking";
import { useState } from "react";

interface ConferenceRoomsTableProps {
  rooms: ConferenceRoom[];
  total: number;
  loading: boolean;
  page: number;
  rowsPerPage: number;
  onPageChange: (page: number) => void;
  onRowsPerPageChange: (rows: number) => void;
  onEdit: (room: ConferenceRoom) => void;
  onDelete: (roomId: number) => void;
  onFilterChange: (filters: { search: string; availability: string }) => void;
}

type Order = "asc" | "desc";
type OrderBy = "name" | "capacity" | "location";

export function ConferenceRoomsTable({
  rooms,
  total,
  loading,
  page,
  rowsPerPage,
  onPageChange,
  onRowsPerPageChange,
  onEdit,
  onDelete,
  onFilterChange,
}: ConferenceRoomsTableProps) {
  const [filters, setFilters] = useState({ search: "", availability: "all" });
  const [order, setOrder] = useState<Order>("asc");
  const [orderBy, setOrderBy] = useState<OrderBy>("name");

  const handleFilterChange = (field: string, value: string) => {
    const newFilters = { ...filters, [field]: value };
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  const handleSort = (property: OrderBy) => {
    const isAsc = orderBy === property && order === "asc";
    setOrder(isAsc ? "desc" : "asc");
    setOrderBy(property);
  };

  const sortedRooms = [...rooms].sort((a, b) => {
    let aValue: any = a[orderBy];
    let bValue: any = b[orderBy];

    if (orderBy === "capacity") {
      aValue = Number(aValue);
      bValue = Number(bValue);
    }

    if (order === "asc") {
      return aValue > bValue ? 1 : -1;
    } else {
      return aValue < bValue ? 1 : -1;
    }
  });

  return (
    <Paper>
      <Box sx={{ p: 2 }}>
        <Box sx={{ display: "flex", gap: 2, mb: 2 }}>
          <TextField
            select
            size="small"
            label="Filter by availability"
            value={filters.availability}
            onChange={(e) => handleFilterChange("availability", e.target.value)}
            sx={{ minWidth: 200 }}
          >
            <MenuItem value="all">All</MenuItem>
            <MenuItem value="available">Available</MenuItem>
            <MenuItem value="unavailable">Unavailable</MenuItem>
          </TextField>
          <TextField
            size="small"
            label="Search by name or location"
            value={filters.search}
            onChange={(e) => handleFilterChange("search", e.target.value)}
            sx={{ flex: 1 }}
          />
        </Box>
      </Box>

      <TableContainer>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>
                <TableSortLabel
                  active={orderBy === "name"}
                  direction={orderBy === "name" ? order : "asc"}
                  onClick={() => handleSort("name")}
                >
                  Name
                </TableSortLabel>
              </TableCell>
              <TableCell>
                <TableSortLabel
                  active={orderBy === "capacity"}
                  direction={orderBy === "capacity" ? order : "asc"}
                  onClick={() => handleSort("capacity")}
                >
                  Capacity
                </TableSortLabel>
              </TableCell>
              <TableCell>
                <TableSortLabel
                  active={orderBy === "location"}
                  direction={orderBy === "location" ? order : "asc"}
                  onClick={() => handleSort("location")}
                >
                  Location
                </TableSortLabel>
              </TableCell>
              <TableCell>Available</TableCell>
              <TableCell>Created</TableCell>
              <TableCell align="center">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell colSpan={6} align="center" sx={{ py: 4 }}>
                  <CircularProgress />
                </TableCell>
              </TableRow>
            ) : sortedRooms.length === 0 ? (
              <TableRow>
                <TableCell colSpan={6} align="center" sx={{ py: 4 }}>
                  No conference rooms found
                </TableCell>
              </TableRow>
            ) : (
              sortedRooms.map((room) => (
                <TableRow key={room.id} hover>
                  <TableCell>{room.name}</TableCell>
                  <TableCell>{room.capacity}</TableCell>
                  <TableCell>{room.location}</TableCell>
                  <TableCell>
                    <Chip
                      label={room.is_active ? "Available" : "Unavailable"}
                      color={room.is_active ? "success" : "default"}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>
                    {new Date(room.created_at).toLocaleDateString()}
                  </TableCell>
                  <TableCell align="center">
                    <Tooltip title="Edit">
                      <IconButton size="small" onClick={() => onEdit(room)}>
                        <Edit fontSize="small" />
                      </IconButton>
                    </Tooltip>
                    <Tooltip title="Delete">
                      <IconButton
                        size="small"
                        color="error"
                        onClick={() => onDelete(room.id)}
                      >
                        <Delete fontSize="small" />
                      </IconButton>
                    </Tooltip>
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
      />
    </Paper>
  );
}
