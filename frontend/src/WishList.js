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

    const random = [
        {
            "WishlistId": 10,
            "CustomerId": 26,
            "ListOfProducts": [
                {
                    "BookTitle": "Queen of Shadows",
                    "DateAdded": "2022-4-29"
                },
                {
                    "BookTitle": "We",
                    "DateAdded": "2022-4-29"
                }
            ]
        },
        {
            "WishlistId": 11,
            "CustomerId": 26,
            "ListOfProducts": [
                {
                    "BookTitle": "Harry Potter and the Sorcerer's Stone",
                    "DateAdded": "2022-4-13"
                },
                {
                    "BookTitle": "Throne of Glass",
                    "DateAdded": "2022-4-7"
                },
                {
                    "BookTitle": "Cézanne",
                    "DateAdded": "2022-4-13"
                },
                {
                    "BookTitle": "The Martian",
                    "DateAdded": "2022-4-13"
                },
                {
                    "BookTitle": "The Subtle Art of Not Giving a F*ck: A Counterintuitive Approach to Living a Good Life",
                    "DateAdded": "2022-4-13"
                },
                {
                    "BookTitle": "Interview with the Vampire",
                    "DateAdded": "2022-4-13"
                },
                {
                    "BookTitle": "Queen of Shadows",
                    "DateAdded": "2022-4-8"
                }
            ]
        }
    ]

    return <Card.Group>
        <WishProducts info={data}/>
    </Card.Group>
}
export default WishListProducts