import React, {Component, useState} from 'react';
import {Button, Card, Container, Header, Modal, Tab} from "semantic-ui-react";

function AllProducts(props) {
    console.log(props)
    props.info.forEach(value => console.log(value.pname));
    return props.info.map(value => {return <Card>
        <Card.Content>
            <Card.Header>{value.pname}</Card.Header>
            <Card.Meta>{value.pprice}</Card.Meta>
            <Card.Description>
                {value.pname}
            </Card.Description>
        </Card.Content>
        <Card.Content extra>
            <div className='ui two buttons'>
                <Button basic color='green'>
                    Add to Wish List
                </Button>
                <Button basic color='green'>
                    Add to Cart
                </Button>
            </div>
        </Card.Content>
    </Card>});
}

function CartProducts(props){
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
                <Button basic color='green'>
                    Add to Wish List
                </Button>
                <Button basic color='red'>
                    Remove from Cart
                </Button>
            </div>
        </Card.Content>
    </Card>});
}

function WishProducts(props){
    console.log(props)
    props.info.forEach(value => console.log(value.WishlistId));
    return props.info.map(value => {return <div> <Header>Wishlist #{value.WishlistId}</Header> {value.ListOfProducts.map(value => {return <Card>
        <Card.Content>
            <Card.Header>{value.BookTitle}</Card.Header>
            <Card.Meta>Date added: {value.DateAdded}</Card.Meta>
        </Card.Content>
        <Card.Content extra>
            <div className='ui two buttons'>
                <Button basic color='green'>
                    Add to Cart
                </Button>
                <Button basic color='red'>
                    Remove from Wish List
                </Button>
            </div>
        </Card.Content>
    </Card>})}</div>});
}

export default AllProducts;
export {CartProducts, WishProducts}