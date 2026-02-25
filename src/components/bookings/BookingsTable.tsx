"use client";

import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  IconButton,
  Tooltip,
} from "@mui/material";
import { Cancel } from "@mui/icons-material";
import { Booking } from "@/types/booking";
import { format } from "date-fns";

interface BookingsTableProps {
  bookings: Booking[];
  onCancel: (bookingId: number) => void;
  showUserName?: boolean;
}

export default function BookingsTable({
  bookings,
  onCancel,
  showUserName = false,
}: BookingsTableProps) {
  const formatDateTime = (dateString: string) => {
    return format(new Date(dateString), "MMM dd, yyyy HH:mm");
  };

  const isPastBooking = (endTime: string) => {
    return new Date(endTime) < new Date();
  };

  return (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Room</TableCell>
            {showUserName && <TableCell>Booked By</TableCell>}
            <TableCell>Start Time</TableCell>
            <TableCell>End Time</TableCell>
            <TableCell>Purpose</TableCell>
            <TableCell>Status</TableCell>
            <TableCell align="center">Actions</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {bookings.length === 0 ? (
            <TableRow>
              <TableCell colSpan={showUserName ? 7 : 6} align="center">
                No bookings found
              </TableCell>
            </TableRow>
          ) : (
            bookings.map((booking) => (
              <TableRow key={booking.id}>
                <TableCell>{booking.room_name}</TableCell>
                {showUserName && <TableCell>{booking.user_name}</TableCell>}
                <TableCell>{formatDateTime(booking.start_time)}</TableCell>
                <TableCell>{formatDateTime(booking.end_time)}</TableCell>
                <TableCell>{booking.purpose}</TableCell>
                <TableCell>
                  <Chip
                    label={
                      booking.status === "CONFIRMED" 
                        ? "Confirmed" 
                        : booking.status === "CANCELLED" 
                        ? "Cancelled" 
                        : "Complete"
                    }
                    color={
                      booking.status === "CONFIRMED" 
                        ? "success" 
                        : booking.status === "COMPLETE" 
                        ? "info" 
                        : "default"
                    }
                    size="small"
                  />
                </TableCell>
                <TableCell align="center">
                  {booking.status === "CONFIRMED" && !isPastBooking(booking.start_time) && (
                    <Tooltip title="Cancel Booking">
                      <IconButton
                        color="error"
                        size="small"
                        onClick={() => onCancel(booking.id)}
                      >
                        <Cancel />
                      </IconButton>
                    </Tooltip>
                  )}
                </TableCell>
              </TableRow>
            ))
          )}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
