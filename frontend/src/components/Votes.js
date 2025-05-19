import { useEffect, useState } from "react";
import Navbar from "./Navbar";

const VotesPage = () => {
    const [polls, setPolls] = useState([]);
    const [votes, setVotes] = useState({}); // poll ID : option ID
    const [message, setMessage] = useState("");

    useEffect(() => {
        fetchPolls();
    }, []);

    const fetchPolls = async () => {
        try {
            const res = await fetch("http://localhost:5000/polls", {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("authToken")}`,
                }
            });
            const data = await res.json();
            setPolls(data);
        } catch(error) {
            console.error("Failed to fetch polls", error);
        }
    };

    const handleOptionChange = (pollId, optionId) => {
        setVotes((prevVotes) => ({
            ...prevVotes,
            [pollId]: optionId
        }));
    };

    const handleVoteSubmit = async (pollId) => {
        const selectedOptionId = votes[pollId];
        if(!selectedOptionId) {
            setMessage("Please select an option.");
            return;
        }

        try {
            const res = await fetch(`http://localhost:5000/vote/${pollId}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${localStorage.getItem("authToken")}`,
                },
                body: JSON.stringify({ optionId: selectedOptionId}),
            });

            const data = await res.json()
            if (res.ok) {
                setMessage("Vote submitted!");
                fetchPolls();
            } else {
                setMessage(data.msg || "Error submitting vote");
            }
        } catch (error){
            setMessage("failed to submit vote.");
        }
    };

    return (
        <div style={{paddingTop: "80px"}}>
            <Navbar />
            <h1>Vote on Current Polls</h1>
            {message && <p>{message}</p>}

            {polls.map((poll) => (
                <div key={poll.id} style={{marginBottom: "30px", border: "1px solid gray", padding: "10px" }}>
                    <h3>{poll.question}</h3>
                    {poll.options.map((option) => (
                        <div key={option.id}>
                            <input type="radio" id={option.id} name={`poll-${poll.id}`} value={option.id} 
                            checked={votes[poll.id] === option.id} onChange={() => handleOptionChange(poll.id, option.id)} />
                            <label htmlFor={option.id}>{option.text}</label>
                        </div>
                    ))}
                    <button onClick={() => handleVoteSubmit(poll.id)}>Submit Vote</button>
                </div>
            ))}
        </div>
    )
}

export default VotesPage;