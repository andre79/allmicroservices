import React, { useEffect, useState } from 'react';
import { Grid, Container, Message, Header, Segment } from 'semantic-ui-react';
import Menu from '../../components/header';
import styled from 'styled-components';
import { fetchData, listCache } from '../../services/Resource';

const Purchased = () => {

    const [ data, setData ] = useState([]);

    useEffect(() => {

        const auth = listCache('userCoffee');

        if(auth){
            fetchData(`checkout/${auth.id}`).then(res => {
                const response = res.data;
                setData(response.checkout);
            }); 
        }

    }, []);

    return (
        <Page>
            <Menu page="purchased" />
            <Container>
                <Grid columns='equal' className="content-inner">
                    
                   { data.length > 0 ?
                        
                        <div style={{ width: '100%' }}>
                            {data.map(item =>                                 
                                <Segment.Group style={{ width: '100%' }}>
                                    <Segment>
                                        <Grid>
                                            <Grid.Column width={2}>
                                                <Header
                                                    as='h5'
                                                    content='Nº do pedido'
                                                    subheader={item.order}
                                                />
                                            </Grid.Column>
                                            <Grid.Column width={3}>
                                                <Header
                                                    as='h5'
                                                    content='Pedido realizado'
                                                    subheader={item.dateOrder}
                                                />
                                            </Grid.Column>
                                            <Grid.Column width={3}>
                                                <Header
                                                    as='h5'
                                                    content='Data de entrega'
                                                    subheader={item.dateDelivery}
                                                />
                                            </Grid.Column>
                                            <Grid.Column width={2}>
                                                <Header
                                                    as='h5'
                                                    content='Total'
                                                    subheader={`R$ ${item.amount}`}
                                                />
                                            </Grid.Column>
                                            <Grid.Column width={3}>                                                
                                                <Header
                                                    as='h5'
                                                    content='Status'
                                                    subheader={item.statusOrder}
                                                />
                                            </Grid.Column>
                                        </Grid>
                                    </Segment>
                                    <Segment>
                                        { item.products &&
                                            item.products.map( product => 
                                                <h4>{product.name}</h4>
                                            )
                                        }
                                    </Segment>
                                </Segment.Group>
                            )}
                        </div>

                        :

                        <Message visible>Você não tem pedidos realizados</Message>
                   }
                </Grid>
            </Container>
        </Page>
    )
};

export default Purchased;

const Page = styled.section`
    .content-inner {
        margin-top: 20px;
    }
`
