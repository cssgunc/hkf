import React, { useState } from "react";  
import { read, utils, write, writeFile } from 'xlsx';

const ChooseComponent = () => {
    const [people, setPeople] = useState([]);

    const handleImport = ($event) => {
        const files = $event.target.files;
        if (files.length) {
            const file = files[0];
            const reader = new FileReader();
            reader.onload = (event) => {
                const wb = read(event.target.result);
                const sheets = wb.SheetNames;

                if (sheets.length) {
                    const rows = utils.sheet_to_json(wb.Sheets[sheets[0]]);
                    setPeople(rows)
                }
            }
            reader.readAsArrayBuffer(file);
        }
    }

    const handleDownload = () => {
        const headings = [[
            'First Name',
            'Last Name',
            'Inmate ID',
            'Prison Name',
            'Address 1',
            'City',
            'State',
            'Zip Code'
        ]];
        const wb = utils.book_new();
        const ws = utils.json_to_sheet([]);
        utils.sheet_add_aoa(ws, headings);
        utils.sheet_add_json(ws, people, { origin: 'A2', skipHeader: true });
        utils.book_append_sheet(wb, ws, 'Report');
        writeFile(wb, 'Inmate Report.csv');

        
    }

    return (
        <> 
            <div className="custom-file">
                <input type="file" name="file" className="custom-file-input" id="inputGroupFile" required onChange={handleImport}
                    accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel"/>
                <label className="custom-file-label" htmlFor="inputGroupFile"></label>
            </div>
            <div>
                <button onClick={handleDownload} className="btn btn-primary float-right">
                    Download as CSV<i className="fa fa-download"></i>
                </button>
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
                            {/* <th scope="col">Found in Inmate Search?</th>
                            <th scope="col">Same Address?</th>
                            <th scope="col">New Prison Name</th>
                            <th scope="col">New Prison Address</th> */}
                        </tr>
                    </thead>
                    <tbody> 
                            {
                                people.length
                                ?
                                people.map((person, index) => (
                                    <tr key={index}>
                                        <th scope="row">{ index + 1 }</th>
                                        <td>{ person.Fname}</td>
                                        <td>{ person.Lname}</td>
                                        <td>{ person.InmateID}</td>
                                        <td>{ person.PrisonName}</td>
                                        <td>{ person.ADD1}</td>
                                        <td>{ person.CITY}</td>
                                        <td>{ person.STATE}</td>
                                        <td>{ person.ZIP}</td> 
                                        {/* <td>{ person.Found_in_Inmate_Search}</td>
                                        <td>{ person.Same_Address}</td>
                                        <td>{ person.New_Prison_Name}</td>
                                        <td>{ person.New_Prison_Address}</td>  */}
                                    </tr> 
                                ))
                                :
                                <tr>
                                    <td colSpan="5" className="text-center">No Data.</td>
                                </tr> 
                            }
                    </tbody>
                </table>
            </div>
        </>

    );
};

export default ChooseComponent;