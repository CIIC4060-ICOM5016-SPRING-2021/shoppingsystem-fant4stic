import React, {Component, useState, useEffect} from 'react';
import {Button, Card, Container, Divider, Grid, Header, Icon, Modal, Segment} from "semantic-ui-react";
import {Bar, BarChart, CartesianGrid, Legend, Pie, PieChart, Tooltip, XAxis, YAxis} from "recharts";
import Axios from "axios";

// Dashboard for Global Statistics of store
function Dashboard(){
    //Hooks for most bougth category, product, cheapest, most expensive, and liked product globally
    const [globalRankMBCat, setGlobalRankMBCat] = useState([])
    const [globalMBProd, setGlobalMBProd] = useState([])
    const [globalCheapestProd, setGlobalCheapestProd] = useState([])
    const [globalMExpenProd, setGlobalMExpenProd] = useState([])
    const [globalMLikedProd, setGlobalMLikedProd] = useState([])

    console.log(globalRankMBCat)
    console.log(globalMBProd)
    console.log(globalCheapestProd)
    console.log(globalMExpenProd)
    console.log(globalMLikedProd)

    useEffect(() => {
        Axios.get('https://fant4stic-books.herokuapp.com/fant4stic/order/most_bought_category')
            .then(res => {
                console.log("Most Bought Categories Globally:", res.data)
                setGlobalRankMBCat(res.data)
            }).catch(err => console.log(err))
    }, [])

    useEffect(() => {
        Axios.get('https://fant4stic-books.herokuapp.com/fant4stic/order/most_bought_product')
            .then(res => {
                console.log("Most Bought Products Globally:", res.data)
                setGlobalMBProd(res.data)
            }).catch(err => console.log(err))
    }, [])

    useEffect(() => {
        Axios.get('https://fant4stic-books.herokuapp.com/fant4stic/inventory/get_cheapest_product')
            .then(res => {
                console.log("Cheapest Product:", res.data)
                setGlobalCheapestProd(res.data)
            }).catch(err => console.log(err))
    }, [])

    useEffect(() => {
        Axios.get('https://fant4stic-books.herokuapp.com/fant4stic/inventory/get_most_expensive_product')
            .then(res => {
                console.log("Most Expensive Product:", res.data)
                setGlobalMExpenProd(res.data)
            }).catch(err => console.log(err))
    }, [])

    useEffect(() => {
        Axios.get('https://fant4stic-books.herokuapp.com/fant4stic/wishlist/get_most_liked_product')
            .then(res => {
                console.log("Most Liked Product:", res.data)
                setGlobalMLikedProd(res.data)
            }).catch(err => console.log(err))
    }, [])

    return (<>
        <Divider horizontal>
            <Header as='h4'>
                <Icon name='chart bar'/>
                Global Statistics of Fant4stic Store
            </Header>
        </Divider>
        <Segment>
            <Grid columns={2} stackable textAlign='center'>
                <Divider vertical></Divider>

                <Grid.Row verticalAlign='middle'>
                    <Grid.Column>
                        <h2>Global - Most Bought Categories in Store</h2>
                        <BarChart width={700} height={300} data={globalRankMBCat} margin={{top: 5,right: 50,left: 50, bottom: 5,}}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="Genre" />
                            <YAxis />
                            <Tooltip />
                            <Legend />
                            <Bar dataKey="AmountBoughtFromCategory" fill="#f3bf0a" />
                        </BarChart>
                    </Grid.Column>

                    <Grid.Column>
                        <h2>Global - Most Bought Products in Store</h2>
                        <BarChart width={700} height={300} data={globalMBProd} margin={{top: 5,right: 50,left: 50, bottom: 5,}}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="Title"/>
                            <YAxis />
                            <Tooltip />
                            <Legend />
                            <Bar dataKey="AmountOfCopiesBought" fill="#25bff5"/>
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
                        <h2>Global - Cheapest Product in Store</h2>
                        <PieChart width={700} height={200}>
                            <Pie data={globalCheapestProd} dataKey="Book_price" nameKey="Book_title" cx="50%" cy="50%" innerRadius={0} outerRadius={100} fill="#8bf60b" label />
                            <Tooltip />
                        </PieChart>
                    </Grid.Column>

                    <Grid.Column>
                        <h2>Global - Most Expensive Product in Store</h2>
                        <PieChart width={700} height={200}>
                            <Pie data={globalMExpenProd} dataKey="Book_price" nameKey="Book_title" cx="50%" cy="50%" innerRadius={0} outerRadius={100} fill="#eff506" label />
                            <Tooltip />
                        </PieChart>
                    </Grid.Column>

                </Grid.Row>
            </Grid>
        </Segment>
        <Segment>
            <Grid columns={1} stackable textAlign='center'>
                <Grid.Row verticalAlign='middle'>
                    <Grid.Column>
                        <h2>Global - Most Liked Product in Store</h2>
                        <PieChart width={1460} height={200}>
                            <Pie data={globalMLikedProd} dataKey="Book_likes" nameKey="Book_title" cx="50%" cy="50%" innerRadius={0} outerRadius={100} fill="#f50606" label />
                            <Tooltip />
                        </PieChart>
                    </Grid.Column>
                </Grid.Row>
            </Grid>
        </Segment>
    </>)
}
export default Dashboard;
