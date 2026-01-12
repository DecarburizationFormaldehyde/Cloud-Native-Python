import {ActionTypes} from "../actions/actionTypes";
import moment from 'moment';
import {createRef} from "react";

const initialState={
    tweets:[],
    loading:false,
    error:null
};

const tweetReducer =(state=initialState,action)=>{
    switch(action.type){
        case ActionTypes.RECEVIED_TWEETS:
            const processedTweets = action.payload.map(tweet =>({
                ...tweet,
                updatedate:moment(tweet.timestamp).fromNow()
            }));
            return {
                ...state,
                tweets:processedTweets,
                loading:false,
            };
        case ActionTypes.RECEIVED_TWEET:
            const newTweet ={
                ...action.payload,
                updatedate:moment(action.payload.timestamp).fromNow()
            };
            return {
                ...state,
                tweets:[newTweet,...state.tweets],
            }
        case "FETCH_TWEETS_START":
            return {
                ...state,
                loading:true,
                error:null
            }
        case "FETCH_TWEETS_ERROR":
            return{
                ...state,
                loading:false,
                error:action.payload
            }
        default:
            return state;
    }

}

export default tweetReducer;