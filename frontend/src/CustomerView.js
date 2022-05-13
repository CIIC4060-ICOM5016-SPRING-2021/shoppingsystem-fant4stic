import React, {Component, useState, useEffect} from 'react';
import {Button, Card, Container, Divider, Header, Icon, Modal, Tab} from "semantic-ui-react";
import Dashboard from "./Dashboard";
import Products from "./Products";
import { useNavigate } from 'react-router-dom';
import CustomerStatistics from "./CustomerStatistics";
import Axios from "axios";
import CartProduct from "./Cart";
import WishListProducts from "./WishList";
import CustomerOrders from "./CustomerOrders";

function CustomerView(){
    const [isAuth, setIsAuth] = useState(true)
    const [verifyLogOut, setVerifyLogOut] = useState(false)
    const [view, setView] = useState('/CustomerView')
    const [allUsers, setAllUsers] = useState([])
    const [customer, setCustomer] = useState({"UserId": "","RoleId": "","FirstName": "","LastName": "",
        "UserName": "","Email": "","Password": "","Age": "","Sex": "","PhoneNumber": ""})
    console.log(customer)
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
                console.log("All Users:", res.data)
                setAllUsers(res.data)
            }).catch(err => console.log(err))
    }, [])

    useEffect(()=>{
        setCustomer(getUserInfo(email,password,allUsers))
    },[allUsers]);

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
                <Tab.Pane active={isAuth}><Header as='h4' height="50">
                    <Icon name='add to cart'/>
                    Wishlists:
                </Header><WishListProducts/></Tab.Pane>
            )
        },
        {
            menuItem: 'Cart', render: () => (
                <Tab.Pane active={isAuth}><Header as='h4'>
                    <Icon name='add to cart'/>
                    Books in Cart
                </Header><CartProduct/></Tab.Pane>
            )
        },
        {
            menuItem: 'History of Orders', render: () => (
                <Tab.Pane active={isAuth}><Header as='h4'>
                    <Icon name='shopping bag'/>
                    Orders
                </Header><CustomerOrders/></Tab.Pane>
            )
        },
        {
            menuItem: 'Dashboard - Global Statistics', render: () => (
                <Tab.Pane active={isAuth}><Dashboard/></Tab.Pane>
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
                    <div style={{float: 'right'}}>
                        <Button content = 'LogOut' color='red' onClick={handleChange}/>
                    </div>
                    <table>
                        <tr>
                            <th>First name</th>
                            <th>Last name</th>
                            <th>Username</th>
                            <th>Email</th>
                            <th>Age</th>
                            <th>Sex</th>
                            <th>Phone number</th>
                        </tr>
                        <tr>
                            <td>{customer.FirstName}</td>
                            <td>{customer.LastName}</td>
                            <td>{customer.UserName}</td>
                            <td>{customer.Email}</td>
                            <td>{customer.Age}</td>
                            <td>{customer.Sex}</td>
                            <td>{customer.PhoneNumber}</td>
                        </tr>
                    </table>
                    <CustomerStatistics/>
                </Tab.Pane>

            )
        }
    ]

    return <Tab panes={panes}/>

}

export function getUserInfo(email, password, arrAllUsers){
    let user = {"UserId": "","RoleId": "","FirstName": "","LastName": "","UserName": "","Email": "",
        "Password": "","Age": "","Sex": "","PhoneNumber": ""}
    for(let i = 0 ; i < arrAllUsers.length ; i++){
        if((email === arrAllUsers[i].Email) && (password === arrAllUsers[i].Password)){
            user = arrAllUsers[i]; //Store all the information of match user
        }
    }
    return user;
}

export default CustomerView;
