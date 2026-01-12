import React from 'react';
import { createRoot } from 'react-dom/client';
import { Provider } from 'react-redux';
import store from './store';
import Main from './components/Main';
import $ from 'jquery';

// 使用Provider包裹整个应用
const documentReady = () => {
     const container = document.getElementById('react');
     const root = createRoot(container);
     root.render(
         <Provider store={store}>
             <Main />
         </Provider>
     );
};

$(documentReady);
