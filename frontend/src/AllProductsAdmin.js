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
import CartProduct from "./Cart";

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
            <Card.Meta>Author: {value.AuthorFirstName} {value.AuthorLastName}</Card.Meta>
            <Card.Meta>Language: {value.Language}</Card.Meta>
            <Card.Meta>Pages: {value.NumPages}</Card.Meta>
            <Card.Meta>Year: {value.YearPublished}</Card.Meta>
            <Card.Meta>${value.PriceUnit}</Card.Meta>
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
            </div>
        </Card.Content>
    </Card>
    });
}

function CartProducts(props){
    const [wishArray, setWish] = useState([""])
    var idsArray = []
    var count = -1

    useEffect(() => {Axios.get("https://fant4stic-books.herokuapp.com/fant4stic/wishlist/get_all")
        .then(res => {console.log("Wishlists:", res.data); setWish(res.data)})}, [])

    wishArray.forEach(value => {if(value.CustomerId == props.userId){idsArray.push(value.WishlistId)}})

    console.log(props)
    props.info.forEach(value => console.log(value.Title));
    return props.info.map(value => {return <Card>
        <Card.Content>
            <Card.Header>{value.Title}</Card.Header>
            <Card.Meta>Price: ${value.BookPrice}</Card.Meta>
            <Card.Description>
                Copies: {value.Copies}
            </Card.Description>
        </Card.Content>
        <Card.Content extra>
            <div className='ui two buttons'>
                <Button basic color='green' onClick={() => {console.log("Added Book:"); console.log(value.Title);
                    var wishListId = window. prompt("On which of the following Wishlists? : " + idsArray.toString()); alert("The indicated Wishlist is: " + wishListId);
                    Axios.post('https://fant4stic-books.herokuapp.com/fant4stic/wishlist',
                        {"Title": String(value.Title), "Customer_id": String(props.userId), "Wishlist_id": String(wishListId)}).then(() => console.log('Addition successful'))
                        .catch(err => {console.log(err);
                            alert("Invalid Wishlist provided or book was already on the indicated Wishlist")} )
                    /*setTimeout("location.reload(true);",1000)*/ /*document.location.reload(true)*/ count = -1}}>
                    Add to Wish List
                </Button>

                <Button basic color='red' onClick={() => {console.log("Deleted Book:"); console.log(value.Title);
                    Axios.delete('https://fant4stic-books.herokuapp.com/fant4stic/cart',
                        {data: {"Title": String(value.Title), "Customer_id": String(props.userId)}}).then(() => console.log('Delete successful'));
                    setTimeout("location.reload(true);",1000) /*document.location.reload(true)*/}}>
                    Remove from Cart
                </Button>
            </div>
        </Card.Content>
    </Card>});
}

function WishProducts(props){
    const [wishArray, setWish] = useState([""])
    var idsArray = []
    var count = -1

    console.log(props)
    props.info.forEach(value => console.log(value.WishlistId));

    useEffect(() => {Axios.get("https://fant4stic-books.herokuapp.com/fant4stic/wishlist/get_all")
        .then(res => {console.log("Wishlists:", res.data); setWish(res.data)})}, [])

    wishArray.forEach(value => {if(value.CustomerId == props.userId){idsArray.push(value.WishlistId)}})

    console.log("Array Ids:")
    console.log(idsArray)
    console.log(props.info)

    if(props.info.length == 0){console.log("If works"); return idsArray.map(value => {count ++; return <Card>
        <CardContent>
            <Card.Header>Wishlist #{idsArray[count]}</Card.Header>
        </CardContent>
    </Card>})}

    return props.info.map(WishList => {return <div> <Header>Wishlist #{WishList.WishlistId}</Header> {WishList.ListOfProducts.map(value => {return <Card>
        <Card.Content>
            <Card.Header>{value.BookTitle}</Card.Header>
            <Card.Meta>Date added: {value.DateAdded}</Card.Meta>
        </Card.Content>
        <Card.Content extra>
            <div className='ui two buttons'>
                <Button basic color='green' onClick={() => {console.log("Added Book:"); console.log(value.BookTitle);
                    var numOfCopies = window. prompt("How much Copies?: "); alert("The indicated amount of copies is: " + numOfCopies)
                    console.log(value.BookTitle)
                    console.log(props.userId)
                    console.log(numOfCopies)
                    const num = numOfCopies
                    Axios.post('https://fant4stic-books.herokuapp.com/fant4stic/cart',
                        {"Title": String(value.BookTitle), "Customer_id": String(props.userId), "Copies": parseInt(numOfCopies)}).then(() => console.log('Addition successful'))
                        .catch(err => {console.log(err); alert("The amount of specified units exceed book availability, book was already on cart, or desired amount of copies was not specified")});
                    /*setTimeout("location.reload(true);",1000)*/ /*document.location.reload(true)*/}}>
                    Add to Cart
                </Button>

                <Button basic color='red' onClick={() => {console.log("Deleted Book:"); console.log(value.BookTitle);
                    Axios.delete('https://fant4stic-books.herokuapp.com/fant4stic/wishlist',
                        {data: {"Title": String(value.BookTitle), "Customer_id": String(props.userId), "Wishlist_id": String(WishList.WishlistId)}}).then(() => console.log('Delete successful'));
                    setTimeout("location.reload(true);",1000) /*document.location.reload(true)*/}}>
                    Remove from Wish List
                </Button>
            </div>
        </Card.Content>
    </Card>})}</div>});
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
export {CartProducts, WishProducts}