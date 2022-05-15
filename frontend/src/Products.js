import React, {Component, useEffect, useState} from 'react';
import {Button, Card, Container, Modal, Tab} from "semantic-ui-react";
import AllProducts from "./AllProducts";
import Axios from "axios";

function Products() {
    const [allProducts, setAllProducts] = useState([]);
    console.log(allProducts)
    useEffect(() => {
        Axios.get('https://fant4stic-books.herokuapp.com/fant4stic/inventory/get_all/show')
            .then(res => {
                console.log("All Products: ", res.data)
                setAllProducts(res.data)
            }).catch(err => console.log(err))
    }, [])

    return <Card.Group>
        <AllProducts info={allProducts}/>
    </Card.Group>
}

export default Products;