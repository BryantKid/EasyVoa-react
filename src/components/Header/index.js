import React, { Component, Fragment} from 'react';
import logo from './logo.png';
import axios from 'axios';
import './style.css'
import { Menu, Icon } from 'antd';
import {Link} from "react-router-dom";

class AppHeader extends Component {
    constructor(prop){
        super(prop)
        this.state = {
            list:[]
        }
    }
    getMenuitem(){
        return(
            this.state.list.map((item)=>{
                return (
                    <Menu.Item key={item.id}>
                        <Link to={`/${item.id}`}>
                            <Icon type={item.icon} />{item.title}
                        </Link>
                    </Menu.Item>
                )

            })
        )
    }

    componentDidMount(){
        axios.get('http://www.dell-lee.com/react/api/header.json').then(
            res=>{
                console.log(res.data.data)
                this.setState({
                list: res.data.data
                });
            })
    }


    render() {
        return (
            <Fragment>
                <Link to='/'>
                    <img className='app-header-logo' src={logo} alt='img'/>
                </Link>
                <Menu mode="horizontal" className="app-header-menu" >
                    {this.getMenuitem()}
                </Menu>
            </Fragment>
        )

    }
}

export default AppHeader;
