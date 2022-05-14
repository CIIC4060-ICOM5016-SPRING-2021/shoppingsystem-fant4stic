import React, {Component, useEffect, useState} from 'react';
import {
    Button,
    Card,
    Container,
    Divider,
    Header,
    Modal,
    Tab,
    Icon,
    Segment,
    Grid,
    Form,
    Input, Table
} from "semantic-ui-react";
import Dashboard from "./Dashboard";
import Products from "./Products";
import { useNavigate } from 'react-router-dom';
import Axios from "axios";
import AllCustomerOrders from "./AllCustomerOrders";

function AdminView(){
    const [isAuth, setIsAuth] = useState(true)
    const [verifyLogOut, setVerifyLogOut] = useState(false)
    const [verifyUpdate, setVerifyUpdate] = useState(false)
    const [verifyDelete, setVerifyDelete] = useState(false)
    const [verifyAdd, setVerifyAdd] = useState(false)
    const [view, setView] = useState('/AdminView')
    const [allUsers, setAllUsers] = useState([])
    const [admin, setAdmin] = useState({"UserId": "","RoleId": "","FirstName": "","LastName": "",
        "UserName": "","Email": "","Password": "","Age": "","Sex": "","PhoneNumber": ""})
    const [adminData, setAdminData] = useState({"FirstName": "","LastName": "",
        "Username": "","Email": "","Password": "","Age": "","Sex": "","PhoneNumber": ""}) //Used for update form
    const [bookData, setBookData] = useState({"UserId": "", "Title": "", "Language": "", "NumberOfPages": "",
        "YearPublished": "", "Genre": "", "AuthorFirstName": "", "AuthorLastName": "", "AuthorCountry": "", "BookPrice": "",
        "BookNumberUnits": ""}) //Used for add product form
    console.log(admin)
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

    const handleChange1 = (event) => {
        setVerifyUpdate(true)
    }

    const handleChange2 = (event) => {
        setVerifyDelete(true)
    }

    const handleChange3 = (event) => {
        setVerifyAdd(true)
    }

    useEffect(() => {
        Axios.get('https://fant4stic-books.herokuapp.com/fant4stic/user/get_all')
            .then(res => {
                console.log("All Users:", res.data)
                setAllUsers(res.data)
            }).catch(err => console.log(err))
    }, [])

    useEffect(()=>{
        setAdmin(getUserInfo(email,password,allUsers))
    },[allUsers]);

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

    const resetAdminData = () =>{
        adminData.FirstName = "";
        adminData.LastName = "";
        adminData.UserName = "";
        adminData.Password = "";
        adminData.Age = "";
        adminData.Sex = "";
        adminData.PhoneNumber = "";
        setVerifyUpdate(false)
        console.log(adminData)
    }

    const updateProfile = () => {
        let data = {
            FirstName: adminData.FirstName,
            LastName: adminData.LastName,
            Username: adminData.Username,
            Email: adminData.Email,
            Password: adminData.Password,
            Age: adminData.Age,
            Sex: adminData.Sex,
            PhoneNumber: adminData.PhoneNumber
        };
        console.log(data);
        //Verify if any of the inputs from the form are empty. If empty sets them to original value
        if (adminData.FirstName === "") {
            data.FirstName = admin.FirstName
        }
        if (adminData.LastName === "") {
            data.LastName = admin.LastName;
        }
        if (adminData.Username === "") {
            data.Username = admin.UserName;
        }
        if (adminData.Email === "") {
            data.Email = admin.Email;
        }
        if (adminData.Password === "") {
            data.Password = admin.Password;
        }
        if (adminData.Age === "") {
            data.Age = admin.Age;
        }
        if (adminData.Sex === "") {
            data.Sex = admin.Sex;
        }
        if (adminData.PhoneNumber === ""){
            data.PhoneNumber = admin.PhoneNumber
        }
        console.log(data);
        console.log(admin.UserId);
        Axios.put('https://fant4stic-books.herokuapp.com/fant4stic/user/crud_operations/' + String(admin.UserId),data)
            .then((response) => {
                console.log(response);
                localStorage.setItem('loginValues',JSON.stringify({inputEmail: data.Email, inputPassword : data.Password}))
            }, (error) => {
                console.log(error);
            });
        setVerifyUpdate(false)
        updateAdmin()
        // setCustomer(getUserInfo(email, password, allUsers))
        setTimeout("location.reload(true);",1000)

    }

    function updateAdmin(){
        admin.FirstName = adminData.FirstName
        admin.LastName = adminData.LastName
        admin.UserName = adminData.Username
        admin.Email = adminData.Email
        admin.Password = adminData.Password
        admin.Age = adminData.Age
        admin.Sex = adminData.Sex
        admin.PhoneNumber = adminData.PhoneNumber
    }

    const deleteAccount = () =>{
        Axios.delete("https://fant4stic-books.herokuapp.com/fant4stic/user/crud_operations/" + String(admin.UserId))
            .then((response) => {
                logOut()
            },(error) => {
                console.log(error);
            });
    }

    const addProduct = () =>{
        const book = {
            UserId: admin.UserId,
            Title: bookData.Title,
            Language: bookData.Language,
            NumberOfPages: String(bookData.NumberOfPages),
            YearPublished: parseInt(bookData.YearPublished),
            Genre: bookData.Genre,
            AuthorFirstName: bookData.AuthorFirstName,
            AuthorLastName: bookData.AuthorLastName,
            AuthorCountry: bookData.AuthorCountry,
            BookPrice: parseInt(bookData.BookPrice),
            BookNumberUnits: parseInt(bookData.BookNumberUnits)
        }
        console.log(book)
        Axios.post('https://fant4stic-books.herokuapp.com/fant4stic/inventory/addproduct', book)
            .then(res=> console.log('Posting Data',res))
            .catch(err=>console.log(err))
        setVerifyAdd(false)
        setTimeout("location.reload(true);",1000)
    }

    const panes = [
        {
            menuItem: 'Products', render: () => (
                <Tab.Pane active={isAuth}>
                    <Container>
                        <Modal
                            centered={false}
                            open={verifyAdd}
                            onClose={() => setVerifyAdd(false)}
                            onOpen={() => setVerifyAdd(true)}
                        >
                            <Modal.Header>Enter book information</Modal.Header>
                            <Segment placeholder>
                                <Grid columns={1} relaxed='very' stackable>
                                    <Grid.Column verticalAlign='middle'>
                                        <Form>
                                            <Form.Field
                                                control = {Input}
                                                label='Title'
                                                placeholder={bookData.Title}
                                                onChange = {e => setBookData({...bookData, Title: e.target.value})}
                                            />
                                            <Form.Field
                                                control = {Input}
                                                label='Language'
                                                placeholder={bookData.Language}
                                                onChange = {e => setBookData({...bookData, Language: e.target.value})}
                                            />
                                            <Form.Field
                                                control = {Input}
                                                label='Number of pages'
                                                placeholder={bookData.NumberOfPages}
                                                onChange = {e => setBookData({...bookData, NumberOfPages: e.target.value})}
                                            />
                                            <Form.Field
                                                control = {Input}
                                                label='Year published'
                                                placeholder={bookData.YearPublished}
                                                onChange = {e => setBookData({...bookData, YearPublished: e.target.value})}
                                            />
                                            <Form.Field
                                                control = {Input}
                                                label='Genre'
                                                placeholder={bookData.Genre}
                                                onChange = {e => setBookData({...bookData, Genre: e.target.value})}
                                            />
                                            <Form.Field
                                                control = {Input}
                                                label='Author first name'
                                                placeholder={bookData.AuthorFirstName}
                                                onChange = {e => setBookData({...bookData, AuthorFirstName: e.target.value})}
                                            />
                                            <Form.Field
                                                control = {Input}
                                                label='Author last name'
                                                placeholder={bookData.AuthorLastName}
                                                onChange = {e => setBookData({...bookData, AuthorLastName: e.target.value})}
                                            />
                                            <Form.Field
                                                control = {Input}
                                                label='Author country'
                                                placeholder={bookData.AuthorCountry}
                                                onChange = {e => setBookData({...bookData, AuthorCountry: e.target.value})}
                                            />
                                            <Form.Field
                                                control = {Input}
                                                label='Price'
                                                placeholder={bookData.BookPrice}
                                                onChange = {e => setBookData({...bookData, BookPrice: e.target.value})}
                                            />
                                            <Form.Field
                                                control = {Input}
                                                label='Number of units'
                                                placeholder={bookData.BookNumberUnits}
                                                onChange = {e => setBookData({...bookData, BookNumberUnits: e.target.value})}
                                            />
                                        </Form>
                                    </Grid.Column>
                                </Grid>
                            </Segment>
                            <Modal.Actions>
                                <Button color='green' onClick={addProduct}>Add product</Button>
                                <Button color='red' onClick={() => {setVerifyAdd(false)}}>Cancel</Button>
                            </Modal.Actions>
                        </Modal>
                        <Header>Modify Fant4stic Store Products:</Header>
                        <div style={{float: 'inline-start'}}>
                            <Button content = 'Add new product' color='orange' onClick={handleChange3}/>
                        </div>
                        <Divider/>
                    </Container>
                    <Products/></Tab.Pane>
            )
        },
        {
            menuItem: 'History of Orders', render: () => (
                <Tab.Pane active={isAuth}><Header as='h4'>
                    <Icon name='shopping bag'/>
                    Orders of All Customers
                </Header><AllCustomerOrders/></Tab.Pane>
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
                    <Header as='h2' color='blue'>
                        <Icon name='briefcase'/>Admin's Profile
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
                                            placeholder={adminData.FirstName}
                                            onChange = {e => setAdminData({...adminData, FirstName: e.target.value})}
                                        />
                                        <Form.Field
                                            control = {Input}
                                            label='Last name'
                                            placeholder={adminData.LastName}
                                            onChange = {e => setAdminData({...adminData, LastName: e.target.value})}
                                        />
                                        <Form.Field
                                            control = {Input}
                                            label='Username'
                                            placeholder={adminData.Username}
                                            onChange = {e => setAdminData({...adminData, Username: e.target.value})}
                                        />
                                        <Form.Field
                                            control = {Input}
                                            label='Email'
                                            placeholder={adminData.Email}
                                            onChange = {e => setAdminData({...adminData, Email: e.target.value})}
                                        />
                                        <Form.Field
                                            control = {Input}
                                            label='Password'
                                            placeholder={adminData.Password}
                                            onChange = {e => setAdminData({...adminData, Password: e.target.value})}
                                        />
                                        <Form.Field
                                            control = {Input}
                                            label='Age'
                                            placeholder={adminData.Age}
                                            onChange = {e => setAdminData({...adminData, Age: e.target.value})}
                                        />
                                        <Form.Field label='Sex'/>
                                        <Form.Field>
                                            <select placeholder={adminData.Sex} onChange={(e)=>{
                                                setAdminData({...adminData, Sex: e.target.value}) }}>
                                                <option value='M'>Male</option>
                                                <option value='F'>Female</option>
                                                <option value='O'>Other</option>
                                            </select>
                                        </Form.Field>
                                        <Form.Field
                                            control = {Input}
                                            label='Phone Number'
                                            placeholder={adminData.PhoneNumber}
                                            onChange = {e => setAdminData({...adminData, PhoneNumber: e.target.value})}
                                        />
                                    </Form>
                                </Grid.Column>
                            </Grid>
                        </Segment>
                        <Modal.Actions>
                            <Button color='green' onClick={updateProfile}>Confirm</Button>
                            <Button color='red' onClick={resetAdminData}>Cancel</Button>
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
                                <Table.Cell>{admin.FirstName}</Table.Cell>
                                <Table.Cell>{admin.LastName}</Table.Cell>
                                <Table.Cell>{admin.UserName}</Table.Cell>
                                <Table.Cell>{admin.Email}</Table.Cell>
                                <Table.Cell>{admin.Age}</Table.Cell>
                                <Table.Cell>{admin.Sex}</Table.Cell>
                                <Table.Cell>{admin.PhoneNumber}</Table.Cell>
                            </Table.Row>
                        </Table.Body>
                    </Table>
                </Tab.Pane>
            )
        }
    ]

    return <Tab panes={panes}/>

}

function getUserInfo(email, password, arrAllUsers){
    let user = {"UserId": "","RoleId": "","FirstName": "","LastName": "","UserName": "","Email": "",
        "Password": "","Age": "","Sex": "","PhoneNumber": ""}
    for(let i = 0 ; i < arrAllUsers.length ; i++){
        if((email === arrAllUsers[i].Email) && (password === arrAllUsers[i].Password)){
            user = arrAllUsers[i]; //Store all the information of match user
        }
    }
    return user;
}

export default AdminView;