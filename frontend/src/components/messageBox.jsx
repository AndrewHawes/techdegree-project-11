import React from 'react';
import styled from "styled-components";

const Link = styled.button``;

export const MessageBox = (props) => {
  const navMsg = props.details === null ? "Start from beginning" : "Next dog"

  const navLink = (
    <p className='text-centered'>
      <Link as="a" onClick={props.getNext}>{navMsg}</Link>
    </p>
  );

  return (
    <div>
      <p className='text-centered'>{props.message}</p>
      {navLink}
    </div>
  );
};