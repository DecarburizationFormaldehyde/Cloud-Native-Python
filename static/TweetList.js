import React from 'react';

export default class TweetList extends React.Component {
    render(){
        const { tweets } = this.props;
        return(
            <div>
                <ul className="collection">
                    {tweets && tweets.map((tweet) => (
                        <li key={tweet.id} className="collection-item avatar">
                            <i className="material-icons circle red">play_arrow</i>
                            <span className="title">{tweet.name}</span>
                            <p>{tweet.body}</p>
                            <p>{tweet.timestamp || 'Just now'}</p>
                        </li>
                    ))}
                </ul>
            </div>
        )
    }

}