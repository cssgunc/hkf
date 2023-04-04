import React, { useState } from "react";
import ChooseFileComponent from "./components/ChooseFileComponent";

function App() {
  // const [people, setPeople] = useState([]);

  return (
    <div>
      <div className="app-body">
        <div className="info">
          <h1>Human Kindness Foundation | Location Tracker</h1>
          <h3>Instructions:</h3>
          <h5>1. Upload a file using the "Choose File" button. The format of this file should be xlsx.</h5>
          <h5>2. Select "Find Addresses" to get each person's location.</h5>
          <h5>3. Download the changed file with "Download New File".</h5>
        </div>
        <ChooseFileComponent/> <br />
        <br />
      </div>
    </div>
  );
}

export default App;
