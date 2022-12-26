import { render } from "@testing-library/react";
import React from "react";
import "./ImageGallery.css";


class ImageGallery extends React.Component {

    state = {
        selectEnabled: false,
        selectButtonText: " Select "
    }

    updateSelect = () => {
        const currentState = this.state.selectEnabled;
        this.setState({ selectEnabled: !currentState })
        this.setState({ selectButtonText: currentState ? "Unselect": " Select " })
    }

    render() {

        const imageStyle = {
            width: '100%',
            height: '100%',
            objectFit: "cover",
            overflow: "hidden",
        };

        return (
            <div>
                <div className="btn-group edit-buttons" role="group" aria-label="Edit Buttons">
                    <button type="button" className="btn btn-secondary" onClick={this.updateSelect}>{this.state.selectButtonText}</button>
                    <button type="button" className="btn btn-secondary">Delete</button>
                </div>
                <div className="image-gallery">
                    {this.props.imageList.map((imageURL, index) => {
                        return <img 
                            className="rounded mx-auto d-block"
                            key={index} src={imageURL} loading="lazy" style={imageStyle} alt="image"/>;
                    })}
                </div>
            </div>
        );
    }
    
}

export default ImageGallery;