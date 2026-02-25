import { Chip } from "@mui/material";
import { UserStatus } from "@/types/user";

interface StatusChipProps {
  status: UserStatus | null;
}

export function StatusChip({ status }: StatusChipProps) {
  if (!status) return <Chip label="N/A" size="small" />;

  return (
    <Chip
      label={status === "active" ? "Active" : "Separated"}
      color={status === "active" ? "success" : "default"}
      size="small"
    />
  );
}
