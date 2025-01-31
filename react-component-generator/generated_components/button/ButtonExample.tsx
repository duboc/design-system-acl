import React from 'react';
import { Button } from './Button';
const ButtonExample: React.FC = () => (
  <div>
    <Button variant="primary" size="small">Small Primary</Button>
    <Button variant="primary" size="medium">Medium Primary</Button>
    <Button variant="primary" size="large">Large Primary</Button>
    <br />
    <Button variant="secondary" size="small">Small Secondary</Button>
    <Button variant="secondary" size="medium">Medium Secondary</Button>
    <Button variant="secondary" size="large">Large Secondary</Button>
  </div>
);
export default ButtonExample;