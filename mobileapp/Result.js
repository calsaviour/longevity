import React from 'react';
import { Text } from 'react-native';

export default class Result extends React.Component {
  render() {
    return (
      <Text>Your predicted life expectancy is {this.props.lifeExpectancy} years.</Text>
    );
  }
}

