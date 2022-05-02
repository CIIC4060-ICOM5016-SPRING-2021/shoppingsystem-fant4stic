import React, {Component, useState} from 'react';
import {Button, Card, Container, Divider, Header, Modal, Tab, Icon} from "semantic-ui-react";
import Dashboard from "./Dashboard";
import Products from "./Products";

function AdminView(){
    const [isAuth, setIsAuth] = useState(true)
    const [notShow, setNotShow] = useState(false)
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
                    <Header as='h2' color='blue'>
                    <Icon name='briefcase'/>Admin's Profile
                    </Header>
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