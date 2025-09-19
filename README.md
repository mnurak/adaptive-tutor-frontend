# Adaptive Tutor Frontend 🎓

Welcome to the official frontend of **Adaptive Tutor** — a modern, conversational learning platform built with **React** and **Vite**. This application delivers a dynamic, personalized educational experience by integrating seamlessly with an AI-powered backend.

## 📦 Backend Repository

Find the backend here:  
[Adaptive Tutor Backend](https://github.com/mnurak/adaptive-tutor-backend)

---

## ✨ Features

- **💬 Conversational Tutor:** Real-time, ChatGPT-like interface. The AI tutor adapts its teaching style based on user input and feedback.
- **📚 Structured Lesson Generator:** Request complete, structured lessons on specific topics, tailored to your cognitive profile.
- **🧠 Dynamic Profile Adaptation:** The backend analyzes user prompts to update cognitive profiles in real-time for personalized learning.
- **🔐 User Authentication:** Secure registration and JWT-based login for personalized sessions.
- **📱 Responsive Design:** Clean, modern, and mobile-friendly UI.
- **📊 Visual Learning Support:** Renders **Markdown** and **Mermaid.js** diagrams for visual explanations.

---

## 🛠️ Tech Stack

- **Framework:** React.js
- **Build Tool:** Vite
- **Routing:** React Router
- **API Communication:** Axios
- **Styling:** CSS Modules
- **Diagrams:** Mermaid.js

---

## 🚀 Getting Started

Follow these steps to set up the project locally for development and testing.

### Prerequisites

- **Node.js** (v18.x or higher)
- **npm** (or compatible package manager)

---

### Local Setup

#### 1. Set Up the Backend

This frontend requires the backend server.  
Follow setup instructions in the [backend repository](https://github.com/mnurak/adaptive-tutor-backend).  
By default, the backend runs at `http://localhost:8000`.

#### 2. Clone the Frontend Repository

```bash
git clone https://github.com/mnurak/adaptive-tutor-frontend.git
```

#### 3. Navigate to the Project Directory

```bash
cd adaptive-tutor-frontend
```

#### 4. Install Dependencies

```bash
npm install
```

#### 5. Configure Environment Variables

Create a `.env` file in the root directory with:

```env
# .env

# The full URL of your running backend API server
VITE_API_BASE_URL=http://localhost:8000
```

#### 6. Run the Development Server

```bash
npm run dev
```

The app will be accessible at [http://localhost:5173](http://localhost:5173).

---

## 📜 Available Scripts

- `npm run dev` — Start development server with hot-reloading.
- `npm run build` — Bundle the app for production (output in `dist`).
- `npm run preview` — Preview the production build locally.

---

## 🚢 Deployment

This Vite project is ready for deployment on platforms like **Vercel**, **Netlify**, or any static site host.

**Deployment Steps:**

1. Push your code to a Git provider (GitHub, GitLab, etc.).
2. Import your repository into your chosen hosting platform.
3. Set the `VITE_API_BASE_URL` environment variable in your platform’s settings (should be the public URL of your backend API).
4. The platform will detect the Vite project, run `npm run build`, and deploy the `dist` folder.
