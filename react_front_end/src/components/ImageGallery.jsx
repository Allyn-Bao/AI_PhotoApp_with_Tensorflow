import { render } from "@testing-library/react";
import React from "react";
import "./ImageGallery.css";


class ImageGallery extends React.Component {

    render() {

        const imageStyle = {
            objectFit: "cover",
            overflow: "hidden",
        };

        return (
            <div>
                {/* <h4 className="text-muted">{this.props.imageGalleryMessage}</h4> */}
                <div className="btn-group edit-buttons " role="group" aria-label="Edit Buttons">
                    <button type="button" className="btn btn-secondary opacity-80 bg-dark border-dark" onClick={this.props.updateSelect}>{this.props.selectEnabled ? "Unselect": "Select"}</button>
                    <button type="button" className="btn btn-secondary opacity-80 bg-dark border-dark" onClick={this.props.handleDeleteImages}>Delete</button>
                </div>
                
                <div className="image-gallery">
                    {this.props.imageList.map((imageURL, index) => {
                        return (
                            <div key={index} className="image-container">
                                {
                                    this.props.selectEnabled &&  <input className="form-check-input check-select" 
                                                                        type="checkbox" value="" 
                                                                        id="flexCheckDefault" 
                                                                        onChange={() => this.props.handleSelectGalleryImage(index)}></input>
                                }
                                 <img 
                                    className="rounded mx-auto d-block image"
                                    key={index} src={imageURL} loading="lazy" style={imageStyle} alt="image"/>
                            </div>
                        )
                    })}
                </div>
            </div>
        );
    }
    
}

export default ImageGallery;