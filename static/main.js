import React from 'react';
import { createRoot } from 'react-dom/client';  // 使用现代的 React DOM API
import Tweet from "./Tweet";
import TweetList from "./TweetList";
import cookie from "react-cookies"

class Main extends React.Component{
    constructor(props) {
        super(props);
        // 初始化状态
        this.state = {
            userId:cookie.load('session'),
            tweets: [
                {
                    id: 1,
                    name: 'guest',
                    body: '"Listen to your heart. It knows all things." - Paulo Coelho #Motivation'
                }
            ],
            isLoading: false
        }
    }
    addTweet(tweet){
        if(tweet == null){  // 只检查 tweet 是否为 null 或 undefined
            return;
        }
        const newTweet = [...this.state.tweets];
        newTweet.unshift({
            id: Date.now(),
            name: 'guest',
            body: tweet
        });
        this.setState({tweets: newTweet})
    }
    render(){
        return(
            <div>
                <Tweet sendTweet={this.addTweet.bind(this)}/>
                <TweetList tweets={this.state.tweets}/>
            </div>
        );
    }
}

// 等待 DOM 加载完成
document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById("react");
    if(container){
        const root = createRoot(container);
        root.render(<Main/>);
    } else {
        console.error("找不到 id 为 'react' 的容器元素");
    }
});

// 如果 DOM 已经加载完成，直接执行
if (document.readyState === 'loading') {
    // DOM 仍在加载中，上面的事件监听器会处理
} else {
    // DOM 已经加载完成，立即执行
    const container = document.getElementById("react");
    if(container){
        const root = createRoot(container);
        root.render(<Main/>);
    } else {
        console.error("找不到 id 为 'react' 的容器元素");
    }
}