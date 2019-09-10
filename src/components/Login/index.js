import React, {Component} from 'react';
import {Modal, Button, Input, message} from 'antd';
import axios from 'axios';
import {Link} from 'react-router-dom';
import './style.css';

class Login extends Component{

    constructor(props){
        super(props);
        this.clickVisible = this.clickVisible.bind(this);
        this.handleCancel = this.handleCancel.bind(this);
        this.inputusername = this.inputusername.bind(this);
        this.inputpassword = this.inputpassword.bind(this);
        this.handleOk = this.handleOk.bind(this);
        this.logout = this.logout.bind(this);
        this.state = {
            login: false,
            visible: false,
            password:"",
            username:""
        };
    }
    logout(){
        axios.get('http://www.dell-lee.com/react/api/logout.json',{
            withCredentials:true
        }).then(
            res=>{
                console.log(res.data.data)
                const logout = res.data.data.logout
                if (logout){
                    this.setState({login: false})
                }
                // this.setState(res.data.data)
            }
        )
    }
    handleOk(){
        const {username, password} = this.state;
        let url = `http://www.dell-lee.com/react/api/login.json?user=${username}&password=${password}`;
        axios.get(url,{
            withCredentials:true
        }).then(res=>{
            const login = res.data.data.login
            this.setState({login: login})
            if (login){
                message.success('登陆成功');
                this.setState({
                    visible: false,
                    login: true
                })
            }else {
                message.error('登陆失败');
            }
        })
    }
    inputusername(e){
        this.setState({username:e.target.value})
    }
    inputpassword(e){
        this.setState({password:e.target.value})
    }
    clickVisible(){
        this.setState({ visible: true});
    }
    handleCancel(){
        this.setState({ visible: false});
    }
    render(){
        return(
            <div className='button'>
                {this.state.login ?  <Link to='/'><Button type="primary" onClick={this.logout}>退出</Button> </Link>
                    : <Button type="primary" onClick={this.clickVisible}>登陆</Button>}
                <Modal
                    title="Basic Modal"
                    visible={this.state.visible}
                    onOk={this.handleOk}
                    onCancel={this.handleCancel}

                >
                    <Input placeholder="请输入用户名" style={{marginBottom: 10}} value={this.state.username} onChange={this.inputusername}/>
                    <Input placeholder="请输入密码" type='password' value={this.state.password} onChange={this.inputpassword}/>
                </Modal>
                <Link to='/vip'>
                    <Button type="primary" style={{marginLeft:10}}>vip</Button>
                </Link>
            </div>
        )
    }

    componentDidMount() {
        axios.get('http://www.dell-lee.com/react/api/isLogin.json',{
            withCredentials:true
        }).then(
            res=>{
                this.setState(res.data.data)
            }
        )
    }
}

export default Login;
