import { render } from "@testing-library/react";
import React from "react"

class ImageGallery extends React.Component {
    render() {

        const imageStyle = {
            width: '300px',
            height: 'auto',
        };

        return (
            <div className="image-gallery">
                {this.props.imageList.map((imageURL, index) => {
                    return <img key={index} src={imageURL} style={imageStyle} alt="image"/>;
                })}
            </div>
        );
    }
    
}

export default ImageGallery;