import React, {Component, useState, useEffect} from 'react';
import {Button, Card, Container, Divider, Header, Icon, Modal, Segment, Tab, Input, Form, Grid, Table, Image} from "semantic-ui-react";
import Dashboard from "./Dashboard";
import Products from "./Products";
import { useNavigate } from 'react-router-dom';
import CustomerStatistics from "./CustomerStatistics";
import Axios from "axios";
import CartProduct from "./Cart";
import WishListProducts from "./WishList";
import CustomerOrders from "./CustomerOrders";
import './CustomerAndAdminView.css';
import logo from './images/ProjectsLogoHomePage.png'

function CustomerView(){
    const [isAuth, setIsAuth] = useState(true)
    const [verifyLogOut, setVerifyLogOut] = useState(false)
    const [verifyUpdate, setVerifyUpdate] = useState(false)
    const [verifyDelete, setVerifyDelete] = useState(false)
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
    const [wishArray, setWish] = useState([""])



    const handleChange = (event) => {
        setVerifyLogOut(true)
    }

    const handleChange1 = (event) => {
        setVerifyUpdate(true)
    }

    const handleChange2 = (event) => {
        setVerifyDelete(true)
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

    useEffect(() => {Axios.get("https://fant4stic-books.herokuapp.com/fant4stic/wishlist/get_all")
        .then(res => {
            console.log("Wishlists:", res.data);
            setWish(res.data)})
    }, [])

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

    const deleteAccount = () =>{
        Axios.delete("https://fant4stic-books.herokuapp.com/fant4stic/user/crud_operations/" + String(customer.UserId))
            .then((response) => {
                logOut()
            },(error) => {
                console.log(error);
            });
    }

    const panes = [
        {
            menuItem: 'Products', render: () => (
                <Tab.Pane active={isAuth}>
                    <Container>
                        <Header size="huge" textAlign='centered'>
                            <Image src={logo} size='2140*1200'/> Fant4stic Store Products <Image src={logo} size='2140*1200'/>
                        </Header>
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
                    <div style={{float: 'right'}}>
                        <Button type={"button"} color={"red"} negative onClick={() => {
                            const loginvalues = JSON.parse(localStorage.getItem('loginValues'));
                            const email = loginvalues['inputEmail'];
                            const password = loginvalues['inputPassword'];
                            var idsArray = []

                            const user = getUserInfo(email,password,allUsers)

                            wishArray.forEach(value => {if(value.CustomerId == user.UserId){idsArray.push(value.WishlistId)}})

                            var wishListId = window. prompt("Which of the following Wishlists? : " + idsArray.toString()); alert("The indicated Wishlist is: " + wishListId);
                            Axios.delete("https://fant4stic-books.herokuapp.com/fant4stic/wishlist/delete",{ data:{"User_id": parseInt(user.UserId), "Wishlist_id": parseInt(wishListId)}})
                                .catch(err => {console.log(err); alert("The indicated Wishlist(" + String(wishListId) + ") is not valid")}); setTimeout("location.reload(true);",1000)}}>
                            Delete Wishlist</Button>
                    </div>

                    <div style={{float: 'right'}}>
                        <Button type={"button"} color={"green"} positive onClick={() => {
                            const loginvalues = JSON.parse(localStorage.getItem('loginValues'));
                            const email = loginvalues['inputEmail'];
                            const password = loginvalues['inputPassword'];

                            const user = getUserInfo(email,password,allUsers)
                            Axios.post("https://fant4stic-books.herokuapp.com/fant4stic/wishlist/create",{"User_id": parseInt(user.UserId)}); setTimeout("location.reload(true);",1000)}}>
                            Create Wishlist</Button>
                    </div>
                </Header><WishListProducts/></Tab.Pane>
            )
        },
        {
            menuItem: 'Cart', render: () => (
                <Tab.Pane active={isAuth}><Header as='h4'>
                    <Icon name='add to cart'/>
                    Books in Cart
                    <div style={{float: 'right'}}>
                    <Button type={"button"} color={"red"} negative onClick={() => {
                        const loginvalues = JSON.parse(localStorage.getItem('loginValues'));
                        const email = loginvalues['inputEmail'];
                        const password = loginvalues['inputPassword'];

                        const user = getUserInfo(email,password,allUsers)
                        Axios.delete("https://fant4stic-books.herokuapp.com/fant4stic/user/clear_cart_content/" + String(user.UserId)); setTimeout("location.reload(true);",1000)}}>
                        Clear Cart Content</Button>
                    </div>

                    <div style={{float: 'right'}}>
                        <Button type={"button"} color={"green"} positive onClick={() => {
                            const loginvalues = JSON.parse(localStorage.getItem('loginValues'));
                            const email = loginvalues['inputEmail'];
                            const password = loginvalues['inputPassword'];

                            const user = getUserInfo(email,password,allUsers)
                            Axios.post("https://fant4stic-books.herokuapp.com/fant4stic/user/buy_all/" + String(user.UserId)); alert("When purchased, any remaining books in cart mean they could not be bought due to lack of availability at the moment"); setTimeout("location.reload(true);",1000)}}>
                            Buy Everything</Button>
                    </div>
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
                    <Modal
                        centered={false}
                        open={verifyDelete}
                        onClose={() => setVerifyDelete(false)}
                        onOpen={() => setVerifyDelete(true)}
                    >
                        <Modal.Header>Are you sure you want to delete your account?</Modal.Header>
                        <Modal.Actions>
                            <Button color='green' onClick={deleteAccount}>Confirm</Button>
                            <Button color='red' onClick={() => {setVerifyDelete(false)}}>Cancel</Button>
                        </Modal.Actions>
                    </Modal>
                    <Header as='h2' color='red'>
                        <Icon name='address card'/>Customer's Profile
                    </Header>
                    <div style={{float: 'right'}}>
                        <Button content = 'LogOut' color='red' onClick={handleChange}/>
                    </div>
                    <div style={{float: 'left'}}>
                        <Button content = 'Update Profile' color='blue' onClick={handleChange1}/>
                    </div>
                    <div style={{float: 'right'}}>
                        <Button content = 'Delete Account' color='black' onClick={handleChange2}/>
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

                    <Table celled fixed singleLine>
                        <Table.Header>
                            <Table.Row>
                                <Table.HeaderCell>First name</Table.HeaderCell>
                                <Table.HeaderCell>Last name</Table.HeaderCell>
                                <Table.HeaderCell>Username</Table.HeaderCell>
                                <Table.HeaderCell>Email</Table.HeaderCell>
                                <Table.HeaderCell>Age</Table.HeaderCell>
                                <Table.HeaderCell>Sex</Table.HeaderCell>
                                <Table.HeaderCell>Phone number</Table.HeaderCell>
                            </Table.Row>
                        </Table.Header>

                        <Table.Body>
                            <Table.Row>
                                <Table.Cell>{customer.FirstName}</Table.Cell>
                                <Table.Cell>{customer.LastName}</Table.Cell>
                                <Table.Cell>{customer.UserName}</Table.Cell>
                                <Table.Cell>{customer.Email}</Table.Cell>
                                <Table.Cell>{customer.Age}</Table.Cell>
                                <Table.Cell>{customer.Sex}</Table.Cell>
                                <Table.Cell>{customer.PhoneNumber}</Table.Cell>
                            </Table.Row>
                        </Table.Body>
                    </Table>
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
