import React from 'react';
import { List } from './List';
const ListExample: React.FC = () => {
  return (
    <div>
      <List variant="primary" size="large">
        <p>Item 1</p>
        <p>Item 2</p>
      </List>
      <br />
      <List variant="secondary" size="small">
        <p>Item 3</p>
        <p>Item 4</p>
      </List>
    </div>
  );
};
export default ListExample;