import React from "react";
import "./ImageGallery.css";
import EditButtons from "./EditButtons";


class ImageGallery extends React.Component {

    render() {

        const imageStyle = {
            objectFit: "cover",
            overflow: "hidden",
        };

        return (
            <div>
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
                <div className="edit-buttons">
                <EditButtons 
                    selectEnabled={this.props.selectEnabled}
                    updateSelect={this.props.updateSelect}
                    handleDeleteImages={this.props.handleDeleteImages}   
                />
                </div>
            </div>
        );
    }
    
}

export default ImageGallery;