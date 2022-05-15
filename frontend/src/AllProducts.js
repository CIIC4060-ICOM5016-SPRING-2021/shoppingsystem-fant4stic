import React, {Component, useEffect, useState} from 'react';
import {Button, Card, CardContent, CardHeader, Container, Header, Image, Modal, Tab} from "semantic-ui-react";
import Axios from "axios";
import CartProduct from "./Cart";
import Art from "./images/Art.png"
import Children from "./images/Children.png"
import Comics from "./images/Comics.png"
import Default from "./images/Default.png"
import Development from "./images/Development.png"
import Dystopian from "./images/Dystopian.png"
import Fantasy from "./images/Fantasy.png"
import Health from "./images/Health.png"
import History from "./images/History.png"
import Horror from "./images/Horror.png"
import Romance from "./images/Romance.png"
import ScienceFiction from "./images/Science Fiction.png"

function AllProducts(props) {
    const [wishArray, setWish] = useState([""])
    var idsArray = []
    var count = -1

    useEffect(() => {Axios.get("https://fant4stic-books.herokuapp.com/fant4stic/wishlist/get_all")
        .then(res => {console.log("Wishlists:", res.data); setWish(res.data)})}, [])

    wishArray.forEach(value => {if(value.CustomerId == props.userId){idsArray.push(value.WishlistId)}})

    console.log(props.info)
    props.info.forEach(value => console.log(value.Title));
    return props.info.map(value => {return <Card>
        <Card.Content>
            <Card.Header>{value.Title}</Card.Header>
            <div>
            <Card.Meta><Image src= {getImage(value.GenreName)} alt={String(value.GenreName)} centered verticalAlign='middle'/></Card.Meta>
            </div>
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
            <div className='ui two buttons'>
                <Button basic color='blue' onClick={() => {console.log("Added Book:"); console.log(value.Title);
                    var wishListId = window. prompt("On which of the following Wishlists? : " + idsArray.toString()); alert("The indicated Wishlist is: " + wishListId);
                    Axios.post('https://fant4stic-books.herokuapp.com/fant4stic/wishlist',
                        {"Title": String(value.Title), "Customer_id": String(props.userId), "Wishlist_id": String(wishListId)}).then(() => console.log('Addition successful'))
                        .catch(err => {console.log(err);
                            alert("Invalid Wishlist provided or book was already on the indicated Wishlist")} )
                    /*setTimeout("location.reload(true);",1000)*/ /*document.location.reload(true)*/ count = -1}}>
                    Add to Wish List
                </Button>
                <Button basic color='yellow' onClick={() => {console.log("Added Book:"); console.log(value.Title);
                    var numOfCopies = window. prompt("How much Copies?: "); alert("The indicated amount of copies is: " + numOfCopies)
                    console.log(value.Title)
                    console.log(props.userId)
                    console.log(numOfCopies)
                    const num = numOfCopies
                    Axios.post('https://fant4stic-books.herokuapp.com/fant4stic/cart',
                        {"Title": String(value.Title), "Customer_id": String(props.userId), "Copies": parseInt(numOfCopies)}).then(() => console.log('Addition successful'))
                        .catch(err => {console.log(err); alert("The amount of specified units exceed book availability, book was already on cart, or desired amount of copies was not specified")});
                    /*setTimeout("location.reload(true);",1000)*/ /*document.location.reload(true)*/}}>
                    Add to Cart
                </Button>
            </div>
        </Card.Content>
    </Card>});
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

function getImage(genreName) {
    switch (genreName) {
        case "Art":
            return Art
            break;
        case "Children":
            return Children
            break;
        case "Comics":
            return Comics
            break;
        case "Development":
            return Development
            break;
        case "Dystopian":
            return Dystopian
            break;
        case "Fantasy":
            return Fantasy
            break;
        case "Health":
            return Health
            break;
        case "History":
            return History
            break;
        case "Horror":
            return Horror
            break;
        case "Romance":
            return Romance
            break;
        case "Science fiction":
            return ScienceFiction
            break;
        default:
            return Default
            break;
    }
}

export default AllProducts;
export {CartProducts, WishProducts, getImage}
