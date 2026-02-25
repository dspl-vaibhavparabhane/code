import { Card, CardContent, Typography, Grid, Box, Divider } from "@mui/material";
import { User } from "@/types/user";
import { RoleChip } from "@/components/common/RoleChip";
import { StatusChip } from "@/components/common/StatusChip";

interface UserProfileCardProps {
  user: User;
}

export function UserProfileCard({ user }: UserProfileCardProps) {
  const formatDate = (date: string | null) => {
    if (!date) return "N/A";
    return new Date(date).toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  };

  return (
    <Card>
      <CardContent>
        <Box sx={{ mb: 3 }}>
          <Typography variant="h5" sx={{ fontWeight: "bold", mb: 1 }}>
            {user.name || "N/A"}
          </Typography>
          <Typography color="textSecondary">{user.email}</Typography>
        </Box>

        <Divider sx={{ my: 2 }} />

        <Grid container spacing={3}>
          <Grid item xs={12} sm={6}>
            <Typography variant="caption" color="textSecondary" display="block">
              Role
            </Typography>
            <Box sx={{ mt: 0.5 }}>
              <RoleChip role={user.role} />
            </Box>
          </Grid>

          <Grid item xs={12} sm={6}>
            <Typography variant="caption" color="textSecondary" display="block">
              Status
            </Typography>
            <Box sx={{ mt: 0.5 }}>
              <StatusChip status={user.status} />
            </Box>
          </Grid>

          <Grid item xs={12} sm={6}>
            <Typography variant="caption" color="textSecondary" display="block">
              User ID
            </Typography>
            <Typography sx={{ fontWeight: 500, mt: 0.5 }}>{user.id}</Typography>
          </Grid>

          <Grid item xs={12} sm={6}>
            <Typography variant="caption" color="textSecondary" display="block">
              Join Date
            </Typography>
            <Typography sx={{ fontWeight: 500, mt: 0.5 }}>{formatDate(user.join_date)}</Typography>
          </Grid>

          <Grid item xs={12} sm={6}>
            <Typography variant="caption" color="textSecondary" display="block">
              Separation Date
            </Typography>
            <Typography sx={{ fontWeight: 500, mt: 0.5 }}>{formatDate(user.separation_date)}</Typography>
          </Grid>

          <Grid item xs={12} sm={6}>
            <Typography variant="caption" color="textSecondary" display="block">
              Created At
            </Typography>
            <Typography sx={{ fontWeight: 500, mt: 0.5 }}>{formatDate(user.created_at)}</Typography>
          </Grid>

          <Grid item xs={12} sm={6}>
            <Typography variant="caption" color="textSecondary" display="block">
              Updated At
            </Typography>
            <Typography sx={{ fontWeight: 500, mt: 0.5 }}>{formatDate(user.updated_at)}</Typography>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
}
