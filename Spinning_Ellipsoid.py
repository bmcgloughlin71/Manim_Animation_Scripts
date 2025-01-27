from manim import *
from SearchFunctions import *

class RotatingEllipsoid(ThreeDScene):
    def construct(self):
        # Parameters
        f_spin = 5  # Spin frequency in rotations per second
        run_time = 5  # Total animation duration in seconds

        # Set up axes
        axes = ThreeDAxes()

        # Create the ellipsoid as a surface
        ellipsoid = Surface(
            lambda u, v: axes.c2p(
                2 * np.cos(u) * np.sin(v),  # x-coordinate
                np.sin(u) * np.sin(v),     # y-coordinate
                np.cos(v)                  # z-coordinate
            ),
            u_range=[0, TAU],
            v_range=[0, PI],
            resolution=(24, 24),
        )
        ellipsoid.set_color(BLUE)
        ellipsoid.set_opacity(0.8)
        
        phi_tracker = ValueTracker(90 * DEGREES)
        
        # Create a function to update the phi label
        phi_label = always_redraw(lambda: MathTex(
            f"\\iota = {phi_tracker.get_value() / DEGREES:.1f}^\circ"
        ).to_corner(UP + RIGHT))

        # Add the label to the fixed frame (always facing the screen)
        self.add_fixed_in_frame_mobjects(phi_label)

        # Set up the initial scene
        self.set_camera_orientation(phi=phi_tracker.get_value(), theta=0 * DEGREES)  # Look directly down the z-axis
        self.add(axes, ellipsoid)

        # Calculate the total rotation angle based on frequency and run time
        total_rotation_angle = 2 * PI * f_spin * run_time

        # Animate the rotation of the ellipsoid
        self.play(Rotate(ellipsoid, angle=total_rotation_angle, axis=OUT, about_point=ORIGIN, run_time=run_time, rate_func=linear))

        # Simultaneously move the camera to tilt toward the spin plane
        self.move_camera(
            phi=0 * DEGREES, 
            theta=0 * DEGREES, 
            run_time=run_time, 
            added_anims=[
                Rotate(ellipsoid, angle=total_rotation_angle, axis=OUT, about_point=ORIGIN, run_time=run_time, rate_func=linear),
                phi_tracker.animate.set_value(0 * DEGREES)  # Update phi_tracker during the animation
            ]
        )

        # Pause to show the final scene
        self.wait()
