import React from 'react';
import Button from './Button';
const ButtonExample: React.FC = () => (
  <div>
    <Button variant="primary" size="small">Small Primary</Button>
    <Button variant="secondary" size="medium">Medium Secondary</Button>
    <Button variant="primary" size="large">Large Primary</Button>
  </div>
);
export default ButtonExample;