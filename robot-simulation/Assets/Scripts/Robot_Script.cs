using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Text;
using UnityEngine.UI;


public class Robot_Script : MonoBehaviour
{   

    public float obj_vel = 0f;

    public float obj_ang_vel = 0f;

    public float move_speed = 5f;
    public float rotation_speed = 30f;
    public Rigidbody rb;
    public string movement_state = "MANUAL";

    public Text robot_state_label;

    public float rotation = 0;
    public float movement = 0;

    public int movement_const = 10;

    public int move_multiplier = 1;
    public float rotation_const = 10f;

    public int difference = 50;

    


    // Start is called before the first frame update
    void Start()
    {   
        robot_state_label.text = "Current Movement: " + movement_state;
    }

    void HandleKeyPress()
    {

        if(movement_state == "MANUAL")
        {
            rotation = 0;
            if (Input.GetKey(KeyCode.D))
            {
                // Rotate right
                obj_ang_vel = rotation_const;
                obj_vel = 0;
                rotation = rotation_speed * Mathf.Deg2Rad;

            }
            if (Input.GetKey(KeyCode.A))
            {
                // Rotate left
                obj_ang_vel = -rotation_const;
                obj_vel = 0;
                rotation = -rotation_speed * Mathf.Deg2Rad;
            }

            movement = 0;
            if (Input.GetKey(KeyCode.W))
            {
                movement = move_speed * Time.deltaTime; //* difference;
                obj_vel = move_multiplier;
                obj_ang_vel = 0;
            }
            if (Input.GetKey(KeyCode.S))
            {
                movement = -move_speed * Time.deltaTime; //* difference;
                obj_vel = -move_multiplier;
                obj_ang_vel = 0;
            }

        }

        if (Input.GetKeyUp(KeyCode.Q))
        {
            // change mode from manual to autonomous

            if(movement_state == "MANUAL")
            {
                obj_vel = obj_vel * 0;
                obj_ang_vel = obj_ang_vel * 0;
                movement_state = "AUTO";
            }
            else if(movement_state == "AUTO")
            {
                obj_vel = obj_vel * 0;
                obj_ang_vel = obj_ang_vel * 0;
                movement_state = "MANUAL";
            }
            else
            {
                Debug.Log("INVALID MOVEMENT STATE");
            }

            robot_state_label.text = "Current Movement: " + movement_state;
        }
    }

    

    // Update is called once per frame
    void Update()
    {

        HandleKeyPress();

        rb.velocity = transform.forward * obj_vel * movement_const;  
        rb.angularVelocity = Vector3.up * obj_ang_vel;

        

    }

    public void Move(float[] movement_and_rotation)
    {   
        if(movement_state == "AUTO" && movement_and_rotation.Length == 2)
        {
            obj_vel = movement_and_rotation[0];
            obj_ang_vel = movement_and_rotation[1];
        }   

         
        
            

    }


}