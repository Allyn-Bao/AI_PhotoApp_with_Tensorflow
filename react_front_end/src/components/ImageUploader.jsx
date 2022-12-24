import React from "react";
import {Form} from "react-bootstrap";

class ImageUploader extends React.Component {

    render() {
        return (
            <div>
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
            </div>
        );
    }
}

export default ImageUploader;