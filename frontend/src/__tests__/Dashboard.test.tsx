import React from 'react';
import renderer from 'react-test-renderer';
import { Dashboard } from '../components/Dashboard';

test('snapshot for empty-data scenario', () => {
  const tree = renderer.create(<Dashboard data={null} />).toJSON();
  expect(tree).toMatchSnapshot();
});
