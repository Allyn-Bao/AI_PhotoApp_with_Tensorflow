import { render } from "@testing-library/react";
import React from "react";
import "./AlbumList.css";
import {Link} from "react-router-dom";


class AlbumList extends React.Component {

    render() {

        const imageStyle = {
            objectFit: "cover",
            overflow: "hidden",
        };

        return (
            <div>
                <div className="album-list">
                    {this.props.albumCoverList.map((albumCoverURL, index) => {
                        return (
                            <div key={index} className="image-container">
                                <h1 className="album-label"
                                    onClick={() => this.props.handleAlbumClick(index)}
                                    >{this.props.albumLabelList[index]}</h1>
                                 <img 
                                    className="rounded mx-auto d-block album-cover"
                                    onClick={() => this.props.handleAlbumClick(index)}
                                    key={index} src={albumCoverURL} loading="lazy" style={imageStyle} alt="image"/>
                            </div>
                        )
                    })}
                </div>
            </div>
        );
    }
    
}

export default AlbumList;