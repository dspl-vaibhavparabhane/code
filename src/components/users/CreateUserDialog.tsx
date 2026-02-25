import { useState } from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  MenuItem,
  Stack,
  Alert,
} from "@mui/material";
import { UserRole, UserStatus, CreateUserPayload } from "@/types/user";

interface CreateUserDialogProps {
  open: boolean;
  onClose: () => void;
  onSubmit: (payload: CreateUserPayload) => Promise<void>;
  currentUserRole: UserRole | null;
}

export function CreateUserDialog({ open, onClose, onSubmit, currentUserRole }: CreateUserDialogProps) {
  const [formData, setFormData] = useState<CreateUserPayload>({
    email: "",
    password: "",
    name: "",
    role: "Employee",
    join_date: "",
    separation_date: "",
    status: "active",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (field: keyof CreateUserPayload, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async () => {
    setError("");

    if (!formData.email || !formData.password || !formData.name || !formData.join_date) {
      setError("Please fill all required fields");
      return;
    }

    setLoading(true);
    try {
      const payload = { ...formData };
      if (!payload.separation_date) {
        delete payload.separation_date;
      }
      await onSubmit(payload);
      handleClose();
    } catch (err: any) {
      setError(err.response?.data?.error || "Failed to create user");
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    setFormData({
      email: "",
      password: "",
      name: "",
      role: "Employee",
      join_date: "",
      separation_date: "",
      status: "active",
    });
    setError("");
    onClose();
  };

  const availableRoles: UserRole[] = currentUserRole === "Admin" ? ["Employee", "HR", "Admin"] : ["Employee"];

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
      <DialogTitle>Create New User</DialogTitle>
      <DialogContent>
        <Stack spacing={2} sx={{ mt: 1 }}>
          {error && <Alert severity="error">{error}</Alert>}

          <TextField
            fullWidth
            required
            label="Name"
            value={formData.name}
            onChange={(e) => handleChange("name", e.target.value)}
          />

          <TextField
            fullWidth
            required
            type="email"
            label="Email"
            value={formData.email}
            onChange={(e) => handleChange("email", e.target.value)}
          />

          <TextField
            fullWidth
            required
            type="password"
            label="Password"
            value={formData.password}
            onChange={(e) => handleChange("password", e.target.value)}
          />

          <TextField
            select
            fullWidth
            required
            label="Role"
            value={formData.role}
            onChange={(e) => handleChange("role", e.target.value as UserRole)}
          >
            {availableRoles.map((role) => (
              <MenuItem key={role} value={role}>
                {role}
              </MenuItem>
            ))}
          </TextField>

          <TextField
            fullWidth
            required
            type="date"
            label="Join Date"
            value={formData.join_date}
            onChange={(e) => handleChange("join_date", e.target.value)}
            InputLabelProps={{ shrink: true }}
          />

          <TextField
            fullWidth
            type="date"
            label="Separation Date"
            value={formData.separation_date}
            onChange={(e) => handleChange("separation_date", e.target.value)}
            InputLabelProps={{ shrink: true }}
          />

          <TextField
            select
            fullWidth
            required
            label="Status"
            value={formData.status}
            onChange={(e) => handleChange("status", e.target.value as UserStatus)}
          >
            <MenuItem value="active">Active</MenuItem>
            <MenuItem value="separated">Separated</MenuItem>
          </TextField>
        </Stack>
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose} disabled={loading}>
          Cancel
        </Button>
        <Button onClick={handleSubmit} variant="contained" disabled={loading}>
          {loading ? "Creating..." : "Create User"}
        </Button>
      </DialogActions>
    </Dialog>
  );
}
