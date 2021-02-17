import React from 'react';
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Home from './pages/home';
import Cafe from './pages/coffee';
import Acessorio from './pages/accessory';
import Promocao from './pages/sale';
import Login from './pages/login';
import User from './pages/user';
import Cart from './pages/cart';
import Purchased from './pages/purchased';
import Confirmed from './pages/confirmed';

const App = () => {
  return (
    <Router>    
      <Switch>
        <Route
          exact
          path="/"
          component={Home}
        />
        <Route
          path="/cafe"
          component={Cafe}
        />
        <Route
          path="/acessorio"
          component={Acessorio}
        />
        <Route
          path="/promocao"
          component={Promocao}
        />
        <Route
          path="/login"
          component={Login}
        />
        <Route
          path="/sacola"
          component={Cart}
        />
        <Route
          path="/pedidos"
          component={Purchased}
        />
        <Route
          path="/user"
          component={User}
        />
        <Route
          path="/confirmed"
          component={Confirmed}
        />
      </Switch>
    </Router>

  );
}

export default App;
