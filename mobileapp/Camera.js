import React from 'react';
import { Button, Image } from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import Result from './Result';

export default class Camera extends React.Component {
  state = {
    image: null,
    result: null,
  }

  pickImage = async () => {
    let result = await ImagePicker.launchCameraAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.All,
      quality: 1,
    });

    if (!result.cancelled) {
      this.setState({ image: result.uri });
      this.predictLifeExpectancy(result.uri);
    }
  };

  predictLifeExpectancy = async (imageUri) => {
    let formData = new FormData();
    formData.append('file', {
      uri: imageUri,
      name: 'selfie.jpg',
      type: 'image/jpg'
    });

    let response = await fetch('http://<your server URL>/predict', {
      method: 'POST',
      body: formData
    });

    let result = await response.json();
    this.setState({ result: result.life_expectancy });
  };

  render() {
    let { image, result } = this.state;

    return (
      <View>
        <Button title="Take a Selfie" onPress={this.pickImage} />
        {image && <Image source={{ uri: image }} style={{ width: 200, height: 200 }} />}
        {result && <Result lifeExpectancy={result} />}
      </View>
    );
  }
}
