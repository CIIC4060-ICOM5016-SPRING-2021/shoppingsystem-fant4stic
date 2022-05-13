import React, {Component, useState, useEffect} from 'react';
import { useNavigate } from 'react-router-dom';
import {Button, Card, Modal, List, Table} from 'semantic-ui-react';
import Axios from "axios";

function AllCustomerOrders(){
    const [historyOrders, setHistoryOrders] = useState([]);
    console.log(historyOrders);
    useEffect(()=>{
        Axios.get('https://fant4stic-books.herokuapp.com/fant4stic/order/historyofallorders')
            .then(res => {
                console.log("Get Order History of All the Customers:", res.data)
                setHistoryOrders(res.data)
            }).catch(err => console.log(err))
    },[]);

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

    return (
        <Card.Group>
            {historyOrders.map((value) => (
                <Card
                    header={'Order # '+String(value.OrderId) +' of Customer # '+String(value.UserId)}
                    meta={'Order Date and Time: '+value.OrderDate+'/'+value.OrderTime}
                    description={'Total Price of Order: $'+String(value.TotalPrice)}
                    extra={<Modal
                        trigger={<Button color='white'>Products Bought</Button>}
                        header={'Products from Order #'+String(value.OrderId)}
                        content={tableProductsBought(value)}
                        actions={[{ key: 'done', content: 'Done', positive: true }]}
                    />}
                />
            ))}
        </Card.Group>
    )
}

export default AllCustomerOrders;