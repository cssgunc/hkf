import React, { useState } from "react";
import ChooseFileComponent from "./components/ChooseFileComponent";

function App() {
  // const [people, setPeople] = useState([]);

  return (
    <div>
      <div className="app-body">
        <h1>Human Kindness Foundation | Location Tracker</h1>
        <ChooseFileComponent/> <br />
        <br />
      </div>
    </div>
  );
}

export default App;
