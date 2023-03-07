import React, { useState } from "react";
import axios from 'axios';
import { read, utils, write, writeFile } from "xlsx";
import './ChooseFileComponent.css';

function ChooseFileComponent() {
  const [people, setPeople] = useState([]); //original excel file uploaded by user
  const [excel, setExcel] = useState([]); //displays uploaded file (NOTE: change to preview)
  const [newExcel, setNewExcel] = useState([]); //should store new file returned by API
  const [status, setStatus] = useState(''); //process status

  //accepts an xlsx file for API call; also generates preview on site
  function handleImport(event) {
    setPeople(event.target.files[0]);

    const files = event.target.files;
    if (files.length) {
      const file = files[0];
      const reader = new FileReader();
      reader.onload = (event) => {
        const wb = read(event.target.result);
        const sheets = wb.SheetNames;

        if (sheets.length) {
          const rows = utils.sheet_to_json(wb.Sheets[sheets[0]]);
          setExcel(rows);
        }
      };
      reader.readAsArrayBuffer(file);
    }
  }

  //sends a POST request with Excel file, currently to Postman
  function handleRequest(e) {
    e.preventDefault();
    const formData = new FormData();
    formData.append('profileImg', people);
    //replace temporary Postman POST request with API call
    axios.post('https://8ed818d6-4b3c-405d-b4d8-0c3dae7eec19.mock.pstmn.io/post', formData, {
    }).then(res => {
      console.log("Successfully sent POST request to Postman: ", res.data.data);
      // console.log(excel);
      setNewExcel(res.data.data);
      setStatus("complete");
    })
  }

  //sends a GET request to Postman
  //SHOULD return an Excel file for download when calling the actual API
  function handleExport() {
    //temporary Postman GET request to get changed Excel file
    axios.get('https://8ed818d6-4b3c-405d-b4d8-0c3dae7eec19.mock.pstmn.io/get', {
      method: 'GET'
    }).then((response) => {
      //GET request SHOULD return an Excel file here and then call setNewExcel() to set the value of newExcel
      //The following takes newExcel, which is an Excel sheet, and downloads it
      const wb = utils.book_new();
      const ws = utils.json_to_sheet([]);
      utils.sheet_add_json(ws, newExcel, { origin: "A2", skipHeader: true });
      utils.book_append_sheet(wb, ws, "Report");
      writeFile(wb, "Report.xlsx");
      setStatus("downloaded");
    });
  }

  return (
    <div className="wrapper">
      <div className="form">
        <form onSubmit={handleRequest} encType="multipart/form-data">
          <div className="form-group">
            <input
              type="file"
              name="file"
              onChange={handleImport}
              accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel"
              required
            />
          </div>
          <div className="form-group">
            <button className="btn btn-primary" type="submit">Find Addresses</button>
          </div>
        </form>
      </div>

      <div className="status">
        <label for="change-status">Status: </label>
        <input type="text" id="change-status" value={status} readOnly></input>
        <button className="tab" onClick={handleExport}>Download New File</button>
      </div>

      {/* the following div contains a preview of the uploaded excel sheet--probably clutters too much and will be removed */}
      <div className="preview">
        <table className="table">
          <thead>
            <tr>
              <th scope="col"></th>
              <th scope="col">First Name</th>
              <th scope="col">Last Name</th>
              <th scope="col">Inmate ID</th>
              <th scope="col">Prison Name</th>
              <th scope="col">Address 1</th>
              <th scope="col">City</th>
              <th scope="col">State</th>
              <th scope="col">Zip Code</th>
            </tr>
          </thead>
          <tbody className="max-height">
            {excel.length ? (
              excel.map((person, index) => (
                <tr key={index}>
                  <th scope="row">{index + 1}</th>
                  <td>{person.Fname}</td>
                  <td>{person.Lname}</td>
                  <td>{person.InmateID}</td>
                  <td>{person.PrisonName}</td>
                  <td>{person.ADD1}</td>
                  <td>{person.CITY}</td>
                  <td>{person.STATE}</td>
                  <td>{person.ZIP}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="8" className="low-opacity">
                  A preview of your spreadsheet will be shown here.
                </td>
              </tr>
            )}
          </tbody>
        </table>
        <br />
      </div>
    </div>
  );
}

export default ChooseFileComponent;