from manim import *
import numpy as np

class RotatingEllipsoid(ThreeDScene):
    def construct(self):
        # Parameters
        f_spin = 1  # Initial spin frequency (Hz)
        f_dot = -1e-9  # Spindown value (Hz/s)
        run_time = 30  # Total animation duration (s)

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
        ellipsoid.set_color_by_gradient(PURPLE)
        ellipsoid.set_opacity(1)

        phi_tracker = ValueTracker(90 * DEGREES)
       

        # Compute total rotation angle with spindown
        total_rotation_angle = 2 * PI * (f_spin * run_time + 0.5 * f_dot * run_time**2)
        instantaneous_freq_tracker = ValueTracker(f_spin)  # Tracks the total spin angle

        # Create labels
        phi_label = always_redraw(lambda: MathTex(
            f"\\iota = {phi_tracker.get_value() / DEGREES:.1f}^\\circ"
        ).to_corner(UP + LEFT))

        freq_label = MathTex(
            r"f_{\textrm{spin}} = 1 \text{Hz}"
        ).next_to(phi_label, DOWN)

        spindown_label = MathTex(
            r"\dot{f}_{\textrm{spin}} = -10^{-9} \text{Hz/s}"
        ).next_to(freq_label, DOWN).shift(RIGHT * 0.75)

        instant_freq_label = always_redraw(lambda: MathTex(
            f"f(t) = {instantaneous_freq_tracker.get_value() :.9f} \\text{{ Hz }}"
        ).to_corner(UP + RIGHT))

        self.add_fixed_in_frame_mobjects(phi_label, freq_label, spindown_label, instant_freq_label)

        # Set up the initial scene
        self.set_camera_orientation(phi=phi_tracker.get_value(), theta=0 * DEGREES)  
        self.add(axes, ellipsoid)

        # Animate the rotation of the ellipsoid
        self.play(
            Rotate(ellipsoid, angle=total_rotation_angle * (2/3), axis=OUT, about_point=ORIGIN, run_time=20, rate_func=linear),
            instantaneous_freq_tracker.animate.set_value(f_spin + f_dot * 20), run_time=20, rate_func=linear
        )

        # Simultaneously move the camera
        self.move_camera(
            phi=0 * DEGREES, 
            theta=0 * DEGREES, 
            run_time=5, 
            added_anims=[
                Rotate(ellipsoid, angle=total_rotation_angle * (5/30), axis=OUT, about_point=ORIGIN, run_time=5, rate_func=linear),
                phi_tracker.animate.set_value(0 * DEGREES),
                instantaneous_freq_tracker.animate.increment_value(f_dot * 5)
            ]
        )

        # Pause to show the final scene
        self.play(
            Rotate(ellipsoid, angle=total_rotation_angle * (5/30), axis=OUT, about_point=ORIGIN, run_time=5, rate_func=linear),
            instantaneous_freq_tracker.animate.increment_value(f_dot * 5), run_time=5, rate_func=linear
        )
