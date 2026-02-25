"use client";

import { useState, useEffect } from "react";
import {
  Box,
  Button,
  Typography,
  Paper,
  Alert,
  CircularProgress,
  ToggleButtonGroup,
  ToggleButton,
} from "@mui/material";
import { Add } from "@mui/icons-material";
import CreateBookingDialog from "@/components/bookings/CreateBookingDialog";
import BookingsTable from "@/components/bookings/BookingsTable";
import RoomCalendarView from "@/components/bookings/RoomCalendarView";
import { bookingService } from "@/services/bookings";
import { conferenceRoomService } from "@/services/conferenceRooms";
import { Booking, ConferenceRoom } from "@/types/booking";

export default function BookingsPage() {
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [rooms, setRooms] = useState<ConferenceRoom[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [dialogOpen, setDialogOpen] = useState(false);
  const [filter, setFilter] = useState<"all" | "upcoming">("upcoming");

  const fetchData = async () => {
    setLoading(true);
    setError("");
    try {
      const [bookingsData, roomsData] = await Promise.all([
        bookingService.getMyBookings(filter === "upcoming"),
        conferenceRoomService.getAllRooms(),
      ]);
      setBookings(bookingsData);
      setRooms(roomsData);
    } catch (err: any) {
      setError(err.response?.data?.error || "Failed to load data");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [filter]);

  const handleCancel = async (bookingId: number) => {
    if (!confirm("Are you sure you want to cancel this booking?")) return;

    try {
      await bookingService.cancelBooking(bookingId);
      fetchData();
    } catch (err: any) {
      alert(err.response?.data?.error || "Failed to cancel booking");
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" p={4}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">My Bookings</Typography>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => setDialogOpen(true)}
        >
          Book Room
        </Button>
      </Box>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      {rooms.length > 0 && <RoomCalendarView rooms={rooms} />}

      <Paper sx={{ p: 2, mb: 2 }}>
        <ToggleButtonGroup
          value={filter}
          exclusive
          onChange={(_, value) => value && setFilter(value)}
          size="small"
        >
          <ToggleButton value="upcoming">Upcoming</ToggleButton>
          <ToggleButton value="all">All Bookings</ToggleButton>
        </ToggleButtonGroup>
      </Paper>

      <BookingsTable bookings={bookings} onCancel={handleCancel} />

      <CreateBookingDialog
        open={dialogOpen}
        onClose={() => setDialogOpen(false)}
        rooms={rooms}
        onSuccess={fetchData}
      />
    </Box>
  );
}
