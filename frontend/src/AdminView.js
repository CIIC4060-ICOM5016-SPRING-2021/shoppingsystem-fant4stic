import React, {Component, useEffect, useState} from 'react';
import {Button, Card, Container, Divider, Header, Modal, Tab, Icon} from "semantic-ui-react";
import Dashboard from "./Dashboard";
import Products from "./Products";
import { useNavigate } from 'react-router-dom';

function AdminView(){
    const [isAuth, setIsAuth] = useState(true)
    const [verifyLogOut, setVerifyLogOut] = useState(false)
    const [view, setView] = useState('/AdminView')
    const navigate = useNavigate();
    //Retrieve info of admin login values, same thing should be done for registered values:
    const loginvalues = JSON.parse(localStorage.getItem('loginValues'));
    const email = loginvalues['inputEmail'];
    console.log("Email Stored: " + email);
    const password = loginvalues['inputPassword'];
    console.log("Password Stored: " + password);

    const handleChange = (event) => {
        setVerifyLogOut(true)
    }

    const logOut = (event) =>{
        if(view === '/AdminView'){
            // When login out reset login values used to enter to website
            localStorage.setItem('loginValues',JSON.stringify({inputEmail: "", inputPassword : ""}))
            setView('/')
            navigate('/')
        }
        else if(view === '/'){
            setView('/AdminView')
        }
    }

    const panes = [
        {
            menuItem: 'Products', render: () => (
                <Tab.Pane active={isAuth}>
                    <Container>
                        <Header>Modify Fant4stic Store Products:</Header>
                        <Divider/>
                    </Container>
                    <Products/></Tab.Pane>
            )
        },
        {
            menuItem: 'Profile', render: () => (
                <Tab.Pane active={isAuth}>
                    <Modal
                        centered={false}
                        open={verifyLogOut}
                        onClose={() => setVerifyLogOut(false)}
                        onOpen={() => setVerifyLogOut(true)}
                    >
                        <Modal.Header>Are you sure you want to Logout?</Modal.Header>
                        <Modal.Actions>
                            <Button color='green' onClick={logOut}>YES</Button>
                            <Button color='red' onClick={() => {setVerifyLogOut(false)}}>NO</Button>
                        </Modal.Actions>
                    </Modal>
                    <Header as='h2' color='blue'>
                    <Icon name='briefcase'/>Admin's Profile
                    </Header>
                    <Button content = 'LogOut' color='red' onClick={handleChange}/>
                </Tab.Pane>
            )
        },
        {
            menuItem: 'Dashboard', render: () => (
                <Tab.Pane active={isAuth}><Dashboard/></Tab.Pane>
            )
        }
    ]

    return <Tab panes={panes}/>

}
export default AdminView;