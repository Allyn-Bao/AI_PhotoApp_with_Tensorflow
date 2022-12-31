import { render } from "@testing-library/react";
import React from "react";
import "./AlbumList.css";
import {Link} from "react-router-dom";
import ImageGallery from "./UploadImages";


class AlbumList extends React.Component {

    render() {

        const imageStyle = {
            objectFit: "cover",
            overflow: "hidden",
        };

        return (
            <div>
                {
                    this.props.currentAlbum == null ? 

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
                    
                    : 

                    <div className="album-gallery">
                    <ImageGallery
                        imageList={this.props.imageList}
                        selectEnabled={this.props.selectEnabled}
                        updateSelect={this.props.updateSelect}
                        handleSelectGalleryImage={this.props.handleSelectGalleryImage}
                        handleDeleteImages={this.props.handleDeleteImages}
                        imageGalleryMessage={this.props.imageGalleryMessage}
                    />
                    </div>
                }
            </div>
        );
    }
    
}

export default AlbumList;