import { useState } from "react";
import "./App.css";
import GetYourPhotos from "./app/GetYourPhotos";

function App() {
  const [events, setEvents] = useState([]);

  return <GetYourPhotos />;
}

export default App;
