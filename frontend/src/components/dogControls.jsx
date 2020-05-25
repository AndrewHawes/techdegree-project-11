import React, { memo } from 'react';

import { ReactComponent as LikeButton } from '../static/icons/liked.svg'
import { ReactComponent as DislikeButton } from '../static/icons/disliked.svg';
import { ReactComponent as UndecideButton } from '../static/icons/undecided.svg';
import { ReactComponent as PrevButton } from '../static/icons/prev.svg';
import { ReactComponent as NextButton } from '../static/icons/next.svg';

import styled from 'styled-components';

const P = styled.p`
  text-align: center; 
`;

const buttonProps = {width: '45px', height: '45px', className: 'icon-button'};

function DogControls(props) {
  const statusProps = (status) => (
    {...buttonProps, onClick: () => props.changeStatus(status), key: status}
  );

  const like = <LikeButton {...statusProps('liked')} />;
  const dislike = <DislikeButton {...statusProps('disliked')} />;
  const undecide = <UndecideButton {...statusProps('undecided')} />;
  const prev = <PrevButton {...buttonProps} onClick={props.getPrev} key='prev' />;
  const next = <NextButton {...buttonProps} onClick={props.getNext} key='next' />;

  const filters = {
    liked: [prev, dislike, undecide, next],
    disliked: [prev, like, undecide, next],
    undecided: [prev, dislike, like, next],
  };

  return (
    <P>
      {filters[props.filter]}
    </P>
  );
}

function arePropsEqual(prevProps, nextProps) {
  return prevProps.filter === nextProps.filter;
}

export default memo(DogControls, arePropsEqual);