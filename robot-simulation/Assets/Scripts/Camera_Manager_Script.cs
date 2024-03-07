using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class CameraManager : MonoBehaviour
{
    public Text camera_label; // Label displaying the name of the current camera
    public List<GameObject> cameras = new List<GameObject>(); // List of cameras
    private int current_index = 0; // Index of visible camera, initialized to 0

    // Start is called before the first frame update
    void Start()
    {
        // set every camera to invisible
        foreach (GameObject cam in cameras)
        {
            cam.SetActive(false);
        }

        // set the default camera to visible
        SetCameraActive(current_index, true);
    }


    // Update is called once per frame
    void Update()
    {
        
        Debug.Log(cameras[0].GetComponent<Camera>().focalLength);
        // if escape is pressed, switch cameras
        if (Input.GetKeyDown(KeyCode.Escape))
        {
            SwitchToNextCamera();
        }
    }

    // sets a camera to be visible or invisible
    void SetCameraActive(int index, bool isActive)
    {
        // set the selected camera to be visible
        if (index >= 0 && index < cameras.Count)
        {
            // Update the camera_label text with the current camera name
            camera_label.text = "Current Camera: " + cameras[index].name;
            Debug.Log(camera_label.text);

            // Set the selected camera to active/inactive
            cameras[index].SetActive(isActive);
        }
    }


    // deactivates the current camera and activates the next camera
    void SwitchToNextCamera()
    {
        // set the current camera to invisible
        SetCameraActive(current_index, false);

        // increment the index circularly
        current_index = (current_index + 1) % cameras.Count;

        // set the next camera to be visible
        SetCameraActive(current_index, true);
    }
}
