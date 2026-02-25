/**
 * Dashboard Redirect Page -> Redirects to appropriate role-based dashboard.
 */

"use client";

import { useAuth } from "@/contexts/AuthContext";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { ProtectedRoute } from "@/components/ProtectedRoute";

export default function DashboardPage() {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (loading) return;

    if (user) {
      if (user.role === "Admin") {
        router.push("/dashboard/admin");
      } else if (user.role === "HR") {
        router.push("/dashboard/hr");
      } else {
        router.push("/dashboard/employee");
      }
    }
  }, [user, loading, router]);

  return (
    <ProtectedRoute>
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <h1 className="text-2xl font-bold mb-4">Loading...</h1>
          <p className="text-gray-600">Redirecting to your dashboard...</p>
        </div>
      </div>
    </ProtectedRoute>
  );
}
