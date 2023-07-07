import React from 'react';
import { Button, Image, View, TextInput } from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import Result from './Result';


export default class Camera extends React.Component {
  state = {
    image: null,
    result: null,
    age: '',
  }

 
  pickImage = async () => {
      console.log("waiting for image");
      const { status } = await ImagePicker.requestCameraRollPermissionsAsync();
      if (status !== 'granted') {
          alert('Sorry, we need camera roll permissions to make this work!');
          return;
      }
      
      const { status: cameraStatus } = await ImagePicker.requestCameraPermissionsAsync();
      if (cameraStatus !== 'granted') {
          alert('Sorry, we need camera permissions to make this work!');
          return;
      }
  
      let result = await ImagePicker.launchCameraAsync({
          mediaTypes: ImagePicker.MediaTypeOptions.All,
          quality: 1,
      });
  
      if (!result.cancelled) {
          this.setState({ image: result.uri });
          this.predictLifeExpectancy(result.uri, this.state.age);
      }
  };

  predictLifeExpectancy = async (imageUri, age) => {
    console.log("predicting LEX");
    let formData = new FormData();

    formData.append('file', {
      uri: Platform.OS === 'android' ? imageUri : imageUri.replace('file://', ''), 
      name: 'selfie.jpg', 
      type: 'image/jpg',
    });

    // append age to the form data
    formData.append('age', age);

    let response = await fetch('http://192.168.0.21:5000/predict', {
      method: 'POST',
      body: formData
    });

    let result = await response.json();
    this.setState({ result: result.life_expectancy });
  };

  render() {
    console.log("rendering");
    let { image, result } = this.state;

    return (
      <View style={{flex: 1, justifyContent: 'center', alignItems: 'center'}}>
        <View>
          <Button title="Take a Hot Selfie" onPress={this.pickImage} />
          {image && <Image source={{ uri: image }} style={{ width: 200, height: 200 }} />}
          {result && <Result lifeExpectancy={result} />}
        </View>
      </View>
    );
 }
}

