import React from "react";
import "./EditButtons.css";

class EditButtons extends React.Component {
    render() {
        return (
            <div className="btn-group" role="group" aria-label="Edit Buttons">
                    <button type="button" className="btn btn-secondary btn-dark border-dark" onClick={this.props.updateSelect}>{this.props.selectEnabled ? "Unselect": "Select"}</button>
                    <button type="button" className="btn btn-secondary btn-dark border-dark" onClick={this.props.handleDeleteImages}>Delete</button>
            </div>
        )
    }
}

export default EditButtons;