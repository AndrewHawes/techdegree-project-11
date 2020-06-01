import React from 'react';
import styled from "styled-components";

const Link = styled.button``;

export const MessageBox = (props) => {
  const restartLink = (
    <p className='text-centered'>
      <Link as="a" onClick={props.getNext}>Start from beginning</Link>
    </p>
  );

  return (
    <div>
      <p className='text-centered'>{props.message}</p>
      {props.details === null && restartLink}
    </div>
  );
};