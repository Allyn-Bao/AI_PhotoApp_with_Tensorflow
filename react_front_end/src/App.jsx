import React from "react";
import {setState, useState} from "react";
import NavigationBar from "./components/NavigationBar";
import ImageGallery from "./components/ImageGallery";
import ImageUploader from "./components/ImageUploader";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";


class App extends React.Component {

  ROOT = "http://localhost:3000";
  SERVER_URL = "http://127.0.0.1:5000";

  state = {
    allImages:[], // all images without filters, for quick reloading to all images
    imageList: [],  // list of image URLs given the current filters applied
    searchKeywords: "",  // current search keyword in the search bar
    uploadImageURLs: [],  // list of image URLs going to be uploaded to the backend
    uploadMessage: "", // message prompt for comforming successful upload
    selectEnabled: false, // select control for delete / download images in Gallary, checkboxes appears when selectEnabled
    selectedIndex: [], // image index in imageList if images are selected - keep track of if images are selected / should be unselected
    selectedImages: [], // images in Gallery selected
    imageGalleryMessage: "", // message prompt for search / select / delete
    updated: false  // false when page is reload or image uploaded, a signal to update / fatch the imageList
    
  }
  
  /*
  Go to page / reload page and update content
  */
  // when Home button in navbar is pressed
  handleHomeClick = () => {
    // reset images to all, clear all keyword search
    this.setState({ imageList: this.state.allImages })
    this.setState({ searchKeywords: "" })
    this.setState({ imageGalleryMessage: "" })
    // if comming from Add Photos: clear uploadImageURLs
    this.setState({ uploadImageURLs: [] })
    this.setState({ uploadMessage: "" })
  }
  // when album button in navbar is pressed
  handleAlbumClick = () => {
  }

  /*
  Search bar functions
  */
  // When Search input updated ( user changed text in search bar )
  handleSearchInput = event => {
    // when search input onChange: update state variable searchKeyword with new input
    this.setState({
      searchKeywords: event.target.value
    });
  }
  // When "Search" button is clicked - get search result and update imageList
  handleSearch = (keyword) => {
    // update state variable image list according to album / keywords
    console.log("searching: ", keyword)

    fetch('http://127.0.0.1:5000/images', {
      method:'POST',
      body: JSON.stringify({
        album: null,
        keywords: [keyword],
      }),
      headers: {
        'Content-Type': 'application/json'
      },
    })
      .then((response) => response.json())
      .then((data) => {
        // response data
        console.log(data.condition)
        this.setState({ imageList: data.images })
        this.setState({ imageGalleryMessage: data.condition })
      })
        .catch((error) => {
          console.error(error);
        });

  }

  /*
  ImageGallery
  */
  // When select clicked
  updateSelect = () => {
    // toogle the state of selectEnabled between true and false
    const currentState = this.state.selectEnabled;
    this.setState({ selectEnabled: !currentState })
    // if select toogled off - clear all selectedImages
    if (currentState) {
      this.setState({ selectedIndex: [] })
      this.setState({ selectedImages: [] })
    }
}
  // When Image selected
  handleSelectGalleryImage = (index) => {
    console.log(`Selected: index: ${index}`)
    // selected image
    const selectedImage = this.state.imageList[index];
    // if index already in selected index - need to unselect - remove from list
    if (this.state.selectedIndex.includes(index)) {
      // new selectedIndex & selectedImages with current image removed
      const updatedSelectedIndex = this.state.selectedIndex.filter(i => i != index);
      const updatedSelectedImages = this.state.selectedImages.filter(image => image != selectedImage);
      this.setState({ selectedIndex: updatedSelectedIndex })
      this.setState({ selectedImages: updatedSelectedImages })
      
    } else {
      // select image, add to lists
      const updatedSelectedIndex = this.state.selectedIndex.concat(index);
      const updatedSelectedImages = this.state.selectedImages.concat(selectedImage)
      this.setState({ selectedIndex: updatedSelectedIndex })
      this.setState({ selectedImages: updatedSelectedImages })
    }
  }
  // handle delte images
  handleDeleteImages = () => {
    // check if selected Enabled
    if (this.state.selectEnabled) {
      console.log(`index to delete: ${this.state.selectedIndex}`)
      console.log(`images to delete: ${this.state.selectedImages}`)
      // send delete request back to server
      fetch('http://127.0.0.1:5000/delete_images', {
      method:'POST',
      body: JSON.stringify({
        deleteImages: this.state.selectedImages,
        album: null,
        keywords: [],
      }),
      headers: {
        'Content-Type': 'application/json'
      },
    })
      .then((response) => response.json())
      .then((data) => {
        // response data
        console.log(data.condition)
        this.setState({ imageList: data.updated_images })
        this.setState({ allImages: data.all_images })
        this.setState({ imageGalleryMessage: data.condition })
      })
        .catch((error) => {
          console.error(error);
        });
      // reset selected images lists
      this.updateSelect();
    }
  }

  /*
  Upload images
  */
  // When user select file from local - update uploadImageURLs with URLs of selected file
  handleImageUploadSelect = (event) => {
    // when file uploader input onChange: update state variable uploadImageFiles with only image files
    const files = event.target.files;
    // read image file content
    const imageURLs = Array.from(files).map((file) => {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = event => {
          resolve(event.target.result);
        };
        reader.onerror = reject;
        reader.readAsDataURL(file);
      });
    });
    Promise.all(imageURLs).then((imageURLs) => {
      this.setState({ uploadImageURLs: imageURLs });
    });
  };
  // When "Upload" button is clicked - upload image URLs to the backend and get updated imageList
  handleImageUpload = event => {
    // stop auto refreshing for debugging
    // event.preventDefault();
    // send uploadImageURLs back to flask server
    fetch('http://127.0.0.1:5000/add_images', {
      method:'POST',
      body: JSON.stringify({
        imageURLs: this.state.uploadImageURLs,
        album: null,
        keywords: [],
      }),
      headers: {
        'Content-Type': 'application/json'
      },
    })
      .then((response) => response.json())
      .then((data) => {
        // response data
        // console.log(data)
        // this.setState({ imageList: data.updated_images })
        // this.setState({ allImages: data.all_images })
        console.log(data.condition)
        this.setState({ uploadMessage: data.condition })

      })
        .catch((error) => {
          console.error(error);
        });
    // set to reload
    // this.setState({ updated: false })
  }

  render() {
    
    // update displayed images when page is refreshed or new images uploaded
    if (this.state.updated == false) {
      // get image
      fetch(`http://127.0.0.1:5000/images`, {
        method:'POST',
        body: JSON.stringify({
          album: null,
          keywords: [],
        }),
        headers: {
          'Content-Type': 'application/json'
        },
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(data.condition)
          this.state.allImages = data.images;
          this.state.imageList = data.images;
          this.setState({ updated: true });
          this.setState({ imageGalleryMessage: "" })
        })
          .catch((error) => {
            console.error(error);
          }) 
    }

    return (
      <div>
        <Router>
        <NavigationBar
          handleRoute={this.handleRoute}
          handleSearchInput={this.handleSearchInput}
          handleSearch={this.handleSearch}
          searchKeywords={this.state.searchKeywords}
          handleHomeClick={this.handleHomeClick}
        />
        <Switch>
          <Route path="/albums">
            <h1>Albums</h1>
          </Route>
          <Route path="/add_photos">
            <div>
            <ImageUploader
              handleImageUploadSelect={this.handleImageUploadSelect}
              handleImageUpload={this.handleImageUpload}
              imageList={this.state.uploadImageURLs}
              uploadMessage={this.state.uploadMessage}
            />
            </div>
          </Route>
          <Route path="/">
            <ImageGallery
              imageList={this.state.imageList}
              selectEnabled={this.state.selectEnabled}
              updateSelect={this.updateSelect}
              handleSelectGalleryImage={this.handleSelectGalleryImage}
              handleDeleteImages={this.handleDeleteImages}
              imageGalleryMessage={this.state.imageGalleryMessage}
            />
          </Route>
        </Switch>
        </Router>
      </div>
    );
  }
}

export default App;