import React from "react";
import NavigationBar from "./components/NavigationBar";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";

class App extends React.Component {

  state = {
    searchText: ""
  }

  handleRoute(route) {
    console.log("route to: ", route)
  }

  handleSearchInput = event => {
    this.setState({
      searchText: event.target.value
    });
  }

  handleSearch(keyword) {
    console.log("searching: ", keyword)
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
            <h1>Add Photos</h1>
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