import React, {Component, useEffect, useState} from 'react';
import {
    Button,
    Card,
    CardContent,
    CardHeader,
    Container,
    Form,
    Grid,
    Header,
    Input,
    Modal, Segment,
    Tab
} from "semantic-ui-react";
import Axios from "axios";

function AllProductsAdmin(props) {
    const [books, setBooks] = useState([""])
    const [bookPrice, setBookPrice] = useState("")
    const [allUsers, setAllUsers] = useState([])
    var bookId;
    const [admin, setAdmin] = useState({"UserId": "","RoleId": "","FirstName": "","LastName": "",
        "UserName": "","Email": "","Password": "","Age": "","Sex": "","PhoneNumber": ""})
    const loginvalues = JSON.parse(localStorage.getItem('loginValues'));
    const email = loginvalues['inputEmail'];
    const password = loginvalues['inputPassword'];

    useEffect(() => {Axios.get("https://fant4stic-books.herokuapp.com/fant4stic/book/get_all")
        .then(res => {console.log("Books:", res.data); setBooks(res.data)})}, [])

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


    console.log(props)
    props.info.forEach(value => console.log(value.Title));
    return props.info.map(value => {return <Card>
        <Card.Content>
            <Card.Header>{value.Title}</Card.Header>
            <Card.Meta>Language: {value.Language}</Card.Meta>
            <Card.Meta>Number of Pages: {value.NumPages}</Card.Meta>
            <Card.Meta>Year Published: {value.YearPublished}</Card.Meta>
            <Card.Meta>Genre: {value.GenreName}</Card.Meta>
            {value.Authors.map((val)=>{
                return <Card.Meta>Author: {val.AuthorName}</Card.Meta>
            })}
            <Card.Meta>Available Copies: {value.AvailableUnits}</Card.Meta>
            <Card.Meta>Unit Price: ${value.PriceUnit}</Card.Meta>
        </Card.Content>
        <Card.Content extra>
            <div className='ui three buttons'>
                <Button content = 'Edit price' basic color='green' onClick={() => {
                    books.forEach( val=> {if (value.Title === val.BookTitle) {bookId = val.BookId}});
                    var bookPrice = window. prompt("Enter new book price: ");
                    if (bookPrice === null){
                        bookPrice = value.PriceUnit
                    }
                    Axios.put('https://fant4stic-books.herokuapp.com/fant4stic/inventory/updatepriceproduct',{"BookId": bookId, "PriceUnit": bookPrice, "UserId": admin.UserId})
                        .then((response) => {
                            console.log(response);
                        }, (error) => {
                            console.log(error);
                        });
                    setTimeout("location.reload(true);",1000)
                }
                }/>
                <Button content = 'Edit available units' basic color='blue' onClick={() => {
                    books.forEach( val=> {if (value.Title === val.BookTitle) {bookId = val.BookId}});
                    var bookUnits = window. prompt("Enter available units: ");
                    Axios.put('https://fant4stic-books.herokuapp.com/fant4stic/inventory/updateavailableunitsproduct',{"BookId": bookId, "AvailableUnits": bookUnits, "UserId": admin.UserId})
                        .then((response) => {
                            console.log(response);
                        }, (error) => {
                            console.log(error);
                        });
                    setTimeout("location.reload(true);",1000)
                }
                }/>
                <Button content = 'Edit book info' basic color='red' onClick={() => {
                    books.forEach( val=> {if (value.Title === val.BookTitle) {bookId = val.BookId}});
                    var Title = window.prompt("Enter book title: ");
                    if (Title === null){
                        Title = value.Title
                    }
                    var language = window.prompt("Enter book language: ")
                    if (language === null){
                        language = value.Language
                    }
                    var numPages = window.prompt("Enter number of pages: ")
                    if (numPages === null){
                        numPages = value.NumPages
                    }
                    var yearPubl = window.prompt("Enter year published: ")
                    if (yearPubl === null){
                        yearPubl = value.YearPublished
                    }
                    Axios.put('https://fant4stic-books.herokuapp.com/fant4stic/book/crud_operations/' + String(bookId),{"Title": Title, "Language": language, "NumberPages": numPages, "YearPublished": yearPubl})
                        .then((response) => {
                            console.log(response);
                        }, (error) => {
                            console.log(error);
                        });
                    setTimeout("location.reload(true);",1000)
                }
                }/>
            </div>
        </Card.Content>
    </Card>
    });
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

export default AllProductsAdmin;