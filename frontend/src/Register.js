import React, {Component, useState, useEffect} from 'react';
import { useNavigate } from 'react-router-dom';
import {Button, Divider, Form, Grid, Header, Modal, Segment, Tab, Checkbox, Input, Image} from 'semantic-ui-react';
import Axios from "axios";
import logo from './images/ProjectsLogoRegister.png'

function getRegisterValues(){
    const storedVals = localStorage.getItem('RegisterValues');
    if(!storedVals){
        return {role : '', firstName:'', lastName:'',userName:'',age:'',
            sex:'',email: '', password : '', phoneNumber:''};
    }
    return JSON.parse(storedVals);
}
function Register(){
    const [open, setOpen] = useState(false);
    const [openEmailPrompt, setOpenEmailPrompt] = useState(false);
    const [submit, setSubmit] = useState(false);
    const [view, setView] = useState('/Register');
    const [registVal, setRegistVal] = useState(getRegisterValues);
    const [allUsers, setAllUsers] = useState([])
    const navigate = useNavigate();
    console.log(open);

    useEffect(()=>{
        localStorage.setItem('RegisterValues',JSON.stringify(registVal))
    },[registVal]);

    useEffect(()=>{
        const user = {"FirstName": registVal.firstName,
            "LastName" :registVal.lastName,
            "Username" : registVal.userName,
            "Email" : registVal.email,
            "Password" :registVal.password,
            "Age" : registVal.age,
            "Sex" : registVal.sex,
            "PhoneNumber" : registVal.phoneNumber,
            "UserType" : registVal.role}
        Axios.post('https://fant4stic-books.herokuapp.com/fant4stic/user/register_new_user',user).then(res=>
            console.log('Posting Data',res)).catch(err=>console.log(err))

    },[submit]);

    useEffect(() => {
        Axios.get('https://fant4stic-books.herokuapp.com/fant4stic/user/get_all')
            .then(res => {
                console.log("Getting from ::::", res.data)
                setAllUsers(res.data)
            }).catch(err => console.log(err))
    }, [])

    function emailExist(email){
        for( var i =0 ; i < allUsers.length; i++){
            if(email === allUsers[i].Email){
                return true
            }
        }
        return false;
    }

    const handleChange = (event) => {
        var existEmail = emailExist(registVal.email)
        if(existEmail){
            setOpenEmailPrompt(true)
        }
        else if(registVal && !(existEmail)){
            setSubmit(true);
            setOpen(true);
            //Change loginValues with the information stored in RegisterdValues
            localStorage.setItem('loginValues',JSON.stringify({inputEmail: registVal.email, inputPassword : registVal.password}))
            if(registVal.role === 'Admin'){
                setView('/AdminView')
            }
            else if(registVal.role === 'Customer'){
                setView('/CustomerView')
            }
        }
    }

    return (<Segment inverted color = 'light green'>
            <Image src={logo} size='small' centered/>
            <Header dividing
                             color = 'white'
                             textAlign="center" size="huge"
                             content = 'Join Fant4stic' subheader='Create your account today'/>
            <Modal
                centered={false}
                open={open}
                onClose={() => setOpen(false)}
                onOpen={() => setOpen(true)}
            >
                <Modal.Header>Successfully Created your Account</Modal.Header>
                <Modal.Actions>
                    <Button color='green' onClick={() => {setOpen(false); navigate(view);}}>Continue</Button>
                </Modal.Actions>
            </Modal>
            <Modal
                centered={false}
                open={openEmailPrompt}
                onClose={() => setOpenEmailPrompt(false)}
                onOpen={() => setOpenEmailPrompt(true)}
            >
                <Modal.Header>Email already exists. Please try another one.</Modal.Header>
                <Modal.Actions>
                    <Button color='red' onClick={() => {setOpenEmailPrompt(false)}}>Close</Button>
                </Modal.Actions>
            </Modal>
            <Segment placeholder>
                <Grid columns={1} relaxed='very' stackable>
                    <Grid.Column verticalAlign='middle'>
                        <Form>
                            <Form.Field label='Role'/>
                            <Form.Field>
                            <select placeholder='Role' onChange={(e)=>{
                                setRegistVal({...registVal, role: e.target.value}) }}>
                                <option value=''>{setRegistVal.role}</option>
                                <option value='Customer'>Customer</option>
                                <option value='Admin'>Admin</option>
                            </select>
                            </Form.Field>
                            <Form.Field
                                control = {Input}
                                label='First name'
                                placeholder='First name'
                                value = {registVal.firstName}
                                onChange = {e => setRegistVal({...registVal, firstName: e.target.value})}
                            />
                            <Form.Field
                                control = {Input}
                                label='Last name'
                                placeholder='Last name'
                                value = {registVal.lastName}
                                onChange = {e => setRegistVal({...registVal, lastName: e.target.value})}
                            />
                            <Form.Field
                                control = {Input}
                                label='Username'
                                placeholder='Username'
                                value = {registVal.userName}
                                onChange = {e => setRegistVal({...registVal, userName: e.target.value})}
                            />
                            <Form.Field
                                control = {Input}
                                label='Age'
                                placeholder='Age'
                                value = {registVal.age}
                                onChange = {e => setRegistVal({...registVal, age: e.target.value})}
                            />
                            <Form.Field label='Sex'/>
                            <Form.Field>
                                <select placeholder='Sex' onChange={(e)=>{
                                    setRegistVal({...registVal, sex: e.target.value}) }}>
                                    <option value=''>{setRegistVal.role}</option>
                                    <option value='M'>Male</option>
                                    <option value='F'>Female</option>
                                    <option value='O'>Other</option>
                                </select>
                            </Form.Field>
                            <Form.Field
                                control = {Input}
                                label='Email'
                                placeholder='Email'
                                value = {registVal.email}
                                onChange = {e => setRegistVal({...registVal, email: e.target.value})}
                            />
                            <Form.Field
                                control = {Input}
                                label='Password'
                                placeholder='Password'
                                value = {registVal.password}
                                onChange = {e => setRegistVal({...registVal, password: e.target.value})}
                            />
                            <Form.Field
                                control = {Input}
                                label='Phone Number'
                                placeholder='Phone Number'
                                value = {registVal.phoneNumber}
                                onChange = {e => setRegistVal({...registVal, phoneNumber: e.target.value})}
                            />
                            <Button type = 'submit' content='Register' icon='signup' size='small' color='dark green' onClick={handleChange}/>
                        </Form>
                    </Grid.Column>
                </Grid>
            </Segment>
        </Segment>
    )
}

export default Register;