import React from 'react';
import {render} from 'react-dom';
import { BrowserRouter, Switch, Route } from 'react-router-dom'
import * as serviceWorker from './serviceWorker';
import 'bootstrap/dist/css/bootstrap.min.css';

import Main from './pages/main';

render((
    <BrowserRouter>
        <Switch>
            <Route path="/" exact={true} component={Main} />
        </Switch>
    </BrowserRouter>
    ), window.document.getElementById('root'));