import React, {Component, useState, useEffect} from 'react';
import {Button, Card, Container, Header, Icon, Modal, Tab} from "semantic-ui-react";
import AllProducts, {CartProducts} from "./AllProducts";
import Axios from "axios";
import {WishProducts} from "./AllProducts";

function WishListProducts() {
    const [data, setData] = useState([]);
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

    console.log("All Users Test:")
    console.log(allUsers)

    let user = {"UserId": "","RoleId": "","FirstName": "","LastName": "","UserName": "","Email": "",
        "Password": "","Age": "","Sex": "","PhoneNumber": ""}
    for(let i = 0 ; i < allUsers.length ; i++){
        if((email === allUsers[i].Email) && (password === allUsers[i].Password)){
            user = allUsers[i]; //Store all the information of match user
        }
    }

    console.log("User Info:")
    console.log(user)

    console.log("Here")
    console.log(user.UserId)

    useEffect(() => {
        Axios.get('https://fant4stic-books.herokuapp.com/fant4stic/user/getWishlist/' + String(user.UserId))
            .then(res => {
                console.log("WishLists:", res.data)
                setData(res.data)
            }).catch(err => console.log(err))
    }, [allUsers])

    console.log("Here II")
    console.log(data)

    return <Card.Group>
        <WishProducts info={data} userId={user.UserId}/>
    </Card.Group>
}
export default WishListProducts