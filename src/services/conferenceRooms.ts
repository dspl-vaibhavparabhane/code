import apiClient from "./api";
import { ConferenceRoom, CreateRoomPayload, UpdateRoomPayload } from "@/types/booking";

export const conferenceRoomService = {
  getAllRooms: async (activeOnly: boolean = true) => {
    const response = await apiClient.get<{ rooms: ConferenceRoom[] }>(
      `/conference-rooms/?active_only=${activeOnly}`
    );
    return response.data.rooms;
  },

  getRoomById: async (roomId: number) => {
    const response = await apiClient.get<{ room: ConferenceRoom }>(
      `/conference-rooms/${roomId}`
    );
    return response.data.room;
  },

  createRoom: async (payload: CreateRoomPayload) => {
    const response = await apiClient.post("/conference-rooms/", payload);
    return response.data;
  },

  updateRoom: async (roomId: number, payload: UpdateRoomPayload) => {
    const response = await apiClient.put(`/conference-rooms/${roomId}`, payload);
    return response.data;
  },

  deleteRoom: async (roomId: number) => {
    const response = await apiClient.delete(`/conference-rooms/${roomId}`);
    return response.data;
  },
};
