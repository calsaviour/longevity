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
    const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (status !== 'granted') {
      alert('Sorry, we need camera roll permissions to make this work!');
      return;
    }
  
    let result = await ImagePicker.launchImageLibraryAsync({
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
      name: 'upload.jpg', 
      type: 'image/jpg',
    });

    formData.append('age', age);

    console.log("contacting server");
    let response = await fetch('http://192.168.0.24:5002/predict', {
      method: 'POST',
      body: formData
    });

    let result = await response.json();
    this.setState({ result: result.life_expectancy });
    console.log(result)
  };

  render() {
    console.log("rendering");
    let { image, result, age } = this.state;

    return (
      <View style>
          <TextInput 
            style={{height: 30, borderColor: 'gray', borderRadius: 10, borderWidth: 0.5, 
	           paddingHorizontal: 20}}
            onChangeText={text => this.setState({age: text})}
            value={age}
            placeholder="Enter your age"
            keyboardType="numeric"
          />
	  <View style={{marginTop: '10%', align: 'center'}}>
          {image && <Image source={{ uri: image }} style={{ width: 200, height: 200 }} />}
	  </View>
          {result && <Result lifeExpectancy={result} />}
	  <View style={{marginTop: '9%'}}>
          <Button title="Upload Picture of a person" onPress={this.pickImage} />
	  </View>
      </View>
    );
  }
}
