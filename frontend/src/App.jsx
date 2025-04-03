import { useState } from "react";
import "./App.css";
import FaceMatch from "./app/FaceMatch";
function App() {
    const [events, setEvents] = useState([]);

    return <FaceMatch />;
}

export default App;
