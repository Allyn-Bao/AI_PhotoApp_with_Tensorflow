import React from "react";
import "./ImageUploader.css"
import UploadImages from "./UploadImages";

class ImageUploader extends React.Component {

    render() {
        return (
            <div className="container image-uploader">
            <span className="card d-flex flex-column border border-dark rounded p-3" >
                <h3>Upload Images
                <small className="text-muted">  Currenty Supported: JPEG</small>
                </h3>
                <div className="d-flex flex-row justify-content-center align-items-center">
                    <input 
                        className="form-control"
                        type="file" 
                        multiple
                        onChange={(event) => this.props.handleImageUploadSelect(event)}
                        accept="image/jepg"
                    />
                    <button 
                        className="btn btn-dark"
                        type="submit"
                        onClick={this.props.handleImageUpload}
                    >Upload</button>
                </div>
            </span>
            <h4 class="text-muted">{this.props.uploadMessage}</h4>
            <UploadImages imageList={this.props.imageList}/>
            </div>
        );
    }
}

export default ImageUploader;