# Video Analytics Frontend

React + Vite UI for video uploads, processed-video playback, and analytics visualization backed by FastAPI.

## Local setup

```bash
cd frontend
npm install
npm run dev
```

Default dev URL: `http://localhost:5173`

## Backend API URL

Optional: create `frontend/.env.local` to override backend URL:

```bash
VITE_API_BASE_URL=http://localhost:8000
```

If `VITE_API_BASE_URL` is not set, the app uses the current browser host with port `8000` (for example, `http://13.53.42.135:8000` when opened via EC2 public IP).

## Dashboard behavior

- `Total Videos` shows the overall number of processed videos.
- Other top-level analytics are intentionally gated until a user clicks `View` on a processed video row.
- After `View`, cards and chart display analytics for the selected video.

## Available scripts

- `npm run dev`: start Vite development server
- `npm run build`: create production build
- `npm run preview`: preview production build locally
- `npm run test`: run tests once
- `npm run test:watch`: run tests in watch mode
