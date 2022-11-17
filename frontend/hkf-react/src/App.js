import React, {Component} from 'react';
import ButtonComponent from './ButtonComponent';
import ChooseComponent from './ChooseFileComponent';

class App extends Component {

  render() {
    return (
        <div>
            <div className="app-body">
                <h1>HKF</h1>
                <ChooseComponent/> <br/><br/>
            </div>
        </div>
    );
  }


  constructor() {
    super();

    this.state = {
      result: ""
    }
  }

  onClick = button => {
  }

}

export default App;
