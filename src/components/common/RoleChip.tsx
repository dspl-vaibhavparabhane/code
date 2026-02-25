import { Chip } from "@mui/material";
import { UserRole } from "@/types/user";

interface RoleChipProps {
  role: UserRole | null;
}

export function RoleChip({ role }: RoleChipProps) {
  if (!role) return <Chip label="N/A" size="small" />;

  const colorMap = {
    Admin: "error",
    HR: "warning",
    Employee: "primary",
  } as const;

  return <Chip label={role} color={colorMap[role]} size="small" />;
}
