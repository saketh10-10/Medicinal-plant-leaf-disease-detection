# 🌱 Plant Care Manager

A full-stack web application for managing your plant collection and tracking their care needs.

## Features

- **Plant Management**: Add, edit, and delete plants from your collection
- **Care Tracking**: Monitor watering schedules and sunlight requirements
- **Visual Indicators**: Color-coded care levels and overdue watering alerts
- **Responsive Design**: Works on desktop and mobile devices
- **Modern UI**: Clean, intuitive interface built with React and Tailwind CSS

## Tech Stack

### Frontend
- **React 19** with TypeScript
- **Vite** for build tooling
- **Tailwind CSS** for styling

### Backend
- **Node.js** with Express.js
- **CORS** for cross-origin requests
- **In-memory storage** (ready for database integration)

## Getting Started

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn

### Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd D:\PLANT
   ```

2. **Install all dependencies**
   ```bash
   npm run install:all
   ```
   This will install dependencies for both frontend and backend.

### Running the Application

#### Option 1: Run both frontend and backend together (Recommended)
```bash
npm start
```
This will start both the backend API (port 3001) and frontend development server (port 5173) concurrently.

#### Option 2: Run separately

**Start the backend:**
```bash
npm run dev:backend
# or
cd backend && npm start
```

**Start the frontend:**
```bash
npm run dev:frontend
# or
cd frontend && npm run dev
```

### Access the Application

- **Frontend**: Open [http://localhost:5173](http://localhost:5173) in your browser
- **Backend API**: Available at [http://localhost:3001](http://localhost:3001)

## API Endpoints

The backend provides the following REST API endpoints:

- `GET /api/plants` - Get all plants
- `GET /api/plants/:id` - Get a specific plant
- `POST /api/plants` - Add a new plant
- `PUT /api/plants/:id` - Update a plant
- `DELETE /api/plants/:id` - Delete a plant
- `PATCH /api/plants/:id/water` - Mark a plant as watered

## Usage

1. **Add Plants**: Click the "Add New Plant" button to add plants to your collection
2. **Track Care**: View care level indicators and watering schedules
3. **Water Plants**: Use the "💧 Water" button to update the last watered date
4. **Edit/Delete**: Modify plant details or remove plants from your collection

## Development

### Project Structure
```
PLANT/
├── backend/           # Express.js API server
│   ├── index.js      # Main server file
│   └── package.json
├── frontend/          # React application
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── services/    # API service functions
│   │   └── ...
│   └── package.json
└── package.json       # Root package for running both services
```

### Available Scripts

- `npm start` - Start both frontend and backend
- `npm run dev` - Same as start
- `npm run dev:frontend` - Start only frontend
- `npm run dev:backend` - Start only backend
- `npm run install:all` - Install dependencies for all parts

### Frontend Scripts
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build

## Future Enhancements

- [ ] Database integration (MongoDB/PostgreSQL)
- [ ] User authentication and multiple collections
- [ ] Plant identification using image recognition
- [ ] Care reminders and notifications
- [ ] Plant growth tracking with photos
- [ ] Export/import plant data

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the ISC License.
