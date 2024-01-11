using System;
using System.Collections;
using System.Collections.Generic;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using UnityEngine;



[Serializable]
public class JSONObject
{
    public byte[] screenshotPNG;
}

[Serializable]
public class ServerResponse
{
    public string status;
    public float[] movements;
}

public class Client_Communication : MonoBehaviour
{
    public string serverIP = "127.0.0.1";
    public int serverPort = 2345;
    public Camera captureCamera;
    public Robot_Script robotScript;

    private TcpClient client;
    private NetworkStream stream;
    private float updateInterval = 0.05f;
    private float timeSinceLastUpdate = 0f;

    private Thread clientThread;

    private bool isRunning = true;

    private string lastScreenshotJson = null;

    private float[] robot_movements = null;
    private bool updated_robot_movements = false;

    private void Start()
    {
        timeSinceLastUpdate = updateInterval;
        ConnectToServer();

        // Start a separate thread for client communication.
        clientThread = new Thread(ClientThreadFunction);
        clientThread.Start();
    }

    private void ClientThreadFunction()
    {
        while (isRunning)
        {
            if (lastScreenshotJson != null)
            {
                SendMessageToServer(lastScreenshotJson);
                lastScreenshotJson = null;
            }
        }
    }

    public string CaptureScreenshot()
    {

        RenderTexture renderTexture = new RenderTexture(Screen.width, Screen.height, 24);
        captureCamera.targetTexture = renderTexture;
        Texture2D screenshot = new Texture2D(Screen.width, Screen.height, TextureFormat.RGB24, true);
        captureCamera.Render();
        RenderTexture.active = renderTexture;
        screenshot.ReadPixels(new Rect(0, 0, Screen.width, Screen.height), 0, 0);
        byte[] screenshotBytes = screenshot.EncodeToPNG();
        var jsonObject = new JSONObject { screenshotPNG = screenshotBytes };
        string jsonPayloadString = JsonUtility.ToJson(jsonObject) + "\n";
        captureCamera.targetTexture = null;
        RenderTexture.active = null;
        Destroy(renderTexture);
        return jsonPayloadString;
    }

    private void ConnectToServer()
    {
        try
        {
            client = new TcpClient(serverIP, serverPort);
            stream = client.GetStream();
        }
        catch (Exception ex)
        {
            Debug.LogError($"Error: {ex.Message}");
        }
    }

    private void Update()
    {
        timeSinceLastUpdate += Time.deltaTime;

        if (timeSinceLastUpdate >= updateInterval)
        {
            lastScreenshotJson = CaptureScreenshot();
            timeSinceLastUpdate = 0f;
        }

        lock(this)
        {
            if(updated_robot_movements)
            {
                robotScript.Move(robot_movements);
                updated_robot_movements = false;
            }
        }
    }

    private void SendMessageToServer(string message)
    {
        if (stream == null)
        {
            return;
        }

        try
        {
            byte[] data = Encoding.UTF8.GetBytes(message);
            stream.Write(data, 0, data.Length);
            HandleServerResponse(message);
        }
        catch (Exception ex)
        {
            Debug.LogError($"Error sending message: {ex.Message}");
        }
    }

    private void HandleServerResponse(string message)
    {
        byte[] responseBuffer = new byte[1024];
        int bytesRead = stream.Read(responseBuffer, 0, responseBuffer.Length);
        string response = Encoding.UTF8.GetString(responseBuffer, 0, bytesRead);
        ServerResponse serverResponse = JsonUtility.FromJson<ServerResponse>(response);

        lock(this)
        {
            robot_movements = serverResponse.movements;
            /**string movements_str = float.Parse(robot_movements);
            Debug.Log("robot movements: {0}", movements_str);*/
            updated_robot_movements = true;
        }
        

        
        

        if (serverResponse.status == "failure")
        {
            // Handle failure as needed.
        }
    }

    private void OnDestroy()
    {
        isRunning = false;

        if (client != null)
        {
            client.Close();
        }
    }
}
