import React from "react";

function NavigationBar(props) {

    return (
        <div className="NavigationBar">
            <img src={props.appIcon} alt="app-icon" />
            <span>{props.appName}</span>
            <input type="text" placeholder="keyword" />
            <button onClick={ () => props.onSearchClick(input.value)}>Search</button>
        </div>
    );
}

export default NavigationBar;