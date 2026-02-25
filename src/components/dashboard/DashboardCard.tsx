import { Card, CardContent, Typography, Box } from "@mui/material";
import { useRouter } from "next/navigation";

interface DashboardCardProps {
  title: string;
  description: string;
  icon: React.ReactNode;
  path: string;
  color?: string;
}

export function DashboardCard({ title, description, icon, path, color = "#4f46e5" }: DashboardCardProps) {
  const router = useRouter();

  return (
    <Card
      onClick={() => router.push(path)}
      sx={{
        cursor: "pointer",
        transition: "all 0.3s",
        "&:hover": {
          transform: "translateY(-4px)",
          boxShadow: 4,
        },
      }}
    >
      <CardContent sx={{ p: 3 }}>
        <Box sx={{ display: "flex", alignItems: "center", gap: 2, mb: 2 }}>
          <Box
            sx={{
              bgcolor: color,
              color: "white",
              p: 1.5,
              borderRadius: 2,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            {icon}
          </Box>
          <Typography variant="h6" sx={{ fontWeight: "bold" }}>
            {title}
          </Typography>
        </Box>
        <Typography color="textSecondary">{description}</Typography>
      </CardContent>
    </Card>
  );
}
