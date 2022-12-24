import React from "react";


class UploadImageList extends React.Component {

    render() {

        const imageStyle = {
            width: '600px',
            height: 'auto',
        };

        return (
            <div className="upload image list">
                {this.props.uploadImageURLs.map((imageURL, index) => {
                    return <img 
                    key={index}
                    src={imageURL} 
                    style={imageStyle} 
                    alt="image"/>;
                })}
            </div>
        )
    }
}

export default UploadImageList;