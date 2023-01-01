import React from "react";
import "./Message.css"

class Message extends React.Component {
    render() {
        return (
            this.props.message != "" && <h4 className="message">{this.props.message}</h4>
        )
    }
}

export default Message;

