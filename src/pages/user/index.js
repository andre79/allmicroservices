import React, {useState} from 'react';
import styled from 'styled-components';
import Logo from '../../logo.svg';
import { Link, useHistory } from "react-router-dom";
import { Container, Grid, Segment, Header, Form, Button, Input, Divider, Message } from 'semantic-ui-react';
import { postDataUser } from "../../services/Resource";

const User = () => {

    let history = useHistory();

    const [ name, setName ] = useState('');
    const [ email, setEmail ] = useState('');
    const [ user, setUser ] = useState('');
    const [ password, setPassword ] = useState('');
    const [ message, setMessage ] = useState(false);
    const [ textMessage, setTextMessage ] = useState('');

    const handleSubmit = () => {
        const params = {name, email, user, password};

        const validateInputs = Object.values(params).filter( item => item === "");
        console.log(validateInputs.length)    
        
        if(validateInputs.length === 0) {            
            postDataUser('user', params).then(({ data }) => {
                history.push("/login");
            }).catch(err => {
                setMessage(true);
                setTextMessage('Usuário já cadastrado');
            });
        } else {
            setMessage(true);
            setTextMessage('Preencha os campos obrigatórios');
        };
        
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
                                content='Cadastro de Usuários'
                                subheader='Entre com os daods do usuários'
                            />

                            <Divider />
                            
                            { message &&
                                <Message
                                    error
                                    header={textMessage}
                                />
                            }                            

                            <Form  onSubmit={handleSubmit}>
                                <Form.Field error={message && name === '' ? true : false}>
                                    <Input icon='user' iconPosition='left' placeholder='Nome Completo' type="text" value={name} onChange={ e => setName(e.target.value) } />
                                </Form.Field>
                                <Form.Field error={message && email === '' ? true : false}>
                                    <Input icon='mail' iconPosition='left' placeholder='E-mail' type="text" value={email} onChange={ e => setEmail(e.target.value) } />
                                </Form.Field>
                                <Form.Field error={message && user === '' ? true : false}>
                                    <Input icon='user' iconPosition='left' placeholder='user' type="text" value={user} onChange={ e => setUser(e.target.value) }/>
                                </Form.Field>
                                <Form.Field error={message && password === '' ? true : false}>
                                    <Input icon='lock' iconPosition='left' placeholder='Senha' type="password" value={password} onChange={ e => setPassword(e.target.value) }/>
                                </Form.Field>
                                <Button type='submit' fluid color="brown">Cadastrar</Button>
                            </Form>
                        </Segment>
                    </Grid.Column>
                </Grid>
           </Container>
        </Page>
    )
}

export default User;

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
