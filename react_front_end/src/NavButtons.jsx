import React from "react";

function NavButtons(props) {

    return (
        <div>
            <button onClick={props.onHomeClick}>Home</button>
            <button onClick={props.onAlbumsClick}>Albums</button>
        </div>
    )
}

export default NavButtons;