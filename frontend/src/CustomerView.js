import React, {Component, useState} from 'react';
import {Button, Card, Container, Divider, Header, Icon, Modal, Tab} from "semantic-ui-react";
import Dashboard from "./Dashboard";
import Products from "./Products";


function CustomerView(){
    const [isAuth, setIsAuth] = useState(true)
    const [notShow, setNotShow] = useState(false)
    const panes = [
        {
            menuItem: 'Products', render: () => (
                <Tab.Pane active={isAuth}>
                    <Container>
                        <Header>Fant4stic Store Products:</Header>
                        <Divider/>
                    </Container>
                    <Products/></Tab.Pane>
            )
        },
        {
            menuItem: 'WishList', render: () => (
                <Tab.Pane active={isAuth}><Products/></Tab.Pane>
            )
        },
        {
            menuItem: 'Cart', render: () => (
                <Tab.Pane active={isAuth}><Products/></Tab.Pane>
            )
        },
        {
            menuItem: 'Profile', render: () => (
                <Tab.Pane active={isAuth}>
                    <Header as='h2' color='red'>
                        <Icon name='address card'/>Customer's Profile
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
export default CustomerView;
