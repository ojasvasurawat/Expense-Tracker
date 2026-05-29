import * as WebBrowser from "expo-web-browser";
import * as Google from "expo-auth-session/providers/google";
import * as AuthSession from "expo-auth-session";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { GOOGLE_ANDROID_CLIENT_ID, GOOGLE_WEB_CLIENT_ID } from "@env";
import React from "react";
import { TouchableOpacity, Text, View } from "react-native";
import axios from 'axios';
import GoogleIcon from "./GoogleIcon";

WebBrowser.maybeCompleteAuthSession();
interface UserInfo {

} 
interface setUserInfoprop{
    setUserInfo: React.Dispatch<React.SetStateAction<UserInfo | null>>,
}

export default function GoogleAuthButton({setUserInfo} : setUserInfoprop) {
    const redirectUri = AuthSession.makeRedirectUri({ scheme: "frontend" })
    console.log("red ", redirectUri)
    const config = {
        androidClientId: GOOGLE_ANDROID_CLIENT_ID,
        webClientId: GOOGLE_WEB_CLIENT_ID,
        redirectUri
    }
    const [request, response, promptAsync] = Google.useAuthRequest(config);

    const getUserInfo = async (token: any) => {
        if (!token) return;
        try {
            const response = await axios.get('https://www.googleapis.com/userinfo/v2/me', {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            })
            const user = await response.data;
            console.log("res ", user);
            await AsyncStorage.setItem("user", JSON.stringify(user));
            setUserInfo(user);

        } catch (e) {
            console.log('google signin failed ', e);
        }
    }
    const signinGoogle = async () => {
        try {
            const userJson = await AsyncStorage.getItem("user");
            if (userJson) {
                setUserInfo(JSON.parse(userJson));
            }
            else if (response?.type === "success") {
                getUserInfo(response.authentication?.accessToken);
            }
        } catch (error) {
            console.error(error)
        }
    }
    React.useEffect(() => {
        signinGoogle();
    }, [response]);
    console.log("req: ", request);
    return (
        <TouchableOpacity onPress={() => promptAsync()} className="text-center border-2 p-2 rounded-xl mb-5 border-gray-100">
            <View className="flex-row gap-3">
                <GoogleIcon/>
                <Text className="text-gray-600 text-sm">Sign in with google</Text>
            </View>
        </TouchableOpacity>
    )
}