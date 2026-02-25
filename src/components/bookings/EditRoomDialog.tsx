"use client";

import { useState, useEffect } from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Alert,
  FormControlLabel,
  Switch,
} from "@mui/material";
import { ConferenceRoom, UpdateRoomPayload } from "@/types/booking";
import { conferenceRoomService } from "@/services/conferenceRooms";

interface EditRoomDialogProps {
  open: boolean;
  onClose: () => void;
  room: ConferenceRoom | null;
  onSuccess: () => void;
}

export default function EditRoomDialog({
  open,
  onClose,
  room,
  onSuccess,
}: EditRoomDialogProps) {
  const [formData, setFormData] = useState<UpdateRoomPayload>({
    name: "",
    capacity: 0,
    location: "",
    is_active: true,
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (room) {
      setFormData({
        name: room.name,
        capacity: room.capacity,
        location: room.location,
        is_active: room.is_active,
      });
    }
  }, [room]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!room) return;
    
    setError("");
    setLoading(true);

    try {
      await conferenceRoomService.updateRoom(room.id, formData);
      onSuccess();
      onClose();
    } catch (err: any) {
      setError(err.response?.data?.error || "Failed to update room");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>Edit Conference Room</DialogTitle>
      <form onSubmit={handleSubmit}>
        <DialogContent>
          {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
          
          <TextField
            fullWidth
            label="Room Name"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            required
            margin="normal"
          />

          <TextField
            fullWidth
            label="Capacity"
            type="number"
            value={formData.capacity || ""}
            onChange={(e) => setFormData({ ...formData, capacity: Number(e.target.value) })}
            required
            margin="normal"
            inputProps={{ min: 1 }}
          />

          <TextField
            fullWidth
            label="Location"
            value={formData.location}
            onChange={(e) => setFormData({ ...formData, location: e.target.value })}
            required
            margin="normal"
          />

          <FormControlLabel
            control={
              <Switch
                checked={formData.is_active}
                onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })}
              />
            }
            label="Available"
            sx={{ mt: 2 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={onClose}>Cancel</Button>
          <Button type="submit" variant="contained" disabled={loading}>
            {loading ? "Updating..." : "Update Room"}
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
}
