import React from "react";
import {Form} from "react-bootstrap";
import "./ImageUploader.css"
import ImageGallery from "./ImageGallery";

class ImageUploader extends React.Component {

    render() {
        return (
            <div className="image-uploader">
            <Form>
                <h1>Upload Images</h1>
                <input 
                    type="file" 
                    multiple
                    onChange={(event) => this.props.handleImageUploadSelect(event)}
                    accept="image/jepg"
                />
                <button 
                    type="submit"
                    onClick={this.props.handleImageUpload}
                >Upload</button>
            </Form>
            <h1>Selected Images</h1>
            <ImageGallery imageList={this.props.files}/>
            </div>
        );
    }
}

export default ImageUploader;