import React, { useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";

export default function Reflection() {
  const { articleId } = useParams();
  const [content, setContent] = useState("");
  const [message, setMessage] = useState("");

  const submitReflection = () => {
    axios.post(`/api/reflect/${articleId}`, { content })
      .then(res => setMessage(res.data.message))
      .catch(err => setMessage("Failed to save reflection"));
  };

  return (
    <div>
      <h2>Write a Reflection</h2>
      <textarea
        rows={8}
        value={content}
        onChange={(e) => setContent(e.target.value)}
        placeholder="Write your thoughts here..."
      />
      <br />
      <button onClick={submitReflection}>Save</button>
      <p>{message}</p>
    </div>
  );
}