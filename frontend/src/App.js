import React from "react";
import { MantineProvider } from "@mantine/core";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LoginRegister from "./components/Auth/LoginRegister";

function App() {
  return (
    <MantineProvider withGlobalStyles withNormalizeCSS>
    <Router>
      <Routes>
        {/* Login/Register route */}
        <Route path="/auth" element={<LoginRegister />} />
      </Routes>

    </Router>
    </MantineProvider>
  );
}

export default App;
