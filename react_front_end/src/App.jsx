import React from "react";
import NavigationBar from "./components/NavigationBar";
import ImageUploader from "./components/ImageUploader"
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import { ThemeConsumer } from "react-bootstrap/esm/ThemeProvider";

class App extends React.Component {

  ROOT = "http://localhost:3000";
  SERVER_URL = "http://127.0.0.1:5000";

  state = {
    searchText: "",
    uploadImageURLs: [],
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
    // reset state variable uploadImageURLs
    let imageURLs = [];
    // when file uploader input onChange: update state variable uploadImageFiles with only image files
    const files = event.target.files;
    // read image file content
    for ( let i = 0; i < files.length; i++ ) {
      // load file object
      const file = files[i]
      // file reader
      const reader = new FileReader();
      reader.onload = (event) => {
        const dataURL = event.target.result;
        // add dataURL to the state variable
        imageURLs[i] = dataURL;
      }
      reader.readAsDataURL(file);
    }
    this.state.uploadImageURLs = imageURLs;
  }

  handleImageUpload = event => {
    event.preventDefault();
    // send uploadImageURLs back to flask server
    const data = { images: this.state.uploadImageURLs };
    console.log(data)
    fetch('http://127.0.0.1:5000/add_images_check', {
      method:'POST',
      body: JSON.stringify(data),
      headers: {
        'Content-Type': 'application/json'
      },
    })
      .then((response) => response.json())
      .then((data) => {
        // response data
        console.log(data)
      })
        .catch((error) => {
          console.error(error);
        });
  }

  render() {
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
            <ImageUploader
              handleImageUploadSelect={this.handleImageUploadSelect}
              handleImageUpload={this.handleImageUpload}
              files={this.state.uploadImageURLs}
            />
          </Route>
          <Route path="/">
            <h1>Home</h1>
          </Route>
        </Switch>
        </Router>
      </div>
    );
  }
}

export default App;