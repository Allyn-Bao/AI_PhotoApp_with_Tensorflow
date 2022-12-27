import { render } from "@testing-library/react";
import React from "react";
import "./UploadImages.css";


class ImageGallery extends React.Component {

    render() {

        const imageStyle = {
            width: "100%",
            height: "100%",
            objectFit: "cover",
            overflow: "hidden",
        };

        return (
            <div>
                <div className="image-list">
                    {this.props.imageList.map((imageURL, index) => {
                        return (
                            <div key={index} className="image-container">
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