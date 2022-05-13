import React, {Component, useState, useEffect} from 'react';
import {Button, Card, Container, Divider, Header, Icon, Modal, Segment, Tab, Input, Form, Grid} from "semantic-ui-react";
import Dashboard from "./Dashboard";
import Products from "./Products";
import { useNavigate } from 'react-router-dom';
import CustomerStatistics from "./CustomerStatistics";
import Axios from "axios";
import CartProduct from "./Cart";
import WishListProducts from "./WishList";
import CustomerOrders from "./CustomerOrders";
import * as url from "url";

function CustomerView(){
    const [isAuth, setIsAuth] = useState(true)
    const [verifyLogOut, setVerifyLogOut] = useState(false)
    const [verifyUpdate, setVerifyUpdate] = useState(false)
    const [view, setView] = useState('/CustomerView')
    const [allUsers, setAllUsers] = useState([])
    const [customer, setCustomer] = useState({"UserId": "","RoleId": "","FirstName": "","LastName": "",
        "UserName": "","Email": "","Password": "","Age": "","Sex": "","PhoneNumber": ""})
    const [customerData, setCustomerData] = useState({"FirstName": "","LastName": "",
        "Username": "","Email": "","Password": "","Age": "","Sex": "","PhoneNumber": ""}) //Used for update form
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

    const handleChange1 = (event) => {
        setVerifyUpdate(true)
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

    const resetCustomerData = () =>{
        customerData.FirstName = "";
        customerData.LastName = "";
        customerData.UserName = "";
        customerData.Password = "";
        customerData.Age = "";
        customerData.Sex = "";
        customerData.PhoneNumber = "";
        setVerifyUpdate(false)
        console.log(customerData)
    }

    const updateProfile = () => {
        let data = {
            FirstName: customerData.FirstName,
            LastName: customerData.LastName,
            Username: customerData.Username,
            Email: customerData.Email,
            Password: customerData.Password,
            Age: customerData.Age,
            Sex: customerData.Sex,
            PhoneNumber: customerData.PhoneNumber
        };
        console.log(data);
        //Verify if any of the inputs from the form are empty. If empty sets them to original value
        if (customerData.FirstName === "") {
            data.FirstName = customer.FirstName
        }
        if (customerData.LastName === "") {
            data.LastName = customer.LastName;
        }
        if (customerData.Username === "") {
            data.Username = customer.UserName;
        }
        if (customerData.Email === "") {
            data.Email = customer.Email;
        }
        if (customerData.Password === "") {
            data.Password = customer.Password;
        }
        if (customerData.Age === "") {
            data.Age = customer.Age;
        }
        if (customerData.Sex === "") {
            data.Sex = customer.Sex;
        }
        if (customerData.PhoneNumber === ""){
            data.PhoneNumber = customer.PhoneNumber
        }
        console.log(data);
        console.log(customer.UserId);
        Axios.put('https://fant4stic-books.herokuapp.com/fant4stic/user/crud_operations/' + String(customer.UserId),data)
            .then((response) => {
                console.log(response);
                localStorage.setItem('loginValues',JSON.stringify({inputEmail: data.Email, inputPassword : data.Password}))
            }, (error) => {
                console.log(error);
            });
        setVerifyUpdate(false)
        updateCustomer()
        // setCustomer(getUserInfo(email, password, allUsers))
        setTimeout("location.reload(true);",1000)

    }

    function updateCustomer(){
        customer.FirstName = customerData.FirstName
        customer.LastName = customerData.LastName
        customer.UserName = customerData.Username
        customer.Email = customerData.Email
        customer.Password = customerData.Password
        customer.Age = customerData.Age
        customer.Sex = customerData.Sex
        customer.PhoneNumber = customerData.PhoneNumber
    }

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
                    <div style={{float: 'right'}}>
                        <Button content = 'Update Profile' color='blue' onClick={handleChange1}/>
                    </div>

                    <Modal
                        centered={false}
                        open={verifyUpdate}
                        onClose={() => setVerifyUpdate(false)}
                        onOpen={() => setVerifyUpdate(true)}
                    >
                        <Modal.Header>Update your information</Modal.Header>

                        <Segment placeholder>
                            <Grid columns={1} relaxed='very' stackable>
                                <Grid.Column verticalAlign='middle'>
                                    <Form>
                                        <Form.Field
                                            control = {Input}
                                            label='First name'
                                            placeholder={customerData.FirstName}
                                            onChange = {e => setCustomerData({...customerData, FirstName: e.target.value})}
                                        />
                                        <Form.Field
                                            control = {Input}
                                            label='Last name'
                                            placeholder={customerData.LastName}
                                            onChange = {e => setCustomerData({...customerData, LastName: e.target.value})}
                                        />
                                        <Form.Field
                                            control = {Input}
                                            label='Username'
                                            placeholder={customerData.Username}
                                            onChange = {e => setCustomerData({...customerData, Username: e.target.value})}
                                        />
                                        <Form.Field
                                            control = {Input}
                                            label='Email'
                                            placeholder={customerData.Email}
                                            onChange = {e => setCustomerData({...customerData, Email: e.target.value})}
                                        />
                                        <Form.Field
                                            control = {Input}
                                            label='Password'
                                            placeholder={customerData.Password}
                                            onChange = {e => setCustomerData({...customerData, Password: e.target.value})}
                                        />
                                        <Form.Field
                                            control = {Input}
                                            label='Age'
                                            placeholder={customerData.Age}
                                            onChange = {e => setCustomerData({...customerData, Age: e.target.value})}
                                        />
                                        <Form.Field label='Sex'/>
                                        <Form.Field>
                                            <select placeholder={customerData.Sex} onChange={(e)=>{
                                                setCustomerData({...customerData, Sex: e.target.value}) }}>
                                                <option value='M'>Male</option>
                                                <option value='F'>Female</option>
                                                <option value='O'>Other</option>
                                            </select>
                                        </Form.Field>
                                        <Form.Field
                                            control = {Input}
                                            label='Phone Number'
                                            placeholder={customerData.PhoneNumber}
                                            onChange = {e => setCustomerData({...customerData, PhoneNumber: e.target.value})}
                                        />
                                    </Form>
                                </Grid.Column>
                            </Grid>
                        </Segment>
                        <Modal.Actions>
                            <Button color='green' onClick={updateProfile}>Confirm</Button>
                            <Button color='red' onClick={resetCustomerData}>Cancel</Button>
                        </Modal.Actions>
                    </Modal>

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
