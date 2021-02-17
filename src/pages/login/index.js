import React, { useState } from 'react';
import styled from 'styled-components';
import Logo from '../../logo.svg';
import { Link, useHistory } from "react-router-dom";
import { Container, Grid, Segment, Header, Form, Button, Input, Divider, Message } from 'semantic-ui-react';
import { listCache, postData, setCache, deleteCache } from '../../services/Resource';

const Login = () => {

    let history = useHistory();

    const [ email, setEmail ] = useState('');
    const [ password, setPassword ] = useState('');
    const [ message, setMessage ] = useState(false);

    const handleSubmit = () => {
        const params = {
            email,
            password
        };

        postData('user/auth', params).then(({ data }) => {
            const goBack = listCache('goBack');

            setCache('userCoffee', data.user);

            if(goBack){
                history.push(`/${goBack}`);
                deleteCache('goBack');
            } else {
                history.push('/');
            }

        }).catch(err => {
            setMessage(true);
        });
    };

    return (
        <Page>
           <div className="header-top">
                <Image src={Logo} alt="" />
                <Link to="/"><span className="logo-font">ART<strong style={{ color: '#a5673f' }}>COFFEE</strong></span></Link>
           </div>

           <Container>
                <Grid centered columns={1}>
                    <Grid.Column style={{ maxWidth: 450 }}>
                        <Segment>
                            <Header
                                as='h2'
                                content='Login'
                                subheader='Entre com as credenciais'
                            />

                            <Divider />

                            {message &&
                                <Message negative>
                                    <Message.Header>Ocorreu algo estranho</Message.Header>
                                    <Message.List>
                                    <Message.Item>Preencha os campos obrigatórios</Message.Item>
                                    <Message.Item>E-mail ou senha estão incorretos</Message.Item>
                                    </Message.List>
                                </Message>
                            }                            

                            <Form onSubmit={handleSubmit}>
                                <Form.Field>
                                    <Input icon='mail' iconPosition='left' placeholder='E-mail' type="text" value={email} onChange={ e => setEmail(e.target.value) } />
                                </Form.Field>
                                <Form.Field>
                                    <Input icon='lock' iconPosition='left' placeholder='Senha' type="password" value={password} onChange={ e => setPassword(e.target.value) } />
                                </Form.Field>
                                <Button type='submit' fluid color="brown">Entrar</Button>
                            </Form>
                        </Segment>
                    </Grid.Column>
                </Grid>
           </Container>
        </Page>
    )
}

export default Login;

const Page = styled.div`
    .ui.grid {
        margin-top: 30px;
    }
    .header-top {
        text-align: center;
        padding: 40px 0;
        background-color: #f7f7f7;
    }
    .logo-font {
        text-transform: lowercase;
        font-size: 1.4em;
        color: black;
    }
    .header {
        text-align: center
    }
    button {
        padding: 20px 0;
    }
`

const Image = styled.img`
    height: 50px;    
    margin-right: 10px
`
