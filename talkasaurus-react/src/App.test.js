import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import App from './App';

test('Renders start button', () => {
  const { getByTestId } = render(<App />);
  const startButton = getByTestId('startButton');
  expect(startButton).toBeInTheDocument();
});

test('Start recording when button is clicked', () => {
  const { getByTestId } = render(<App />);
  const startButton = getByTestId('startButton');
  fireEvent.click(startButton);
  expect(startButton.textContent).toBe("Stop Recording");
});