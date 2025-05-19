import React, { useState } from "react";
import {
    Button,
    Text,
    Group,
    Stack,
    Paper,
    Title,
    Divider,
} from "@mantine/core";
import AwardsShow from "../../assets/images/AwardsShow.jpeg";
import CustomPasswordInput from "../CustomPasswordInput";
import CustomEmailInput from "../CustomEmailInput";
import CustomUsernameInput from "../CustomUsernameInput";
import { useNavigate } from "react-router-dom";

const LoginRegister = ({ setIsAuthenticated }) => {
    const [isLogin, setIsLogin] = useState(true);
    const [formData, setFormData] = useState({ email: "", username: "", password: "" });
    const [message, setMessage] = useState("");
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setMessage("");
    
        const url = isLogin ? "http://127.0.0.1:5000/login" : "http://127.0.0.1:5000/register";
        const payload = isLogin
            ? { email: formData.email, password: formData.password }
            : formData;
    
        try {
            const response = await fetch(url, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload),
            });
    
            const data = await response.json();
    
            if (response.ok) {
                setMessage(isLogin ? "Login successful!" : "Registration successful!");
                if (isLogin) {
                    localStorage.setItem("authToken", data.access_token);  // Save token
                    localStorage.setItem("is_admin", data.is_admin); // admin status

                    setIsAuthenticated(true);
                    navigate("/home");
                }
            } else {
                setMessage(data.msg || "An error occurred.");
            }
        } catch (error) {
            setMessage("Failed to connect to the server.");
        }
    };


    return (
        <div style={{ display: "flex", height: "100vh", fontFamily: "'Poppins', sans-serif" }}>
            {/* Left side: Form */}
            <div
                style={{
                    width: "30%",
                    backgroundColor: "#EFF0E9",
                    boxShadow: "5px 0 15px rgba(0, 0, 0, 0.1)",
                    display: "flex",
                    flexDirection:"column",
                    alignItems: "center",
                    justifyContent: "center",
                    padding: "20px",
                }}
            >
                <div style={{marginBottom: "20px"}}>
                    <Title align="center" order={1}>
                        {isLogin ? "Welcome to the MGI Award Polls" : "Create an Account"}
                    </Title>
                </div>

                <Paper
                    shadow="xl"
                    padding="lg"
                    radius="md"
                    style={{ width: "350px", background: "white" }}
                >
                    <Stack spacing="lg">
                        <Text align="center" c="dimmed">
                            {isLogin
                                ? "Log in to start voting!"
                                : "Sign up to get started!"}
                        </Text>
                        <Divider />
                        <form onSubmit={handleSubmit}>
                            <Stack spacing="md">
                                {!isLogin && (
                                    <CustomUsernameInput 
                                        value={formData.username}
                                        onChange={(e) => setFormData({...formData, username: e.target.value})}
                                    />
                                )}
                                <CustomEmailInput
                                    value={formData.email}
                                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                                />
                                <CustomPasswordInput
                                    value={formData.password}
                                    onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                                />
                                <Button 
                                    type="submit" 
                                    fullWidth size="md"
                                    styles={{
                                        root: {
                                            backgroundColor: "#b8860b", // Dark gold
                                            color: "white", // Button text color
                                            borderRadius: "8px", // Optional: Make it slightly rounded
                                            transition: "background-color 0.3s ease", // Smooth hover transition
                                            padding: "12px 16px",
                                            "&:hover": {
                                                backgroundColor: "#000000",
                                            },
                                        },
                                    }}
                                    >
                                    {isLogin ? "Login" : "Register"}
                                </Button>
                            </Stack>
                        </form>
                        {message && (
                            <Text c="red" align="center" style={{ marginTop: "10px" }}>
                                {message}
                            </Text>
                        )}
                        <Divider />
                        <Group position="center">
                            <Button
                                variant="outline"
                                fullWidth
                                size="md"
                                styles={{
                                    root: {
                                        color: "#b8860b",
                                        borderColor: "#b8860b",
                                        borderRadius: "8px",
                                        transition: "background-color 0.3s ease",
                                        "&:hover": {
                                            backgroundColor: "fdf2db",
                                        },
                                    }
                                }}
                                onClick={() => setIsLogin(!isLogin)}
                            >
                                {isLogin
                                    ? "Don't have an account? Register"
                                    : "Already have an account? Login"}
                            </Button>
                        </Group>
                    </Stack>
                </Paper>
            </div>

            {/* Right side: Image */}
            <div 
                style={{ width: "75%", 
                backgroundSize:"cover",
                backgroundPosition:"center",
                backgroundImage:`url(${AwardsShow})`,
                position:"relative"
                }}
            >   
            </div>
        </div>
    );
};

export default LoginRegister;
