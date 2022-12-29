import React from "react";
import {Navbar, Nav, Container, Form, FormControl, Button} from "react-bootstrap"
import { BrowserRouter, Switch, Route, Link } from "react-router-dom"


class NavigationBar extends React.Component {

    render() {
        return (
            <Navbar  fixed="top" bg="dark" variant="dark" expand="lg">
                <Container>
                    <Navbar.Brand>Photos</Navbar.Brand>
                    <Navbar.Toggle aria-controls="navbarScroll" />
                    <Navbar.Collapse id="navbarScroll">
                    <Nav 
                    className="me-auto my-2 my-lg-0"
                    style={{ maxHeight: '100px' }}
                    navbarScroll
                        >
                        <Nav.Link as={Link} to={"/"} onClick={this.props.handleHomeClick}>Home</Nav.Link>
                        <Nav.Link as={Link} to={"/albums"} onClick={this.props.handleAlbumsClick}>Albums</Nav.Link>
                        <Nav.Link as={Link} to={"/add_photos"}>Add Photos</Nav.Link>
                    </Nav>
                        <Form className="d-flex">
                            <FormControl
                                onChange={this.props.handleSearchInput}
                                type="text"
                                placeholder="keyword"
                                className="me-2"
                            />
                            <Button 
                                variant="outline-success" 
                                onClick={() => this.props.handleSearch(this.props.searchKeywords)}>Search</Button>
                        </Form>
                    </Navbar.Collapse>
                </Container>
            </Navbar>
        )
    }
}

export default NavigationBar;