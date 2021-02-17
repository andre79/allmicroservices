import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { Link, useHistory } from "react-router-dom";
import { Container, Grid, List, Button, Menu, Icon, Label } from 'semantic-ui-react';
import Logo from '../../logo.svg';
import { listCache, deleteCache } from '../../services/Resource';

const Header = ({ page, itemsQuantity }) => {

    let history = useHistory();

    const [ storage, setStorage ] = useState(0);
    const [ userLogged, setUserLogged ] = useState(false);

    useEffect(() => {
        const cacheStorage = listCache('storageCoffee');
        const auth = listCache('userCoffee');

        auth ? setUserLogged(true) : setUserLogged(false);

        setStorage(cacheStorage ? cacheStorage.length : 0);
    }, [itemsQuantity]);

    const logout = () => {
        deleteCache('userCoffee');
        history.push("/");
        document.location.reload(true);
    };

    return (
        <Content>
            <Container>
                <Grid>
                    <Grid.Row>
                        <Grid.Column width={3}>
                            <Image src={Logo} alt="" />
                            <Link to="/"><span className="logo-font">ART<strong style={{ color: '#a5673f' }}>COFFEE</strong></span></Link>
                        </Grid.Column>

                        <Grid.Column width={8}>
                            <List horizontal>
                                <List.Item href='/cafe' style={{ color: page === 'coffee' ? '#a5673f' : '' }}>Cafés</List.Item>
                                <List.Item href='/acessorio' style={{ color: page === 'accessory' ? '#a5673f' : '' }}>Acessórios</List.Item>
                                <List.Item href='/promocao' style={{ color: page === 'sale' ? '#bf2c2c' : '' }}>Promoções</List.Item>
                            </List>
                        </Grid.Column>

                        { userLogged ?    
                            <Grid.Column width={5} floated="right" style={{ marginTop: 7 }}>     
                                <Button basic color='brown' content='Sair' floated="right" onClick={logout} />
                                <Button basic color='brown' content='Meus pedidos' floated="right" onClick={() => history.push('/pedidos') } />
                                <Link to="/sacola">
                                    <Menu compact>
                                        <Menu.Item as='a'>
                                        <Icon name='shopping cart' /> Sacola
                                        <Label color='red' floating> { storage } </Label>
                                        </Menu.Item>
                                    </Menu>
                                </Link>
                            </Grid.Column>
                            :
                            <Grid.Column width={5} floated="right" style={{ marginTop: 7 }}>     
                                <Link to="/user"><Button color='brown' content='Cadastrar' floated="right" /></Link>
                                <Link to="/login"><Button basic color='brown' content='Entrar' floated="right" /></Link>
                                <Link to="/sacola">
                                    <Menu compact>
                                        <Menu.Item as='a'>
                                        <Icon name='shopping cart' /> Sacola
                                        <Label color='red' floating> {storage} </Label>
                                        </Menu.Item>
                                    </Menu>
                                </Link>
                            </Grid.Column>
                        }
                    </Grid.Row>
                </Grid>
            </Container>
        </Content>
    )
}

export default Header;

const Content = styled.div`
    background-color: white;
    font-family: 'Andika New Basic', sans-serif;
    box-shadow: 0 1px 3px rgba(0,0,0,.1), 0 2px 2px rgba(0,0,0,.06), 0 0 2px rgba(0,0,0,.07);
    height: 10vh;
    display: flex;
    align-items: center;
    text-transform: uppercase;

    .ui.list {
        margin: 10px 0 0 25px;

        .item {
            color: black;
            padding-right: 10px;
        }
    }
    .logo-font {
        text-transform: lowercase;
        font-size: 1.4em;
        color: black;
    }
` 



const Image = styled.img`
    height: 50px;    
    margin-right: 10px
`
