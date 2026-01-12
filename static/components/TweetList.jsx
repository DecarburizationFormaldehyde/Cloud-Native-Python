import React from 'react';
import TweetTemplate from './TweetTemplate';

const TweetList = ({ tweets }) => {
  return (
    <div>
      <ul className="collection">
        {tweets.map(tweet => (
          <TweetTemplate key={tweet.id || tweet._id} {...tweet} />
        ))}
      </ul>
    </div>
  );
};

export default TweetList;