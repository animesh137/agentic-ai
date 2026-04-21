import React from 'react';
import { render, screen } from '@testing-library/react';
import { Dashboard } from '../components/Dashboard';

test('Graceful empty state rendered when dataset is null/empty', () => {
  render(<Dashboard data={null} />);
  expect(screen.getByTestId('empty-state')).toBeTruthy();
});
