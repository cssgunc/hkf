import React, { useState } from "react";
import axios from 'axios';
import { read, utils} from "xlsx";
import * as Excel from "exceljs";
import {Readable} from 'readable-stream'

import './ChooseFileComponent.css';

function ChooseFileComponent() {
  const [parsedSheet, setParsedSheet] = useState('')
  const [people, setPeople] = useState([]); //original excel file uploaded by user
  const [excel, setExcel] = useState([]); //displays uploaded file
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
          setParsedSheet(JSON.stringify(rows))
          setExcel(rows);
        }
      };
      reader.readAsArrayBuffer(file);
    }
  }

  //sends a POST request with the uploaded Excel file, currently to Postman
  function handleRequest(e) {
    e.preventDefault();
    //replace temporary Postman POST request with API call

    const formData = new FormData();
    formData.append('data', parsedSheet);
    setStatus("loading")
    fetch('/input', {
      method: "POST",
      body: formData
    }).then(async res => {
      const data = await res.text()
/*
      var element = document.createElement('a');
      element.setAttribute('href', encodeURIComponent(data));
      element.setAttribute('download', 'output.');
    
      element.style.display = 'none';
      document.body.appendChild(element);
    
      element.click();
    
      document.body.removeChild(element);
*/
      const s = new Readable()
      s.push(data)
      s.push(null)
      const work = new Excel.Workbook()
      await work.csv.read(s)
      const buffer = await work.xlsx.writeBuffer()

      var a = document.createElement("a");
      document.body.appendChild(a);
      a.style = "display: none";
      var blob = new Blob([buffer], {type: "application/xlsx"});
      let url = window.URL.createObjectURL(blob);
    a.href = url;
    a.download = "output.xlsx";
    a.click();
    window.URL.revokeObjectURL(url);
    setStatus("success")

    }).catch(err =>{
      console.error(err)
      setStatus("error")
    })
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
      </div>

      {/* the following div contains a preview of the uploaded excel sheet*/}
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