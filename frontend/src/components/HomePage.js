import React from 'react';
import { Button, Container, Stack, Title, Text} from "@mantine/core";
import { useNavigate } from "react-router-dom";
import Navbar from './Navbar';


const HomePage = ({ onLogout }) => {
    const navigate = useNavigate();

    const isAdmin = localStorage.getItem("is_admin") === "true";

    return (
        <Container style={{ 
            height:"100vh", 
            display:"flex", 
            flexDirection: "column",
            alignItems:"center",
            paddingTop: "80px"
        }}>
            <Navbar />
            <Stack align="center" spacing="xl">
                <Title align="center" order={1} style={{color : "#b8860b"}}>
                    Welcome to the MGI Award Polls!
                </Title>
                <Text align="center" size="lg" color="dimmed">
                    Cast your votes!
                </Text>
                <Button 
                    align="center"
                    size = "lg"
                    style = {{ backgroundColor: "#b8860b", color: "white", borderRadius:"8px"}}
                    onClick={() => navigate("/vote")}>
                        Let's Get to The Votes!
                </Button>
                <Button 
                    onClick = {onLogout}>
                    Logout
                </Button>
                {isAdmin && (
                <Button 
                    align="center"
                    size = "lg"
                    style = {{ backgroundColor: "#b8860b", color: "white", borderRadius:"8px"}}
                    onClick={() => navigate("/admin-dashboard")}>
                        Admin Dashboard
                </Button>
                )}
                
            </Stack>
        </Container>
    );
}

export default HomePage;