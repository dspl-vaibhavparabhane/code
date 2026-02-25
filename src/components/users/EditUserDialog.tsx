import { useState, useEffect } from "react";
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
import { User, UserRole, UserStatus, UpdateUserPayload } from "@/types/user";

interface EditUserDialogProps {
  open: boolean;
  user: User | null;
  onClose: () => void;
  onSubmit: (id: number, payload: UpdateUserPayload) => Promise<void>;
  currentUserRole: UserRole | null;
}

export function EditUserDialog({ open, user, onClose, onSubmit, currentUserRole }: EditUserDialogProps) {
  const [formData, setFormData] = useState<UpdateUserPayload>({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (user) {
      setFormData({
        name: user.name || "",
        email: user.email,
        role: user.role || "Employee",
        join_date: user.join_date || "",
        separation_date: user.separation_date || "",
        status: user.status || "active",
      });
    }
  }, [user]);

  const handleChange = (field: keyof UpdateUserPayload, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async () => {
    if (!user) return;

    setError("");
    setLoading(true);
    try {
      // Clean payload - remove empty strings
      const cleanPayload: UpdateUserPayload = {};
      if (formData.name?.trim()) cleanPayload.name = formData.name.trim();
      if (formData.email?.trim()) cleanPayload.email = formData.email.trim();
      // Only include role if user is Admin
      if (currentUserRole === "Admin" && formData.role) cleanPayload.role = formData.role;
      if (formData.join_date) cleanPayload.join_date = formData.join_date;
      if (formData.separation_date) cleanPayload.separation_date = formData.separation_date;
      if (formData.status) cleanPayload.status = formData.status;

      await onSubmit(user.id, cleanPayload);
      handleClose();
    } catch (err: any) {
      setError(err.response?.data?.error || "Failed to update user");
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    setFormData({});
    setError("");
    onClose();
  };

  const canEditRole = currentUserRole === "Admin";
  const availableRoles: UserRole[] = currentUserRole === "Admin" ? ["Employee", "HR", "Admin"] : ["Employee"];

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
      <DialogTitle>Edit User</DialogTitle>
      <DialogContent>
        <Stack spacing={2} sx={{ mt: 1 }}>
          {error && <Alert severity="error">{error}</Alert>}

          <TextField
            fullWidth
            label="Name"
            value={formData.name || ""}
            onChange={(e) => handleChange("name", e.target.value)}
          />

          <TextField
            fullWidth
            type="email"
            label="Email"
            value={formData.email || ""}
            onChange={(e) => handleChange("email", e.target.value)}
          />

          <TextField
            select
            fullWidth
            label="Role"
            value={formData.role || "Employee"}
            onChange={(e) => handleChange("role", e.target.value as UserRole)}
            disabled={!canEditRole}
          >
            {availableRoles.map((role) => (
              <MenuItem key={role} value={role}>
                {role}
              </MenuItem>
            ))}
          </TextField>

          <TextField
            fullWidth
            type="date"
            label="Join Date"
            value={formData.join_date || ""}
            onChange={(e) => handleChange("join_date", e.target.value)}
            InputLabelProps={{ shrink: true }}
          />

          <TextField
            fullWidth
            type="date"
            label="Separation Date"
            value={formData.separation_date || ""}
            onChange={(e) => handleChange("separation_date", e.target.value)}
            InputLabelProps={{ shrink: true }}
          />

          <TextField
            select
            fullWidth
            label="Status"
            value={formData.status || "active"}
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
          {loading ? "Updating..." : "Update User"}
        </Button>
      </DialogActions>
    </Dialog>
  );
}
