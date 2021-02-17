import React from 'react';
import styled from 'styled-components';
import Header from '../../components/header';
import Image from '../../assets/images/bannerHome.jpg';

const Home = () => {

    return (
        <>
            <Header />
            <Banner>
                <img src={Image} alt="" />          
            </Banner>
            <Categories />
        </>
    )
}

export default Home;

const Banner = styled.section` 

    img {
        background-size: cover;
        height: 80vh;
    }    
` 

const Categories = styled.section`
    background-color: #a5673f;
    height: 10vh
`