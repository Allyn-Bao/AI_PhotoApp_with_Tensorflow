import logo from './logo.svg';
import './App.css';
import React from "react";
import { useState } from 'react';
import NavigationBar from './NavigationBar';
import ImageGallery from './ImageGallery';
import NavButtons from './navButtons';

function App() {
  // constants
  const appIcon = useState("")

  // state variables
  // images list
  const [images, setImages] = useState([]);
  // albums
  const [albums, setAlbums] = useState([]);
  // album covers
  const [albumCovers, setAlbumCovers] = useState([]);
  // toggle between home and albums
  const [isHome, setIsHome] = useState(true);

  // when home button is clicked
  function handleHomeClick() {
    setIsHome(true);
  }
  // when album button is clicked
  function handleAlbumClick() {
    setIsHome(false);
  }
  // search
  function handleSearchClick(searchTerm) {
    // 
    console.log("term searched: " + searchTerm)
  }

  return (
    <div className="App">
      <NavigationBar
      appIcon={appIcon}
      onSearchClick={handleSearchClick}
      />
      <ImageGallery

      />
      <NavButtons
      />


    </div>
  );
}

export default App;
