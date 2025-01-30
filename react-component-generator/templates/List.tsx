import React from 'react';
import './List.css';

interface ListProps extends React.HTMLAttributes<HTMLUListElement> {
  variant?: 'default' | 'bordered' | 'card';
  size?: 'small' | 'medium' | 'large';
  children: React.ReactNode;
}

export const List: React.FC<ListProps> = ({
  variant = 'default',
  size = 'medium',
  children,
  className,
  ...props
}) => {
  const listClasses = `list list--${variant} list--${size} ${className || ''}`;

  return (
    <ul className={listClasses.trim()} {...props}>
      {React.Children.map(children, (child, index) => (
        <li className="list__item">
          {child}
        </li>
      ))}
    </ul>
  );
};

export default List; 