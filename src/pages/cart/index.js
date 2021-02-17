import React, { useState, useEffect } from 'react';
import { useHistory } from "react-router-dom";
import styled from 'styled-components';
import { Grid, Container, Table, Message, Button, Header, List, Divider, Input, Step, Icon, Form } from 'semantic-ui-react'
import Menu from '../../components/header';
import { fetchData, listCache, setCache, postData } from '../../services/Resource';
import { useToasts } from 'react-toast-notifications'

const Cart = () => {

    let history = useHistory();

    const initialAddress = {
        cep: '',   
        city: '',
        complement: '',
        neighborhood: '',
        number: '',
        phone: '',
        recipient: '',
        'street-name': ''
    };

    const initialCard = {
        'card-number': '',
        'due-date': '',
        'main-name': '',        
        'safe-code': ''
    };

    const { addToast } = useToasts();
    const [ products, setProducts ] = useState([]);
    const [ isLogged, setIsLogged ] = useState(false);
    const [ totalSum, setTotalSum ] = useState('0,00');
    const [ totalQuantity, setTotalQuantity ] = useState(0);
    const [ checkoutItems, setCheckoutItems ] = useState(0);
    const [ cep, setCep ] = useState('');
    const [ orderInfo, setOrderInfo ] = useState(null);
    const [ cepMessage, setCepMessage ] = useState(false);
    const [ stepPage, setStepPage ] = useState(1);
    const [address, setAddress] = useState(initialAddress);
    const [ card, setCard ] = useState(initialCard);

    const sumOfProducts = (checkout) => {
        const convertToSum = checkout.map( item => item.price.replace(',', '.') );
        const totalPrice = convertToSum.reduce( (acumulador, valorAtual) => acumulador + parseFloat(valorAtual), 0);

        return totalPrice.toFixed(2).toString().replace('.', ',');
    };

    const sumTotal = (productValue, deliveryValue) => {
        const convertToSumA = productValue.replace(',', '.');
        const convertToSumB = deliveryValue.replace(',', '.');

        return parseFloat(convertToSumA) + parseFloat(convertToSumB);
    };

    useEffect(() => {
        const storage = listCache('storageCoffee');
        const auth = listCache('userCoffee');

        setTotalSum( storage ? sumOfProducts(storage) : 0 );
        setTotalQuantity( storage ? storage.length : 0 );
        setProducts( storage ? storage : [] );       
        setIsLogged( auth ? true : false );   

    }, [setProducts]);

    const handleRemove = (id) => {
        const newStorage = products.filter( item => item.id !== id);  

        setCache('storageCoffee', [...newStorage]);
        setProducts([...newStorage]);
        setTotalSum(sumOfProducts(newStorage));
        setCheckoutItems(newStorage.length);  
        setTotalQuantity(newStorage.length);
        addToast('Item removido de sua sacola', { appearance: 'success', autoDismiss: true });
    };

    const cepValidate = () => {
        fetchData(`shipping/${cep}`).then(({ data }) => {
            setOrderInfo(data.shipping);
            setCepMessage(false);
        }).catch(err => {
            setCepMessage(true);
        });
    };

    const handleChangeAddress = (event) => {
        const value = event.target.value;

        setAddress({
            ...address,
            [event.target.name]: value
        });
    };

    const handleChangeCard = (event) => {
        const value = event.target.value;

        setCard({
            ...card,
            [event.target.name]: value
        });
    };

    const handleSubmit = () => {

        const auth = listCache('userCoffee');

        const payload = {
            user: {
                idUser: auth.id.toString()
            },
            products,
            address,
            card
        }

        const sum = sumTotal(totalSum, orderInfo.value).toFixed(2);

        payload.card.total = sum.toString().replace('.', ',');

        postData(`checkout`, payload).then(({ data }) => {
            history.push('/confirmed');
        }).catch(err => {
            console.log(err)
        });
    };

    const stepComponent = () => (   
        <Grid.Row>
            <Grid.Column width={16}>
                <Step.Group fluid size='tiny'>
                    <Step active={stepPage === 1 ? true : false} disabled={stepPage === 1 ? false : true}>
                    <Icon name='shopping basket' />
                    <Step.Content>
                        <Step.Title>Checkout</Step.Title>
                        <Step.Description>Selecione os itens para compra</Step.Description>
                    </Step.Content>
                    </Step>

                    <Step active={stepPage === 2 ? true : false} disabled={stepPage === 2 ? false : true}>
                    <Icon name='home' />
                    <Step.Content>
                        <Step.Title>Endereço</Step.Title>
                        <Step.Description>Digite o endereço para entrega</Step.Description>
                    </Step.Content>
                    </Step>

                    <Step active={stepPage === 3 ? true : false} disabled={stepPage === 3 ? false : true}>
                    <Icon name='payment' />
                    <Step.Content>
                        <Step.Title>Pagamento</Step.Title>
                        <Step.Description>Digite os dados para pagamento</Step.Description>
                    </Step.Content>
                    </Step>
                    
                    <Step active={stepPage === 4 ? true : false} disabled={stepPage === 4 ? false : true}>
                    <Icon name='file alternate outline' />
                    <Step.Content>
                        <Step.Title>Pedido</Step.Title>
                        <Step.Description>Revise e confirme o pedido</Step.Description>
                    </Step.Content>
                    </Step>
                </Step.Group>
            </Grid.Column>
        </Grid.Row>
    );

    const stepCheckout = () => (
        <Grid className="content-inner">   
            { products.length > 0 && stepComponent() }
            <Grid.Row>                        
                <Grid.Column width={10}>
                    { products.length > 0 ?    
                        <>                    
                        <Table basic='very'>
                            <Table.Header>
                            <Table.Row>
                                <Table.HeaderCell></Table.HeaderCell>
                                <Table.HeaderCell></Table.HeaderCell>
                                <Table.HeaderCell>Quantidade</Table.HeaderCell>
                                <Table.HeaderCell>Preço</Table.HeaderCell>
                                <Table.HeaderCell></Table.HeaderCell>
                            </Table.Row>
                            </Table.Header>

                            <Table.Body>
                                { products &&
                                    products.map( item => 
                                        <Table.Row>
                                            <Table.Cell style={{ textAlign: 'center'}}><img src={item['image_thumb']} alt="" height="76" /></Table.Cell>
                                            <Table.Cell>{item.name}</Table.Cell>
                                            <Table.Cell>1</Table.Cell>
                                            <Table.Cell>{`R$ ${item.price}`}</Table.Cell>
                                            <Table.Cell><Button circular icon="trash alternate outline" onClick={() => handleRemove(item.id)} /></Table.Cell>
                                        </Table.Row>  
                                    )
                                }
                            </Table.Body>
                        </Table>
                        
                        <Divider />

                        <span>Calcule frete e prazo</span>                  
                        <Input placeholder='Digite o cep' maxlength="8" style={{ margin: '0 10px' }} value={cep} onChange={ e => setCep(e.target.value) } />
                        <Button content='OK' color="blue" onClick={() => cepValidate()} />

                        {cepMessage && <Message visible warning>Ops, ocorreu um erro inesperado. Tente novamente.</Message> }

                        </>

                        :

                        <Message visible>Sua sacola está vazia</Message>
                    }
                </Grid.Column> 
                {products.length > 0 && 
                
                <Grid.Column width={6}>
                    <Order>
                        <Header as='h3'>Resumo do pedido</Header>
                        <List verticalAlign='middle'>
                            <List.Item>
                                <List.Content floated='right'><strong>{`R$ ${totalSum}`}</strong></List.Content>
                                <List.Content>{`${totalQuantity} produtos`}</List.Content>
                            </List.Item>

                            { orderInfo &&
                                <>                                    
                                    <List.Item>
                                        <List.Content floated='right'><strong>{`R$ ${orderInfo.value}`}</strong></List.Content>
                                        <List.Content>Frete</List.Content>
                                    </List.Item>
                                    <List.Item>
                                    <List.Content>Entrega em {orderInfo.days} úteis</List.Content>
                                    </List.Item>                                       

                                    <Divider />

                                    <List.Item>
                                        <List.Content floated='right'><strong>{`R$ ${sumTotal(totalSum, orderInfo.value).toFixed(2)}`}</strong></List.Content>
                                        <List.Content><strong>TOTAL</strong></List.Content>
                                    </List.Item>

                                    <Divider />

                                    <Button fluid color="yellow" onClick={() => { 
                                        if(isLogged){ setStepPage(2) } else { setCache('goBack', 'sacola'); history.push('/login') };  
                                    } }>Fechar pedido</Button>
                                </>
                            }                                   
                        </List>
                    </Order>
                </Grid.Column> 
                }
            </Grid.Row>        
        </Grid>
    );       

    const stepAddress = () => (
        <Grid className="content-inner">
            { products.length > 0 && stepComponent() }
            <Grid.Row>
                <Grid.Column width={16}>
                    <Form>
                        <Form.Group>
                            <Form.Input fluid label='Destinatário' name='recipient' value={address.recipient} onChange={handleChangeAddress} width={16} />
                        </Form.Group>
                        <Form.Group>                        
                            <Form.Input fluid label='Endereço' name='street-name' value={address['street-name']} onChange={handleChangeAddress} width={8} />
                            <Form.Input fluid label='Número' name='number' value={address.number} onChange={handleChangeAddress} width={2} />
                            <Form.Input fluid label='Complemento' name='complement' value={address.complement} onChange={handleChangeAddress} width={6} />
                        </Form.Group>
                        <Form.Group>                        
                            <Form.Input fluid label='CEP' name="cep" value={address.cep} onChange={handleChangeAddress} width={4} />
                            <Form.Input fluid label='Bairro' name="neighborhood" value={address.neighborhood} onChange={handleChangeAddress} width={4} />
                            <Form.Input fluid label='Cidade' name="city" value={address.city} onChange={handleChangeAddress} width={4} />
                            <Form.Input fluid label='Celular' name="phone" value={address.phone} onChange={handleChangeAddress} width={4} />                        
                        </Form.Group>
                        <Form.Group>                        
                            <Form.Button onClick={() => setStepPage(1) }>Voltar</Form.Button>
                            <Form.Button color="blue" onClick={() => setStepPage(3) }>Salvar</Form.Button>                      
                        </Form.Group>                        
                    </Form>
                </Grid.Column>
            </Grid.Row>
        </Grid>
    );

    const stepPayment = () => (
        <Grid className="content-inner">
            { products.length > 0 && stepComponent() }
            <Grid.Row>
                <Grid.Column width={16}>
                    <Form>
                        <Form.Group>
                            <Form.Input fluid label='Nº do cartão' name='card-number' value={card['card-number']} onChange={handleChangeCard} width={16} />
                        </Form.Group>
                        <Form.Group>                        
                            <Form.Input fluid label='Nome no cartão' name='main-name' value={card['main-name']} onChange={handleChangeCard} width={9} />
                            <Form.Input fluid label='Data de vencimento' name='due-date' value={card['due-date']} onChange={handleChangeCard} width={4} />
                            <Form.Input fluid label='Cód. de Segurança' name='safe-code' value={card['safe-code']} onChange={handleChangeCard} width={3} />
                        </Form.Group>
                        <Form.Group>                        
                            <Form.Button onClick={() => setStepPage(2) }>Voltar</Form.Button>
                            <Form.Button color="blue" onClick={() => setStepPage(4) }>Salvar</Form.Button>                      
                        </Form.Group>                        
                    </Form>
                </Grid.Column>
            </Grid.Row>
        </Grid>
    );

    const stepResume = () => (
        <Grid className="content-inner">
            { products.length > 0 && stepComponent() }
            <Grid.Row>
                <Grid.Column width={10}>
                    <Header as='h3'>Endereço de entrega</Header>
                    <p><strong>Destinatário:</strong> {address.recipient}</p>
                    <p><strong>Endereço:</strong> {`${address['street-name']}, ${address['number']}`} <br /> {`${address['complement']} - ${address['neighborhood']}`} <br /> {`${address['cep']} - ${address['city']}`}</p>
                    <p><strong>Fone: </strong> {address['phone']}</p>

                    <Table basic='very'>
                        <Table.Header>
                        <Table.Row>
                            <Table.HeaderCell></Table.HeaderCell>
                            <Table.HeaderCell></Table.HeaderCell>
                            <Table.HeaderCell>Quantidade</Table.HeaderCell>
                            <Table.HeaderCell>Preço</Table.HeaderCell>
                            <Table.HeaderCell></Table.HeaderCell>
                        </Table.Row>
                        </Table.Header>

                        <Table.Body>
                            { products &&
                                products.map( item => 
                                    <Table.Row>
                                        <Table.Cell style={{ textAlign: 'center'}}><img src={item['image_thumb']} alt="" height="76" /></Table.Cell>
                                        <Table.Cell>{item.name}</Table.Cell>
                                        <Table.Cell>1</Table.Cell>
                                        <Table.Cell>{`R$ ${item.price}`}</Table.Cell>
                                        <Table.Cell><Button circular icon="trash alternate outline" onClick={() => handleRemove(item.id)} /></Table.Cell>
                                    </Table.Row>  
                                )
                            }
                        </Table.Body>
                    </Table>

                    <Divider />

                    <Button onClick={() => setStepPage(3) }>Voltar</Button>

                </Grid.Column>
                <Grid.Column width={6}>
                    <Order>
                        <Header as='h3'>Resumo do pedido</Header>
                        <List verticalAlign='middle'>
                            <List.Item>
                                <List.Content floated='right'><strong>{`R$ ${totalSum}`}</strong></List.Content>
                                <List.Content>{`${totalQuantity} produtos`}</List.Content>
                            </List.Item>

                            { orderInfo &&
                                <>                                    
                                    <List.Item>
                                        <List.Content floated='right'><strong>{`R$ ${orderInfo.value}`}</strong></List.Content>
                                        <List.Content>Frete</List.Content>
                                    </List.Item>
                                    <List.Item>
                                    <List.Content>Entrega em {orderInfo.days} úteis</List.Content>
                                    </List.Item>                                       

                                    <Divider />

                                    <List.Item>
                                        <List.Content floated='right'><strong>{`R$ ${sumTotal(totalSum, orderInfo.value).toFixed(2)}`}</strong></List.Content>
                                        <List.Content><strong>TOTAL</strong></List.Content>
                                    </List.Item>

                                    <Divider />

                                    <Button fluid color="green" onClick={() => handleSubmit() }>Finalizar pedido</Button>
                                </>
                            }                                   
                        </List>
                    </Order>
                </Grid.Column> 
            </Grid.Row>
        </Grid>
    );

    return (
        <Page>
            <Menu page="cart" itemsQuantity={checkoutItems} />
            <Container>
                { stepPage === 1 && stepCheckout() }   
                { stepPage === 2 && stepAddress() }   
                { stepPage === 3 && stepPayment() }   
                { stepPage === 4 && stepResume() }             
            </Container>
        </Page>
    )
};

export default Cart;

const Page = styled.section`
    .content-inner {
        margin-top: 20px;
    }
    .table th {
        border-top: none;
    }
`

const Order = styled.div`
    background-color: #f8f8f8;
    padding: 15px;
` 
