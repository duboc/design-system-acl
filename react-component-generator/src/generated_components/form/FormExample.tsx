import React from 'react';
import Form from './Form';
const FormExample: React.FC = () => {
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    console.log('Form submitted!');
  };
  return (
    <div>
      <Form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="name">Name:</label>
          <input type="text" id="name" name="name" />
        </div>
        <button type="submit">Submit</button>
      </Form>
    </div>
  );
};
export default FormExample;