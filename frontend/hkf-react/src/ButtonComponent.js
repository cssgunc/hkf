import React, {Component} from 'react';

//might be useful for download/upload/export functions
class ButtonComponent extends Component {
    render() {
        return (
            <div className="button">
                {/* <button name="upload" onClick ={e => this.props.onClick(e.target.name)}>Upload</button> */}
                {/* <button name="download" onClick ={e => this.props.onClick(e.target.name)}>Download</button> */}
                <button name="export" onClick ={e => this.props.onClick(e.target.name)}>Export</button>
                <br/><br/>
            </div>
        )
    }
}

export default ButtonComponent;