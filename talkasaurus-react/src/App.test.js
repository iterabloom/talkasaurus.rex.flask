import { render, screen } from '@testing-library/react';
import App from './App';

test('renders audio recorder', () => {
  render(<App />);
  const linkElement = screen.getByText(/Start Recording/i); // assuming there's a "Start Recording" button
  expect(linkElement).toBeInTheDocument();
});

// TODO: Implement more specific tests