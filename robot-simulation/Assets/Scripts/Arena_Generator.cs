using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class NewBehaviourScript : MonoBehaviour
{

    public float arena_width;    // Width of the arena
    public float arena_height;   // Height of the arena

    public int boundary_width; // Width of the boundary
    public int boundary_height; // Height of the boundary
    public float boundary_thickness; // Thickness of the boundary

    public float unit_size; // Unit size for distances

    public GameObject ground; // Ground object
    public GameObject[] boundaries; // Boundary objects

    // Start is called before the first frame update
    void Start()
    {
        // If the boundary size is greater than the arena size, throw an exception.
        if(boundary_width > arena_width || boundary_height > arena_height)
        {
            throw new System.Exception("Boundary is greater than arena!");
        }

        // Transform the ground to adhere to the arena_width and arena_height.
        ground.transform.localScale = new Vector3(arena_width, 1, arena_height);

        // Boundary x coordinates = (boundary width scale * position unit size) / 2
        // Divide by 2 as the coordinates are centered, e.g. (-60) and (60) rather than (0) (120)
        float boundary_x_position = boundary_width * unit_size / 2;

        // Boundary y coordinates = (boundary height scale * position unit size) / 2
        // Divide by 2 as the coordinates are centered, e.g. (-60) and (60) rather than (0) (120)
        float boundary_y_position = boundary_height * unit_size / 2;


        // Boundaries create a rectangle of position (-boundary x, -boundary y) (boundary x, boundary y)
        // The boundaries are elevated by boundary_separation to prevent z-fighting with the ground
        boundaries[0].transform.position = new Vector3(boundary_x_position, boundary_thickness / 2, 0);
        boundaries[1].transform.position = new Vector3(-boundary_x_position, boundary_thickness / 2, 0);
        boundaries[2].transform.position = new Vector3(0, boundary_thickness / 2, boundary_y_position);
        boundaries[3].transform.position = new Vector3(0, boundary_thickness / 2, -boundary_y_position);


        // Scale two boundaries by width and two boundaries by height to create a rectangle.
        boundaries[0].transform.localScale = new Vector3(boundary_thickness, boundary_thickness, boundary_y_position * 2);
        boundaries[1].transform.localScale = new Vector3(boundary_thickness, boundary_thickness, boundary_y_position * 2);
        boundaries[2].transform.localScale = new Vector3(boundary_x_position * 2, boundary_thickness, boundary_thickness);
        boundaries[3].transform.localScale = new Vector3(boundary_x_position * 2, boundary_thickness, boundary_thickness);
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
