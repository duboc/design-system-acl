import React from 'react';
import './Button.css';
import { ButtonProps } from './ButtonProps';
export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'medium',
  children,
  className,
  ...props
}) => {
  const buttonClasses = button button--${variant} button--${size} ${className || ''};
  return (
    <button className={buttonClasses.trim()} {...props}>
      {children}
    </button>
  );
};
export default Button;