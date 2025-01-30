import React, { useState } from 'react';
import Button from './components/Button';
import List from './components/List';
import Dialog from './components/Dialog';
import Form from './components/Form';
import './App.css';

function App() {
  const [openDialog, setOpenDialog] = useState<string | null>(null);

  const sampleListItems = [
    'First Item',
    'Second Item',
    'Third Item',
    'Fourth Item',
  ];

  const handleCloseDialog = () => setOpenDialog(null);

  return (
    <div className="app">
      <h1>Design System Components</h1>
      
      <section className="component-section">
        <h2>Button Examples</h2>
        <div className="section-content">
          <div className="button-section">
            <h3>Primary Buttons</h3>
            <div className="button-row">
              <Button size="small">Small</Button>
              <Button size="medium">Medium</Button>
              <Button size="large">Large</Button>
            </div>
          </div>

          <div className="button-section">
            <h3>Secondary Buttons</h3>
            <div className="button-row">
              <Button variant="secondary" size="small">Small</Button>
              <Button variant="secondary" size="medium">Medium</Button>
              <Button variant="secondary" size="large">Large</Button>
            </div>
          </div>

          <div className="button-section">
            <h3>Outline Buttons</h3>
            <div className="button-row">
              <Button variant="outline" size="small">Small</Button>
              <Button variant="outline" size="medium">Medium</Button>
              <Button variant="outline" size="large">Large</Button>
            </div>
          </div>

          <div className="button-section">
            <h3>Disabled State</h3>
            <div className="button-row">
              <Button disabled>Primary</Button>
              <Button variant="secondary" disabled>Secondary</Button>
              <Button variant="outline" disabled>Outline</Button>
            </div>
          </div>
        </div>
      </section>

      <section className="component-section">
        <h2>List Examples</h2>
        <div className="section-content">
          <div className="list-section">
            <h3>Default List</h3>
            <List>
              {sampleListItems.map((item) => item)}
            </List>
          </div>

          <div className="list-section">
            <h3>Bordered List</h3>
            <List variant="bordered">
              {sampleListItems.map((item) => item)}
            </List>
          </div>

          <div className="list-section">
            <h3>Card List</h3>
            <List variant="card">
              {sampleListItems.map((item) => item)}
            </List>
          </div>

          <div className="list-section">
            <h3>Different Sizes</h3>
            <div className="list-row">
              <div className="list-column">
                <h4>Small</h4>
                <List variant="card" size="small">
                  {sampleListItems.slice(0, 2).map((item) => item)}
                </List>
              </div>
              <div className="list-column">
                <h4>Medium</h4>
                <List variant="card" size="medium">
                  {sampleListItems.slice(0, 2).map((item) => item)}
                </List>
              </div>
              <div className="list-column">
                <h4>Large</h4>
                <List variant="card" size="large">
                  {sampleListItems.slice(0, 2).map((item) => item)}
                </List>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="component-section">
        <h2>Dialog Examples</h2>
        <div className="section-content">
          <div className="button-row">
            <Button onClick={() => setOpenDialog('default')}>Open Default Dialog</Button>
            <Button onClick={() => setOpenDialog('info')} variant="outline">Open Info Dialog</Button>
            <Button onClick={() => setOpenDialog('warning')} variant="secondary">Open Warning Dialog</Button>
            <Button onClick={() => setOpenDialog('error')} variant="outline">Open Error Dialog</Button>
          </div>

          <Dialog
            isOpen={openDialog === 'default'}
            onClose={handleCloseDialog}
            title="Default Dialog"
            actions={
              <>
                <Button variant="outline" onClick={handleCloseDialog}>Cancel</Button>
                <Button onClick={handleCloseDialog}>Confirm</Button>
              </>
            }
          >
            <p>This is a default dialog with standard actions.</p>
          </Dialog>

          <Dialog
            isOpen={openDialog === 'info'}
            onClose={handleCloseDialog}
            title="Information"
            variant="info"
            size="small"
            actions={
              <Button onClick={handleCloseDialog}>Got it</Button>
            }
          >
            <p>This is an informational message in a small dialog.</p>
          </Dialog>

          <Dialog
            isOpen={openDialog === 'warning'}
            onClose={handleCloseDialog}
            title="Warning"
            variant="warning"
            actions={
              <>
                <Button variant="outline" onClick={handleCloseDialog}>Cancel</Button>
                <Button onClick={handleCloseDialog}>Proceed</Button>
              </>
            }
          >
            <p>This action might have consequences. Are you sure you want to proceed?</p>
          </Dialog>

          <Dialog
            isOpen={openDialog === 'error'}
            onClose={handleCloseDialog}
            title="Error"
            variant="error"
            size="large"
            actions={
              <Button variant="outline" onClick={handleCloseDialog}>Close</Button>
            }
          >
            <div>
              <p>An error occurred while processing your request.</p>
              <List variant="bordered" size="small">
                <li>Error detail 1</li>
                <li>Error detail 2</li>
                <li>Error detail 3</li>
              </List>
            </div>
          </Dialog>
        </div>
      </section>

      <section className="component-section">
        <h2>Form Examples</h2>
        <div className="section-content">
          <div className="form-section">
            <h3>Primary Form</h3>
            <Form onSubmit={(e: React.FormEvent<HTMLFormElement>) => e.preventDefault()}>
              <input type="text" placeholder="Enter your name" />
              <Button type="submit">Submit</Button>
            </Form>
          </div>

          <div className="form-section">
            <h3>Secondary Form</h3>
            <Form variant="secondary" size="large" onSubmit={(e: React.FormEvent<HTMLFormElement>) => e.preventDefault()}>
              <input type="email" placeholder="Enter your email" />
              <Button variant="secondary" type="submit">Subscribe</Button>
            </Form>
          </div>
        </div>
      </section>
    </div>
  );
}

export default App; 