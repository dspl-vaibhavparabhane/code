"use client";

import { useState, useEffect, useCallback } from "react";
import {
  Box,
  Button,
  Typography,
  Stack,
  Snackbar,
  Alert,
} from "@mui/material";
import { Add } from "@mui/icons-material";
import CreateRoomDialog from "@/components/bookings/CreateRoomDialog";
import EditRoomDialog from "@/components/bookings/EditRoomDialog";
import { ConferenceRoomsTable } from "@/components/bookings/ConferenceRoomsTable";
import { conferenceRoomService } from "@/services/conferenceRooms";
import { ConferenceRoom } from "@/types/booking";

export default function ConferenceRoomsPage() {
  const [rooms, setRooms] = useState<ConferenceRoom[]>([]);
  const [filteredRooms, setFilteredRooms] = useState<ConferenceRoom[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [filters, setFilters] = useState({ search: "", availability: "all" });
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [selectedRoom, setSelectedRoom] = useState<ConferenceRoom | null>(null);
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: "",
    severity: "success" as "success" | "error",
  });

  const fetchRooms = useCallback(async () => {
    setLoading(true);
    try {
      const data = await conferenceRoomService.getAllRooms(false);
      setRooms(data);
      applyFilters(data, filters);
    } catch (err: any) {
      setSnackbar({
        open: true,
        message: err.response?.data?.error || "Failed to load rooms",
        severity: "error",
      });
    } finally {
      setLoading(false);
    }
  }, []);

  const applyFilters = (data: ConferenceRoom[], currentFilters: typeof filters) => {
    let filtered = data;

    if (currentFilters.search) {
      filtered = filtered.filter((room) =>
        room.name.toLowerCase().includes(currentFilters.search.toLowerCase()) ||
        room.location.toLowerCase().includes(currentFilters.search.toLowerCase())
      );
    }

    if (currentFilters.availability === "available") {
      filtered = filtered.filter((room) => room.is_active);
    } else if (currentFilters.availability === "unavailable") {
      filtered = filtered.filter((room) => !room.is_active);
    }

    setFilteredRooms(filtered);
    setTotal(filtered.length);
  };

  useEffect(() => {
    fetchRooms();
  }, [fetchRooms]);

  useEffect(() => {
    applyFilters(rooms, filters);
    setPage(0);
  }, [filters, rooms]);

  const handleFilterChange = (newFilters: { search: string; availability: string }) => {
    setFilters(newFilters);
  };

  const handleEdit = (room: ConferenceRoom) => {
    setSelectedRoom(room);
    setEditDialogOpen(true);
  };

  const handleDelete = async (roomId: number) => {
    if (!confirm("Are you sure you want to delete this conference room?")) return;

    try {
      await conferenceRoomService.deleteRoom(roomId);
      setSnackbar({
        open: true,
        message: "Conference room deleted successfully",
        severity: "success",
      });
      fetchRooms();
    } catch (err: any) {
      setSnackbar({
        open: true,
        message: err.response?.data?.error || "Failed to delete room",
        severity: "error",
      });
    }
  };

  const paginatedRooms = filteredRooms.slice(
    page * rowsPerPage,
    page * rowsPerPage + rowsPerPage
  );

  return (
    <Stack spacing={3}>
      <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <Box>
          <Typography variant="h4" sx={{ fontWeight: "bold" }}>
            Conference Rooms
          </Typography>
          <Typography color="textSecondary">
            Manage conference room inventory
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => setDialogOpen(true)}
        >
          Add Room
        </Button>
      </Box>

      <ConferenceRoomsTable
        rooms={paginatedRooms}
        total={total}
        loading={loading}
        page={page}
        rowsPerPage={rowsPerPage}
        onPageChange={setPage}
        onRowsPerPageChange={(rows) => {
          setRowsPerPage(rows);
          setPage(0);
        }}
        onEdit={handleEdit}
        onDelete={handleDelete}
        onFilterChange={handleFilterChange}
      />

      <CreateRoomDialog
        open={dialogOpen}
        onClose={() => setDialogOpen(false)}
        onSuccess={() => {
          setSnackbar({
            open: true,
            message: "Conference room created successfully",
            severity: "success",
          });
          fetchRooms();
        }}
      />

      <EditRoomDialog
        open={editDialogOpen}
        onClose={() => {
          setEditDialogOpen(false);
          setSelectedRoom(null);
        }}
        room={selectedRoom}
        onSuccess={() => {
          setSnackbar({
            open: true,
            message: "Conference room updated successfully",
            severity: "success",
          });
          fetchRooms();
        }}
      />

      <Snackbar
        open={snackbar.open}
        autoHideDuration={4000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
        anchorOrigin={{ vertical: "top", horizontal: "right" }}
      >
        <Alert
          onClose={() => setSnackbar({ ...snackbar, open: false })}
          severity={snackbar.severity}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Stack>
  );
}
