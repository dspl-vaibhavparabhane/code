"use client";

import { useState } from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Alert,
} from "@mui/material";
import { CreateRoomPayload } from "@/types/booking";
import { conferenceRoomService } from "@/services/conferenceRooms";

interface CreateRoomDialogProps {
  open: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

export default function CreateRoomDialog({
  open,
  onClose,
  onSuccess,
}: CreateRoomDialogProps) {
  const [formData, setFormData] = useState<CreateRoomPayload>({
    name: "",
    capacity: 0,
    location: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      await conferenceRoomService.createRoom(formData);
      onSuccess();
      onClose();
      setFormData({ name: "", capacity: 0, location: "" });
    } catch (err: any) {
      setError(err.response?.data?.error || "Failed to create room");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>Create Conference Room</DialogTitle>
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
            placeholder="e.g., Building A, Floor 2"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={onClose}>Cancel</Button>
          <Button type="submit" variant="contained" disabled={loading}>
            {loading ? "Creating..." : "Create Room"}
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
}
