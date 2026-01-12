import React from 'react';
import moment from 'moment';

const TweetTemplate = ({ tweetedby, body, timestamp, updatedate }) => {
  return (
    <li className="collection-item avatar">
      <i className="material-icons circle red">play_arrow</i>
      <span className="title">{tweetedby}</span>
      <p>{body}</p>
      <p>{updatedate || moment(timestamp).fromNow()}</p>
    </li>
  );
};

export default TweetTemplate;