import React from 'react';
import { createRoot } from 'react-dom/client';  // 使用现代的 React DOM API
import { connect } from 'react-redux';
import { fetchTweets, addTweet } from '../actions/tweetActions';
import Tweet from "./Tweet";
import TweetList from "./TweetList";
import $ from 'jquery';

class Main extends React.Component{
    constructor(props) {
        super(props);
        // 初始化状态
        this.state = {currentUser: null};
    }
    
    componentDidMount() {
        this.props.fetchTweets();
        // 获取当前登录的用户信息
        this.getCurrentUser();
    }
    
    getCurrentUser = () => {
        $.get('/api/v1/session-user', (data) => {
            if (data.username) {
                this.setState({currentUser: data.username});
            }
        }).fail((xhr, status, error) => {
            console.log('Failed to get current user:', error);
        });
    }

    render(){
        const {tweets,addTweet,loading}=this.props;
        if (loading) {
            return <div>Loading...</div>;
        }
        
        // 如果尚未获取到当前用户信息，则显示提示信息
        if (!this.state.currentUser) {
            return <div>Please log in first.</div>;
        }
        
        return(
            <div>
                <Tweet sendTweet={addTweet} currentUser={this.state.currentUser}/>
                <TweetList tweets={tweets}/>
            </div>
        );
    }
}

const mapStateToProps = (state) => {
    return{
        tweets:state.tweets.tweets,
        loading:state.tweets.loading,
        error:state.tweets.error
    };
};

const mapDispatchToProps = (dispatch) => {
    return{
        fetchTweets: () => dispatch(fetchTweets()),
        addTweet: (tweetBody, username) => dispatch(addTweet(tweetBody, username))
    };
};

export default connect(mapStateToProps,mapDispatchToProps)(Main);