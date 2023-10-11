using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.IO;


[Serializable]
public class JSONObject
{
    public byte[] screenshotPNG;
}

/**
 * Creates a client, connects to a server, handles communications.
 **/
public class Client_Communication : MonoBehaviour
{
    // The IP of the server to connect to.
    public string serverIP = "127.0.0.1";

    // The port of the server to connect to.
    public int serverPort = 2345;

    // The camera to receive images from.
    public Camera captureCamera;

    // from System.Net.Sockets, to create an instance of the client.
    private TcpClient client;

    // From System.Net.Sockets, to initialize a data stream.
    private NetworkStream stream;

    public string screenshotBase64;


    /**
     * Code that is run as the unity application is started.
     * Initialise the connection to the server.
     */
    private void Start()
    {
        Debug.Log("Connecting to Server!");
        ConnectToServer();
    }

    public string CaptureScreenshot()
    {
        // Capture the screenshot from the specified camera
        RenderTexture renderTexture = new RenderTexture(Screen.width, Screen.height, 24);
        captureCamera.targetTexture = renderTexture;
        Texture2D screenshot = new Texture2D(Screen.width, Screen.height, TextureFormat.RGB24, false);
        captureCamera.Render();
        RenderTexture.active = renderTexture;
        screenshot.ReadPixels(new Rect(0, 0, Screen.width, Screen.height), 0, 0);
        captureCamera.targetTexture = null;
        RenderTexture.active = null;
        Destroy(renderTexture);

        // Convert the screenshot to a byte array
        byte[] screenshotBytes = screenshot.EncodeToPNG();

        var jsonObject = new JSONObject
        {
            screenshotPNG = screenshotBytes
        };

        Debug.Log(screenshotBase64);

        // Convert the JSON object to a JSON string
        string jsonPayloadString = JsonUtility.ToJson(jsonObject);

        Debug.Log(jsonPayloadString);

        return jsonPayloadString;
    }

    /**
     * Attempt to connect to the given server.
     */
    private void ConnectToServer()
    {
        try
        {
            // Initialise a client to connect to the given server ip and port.
            client = new TcpClient(serverIP, serverPort);

            // Retrieve a stream of data to determine whether the client successfully connected to the server.
            stream = client.GetStream();
            Debug.Log("Connected to server.");
        }
        // If the client failed to connect to the server,
        catch (Exception ex)
        {
            // Throw the exception.
            Debug.LogError($"Error: {ex.Message}");
        }

        
    }

    /**
     * Function called every frame, to send messages to the server if the user presses space.
     */
    private void Update()
    {
        // If the user presses space, send a message to the server.
        if (Input.GetKeyDown(KeyCode.Space))
        {
            string screenshot_json = CaptureScreenshot();

            SendMessageToServer(screenshot_json);
        }
    }

    /**
     * Send a message to the server.
     * message = message to be sent.
     */
    private void SendMessageToServer(string message)
    {
        // If no stream is detected, the client is not connected to the server.
        if (stream == null)
        {
            Debug.LogError("Not connected to the server.");
            return;
        }

        // The client is connected to the server.
        try
        {
            // Convert the message to bytes.
            byte[] data = Encoding.ASCII.GetBytes(message);

            // Write the serialized message to the stream.
            stream.Write(data, 0, data.Length);


            // Read the response from the server
            data = new byte[1024];

            // Store the serialized response from the server in a variable.
            int bytesRead = stream.Read(data, 0, data.Length);

            // Retrieve the value of the response.
            string response = Encoding.ASCII.GetString(data, 0, bytesRead);

            // Print the server response.
            Debug.Log($"Server response: {response}");
        }

        // Throw any problems with sending the message to the server.
        catch (Exception ex)
        {
            Debug.LogError($"Error sending message: {ex.Message}");
        }
    }

    /**
     * If the object is being destroyed, cleanly close the client.
     */
    private void OnDestroy()
    {
        if (client != null)
        {
            client.Close();
        }
    }
}
