import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "./Navbar";

const AdminDashboard = () => {
    const navigate = useNavigate();
    const [users, setUsers] = useState([]);
    const [polls, setPolls] = useState([]);
    const [question, setQuestion] = useState("");
    const [options, setOptions] = useState(["", ""]);
    const [message, setMessage] = useState("");
    const [selectedPollResult, setSelectedPollResult] = useState(null);

    useEffect(() => {
        const isAdmin = localStorage.getItem("is_admin");
        console.log("👀 isAdmin value:", isAdmin);
        console.log("🔄 Running fetchAdminData");


        if (isAdmin !== "true") {
            alert("Access denied! Admins only.");
            navigate("/");
        } else {
            fetchAdminData();
        }
    }, []);

    const fetchAdminData = async () => {
        try {
            const token = localStorage.getItem("authToken");
            const res = await fetch("http://localhost:5000/admin/users", {
                headers: { Authorization: `Bearer ${token}` },
            });

            const userData = await res.json();
            setUsers(userData);

            const pollsRes = await fetch("http://localhost:5000/polls", {
                headers: { Authorization: `Bearer ${token}` },
            });

            const pollData = await pollsRes.json();
            setPolls(pollData);
        } catch (error) {
            console.error("Failed to load admin data");
        }
    };

    const fetchPollResult = async (pollId) => {
        try {
            const res = await fetch(`http://localhost:5000/poll-results/${pollId}`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("authToken")}`,
                },
            });

            const data = await res.json();
            if (res.ok) {
                setSelectedPollResult(data);
            } else {
                setMessage(data.msg || "Failed to fetch results");
            }
        } catch (err) {
            setMessage("Error fetching poll results");
            console.error(err);
        }
    };

    const addOption = () => {
        setOptions([...options, ""]);
    };

    const removeOption = (index) => {
        if (options.length <= 2) return;
        const newOptions = options.filter((_, i) => i !== index);
        setOptions(newOptions);
    };

    const handleOptionChange = (index, value) => {
        const newOptions = [...options];
        newOptions[index] = value;
        setOptions(newOptions);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setMessage("");

        if (question.trim() === "" || options.some(opt => opt.trim() === "")) {
            setMessage("Please fill in all fields.");
            return;
        }

        try {
            const response = await fetch("http://localhost:5000/create-poll", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${localStorage.getItem("authToken")}`,
                },
                body: JSON.stringify({ question, options }),
            });

            const data = await response.json();
            if (response.ok) {
                setMessage("Poll created successfully!");
                setQuestion("");
                setOptions(["", ""]);
                fetchAdminData();
                setSelectedPollResult(null);
            } else {
                if (response.status === 401 && data.msg === "Token has expired") {
                    setMessage("Session expired. Please login again.");
                    localStorage.removeItem("authToken");
                    navigate("/auth");
                } else {
                    setMessage(data.msg || "Error creating poll.");
                }
            }
        } catch (error) {
            setMessage("Failed to connect to the server.");
        }
    };

    return (
        <div>
            <Navbar />
            <h1>Admin Dashboard</h1>
            {message && <p>{message}</p>}

            <h2>Create a Poll</h2>
            <form onSubmit={handleSubmit}>
                <label>Poll Question</label><br />
                <input type="text" placeholder="Poll Question" value={question} onChange={(e) => setQuestion(e.target.value)} required /><br />
                <label>Options</label>
                {options.map((option, index) => (
                    <div key={index} style={{ display: "flex", gap: "8px" }}>
                        <input
                            type="text"
                            placeholder={`Option ${index + 1}`}
                            value={option}
                            onChange={(e) => handleOptionChange(index, e.target.value)}
                            required
                        />
                        {options.length > 2 && (
                            <button type="button" onClick={() => removeOption(index)}>Remove</button>
                        )}
                    </div>
                ))}
                <button type="button" onClick={addOption}>Add Option</button>
                <button type="submit">Create Poll</button>
            </form>

            <h2>Users</h2>
            <ul>
                {users.map(user => (
                    <li key={user.id}>{user.username} - {user.email}</li>
                ))}
            </ul>

            <h2>Polls</h2>
            {polls.length === 0 && <p>No polls found or failed to fetch.</p>}

            <ul>
                {polls.map(poll => (
                    <li key={poll.id}>
                        <strong>{poll.question}</strong>
                        <button onClick={() => fetchPollResult(poll.id)} style={{ marginLeft: "10px" }}>
                            View Results
                        </button>
                    </li>
                ))}
            </ul>

            {selectedPollResult && (
                <div style={{ marginTop: "20px", border: "1px solid gray", padding: "15px" }}>
                    <h3>Results for: {selectedPollResult.question}</h3>
                    <ul>
                        {selectedPollResult.results.map((res, idx) => (
                            <li key={idx}>{res.option}: {res.votes} vote(s)</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default AdminDashboard;
