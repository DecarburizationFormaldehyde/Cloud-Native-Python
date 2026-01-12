import { createStore, applyMiddleware, combineReducers } from 'redux';
import {thunk} from 'redux-thunk';
import tweetReducer from '../reducers/tweetReducer';

// 如果有多个reducer，可以使用combineReducers
const rootReducer = combineReducers({
  tweets: tweetReducer
  // 可以添加其他reducer
});

const store = createStore(
  rootReducer,
  applyMiddleware(thunk)
);

export default store;