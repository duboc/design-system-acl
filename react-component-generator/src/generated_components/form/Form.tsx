import React from 'react';
import './Form.css';
import { FormProps } from './FormProps';
const Form: React.FC<FormProps> = ({ children, variant = 'primary', size = 'medium', onSubmit }) => {
  const formClassName = form form--${variant} form--${size};
  return (
    <form className={formClassName} onSubmit={onSubmit}>
      {children}
    </form>
  );
};
export default Form;