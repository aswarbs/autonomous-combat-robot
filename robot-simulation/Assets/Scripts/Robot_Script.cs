using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Text;
using UnityEngine.UI;
using System;


public class Robot_Script : MonoBehaviour
{   

    public float dist;


    public float obj_vel = 0f;

    public double obj_ang_vel = 0;
    public Rigidbody rb;
    public string movement_state = "MANUAL";

    public Text robot_state_label;

    public double rotation = 0;
    public float movement = 0;

    private double rotation_speed = Math.PI/16;

    public float move_speed = 5;
    


    // Start is called before the first frame update
    void Start()
    {   
        robot_state_label.text = "Current Movement: " + movement_state;
    }

    void HandleKeyPress()
    {

        if(movement_state == "MANUAL")
        {
            if (Input.GetKey(KeyCode.D))
            {
                // Rotate right
                obj_ang_vel = rotation_speed;
                obj_vel = 0;
                rotation = rotation_speed;
                movement = 0;

            }
            if (Input.GetKey(KeyCode.A))
            {
                // Rotate left
                obj_ang_vel = -rotation_speed;
                obj_vel = 0;
                rotation = -rotation_speed;
                movement = 0;
            }

            if (Input.GetKey(KeyCode.W))
            {
                movement = move_speed * Time.deltaTime;
                rotation = 0;
                obj_vel = move_speed;
                obj_ang_vel = 0;
            }
            if (Input.GetKey(KeyCode.S))
            {
                movement = -move_speed * Time.deltaTime;
                rotation = 0;
                obj_vel = -move_speed;
                obj_ang_vel = 0;
            }
            if (Input.GetKey(KeyCode.Space))
            {
                // Rotate right
                obj_ang_vel = 0;
                obj_vel = 0;
                movement = 0;
                rotation = 0;

            }

            if (Input.GetKey(KeyCode.E))
            {




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

        rb.velocity = transform.forward * obj_vel;  
        rb.angularVelocity = Vector3.up * (float)obj_ang_vel;

        

    }

    public void Move(float[] movement_and_rotation)
    {   
        if(movement_state == "AUTO" && movement_and_rotation.Length == 2)
        {
            obj_vel = movement_and_rotation[0];
            obj_ang_vel = movement_and_rotation[1];
            // retrieve ATTACK here.
        }   

         
        
            

    }


}