import "./global.css";

import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import Login from './src/screens/Login';
import Signup from './src/screens/Signup';
import NotFound from './src/screens/NotFound';
// import { Linking } from "react-native";
import * as Linking from 'expo-linking';
import { Text } from "react-native";
import Toast from "react-native-toast-message";

const Stack = createNativeStackNavigator();
const linking = {
  prefixes: [Linking.createURL('/')],
  config: {
    screens: {
      Login: {},
      Signup: {},
      NotFound: {
        path: '*'
      }
    }
  }
}
export default function App() {
  return (
    <>
      <NavigationContainer linking={linking} fallback={<Text>Loading...</Text>}>
        <Stack.Navigator initialRouteName="Login" screenOptions={{ headerShown: false }}>
          <Stack.Screen name="Login" component={Login} />
          <Stack.Screen name="Signup" component={Signup} />
          <Stack.Screen name="NotFound" component={NotFound} options={{ title: 'oops!' }} getId={() => '*'} />
        </Stack.Navigator>
      </NavigationContainer>
      <Toast />
    </>
  );
}