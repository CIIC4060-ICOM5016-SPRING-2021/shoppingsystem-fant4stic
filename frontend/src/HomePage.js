import React, {Component, useState, useEffect} from 'react';
import { useNavigate } from 'react-router-dom';
import {Button, Divider, Form, Grid, Header, Modal, Segment, Tab, Image} from 'semantic-ui-react';
import Axios from "axios";
import logo from "./images/ProjectsLogoHomePage.png"
import giomar from "./images/giomar.jpeg"
import hedin from "./images/hedin.jpeg"
import jeremy from "./images/jeremy.jpeg"
import william from "./images/william.png"
import './HomePage.css'

function getLoginValues(){
    const storedVals = localStorage.getItem('loginValues');
    if(!storedVals){
        return {inputEmail: '', inputPassword : ''};
    }
    return JSON.parse(storedVals);
}

function HomePage() {
    const [open, setOpen] = useState(false);
    const [values, setValues] = useState(getLoginValues);
    const [allUsers, setAllUsers] = useState([])
    var roleId;
    console.log(open);
    console.log(values.inputEmail)
    console.log(values.inputPassword)
    const navigate = useNavigate();

    const handleChange = (event) => {
        roleId = isUserRegistered(values.inputEmail,values.inputPassword,allUsers)
        //Change view corresponding with the roleId of the user
        if(roleId === 1){
            navigate("/CustomerView");
        }
        else if(roleId === 2){
            navigate("/AdminView");
        }
        else {
            console.log(event.target.value)
            setOpen(true);
        }
    }

    useEffect(()=>{
        localStorage.setItem('loginValues',JSON.stringify(values))
    },[values]);

    useEffect(() => {
        Axios.get('https://fant4stic-books.herokuapp.com/fant4stic/user/get_all')
            .then(res => {
                console.log("Getting from ::::", res.data)
                setAllUsers(res.data)
            }).catch(err => console.log(err))
    }, [])

    return (<Segment><Header dividing textAlign="center" size="huge" color='light blue'>
            Welcome to the Fant4stic Book Store <Image src={logo} size='2140*1200'/></Header>
            <Modal
                centered={false}
                open={open}
                onClose={() => setOpen(false)}
                onOpen={() => setOpen(true)}
            >
                <Modal.Header>Login Failed</Modal.Header>
                <Modal.Content>
                    <Modal.Description>
                        Invalid user information. Please re-enter email and password.
                    </Modal.Description>
                </Modal.Content>
                <Modal.Actions>
                    <Button color='red' onClick={() => setOpen(false)}>OK</Button>
                </Modal.Actions>
            </Modal>
            <Segment placeholder>

                <Grid columns={2} relaxed='very' stackable>
                    <Grid.Column>
                        <Form>
                            <Form.Input
                                icon='mail outline'
                                iconPosition='left'
                                label='Email'
                                placeholder='Email'
                                value = {values.inputEmail}
                                onChange = {e => setValues({...values, inputEmail: e.target.value})}
                            />
                            <Form.Input
                                icon='lock'
                                iconPosition='left'
                                label='Password'
                                type='password'
                                placeholder ='Password'
                                value = {values.inputPassword}
                                onChange = {e => setValues({...values, inputPassword: e.target.value})}
                            />
                            <Button content='Login' primary onClick={handleChange}/>
                        </Form>
                    </Grid.Column>
                    <Grid.Column verticalAlign='middle'>
                        <Button content='Sign up' icon='signup' size='big' color='orange' onClick={() => {setOpen(false); navigate('/Register');}}/>
                    </Grid.Column>
                </Grid>

                <Divider vertical>Or</Divider>
            </Segment>

            <Segment color='orange'>
                <Header textAlign='centered' size="medium">
                    "Books have allowed me to travel way more than my passport."
                </Header>
                <Header textAlign='centered' size="medium">
                    "The best is when you find a book you can't put down."
                </Header>
                <Header textAlign='centered' size='small'>
                    Store founded by:
                </Header>
                <p align='center' size='small'>Hedin García <Image src={hedin} size ='small'/></p>
                <p align='center' size='small'>Jeremy Márquez <Image src={jeremy} size='small'/></p>
                <p align='center' size='small'>William Negrón <Image src={william} size='small'/></p>
                <p align='center' size='small'>Giomar Santiago <Image src={giomar} size='small'/></p>

            </Segment>
        </Segment>
    )
}

//Check if User is registered if so return 1 for customer, 2 for admin, and 0 if the user is not registered.
function isUserRegistered(userEmail, userPassword, arrAllUsers){
    var isRegistered = 0;
    for(let i = 0 ; i < arrAllUsers.length ; i++){
        if((userEmail === arrAllUsers[i].Email) && (userPassword === arrAllUsers[i].Password)  && (1 === arrAllUsers[i].RoleId) ){
            isRegistered =1; //Is a Customer
        }
        else if((userEmail === arrAllUsers[i].Email) && (userPassword === arrAllUsers[i].Password)  && (2 === arrAllUsers[i].RoleId) ){
            isRegistered =2; //Is an Admin
        }
    }
    return isRegistered;
}

export default HomePage;
