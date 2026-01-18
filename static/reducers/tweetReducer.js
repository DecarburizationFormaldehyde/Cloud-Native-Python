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
        case ActionTypes.RECEIVED_TWEETS:
            const processedTweets = action.payload.map(tweet => {
                if(typeof tweet ==='string'){
                    try {
                        // 将Python字典格式转换为JSON格式
                        let processedString = tweet
                            .replace(/'/g, '"')  // 单引号替换为双引号
                            .replace(/ObjectId\(['"]([^'"]+)['"]\)/g, '"$1"');  // 处理ObjectId

                        tweet = JSON.parse(processedString);
                    } catch(error) {
                        console.error('JSON parse error:', error, 'Data:', tweet);
                        // 返回默认格式或原始数据
                        return { text: tweet, timestamp: Date.now() };
                    }
                }
                return {
                    ...tweet,
                    updatedate:moment(tweet.timestamp).fromNow()
                }
            });
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