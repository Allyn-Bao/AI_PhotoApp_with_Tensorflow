import { render } from "@testing-library/react";
import React from "react";


class ImagePreview extends React.Component {
  render() {
    const imageStyle = {
      width: "100%",
      height: "100%",
      objectFit: "contain",
    };
    return (
      <div className="image-preview">
        <div className="semi-transparent-black-fill" />
        <img src={this.props.imageURL} style={imageStyle} alt="image" />
        <button onClick={onClose}>Close</button>
      </div>
    );
  }
}

export default ImagePreview;
