import React from 'react';
import renderer from 'react-test-renderer';
import { ErrorBoundary } from '../components/ErrorBoundary';

function Boom() {
  throw new Error('boom');
}

test('Error boundary catches unexpected exceptions', () => {
  const tree = renderer.create(<ErrorBoundary><Boom /></ErrorBoundary>).toJSON();
  expect(tree).toMatchSnapshot();
});
