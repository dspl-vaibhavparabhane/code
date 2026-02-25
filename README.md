# DSPL Asset Pulse - Frontend Dashboard

A modern Next.js dashboard with TypeScript, Material UI, and JWT-based authentication.

## Features

- **Authentication & Authorization**: JWT-based auth with role-based routing
- **User Management**: CRUD operations for users (HR/Admin only)
- **Conference Room Management**: View and manage meeting rooms
- **Booking System**:
  - Create and manage bookings
  - Real-time availability checking
  - Filter by upcoming, completed, or cancelled
  - Calendar view for bookings
- **Responsive Design**: Material-UI components with mobile support
- **Dark/Light Theme**: Toggle between themes
- **Auto Token Refresh**: Seamless authentication experience


##  Project Structure

```
dspl-asset-pulse-frontend/
├── src/
│   ├── app/
│   │   ├── dashboard/
│   │   │   ├── admin/
│   │   │   │   ├── admins/page.tsx
│   │   │   │   ├── assets/page.tsx
│   │   │   │   ├── employees/page.tsx
│   │   │   │   ├── hr/page.tsx
│   │   │   │   └── page.tsx
│   │   │   ├── employee/
│   │   │   │   ├── assets/page.tsx
│   │   │   │   └── page.tsx
│   │   │   ├── hr/
│   │   │   │   ├── assets/page.tsx
│   │   │   │   ├── employees/page.tsx
│   │   │   │   └── page.tsx
│   │   │   ├── bookings/page.tsx
│   │   │   ├── conference-rooms/page.tsx
│   │   │   ├── profile/page.tsx
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx
│   │   ├── login/page.tsx
│   │   ├── unauthorized/page.tsx
│   │   ├── globals.css
│   │   ├── layout.tsx
│   │   ├── metadata.ts
│   │   └── page.tsx
│   ├── components/
│   │   ├── assets/
│   │   ├── bookings/
│   │   │   ├── BookingList.tsx
│   │   │   ├── CreateBookingDialog.tsx
│   │   │   └── CancelBookingDialog.tsx
│   │   ├── conference-rooms/
│   │   │   ├── ConferenceRoomList.tsx
│   │   │   ├── CreateConferenceRoomDialog.tsx
│   │   │   └── EditConferenceRoomDialog.tsx
│   │   ├── common/
│   │   ├── dashboard/
│   │   ├── layout/
│   │   ├── users/
│   │   ├── ProtectedRoute.tsx
│   │   └── ThemeWrapper.tsx
│   ├── contexts/
│   │   └── AuthContext.tsx
│   ├── hooks/
│   │   ├── index.ts
│   │   ├── useAssetManagement.ts
│   │   ├── useBookingManagement.ts
│   │   ├── useConferenceRoomManagement.ts
│   │   ├── useDashboardMetrics.ts
│   │   ├── useDialogState.ts
│   │   ├── useFilters.ts
│   │   ├── usePagination.ts
│   │   ├── useSnackbar.ts
│   │   └── useUserManagement.ts
│   ├── lib/
│   │   ├── constants/
│   │   ├── utils/
│   │   └── index.ts
│   ├── services/
│   │   ├── api.ts
│   │   ├── assets.ts
│   │   ├── auth.ts
│   │   ├── bookings.ts
│   │   ├── conferenceRooms.ts
│   │   └── users.ts
│   ├── theme/
│   │   └── theme.ts
│   └── types/
│       ├── asset.ts
│       ├── booking.ts
│       ├── conferenceRoom.ts
│       ├── common.ts
│       ├── css.d.ts
│       ├── index.ts
│       └── user.ts
├── public/
├── .next/ (build artifacts)
├── package.json
├── tsconfig.json
├── next.config.js
└── README.md

```

##  Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Set Environment Variables

```bash
cp .env.example .env.local
```

### 3. Run Development Server

```bash
npm run dev
```

Visit `http://localhost:3000`

##  Authentication Flow

1. **Login Page**: User enters email and password
2. **Backend Login**: Frontend calls `/api/v1/auth/login`
3. **Token Storage**: Access and refresh tokens stored in localStorage
4. **Protected Routes**: Routes check authentication status
5. **Auto Refresh**: Axios interceptor auto-refreshes expired tokens
6. **Dashboard Redirect**: User redirected to role-based dashboard



##  Dependencies

- **Next.js** 14.0.0 - React framework
- **React** 18.2.0 - UI library
- **TypeScript** 5.3.0 - Type safety
- **Material-UI** 5.x - UI components
- **Axios** 1.6.0 - HTTP client
- **date-fns** - Date manipulation
- **React Hook Form** - Form handling

## Key Features Implementation

### Booking System
- Create bookings with date/time picker
- Real-time conflict detection
- Filter by upcoming/completed/cancelled
- Cancel bookings with confirmation
- View booking history

### Conference Room Management
- List all available rooms
- Create/Edit/Delete rooms (HR/Admin)
- View room capacity and location
- Activate/Deactivate rooms

### Authentication
- JWT token storage in localStorage
- Automatic token refresh on 401
- Role-based route protection
- Redirect to login on auth failure

### API Integration
- Centralized axios client with interceptors
- Automatic Bearer token injection
- Error handling and user feedback
- Type-safe API calls

##  Production Build

```bash
# Build
npm run build

# Start production server
npm start
```

## 🧪 Testing Credentials

| Role | Email | Password |
|------|-------|----------|
| Employee | employee@company.com | password123 |
| HR | hr@company.com | password123 |
| Admin | admin@company.com | password123 |


