export type BookingStatus = "CONFIRMED" | "CANCELLED" | "COMPLETE";

export interface ConferenceRoom {
  id: number;
  name: string;
  capacity: number;
  location: string;
  is_active: boolean;
  created_at: string;
}

export interface Booking {
  id: number;
  room_id: number;
  room_name: string | null;
  user_id: number;
  user_name: string | null;
  start_time: string;
  end_time: string;
  purpose: string;
  status: BookingStatus;
  created_at: string;
}

export interface CreateBookingPayload {
  room_id: number;
  start_time: string;
  end_time: string;
  purpose: string;
}

export interface CreateRoomPayload {
  name: string;
  capacity: number;
  location: string;
}

export interface UpdateRoomPayload {
  name?: string;
  capacity?: number;
  location?: string;
  is_active?: boolean;
}

export interface RoomAvailability {
  room_id: number;
  start_date: string;
  end_date: string;
  booked_slots: Booking[];
}
