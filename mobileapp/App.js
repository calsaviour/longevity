import React, { useEffect, useState } from 'react';
import { View, StyleSheet } from 'react-native';
import Camera from './Camera';
import TypingAnimation from './TypingAnimation';

export default function App() {
  return (
    <View>  
     <View style={{marginTop: '22%', alignItems: 'center'}}>
   	<TypingAnimation text="Predict your life expectancy." />
     </View>
    <View style={{marginTop: '15%', alignItems: 'center'}}>
	<Camera/>
    </View>
    </View>
  );
}

