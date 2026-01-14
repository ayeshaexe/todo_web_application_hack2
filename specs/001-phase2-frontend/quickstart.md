# Quickstart Guide: Phase II Frontend Implementation

## Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- Basic knowledge of TypeScript, React, and Next.js

## Setup Instructions

### 1. Initialize the Project

```bash
# Create a new Next.js project with TypeScript and Tailwind CSS
npx create-next-app@latest frontend --typescript --tailwind --eslint --app

cd frontend
```

### 2. Install Additional Dependencies

```bash
npm install @types/node @types/react @types/react-dom
```

### 3. Configure Tailwind CSS

The project is already set up with Tailwind CSS. You'll need to update the `tailwind.config.js` file to include the required color palette:

```js
// tailwind.config.js
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#1C352D',      // Primary color
        secondary: '#A6B28B',    // Secondary color
        accent: '#F5C9B0',       // Accent color
        background: '#F9F6F3',   // Background color
      },
    },
  },
  plugins: [],
}
```

### 4. Project Structure

After setup, your project structure should look like this:

```
frontend/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   ├── login/
│   │   └── page.tsx
│   ├── signup/
│   │   └── page.tsx
│   └── dashboard/
│       └── page.tsx
├── components/
│   ├── auth/
│   │   ├── LoginForm.tsx
│   │   └── SignupForm.tsx
│   ├── todo/
│   │   ├── TaskCard.tsx
│   │   ├── TaskList.tsx
│   │   ├── TaskForm.tsx
│   │   └── TaskDashboard.tsx
│   ├── ui/
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   └── Card.tsx
│   └── layout/
│       └── DashboardLayout.tsx
├── lib/
│   ├── api/
│   │   └── client.ts
│   ├── types/
│   │   └── index.ts
│   └── auth/
│       └── context.tsx
├── styles/
│   └── globals.css
└── hooks/
    └── useAuth.ts
```

### 5. Environment Variables

Create a `.env.local` file in the frontend directory for future backend configuration:

```env
# API Configuration
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_JWT_SECRET=your-jwt-secret-here
```

### 6. Running the Development Server

```bash
cd frontend
npm run dev
```

The application will be available at http://localhost:3000

### 7. Key Implementation Notes

- All API calls should go through the centralized client in `lib/api/client.ts`
- Authentication state is managed via the AuthContext in `lib/auth/context.tsx`
- Components should be reusable and follow the design system color palette
- Server components should be used by default; only use 'use client' directive when state or browser APIs are needed
- All TypeScript interfaces should be defined in `lib/types/index.ts`

### 8. Testing

To run tests (once implemented):

```bash
npm run test
```

### 9. Building for Production

```bash
npm run build
npm start
```

The application will be available at http://localhost:3000 in production mode.