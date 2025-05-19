import React, { useEffect, useState } from "react";
import { MantineProvider } from "@mantine/core";
import { BrowserRouter as Router, Routes, Route, Navigate} from "react-router-dom";
import LoginRegister from "./components/Auth/LoginRegister";
import HomePage from "./components/HomePage";
import AdminDashboard from "./components/AdminDashboard";
import VotesPage from "./components/Votes";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(() => {
    return localStorage.getItem("authToken") != null;
  });

  // ensure login state is true
  useEffect(() => {
    const token = localStorage.getItem("authToken");
    if(token) {
      setIsAuthenticated(true);
    }
  }, []);

  // logout
  const handleLogout = () => {
    localStorage.removeItem("authToken");
    setIsAuthenticated(false);
    window.location.href="/auth"; // redirect
  }

  return (
    <MantineProvider>
    <Router>
      <Routes>
        <Route path="/auth" element={isAuthenticated ? <Navigate to="/home" /> : <LoginRegister setIsAuthenticated={setIsAuthenticated} />} />
        <Route path="/home" element={isAuthenticated ? <HomePage onLogout={handleLogout} /> : <Navigate to="/auth" />} />
        <Route path="/vote" element={<VotesPage />} />
        <Route path="*" element={<Navigate to={isAuthenticated ? "/home" : "/auth"} />} />
        <Route path="/admin-dashboard" element={<AdminDashboard />} />
      </Routes>
    </Router>
    </MantineProvider>
  );
}

export default App;
