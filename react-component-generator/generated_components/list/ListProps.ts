import React from 'react';
interface ListProps extends React.HTMLAttributes<HTMLUListElement> {
  variant?: 'primary' | 'secondary';
  size?: 'small' | 'medium' | 'large';
  children: React.ReactNode;
}
export { ListProps };