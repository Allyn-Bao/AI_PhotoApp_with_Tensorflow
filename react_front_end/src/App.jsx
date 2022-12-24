import React from "react";
import {setState, useState} from "react";
import NavigationBar from "./components/NavigationBar";
import ImageGallery from "./components/ImageGallery";
import ImageUploader from "./components/ImageUploader";
import UploadImageList from "./components/UploadImageList";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";


class App extends React.Component {

  ROOT = "http://localhost:3000";
  SERVER_URL = "http://127.0.0.1:5000";

  state = {
    imageList: [],
    searchText: "",
    uploadImageURLs: [],
    updated: false
  }

  

  handleRoute(route) {
    console.log("route to: ", route)

    
  }

  handleSearchInput = event => {
    // when search input onChange: update state variable searchText with new input
    this.setState({
      searchText: event.target.value
    });
  }

  handleSearch(keyword) {
    // update state variable image list according to album / keywords
    console.log("searching: ", keyword)

  }

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

  handleImageUpload = event => {
    // stop auto refreshing
    event.preventDefault();
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
        console.log(data)
        this.setState({ imageList: data.updated_images })
      })
        .catch((error) => {
          console.error(error);
        });
    // window.location.reload();
    // set reload home page
    this.setState({ updated: false })
  }

  render() {
    
    if (this.state.updated == false) {
      // get image
      fetch(`${this.SERVER_URL}/images`, {
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
          this.state.imageList = data.images;
          this.setState({ updated: true });
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
          searchText={this.state.searchText}
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
              files={this.state.uploadImageURLs}
            />
            <UploadImageList
              uploadImageURLs={this.state.uploadImageURLs}
            />
            </div>
          </Route>
          <Route path="/">
            <ImageGallery
              imageList={this.state.imageList}
            />
          </Route>
        </Switch>
        </Router>
      </div>
    );
  }
}

export default App;