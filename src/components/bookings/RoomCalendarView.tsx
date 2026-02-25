"use client";

import { useState, useEffect, useMemo } from "react";
import { Calendar, momentLocalizer, View } from "react-big-calendar";
import moment from "moment";
import "react-big-calendar/lib/css/react-big-calendar.css";
import {
  Box,
  Paper,
  Typography,
  TextField,
  MenuItem,
  ToggleButtonGroup,
  ToggleButton,
} from "@mui/material";
import { ConferenceRoom, Booking } from "@/types/booking";
import { bookingService } from "@/services/bookings";

const localizer = momentLocalizer(moment);

interface RoomCalendarViewProps {
  rooms: ConferenceRoom[];
}

export default function RoomCalendarView({ rooms }: RoomCalendarViewProps) {
  const [selectedRoom, setSelectedRoom] = useState<number>(0);
  const [view, setView] = useState<View>("month");
  const [date, setDate] = useState(new Date());
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (selectedRoom > 0) {
      fetchBookings();
    }
  }, [selectedRoom, date, view]);

  const fetchBookings = async () => {
    setLoading(true);
    try {
      const startDate = moment(date).startOf(view === "month" ? "month" : "week").toDate();
      const endDate = moment(date).endOf(view === "month" ? "month" : "week").toDate();
      
      const response = await bookingService.getRoomAvailability(
        selectedRoom,
        startDate.toISOString(),
        endDate.toISOString()
      );
      setBookings(response.booked_slots || []);
    } catch (error) {
      console.error("Failed to fetch bookings:", error);
      setBookings([]);
    } finally {
      setLoading(false);
    }
  };

  const events = useMemo(() => {
    return bookings.map((booking) => ({
      id: booking.id,
      title: booking.purpose,
      start: new Date(booking.start_time),
      end: new Date(booking.end_time),
      resource: booking,
    }));
  }, [bookings]);

  const eventStyleGetter = (event: any) => {
    const booking = event.resource as Booking;
    const style = {
      backgroundColor: booking.status === "CONFIRMED" ? "#4caf50" : "#f44336",
      borderRadius: "5px",
      opacity: 0.8,
      color: "white",
      border: "0px",
      display: "block",
    };
    return { style };
  };

  return (
    <Paper sx={{ p: 3, mb: 3 }}>
      <Typography variant="h6" gutterBottom>
        Room Availability Calendar
      </Typography>

      <Box sx={{ display: "flex", gap: 2, mb: 3, flexWrap: "wrap" }}>
        <TextField
          select
          label="Select Room"
          value={selectedRoom}
          onChange={(e) => setSelectedRoom(Number(e.target.value))}
          sx={{ minWidth: 250 }}
        >
          <MenuItem value={0}>Select a room</MenuItem>
          {rooms.filter(r => r.is_active).map((room) => (
            <MenuItem key={room.id} value={room.id}>
              {room.name} - {room.location}
            </MenuItem>
          ))}
        </TextField>

        <ToggleButtonGroup
          value={view}
          exclusive
          onChange={(_, newView) => newView && setView(newView)}
          size="small"
        >
          <ToggleButton value="month">Month</ToggleButton>
          <ToggleButton value="week">Week</ToggleButton>
        </ToggleButtonGroup>
      </Box>

      {selectedRoom > 0 ? (
        <Box sx={{ height: 600 }}>
          <Calendar
            localizer={localizer}
            events={events}
            startAccessor="start"
            endAccessor="end"
            view={view}
            onView={setView}
            date={date}
            onNavigate={setDate}
            eventPropGetter={eventStyleGetter}
            style={{ height: "100%" }}
          />
        </Box>
      ) : (
        <Box textAlign="center" py={4}>
          <Typography color="text.secondary">
            Please select a room to view availability
          </Typography>
        </Box>
      )}
    </Paper>
  );
}
