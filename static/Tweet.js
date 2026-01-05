import React, { useState, useRef } from 'react'

export default function Tweet({ sendTweet }){
    const [tweetText, setTweetText]=useState('');
    const textAreaRef = useRef(null);

    const handleTweet=(e)=>{
        e.preventDefault(); // 阻止表单默认提交行为
        if (sendTweet && typeof sendTweet === 'function' && tweetText.trim()) {
            sendTweet(tweetText);
            setTweetText('');
        }
        console.log(tweetText);
    }

        return(
            <div className="row">
            <form onSubmit={handleTweet} className="input-field">
                <div>
                    <textarea
                        ref={textAreaRef}
                        value={tweetText}
                        onChange={(e)=>setTweetText(e.target.value)}
                        className={"materialize-textarea"}
                    />

                    <label >How you doing?</label>
                        <button type="submit" className="btn waves-effect waves-light right">Tweet now <i className="material-icons right">send</i></button>
                </div>
            </form>
            </div>
    );

}