import React, {Component, useState, useEffect} from 'react';
import {Container,Grid, Divider, Header, Icon, Segment} from 'semantic-ui-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, PieChart, Pie } from 'recharts';
import Axios from "axios";

function CustomerStatistics(){
    const [allUsers, setAllUsers] = useState([])
    const [customer, setCustomer] = useState({"UserId": "","RoleId": "","FirstName": "","LastName": "",
        "UserName": "","Email": "","Password": "","Age": "","Sex": "","PhoneNumber": ""})
    const [rankMostBoughtCat, setRankMostBoughtCat] = useState([])
    const [rankMostBoughtProd, setRankMostBoughtProd] = useState([])
    const [cheapestProd, setCheapestProd] = useState([])
    const [mostExpensiveProd, setMostExpensiveProd] = useState([])
    const loginvalues = JSON.parse(localStorage.getItem('loginValues'));
    const email = loginvalues['inputEmail'];
    const password = loginvalues['inputPassword'];
    console.log(customer)
    console.log(rankMostBoughtCat)
    console.log(rankMostBoughtProd)
    console.log(cheapestProd)
    console.log(mostExpensiveProd)
    useEffect(() => {
        Axios.get('https://fant4stic-books.herokuapp.com/fant4stic/user/get_all')
            .then(res => {
                console.log("All Users:", res.data)
                setAllUsers(res.data)
            }).catch(err => console.log(err))
    }, [])

    //Store in Customer the last one that did login
    useEffect(()=>{
        setCustomer(getUserInfo(email,password,allUsers))
    },[allUsers]);

    //Store the Customers Statistics:
    //Most Bought Categories:
    useEffect(()=>{
        const customerId = customer.UserId;
        if(customerId !== "") {
            Axios.get('https://fant4stic-books.herokuapp.com/fant4stic/order/rankcustomercategoriesbought/' + String(customerId))
                .then(res => {
                    console.log("Most Bought Categories", res.data)
                    setRankMostBoughtCat(res.data)
                }).catch(err => console.log(err))
        }
    },[customer]);

    //Most Bought Categories:
    useEffect(()=>{
        const customerId = customer.UserId;
        if(customerId !== "") {
            Axios.get('https://fant4stic-books.herokuapp.com/fant4stic/order/rankcustomerproductsbought/' + String(customerId))
                .then(res => {
                    console.log("Most Bought Product", res.data)
                    setRankMostBoughtProd(res.data)
                }).catch(err => console.log(err))
        }
    },[customer]);

    //Cheapest Product:
    useEffect(()=>{
        const customerId = customer.UserId;
        if(customerId !== "") {
            Axios.get('https://fant4stic-books.herokuapp.com/fant4stic/order/cheapestproduct/' + String(customerId))
                .then(res => {
                    console.log("Cheapest Product", res.data)
                    setCheapestProd(res.data)
                }).catch(err => console.log(err))
        }
    },[customer]);

    //Most Expensive Product:
    useEffect(()=>{
        const customerId = customer.UserId;
        if(customerId !== "") {
            Axios.get('https://fant4stic-books.herokuapp.com/fant4stic/order/mostexpensiveproduct/'+String(customerId))
                .then(res => {
                    console.log("Most Expensive Product", res.data)
                    setMostExpensiveProd(res.data)
                }).catch(err => console.log(err))
        }
    },[customer]);


    return (
        <>
            <Divider horizontal>
                <Header as='h4'>
                    <Icon name='chart line'/>
                    User Statistics
                </Header>
            </Divider>
            <Segment>
                <Grid columns={2} stackable textAlign='center'>
                    <Divider vertical></Divider>

                    <Grid.Row verticalAlign='middle'>
                        <Grid.Column>
                        <h2>Rank Most Bought Categories</h2>
                        <BarChart width={700} height={300} data={rankMostBoughtCat} margin={{top: 5,right: 50,left: 50, bottom: 5,}}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="Genre" />
                            <YAxis />
                            <Tooltip />
                            <Legend />
                            <Bar dataKey="AmountBoughtFromCategory" fill="#78ea0c" />
                        </BarChart>
                        </Grid.Column>

                        <Grid.Column>
                            <h2>Rank Most Bought Products</h2>
                            <BarChart width={700} height={300} data={rankMostBoughtProd} margin={{top: 5,right: 50,left: 50, bottom: 5,}}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="Title"/>
                                <YAxis />
                                <Tooltip />
                                <Legend />
                                <Bar dataKey="AmountOfCopiesBought" fill="#0cecab"/>
                            </BarChart>
                        </Grid.Column>

                    </Grid.Row>
                </Grid>
            </Segment>
            <Segment>
                <Grid columns={2} stackable textAlign='center'>
                    <Divider vertical></Divider>

                    <Grid.Row verticalAlign='middle'>
                        <Grid.Column>
                            <h2>Cheapest Product</h2>
                            <PieChart width={700} height={200}>
                                <Pie data={cheapestProd} dataKey="Price" nameKey="Title" cx="50%" cy="50%" innerRadius={0} outerRadius={100} fill="#ec830c" label />
                                <Tooltip />
                            </PieChart>
                        </Grid.Column>

                        <Grid.Column>
                            <h2>Most Expensive Product</h2>
                            <PieChart width={700} height={200}>
                                <Pie data={mostExpensiveProd} dataKey="Price" nameKey="Title" cx="50%" cy="50%" innerRadius={0} outerRadius={100} fill="#ec0c0c" label />
                                <Tooltip />
                            </PieChart>
                        </Grid.Column>

                    </Grid.Row>
                </Grid>
            </Segment>
        </>
    );
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

export default CustomerStatistics;