import React from 'react';

export const MessageBox = (props) => {
  const restartLink = (
    <p className='text-centered'>
      <a onClick={props.getNext}>Start from beginning</a>
    </p>
  );

  return (
    <div>
      <p className='text-centered'>{props.message}</p>
      {props.details === null && restartLink}
    </div>
  );
};