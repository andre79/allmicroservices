import React, { useEffect, useState } from 'react';
import styled from 'styled-components';
import { Grid, Container, Header, Button } from 'semantic-ui-react'
import Menu from '../../components/header';
import { fetchData, setCache, listCache } from '../../services/Resource';
import { useToasts } from 'react-toast-notifications';

const Sale = () => {

    const { addToast } = useToasts();
    const [ data, setData ] = useState([]);
    const [ checkoutItems, setCheckoutItems ] = useState(0);

    useEffect(() => {
        fetchData('products/category/sale').then(res => {
          const response = res.data;
          setData(response.product);
        });
    }, []);

    const handleSubmit = (product) => {
        const storage = listCache('storageCoffee');

        if(storage) {
            setCache('storageCoffee', [...storage, product]);
            addToast('Item adicionado na sacola', { appearance: 'success', autoDismiss: true });
        } else {
            setCache('storageCoffee', [product]);
            addToast('Item adicionado na sacola', { appearance: 'success', autoDismiss: true });
        };

        const items = storage || storage.length > 0 ? storage.length + 1 : 0;
        setCheckoutItems(items);
    };

    return (
        <Page>
            <Menu page="sale" itemsQuantity={checkoutItems} />
            <Container>
                <Grid columns='equal' className="content-inner">

                    {
                        data.map( (item, index) =>
                            <Grid.Column width={4} key={index}>
                                <div>
                                    <Button circular icon='add to cart' color="orange" size="large" floated='right' onClick={() => handleSubmit(item)} />
                                </div>
                                <div style={{ display: 'flex', justifyContent: 'center', clear: 'both' }}>
                                    <img className="coffee-thumb" src={item['image_thumb']} alt="" />
                                </div>
                                <Header as='h4'>{item.name}</Header>
                                <p>
                                    <span className="old-price">{`R$ ${item['old_price']}`}</span>
                                    <br />
                                    <span className="price">{`R$ ${item.price}`}</span>
                                </p>
                            </Grid.Column>
                        )
                    }

                </Grid>
            </Container>
        </Page>
    )
};

export default Sale;

const Page = styled.section`
    .content-inner {
        margin-top: 20px;
    }
    .coffee-thumb {
        height: 190px;
    }
    .old-price {
        color: #9e9e9e;
        font-size: .9rem;
        font-weight: 400;
        padding-right: .5rem;
        text-decoration: line-through;
    }
    .price {
        color: black;
        font-size: 1.3rem;
        font-weight: bold;
    }
`
