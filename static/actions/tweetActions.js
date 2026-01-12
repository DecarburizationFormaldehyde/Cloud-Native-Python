import {ActionTypes} from "./actionTypes";
import $ from 'jquery';

export const receivedTweets =(tweets) =>({
    type: ActionTypes.RECEVIED_TWEETS,
    payload: tweets
    });

export const receivedTweet =(tweet) =>({
    type: ActionTypes.RECEIVED_TWEET,
    payload: tweet
    });

/**
 * 异步Action Creator - 添加推文
 * 使用redux-thunk中间件处理异步操作
 * @param {string} tweetBody - 推文内容
 * @returns {function} 返回一个接收dispatch函数的函数，用于执行异步操作并分发action
 */
export const addTweet = (tweetBody, username) =>{
    return(dispatch)=>{
        return $.ajax({
            url: '/api/v2/tweets',
            contentType: 'application/json',
            type: 'POST',
            data: JSON.stringify({
                username: username || "Anonymous",
                body:tweetBody
            }),
            // 成功回调：处理服务器返回的推文数据，并分发receivedTweet action
            success: (data) => {
                dispatch(receivedTweet({
                    ...data,
                    tweetedby: username || "Anonymous",
                    timestamp: Date.now()
                    }));
            },
            // 错误回调：在控制台输出错误信息
            error: (xhr, status, error) => {
                console.log(error);
            }
        })
    }
}

export const fetchTweets = () =>{
    return(dispatch)=>{
        $.getJSON("/api/v2/tweets", (tweetModels)=>{
            // 确保数据结构正确
            const tweetsData = tweetModels && tweetModels.tweets_list ? tweetModels.tweets_list : [];
            console.log('Fetched tweets:', tweetsData); // 调试日志
            dispatch(receivedTweets(tweetsData));
        }).fail((xhr, status, error) => {
            console.error('Failed to fetch tweets:', error);
        });
    }
}
