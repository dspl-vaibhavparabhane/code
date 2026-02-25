"use client";

import { useState } from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  MenuItem,
  Alert,
} from "@mui/material";
import { ConferenceRoom, CreateBookingPayload } from "@/types/booking";
import { bookingService } from "@/services/bookings";

interface CreateBookingDialogProps {
  open: boolean;
  onClose: () => void;
  rooms: ConferenceRoom[];
  onSuccess: () => void;
}

export default function CreateBookingDialog({
  open,
  onClose,
  rooms,
  onSuccess,
}: CreateBookingDialogProps) {
  const [formData, setFormData] = useState<CreateBookingPayload>({
    room_id: 0,
    start_time: "",
    end_time: "",
    purpose: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      // Validate room selection
      if (!formData.room_id || formData.room_id === 0) {
        setError("Please select a conference room");
        setLoading(false);
        return;
      }

      // Convert datetime-local to ISO format (datetime-local doesn't include timezone)
      const startDate = new Date(formData.start_time);
      const endDate = new Date(formData.end_time);
      
      // Check if dates are valid
      if (isNaN(startDate.getTime()) || isNaN(endDate.getTime())) {
        setError("Invalid date/time format");
        setLoading(false);
        return;
      }

      const payload = {
        room_id: formData.room_id,
        start_time: startDate.toISOString(),
        end_time: endDate.toISOString(),
        purpose: formData.purpose,
      };
      
      console.log("Booking payload:", payload);
      const response = await bookingService.createBooking(payload);
      console.log("Booking response:", response);
      
      onSuccess();
      onClose();
      setFormData({ room_id: 0, start_time: "", end_time: "", purpose: "" });
    } catch (err: any) {
      console.error("Booking error:", err);
      console.error("Error response:", err.response);
      const errorMsg = err.response?.data?.error || err.response?.data?.message || err.message || "Failed to create booking";
      setError(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>Book Conference Room</DialogTitle>
      <form onSubmit={handleSubmit}>
        <DialogContent>
          {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
          
          <TextField
            select
            fullWidth
            label="Conference Room"
            value={formData.room_id}
            onChange={(e) => setFormData({ ...formData, room_id: Number(e.target.value) })}
            required
            margin="normal"
          >
            <MenuItem value={0}>Select a room</MenuItem>
            {rooms.map((room) => (
              <MenuItem key={room.id} value={room.id}>
                {room.name} - Capacity: {room.capacity}
              </MenuItem>
            ))}
          </TextField>

          <TextField
            fullWidth
            label="Start Time"
            type="datetime-local"
            value={formData.start_time}
            onChange={(e) => setFormData({ ...formData, start_time: e.target.value })}
            required
            margin="normal"
            InputLabelProps={{ shrink: true }}
          />

          <TextField
            fullWidth
            label="End Time"
            type="datetime-local"
            value={formData.end_time}
            onChange={(e) => setFormData({ ...formData, end_time: e.target.value })}
            required
            margin="normal"
            InputLabelProps={{ shrink: true }}
          />

          <TextField
            fullWidth
            label="Purpose"
            multiline
            rows={3}
            value={formData.purpose}
            onChange={(e) => setFormData({ ...formData, purpose: e.target.value })}
            required
            margin="normal"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={onClose}>Cancel</Button>
          <Button type="submit" variant="contained" disabled={loading}>
            {loading ? "Booking..." : "Book Room"}
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
}
