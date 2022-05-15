import React, {Component, useEffect, useState} from 'react';
import {Button, Card, Container, Modal, Tab} from "semantic-ui-react";
import AllProductsAdmin from "./AllProductsAdmin";
import Axios from "axios";

function ProductsAdmin() {
    const [allProducts, setAllProducts] = useState([]);

    useEffect(() => {
        Axios.get('https://fant4stic-books.herokuapp.com/fant4stic/inventory/get_all/show')
            .then(res => {
                console.log("All Products: ", res.data)
                setAllProducts(res.data)
            }).catch(err => console.log(err))
    }, [])

    return <Card.Group>
        <AllProductsAdmin info={allProducts}/>
    </Card.Group>
}

export default ProductsAdmin;