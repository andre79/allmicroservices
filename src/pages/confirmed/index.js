import React, { useEffect } from 'react';
import { useHistory } from "react-router-dom";
import styled from 'styled-components';
import { Grid, Container, Message } from 'semantic-ui-react'
import Menu from '../../components/header';
import { deleteCache } from '../../services/Resource';

const Confirmed = () => {

    let history = useHistory();
    
    useEffect(() => {
        deleteCache('storageCoffee');

        setTimeout(() => { history.push('/') }, 5000);

    }, []);

    return (
        <Page>
            <Menu />
            <Container>
                <Grid columns='equal' className="content-inner">
                    <Grid.Column width={16}>
                        <Message
                            success
                            icon='check'
                            header='Pedido realizado com sucesso'
                            content='Acompanhe o status do seu pedido acessando os meus pedidos.'
                        />
                    </Grid.Column>
                </Grid>
            </Container>
        </Page>
    )
};

export default Confirmed;

const Page = styled.section`
    .content-inner {
        margin-top: 20px;
    }
`
