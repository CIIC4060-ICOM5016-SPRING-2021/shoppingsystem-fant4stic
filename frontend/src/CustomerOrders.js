import React, {Component, useState, useEffect} from 'react';
import { useNavigate } from 'react-router-dom';
import {Button, Card, Modal, List} from 'semantic-ui-react';
import Axios from "axios";
import {getUserInfo} from "./CustomerView"

function CustomerOrders(){
    const loginvalues = JSON.parse(localStorage.getItem('loginValues'));
    const [allUsers, setAllUsers] = useState([]);
    const [customer, setCustomer] = useState({"UserId": "","RoleId": "","FirstName": "","LastName": "",
        "UserName": "","Email": "","Password": "","Age": "","Sex": "","PhoneNumber": ""})
    console.log(customer)
    const [historyOrders, setHistoryOrders] = useState([]);
    const email = loginvalues['inputEmail'];
    console.log("Email Stored: " + email);
    const password = loginvalues['inputPassword'];
    console.log("Password Stored: " + password);

    useEffect(() => {
        Axios.get('https://fant4stic-books.herokuapp.com/fant4stic/user/get_all')
            .then(res => {
                console.log("All Users:", res.data)
                setAllUsers(res.data)
            }).catch(err => console.log(err))
    }, [])

    useEffect(()=>{
        setCustomer(getUserInfo(email,password,allUsers))
    },[allUsers]);

    useEffect(()=>{
        const userId = customer.UserId;
        Axios.get('https://fant4stic-books.herokuapp.com/fant4stic/order/historyoforders/'+String(userId))
            .then(res => {
                console.log("Get Order History of Customer:", res.data)
                setHistoryOrders(res.data)
            }).catch(err => console.log(err))
    },[customer]);

    return (
        <Card.Group>
            {historyOrders.map((value) => (
                <Card
                    header={'Order # '+String(value.OrderId)}
                    meta={'Order Date and Time: '+value.OrderDate+'/'+value.OrderTime}
                    description={'Total Price of Order: $'+String(value.TotalPrice)}
                    extra={<Modal
                        trigger={<Button color='gray'>Products Bought</Button>}
                        header={'Products from Order #'+String(value.OrderId)}
                        content={value.ListOfProductsBought.map((val=>(
                            (<List bulleted>
                                <List.Item>Book Title: {val.BookTitle}, Copies: {val.NumberOfQuantities}, Book Price: ${val.BookPrice}</List.Item>
                            </List>
                            )
                        )))}
                        actions={[{ key: 'done', content: 'Done', positive: true }]}
                    />}
                />
            ))}
        </Card.Group>
    )
}

export default CustomerOrders;