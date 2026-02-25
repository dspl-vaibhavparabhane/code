import apiClient from "./api";
import { Booking, CreateBookingPayload, RoomAvailability } from "@/types/booking";

export const bookingService = {
  createBooking: async (payload: CreateBookingPayload) => {
    const response = await apiClient.post("/bookings/", payload);
    return response.data;
  },

  getMyBookings: async (upcomingOnly: boolean = false) => {
    const response = await apiClient.get<{ bookings: Booking[] }>(
      `/bookings/my-bookings?upcoming=${upcomingOnly}`
    );
    return response.data.bookings;
  },

  getAllBookings: async (upcomingOnly: boolean = false) => {
    const response = await apiClient.get<{ bookings: Booking[] }>(
      `/bookings/all?upcoming=${upcomingOnly}`
    );
    return response.data.bookings;
  },

  cancelBooking: async (bookingId: number) => {
    const response = await apiClient.put(`/bookings/${bookingId}/cancel`);
    return response.data;
  },

  getRoomAvailability: async (roomId: number, startDate: string, endDate: string) => {
    const response = await apiClient.get<RoomAvailability>(
      `/bookings/availability?room_id=${roomId}&start_date=${startDate}&end_date=${endDate}`
    );
    return response.data;
  },
};
