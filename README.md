# Adaptive Tutor Frontend

This is a production-ready React.js application for the Adaptive Tutor platform. It provides a seamless user experience for authentication, profile management, and personalized lesson generation by integrating with the Adaptive Tutor API.

## ✨ Features

- **JWT-based Authentication**: Secure user registration and login.
- **Persistent Sessions**: User sessions are maintained across page reloads.
- **Dashboard**: A central hub to access all features.
- **Cognitive Profile Management**: View and dynamically update learning profiles based on user feedback.
- **Personalized Lesson Generation**: Generate lessons on any concept, tailored to the user's cognitive profile.
- **Markdown & Mermaid.js Support**: Renders complex lesson content, including diagrams.
- **Responsive Design**: Mobile-first UI for a great experience on all devices.
- **Global State Management**: Uses React Context for a clean and predictable state.

## 🛠 Tech Stack

- **React.js**: Core frontend framework.
- **React Router**: For client-side routing.
- **Axios**: For making API requests with interceptors for auth.
- **CSS Modules**: For scoped, conflict-free component styling.
- **Mermaid.js**: For rendering diagrams from text.
- **React Markdown**: To safely render Markdown content.

## 🚀 Getting Started

### Prerequisites

- Node.js (v16 or later)
- npm or yarn

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd adaptive-tutor-frontend
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```

3.  **Create an environment file:**
    Create a `.env` file in the root of the project and add your API's base URL.
    ```
    REACT_APP_API_BASE_URL=[http://your-backend-api-url.com](http://your-backend-api-url.com)
    ```
    For local development, this is typically `http://localhost:8000`.

4.  **Run the development server:**
    ```bash
    npm start
    ```
    The application will be available at `http://localhost:3000`.

## 📦 Deployment

This application is configured for easy deployment on platforms like Vercel or Netlify.

### Deploying to Vercel/Netlify

1.  Push your code to a GitHub, GitLab, or Bitbucket repository.
2.  Import the project into your Vercel or Netlify dashboard.
3.  **Configure Environment Variables**:
    In the project settings on your deployment platform, add the following environment variable:
    - `REACT_APP_API_BASE_URL`: Set this to the URL of your **production** backend API.

The platform will automatically detect that it's a Create React App project and use the correct build settings (`npm run build`) and output directory (`build`). No further configuration is needed.