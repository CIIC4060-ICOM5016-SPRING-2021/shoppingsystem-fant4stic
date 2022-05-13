import React, {Component, useState, useEffect} from 'react';
import { useNavigate } from 'react-router-dom';
import {Button, Card, Modal, Transition, Table} from 'semantic-ui-react';
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

    function tableProductsBought(arrayOrders){
        return (<div><Table attached='top' celled stripped>
            <Table.Header>
                <Table.Row>
                    <Table.HeaderCell>Book Title</Table.HeaderCell>
                    <Table.HeaderCell>Copies</Table.HeaderCell>
                    <Table.HeaderCell>Book Price</Table.HeaderCell>
                </Table.Row>
            </Table.Header>
            {arrayOrders.ListOfProductsBought.map((val=>((
                <Table.Body>
                    <Table.Row>
                        <Table.Cell >{val.BookTitle}</Table.Cell>
                        <Table.Cell>{val.NumberOfQuantities}</Table.Cell>
                        <Table.Cell positive>${val.BookPrice}</Table.Cell>
                    </Table.Row>
                </Table.Body>
            ))))}
            </Table>
            <Table attached='bottom' celled>
                    <Table.Header>
                        <Table.Row>
                            <Table.HeaderCell >Total Payment of Order</Table.HeaderCell>
                        </Table.Row>
                        <Table.Body>
                            <Table.Row>
                                <Table.Cell positive>${arrayOrders.TotalPrice}</Table.Cell>
                            </Table.Row>
                        </Table.Body>
                    </Table.Header>
            </Table>
            </div>
        )
    }
    //Display only if Customer has orders
    if(historyOrders.length !==0) {
        return (
            <Card.Group>
                {historyOrders.map((value) => (
                    <Card
                        header={'Order # ' + String(value.OrderId)}
                        meta={'Order Date and Time: ' + value.OrderDate + '/' + value.OrderTime}
                        description={'Total Price of Order: $' + String(value.TotalPrice)}
                        extra={<Modal
                            trigger={<Button color='gray'>Products Bought</Button>}
                            header={'Products from Order #' + String(value.OrderId)}
                            content={tableProductsBought(value)}
                            actions={[{key: 'done', content: 'Done', positive: true}]}
                        />}
                    />
                ))}
            </Card.Group>
        )
    }else{
        return (
                <Card.Group>
                    <Card
                        header='This Customer does not have any orders yet'
                        meta='Consider making a purchase'
                        description='Go to our product section and purchase whatever you like'
                    />
                </Card.Group>
        )
    }
}

export default CustomerOrders;