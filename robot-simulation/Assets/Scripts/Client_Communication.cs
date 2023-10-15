using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.IO;
   

/**
JSON Schema with attributes to send to the server.
*/
[Serializable]
public class JSONObject
{
    // Screenshot from robot in PNG format represented as bytes.
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

    private RenderTexture renderTexture;
    private Texture2D screenshot;

    /**
     * Code that is run as the unity application is started.
     * Initialise the connection to the server.
     */
    private void Start()
    {
        // Initialise the camera settings to be used in the communication.
        initialize_camera_settings();

        // Attempt to initialise the connection between client and server.
        ConnectToServer();
    }

    /**
    Initialise the camera settings such as capture resolution, number of colour channels, etc.
    */
    private void initialize_camera_settings()
    {
        // Initialise the render texture, with resolution as screen size, number of colour channels = 24
        renderTexture = new RenderTexture(Screen.width, Screen.height, 24);

        // Set the target texture of the camera to the render texture to ensure the correct image settings are captured.
        captureCamera.targetTexture = renderTexture;

        // Initialise a Texture2D to hold the screenshot with the same resolution and colour channels as the render texture, set compression to false.
        screenshot = new Texture2D(Screen.width, Screen.height, TextureFormat.RGB24, false);

    }

    /**
        Capture the screenshot from the specified camera.
        Returns: The screenshot in JSON format.
    */
    public string CaptureScreenshot()
    {
        
        // Capture the screenshot on the target camera.
        captureCamera.Render();

        // Set the active render texture to the render texture declared.
        RenderTexture.active = renderTexture;

        // Record the screenshot in the screenshot variable.
        screenshot.ReadPixels(new Rect(0, 0, Screen.width, Screen.height), 0, 0);

        // Convert the screenshot to a byte array.
        byte[] screenshotBytes = screenshot.EncodeToPNG();

        // Create an instance of the JSONObject class to store the variables in a schema.
        var jsonObject = new JSONObject
        {
            screenshotPNG = screenshotBytes
        };

        // Convert the JSON object to a JSON string
        // Add new line delimiter so the server can determine the end of an image
        string jsonPayloadString = JsonUtility.ToJson(jsonObject) + "\n";

        // Return the JSON string
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
            // Retrieve the JSON encoded string of the screenshot.
            string screenshot_json = CaptureScreenshot();

            // Send the JSON String to the server.
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
        byte[] data = Encoding.UTF8.GetBytes(message);

        // Write the serialized message to the stream.
        stream.Write(data, 0, data.Length);
        
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
