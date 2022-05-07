import React from 'react';
import ReactDOM from 'react-dom/client';
import {Route, BrowserRouter, Routes} from 'react-router-dom';
import './index.css';
import '../node_modules/semantic-ui-css/semantic.min.css'
import HomePage from "./HomePage";
import CustomerView from "./CustomerView";
import AdminView from "./AdminView";
import Dashboard from "./Dashboard";
import Register from "./Register";


const root = ReactDOM.createRoot( document.getElementById('root') );
root.render(
    <BrowserRouter>
        <Routes>
            <Route exact path="/" element={<HomePage/>} />
            <Route exact path="/Register" element={<Register/>} />
            <Route exact path="/CustomerView" element={<CustomerView/>} />
            <Route exact path="/AdminView" element={<AdminView/>} />
            <Route exact path="/Dashboard" element={<Dashboard/>} />
        </Routes>
    </BrowserRouter>
);
