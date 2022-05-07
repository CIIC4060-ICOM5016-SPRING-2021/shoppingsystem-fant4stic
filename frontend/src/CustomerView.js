import React, {Component, useState, useEffect} from 'react';
import {Button, Card, Container, Divider, Header, Icon, Modal, Tab} from "semantic-ui-react";
import Dashboard from "./Dashboard";
import Products from "./Products";
import { useNavigate } from 'react-router-dom';
import Axios from "axios";

function CustomerView(){
    const [isAuth, setIsAuth] = useState(true)
    const [verifyLogOut, setVerifyLogOut] = useState(false)
    const [view, setView] = useState('/CustomerView')
    const [data, setDate] = useState([])
    const navigate = useNavigate();
    //Retrieve info of customer login values, same thing should be done for registered values:
    const loginvalues = JSON.parse(localStorage.getItem('loginValues'));
    const email = loginvalues['inputEmail'];
    console.log("Email Stored: " + email);
    const password = loginvalues['inputPassword'];
    console.log("Password Stored: " + password);

    const handleChange = (event) => {
        setVerifyLogOut(true)
    }

    const logOut = (event) =>{
        if(view === '/CustomerView'){
            // When login out reset login values used to enter to website
            localStorage.setItem('loginValues',JSON.stringify({inputEmail: "", inputPassword : ""}))
            setView('/')
            navigate('/')
        }
        else if(view === '/'){
            setView('/CustomerView')
        }
    }

    useEffect(() => {
        Axios.get('https://fant4stic-books.herokuapp.com/fant4stic/user/get_all')
            .then(res => {
                console.log("Getting from ::::", res.data)
                setDate(res.data)
            }).catch(err => console.log(err))
    }, [])

    const arr = data.map((data, index) => {
        return (
            <tr>
               <td>{data.FirstName}</td>
                <td>{data.LastName}</td>
                <td>{data.UserName}</td>
                <td>{data.Email}</td>
                <td>{data.Age}</td>
                <td>{data.Sex}</td>
                <td>{data.PhoneNumber}</td>
            </tr>
        )
    })
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
                    <Header as='h2' color='red'>
                        <Icon name='address card'/>Customer's Profile
                    </Header>
                    <table>
                        <tr>
                            <th>First Name</th>
                            <th>Last Name</th>
                            <th>Username</th>
                            <th>Email</th>
                            <th>Age</th>
                            <th>Sex</th>
                            <th>Phone number</th>
                        </tr>
                        {arr}

                    </table>
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
export default CustomerView;
