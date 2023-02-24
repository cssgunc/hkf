import React, { useState } from "react";
import axios from 'axios';
import { read, utils, write, writeFile } from "xlsx";

function ChooseFileComponent() {
  const [people, setPeople] = useState([]);
  const [excel, setExcel] = useState([]);

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

  function handleDownload(e) {
    e.preventDefault();
    const formData = new FormData();
    formData.append('profileImg', people);
    axios.post('https://8ed818d6-4b3c-405d-b4d8-0c3dae7eec19.mock.pstmn.io/post', formData, {
    }).then(res => {
      console.log(res);
    })
      .catch(error => {
        console.log(error);
      });


    const headings = [
      [
        "First Name",
        "Last Name",
        "Inmate ID",
        "Prison Name",
        "Address 1",
        "City",
        "State",
        "Zip Code",
      ],
    ];
    const wb = utils.book_new();
    const ws = utils.json_to_sheet([]);
    utils.sheet_add_aoa(ws, headings);
    utils.sheet_add_json(ws, excel, { origin: "A2", skipHeader: true });
    utils.book_append_sheet(wb, ws, "Report");
    writeFile(wb, "Inmate Report.csv");
  }

  return (
    <div>
      <div className="container">
        <div className="row">
          <form onSubmit={handleDownload} enctype="multipart/form-data">
            <div className="form-group">
              <input type="file" name="file" onChange={handleImport} />
            </div>
            <div className="form-group">
              <button className="btn btn-primary" type="submit">Upload</button>
              <p>Note of incompleteness: the "upload" button currently sends a call to Postman 
                and downloads an unchanged CSV file.</p>
            </div>
          </form>
        </div>
      </div>

      <div>
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
                <td colSpan="2" className="text-center">
                  No Data.
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