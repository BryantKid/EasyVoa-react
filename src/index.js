import React, { Component } from 'react';
import ReactDom from 'react-dom';
import 'antd/dist/antd.css';
import { Layout } from 'antd';
import './style.css';
import AppHeader from './components/Header/';
import Login from './components/Login';
import {BrowserRouter, Route, Switch} from 'react-router-dom';
import Test from './components/content/Test';
import MyList from './components/content/List';
import Vip from './components/content/vip';

const { Header, Footer, Content } = Layout;

class App extends Component {

    render() {
        return(
            <BrowserRouter>
                <Layout style={{minWidth:1300, height:"100%"}}>
                    <Header className="header">
                        <AppHeader/>
                    </Header>
                    <Content className="content">
                        <Login/>
                        <Switch>
                            <Route path='/vip' component={Vip}></Route>
                            <Route path='/detail/:id' component={Test}></Route>
                            <Route path='/:id?' component={MyList}></Route>
                        </Switch>
                    </Content>
                    <Footer className="footer">@copyright tangdongliang 2018</Footer>
                </Layout>
            </BrowserRouter>
        )
    }
}

ReactDom.render(<App />, document.getElementById('root'));
