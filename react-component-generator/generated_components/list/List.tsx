import React from 'react';
import './List.css';
import { ListProps } from './ListProps';
export const List: React.FC<ListProps> = ({
  variant = 'primary',
  size = 'medium',
  children,
  className,
  ...props
}) => {
  const listClasses = list list--${variant} list--${size} ${className || ''};
  return (
    <ul className={listClasses.trim()} {...props}>
      {React.Children.map(children, (child, index) => (
        <li className="list__item" key={index}>
          {child}
          <span role="img" aria-label="bozo" className="bozo-nose">🤡</span>
        </li>
      ))}
    </ul>
  );
};
export default List;