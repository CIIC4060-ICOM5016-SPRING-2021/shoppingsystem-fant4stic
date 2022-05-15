import React, {Component, useEffect, useState} from 'react';
import {Button, Card, Container, Modal, Tab, Dropdown} from "semantic-ui-react";
import AllProducts from "./AllProducts";
import Axios from "axios";

function Products() {
    const [allProducts, setAllProducts] = useState([]);
    const [genres, setAllGenres] = useState([]);
    const [selectedFilter,setSelectedFilter] = useState([]);
    console.log(allProducts)
    console.log(genres)
    const [allUsers, setAllUsers] = useState([])
    const loginvalues = JSON.parse(localStorage.getItem('loginValues'));
    const email = loginvalues['inputEmail'];
    const password = loginvalues['inputPassword'];

    useEffect(() => {
        Axios.get('https://fant4stic-books.herokuapp.com/fant4stic/user/get_all')
            .then(res => {
                console.log("All Users:", res.data)
                setAllUsers(res.data)
            }).catch(err => console.log(err))
    }, [])

    let user = {"UserId": "","RoleId": "","FirstName": "","LastName": "","UserName": "","Email": "",
        "Password": "","Age": "","Sex": "","PhoneNumber": ""}
    for(let i = 0 ; i < allUsers.length ; i++){
        if((email === allUsers[i].Email) && (password === allUsers[i].Password)){
            user = allUsers[i]; //Store all the information of match user
        }
    }

    useEffect(() => {
        Axios.get('https://fant4stic-books.herokuapp.com/fant4stic/inventory/get_all/show')
            .then(res => {
                console.log("All Products: ", res.data)
                setAllProducts(res.data)
            }).catch(err => console.log(err))
    }, [])

    useEffect(() => {
        Axios.get('https://fant4stic-books.herokuapp.com/fant4stic/genre/get_all')
            .then(res => {
                console.log("All Genres: ", res.data)
                setAllGenres(res.data)
            }).catch(err => console.log(err))
    }, [])

    const filters = [
        { key : 'ap' , value: 'allProducts', text: 'All Products' },
        { key : 'lth', value: 'lowToHigh', text: 'Cheapest to Expensive' },
        { key : 'htl', value: 'highToLow', text: 'Expensive to Cheapest' },
        { key : 'ta', value: 'titleAsc', text: 'Title in Ascending Order' },
        { key : 'td', value: 'titleDesc', text: 'Title in Descending Order' },
    ]
    //Add the genres available in dropdown
    var size = filters.length
    for(let i = 0 ; i < genres.length ; i++){
        filters[size + i] = { key:'g'+String(i), value : String(genres[i].GenreId), text: String(genres[i].GenreName)};
    }

    //Show Products according to filter
    function handleChangeFilterBooks(event, data){
        console.log(data.value)
        setSelectedFilter(data.value)
        if(data.value === 'allProducts'){
            Axios.get('https://fant4stic-books.herokuapp.com/fant4stic/inventory/get_all/show')
                .then(res => {
                    console.log("All Products: ", res.data)
                    setAllProducts(res.data)
                }).catch(err => console.log(err))
        }
        else if(data.value === 'lowToHigh'){
            Axios.get('https://fant4stic-books.herokuapp.com/fant4stic/book/orderInPrice/lowtohigh')
                .then(res => {
                    console.log("HighToLow: ", res.data)
                    setAllProducts(res.data)
                }).catch(err => console.log(err))
        }
        else if(data.value === 'highToLow'){
            Axios.get('https://fant4stic-books.herokuapp.com/fant4stic/book/orderInPrice/hightolow')
                .then(res => {
                    console.log("LowToHigh: ", res.data)
                    setAllProducts(res.data)
                }).catch(err => console.log(err))
        }
        else if(data.value === 'titleAsc'){
            Axios.get('https://fant4stic-books.herokuapp.com/fant4stic/book/orderInAscOrDes/ascending')
                .then(res => {
                    console.log("Title Ascending: ", res.data)
                    setAllProducts(res.data)
                }).catch(err => console.log(err))
        }
        else if(data.value === 'titleDesc'){
            Axios.get('https://fant4stic-books.herokuapp.com/fant4stic/book/orderInAscOrDes/descending')
                .then(res => {
                    console.log("Title Descending: ", res.data)
                    setAllProducts(res.data)
                }).catch(err => console.log(err))
        }
        else if(Number.isInteger(parseInt(data.value))){
            Axios.get('https://fant4stic-books.herokuapp.com/fant4stic/book/desiredgenre/'+String(data.value))
                .then(res => {
                    setAllProducts(res.data)
                }).catch(err => console.log(err))
        }
    }

    return (
        <div>
        <Dropdown placeholder='Book Filtering' fluid search selection value={selectedFilter} options= {filters}
                  onChange={(e,data)=>handleChangeFilterBooks(e,data)}/>
        <Card.Group>
            <AllProducts info={allProducts} userId = {user.UserId}/>
        </Card.Group>
        </div>
    )
}

export default Products;