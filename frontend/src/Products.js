import React, {Component, useEffect, useState} from 'react';
import {Button, Card, Container, Modal, Tab} from "semantic-ui-react";
import AllProducts from "./AllProducts";
import Axios from "axios";

function Products() {
    const [data, setData] = useState("show");
    const [allProducts, setAllProducts] = useState(["show"]);
    // let random_info = [{"pname": "p1", "pprice": 1.01, "pdescription": "description"},
    //     {"pname": "p2", "pprice": 1.01, "pdescription": "description"},
    //     {"pname": "p3", "pprice": 1.01, "pdescription": "description"},
    //     {"pname": "p4", "pprice": 1.01, "pdescription": "description"},
    //     {"pname": "p5", "pprice": 1.01, "pdescription": "description"},
    //     {"pname": "p6", "pprice": 1.01, "pdescription": "description"}];
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

    let book = [{"Title": "", "AuthorFirstName": "", "AuthorLastName": "", "Language": "", "NumPages": "",
        "YearPublished": "", "PriceUnit": ""}]
    for(let i = 0; i < allProducts.length; i++){
        book = allProducts[i];
    }


    return <Card.Group>
        <AllProducts info={allProducts} userId = {user.UserId}/>
    </Card.Group>
}

export default Products;