from manim import *
import numpy as np

class RotatingEllipsoid(ThreeDScene):
    def construct(self):

        ## 3 Part Animation ##
        # 1) Ellipsoid spinning with camera in rotation plane
        # 2) While rotating, move camera from rotation plane to spin-axis
        # 3) Pause to show final orientation

        ## Neutron Star Parameters ##
        f_spin = 1     # Initial spin frequency (Hz)
        f_dot = -1e-9  # Spindown value (Hz/s)

        ## Runtimes ##
        total_runtime = 30  # Total animation duration (s)
        part1_runtime = (2/3) * total_runtime
        part2_runtime = (1/6) * total_runtime
        part3_runtime = (1/6) * total_runtime
        assert(part1_runtime + part2_runtime + part3_runtime == total_runtime)

        ## Set up axes ##
        axes = ThreeDAxes()
        

        ## Create the ellipsoid as a surface ##
        ellipsoid = Surface(
            lambda u, v: axes.c2p(
                2 * np.cos(u) * np.sin(v), # x-coordinate
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
        total_rotation_angle = 2 * PI * (f_spin * total_runtime + 0.5 * f_dot * total_runtime**2)
        instantaneous_freq_tracker = ValueTracker(f_spin)  # Tracks the total spin angle

        ## Labels ##
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

        
        ## Set up the initial scene ##
        self.add_fixed_in_frame_mobjects(phi_label, freq_label, spindown_label, instant_freq_label)
        self.set_camera_orientation(phi=phi_tracker.get_value(), theta=0 * DEGREES)  
        self.add(axes, ellipsoid)

        ### PART 1 - Animate the rotation of the ellipsoid ###
        self.play(
            Rotate(ellipsoid, angle=total_rotation_angle * (part1_runtime/total_runtime), axis=OUT, about_point=ORIGIN, run_time=part1_runtime, rate_func=linear),
            instantaneous_freq_tracker.animate.set_value(f_spin + f_dot * part1_runtime), run_time=part1_runtime, rate_func=linear
        )

        ### PART 2 - Simultaneously move the camera ### 
        self.move_camera(
            phi=0 * DEGREES, 
            theta=0 * DEGREES, 
            run_time=5, 
            added_anims=[
                Rotate(ellipsoid, angle=total_rotation_angle * (part2_runtime/total_runtime), axis=OUT, about_point=ORIGIN, run_time=part2_runtime, rate_func=linear),
                phi_tracker.animate.set_value(0 * DEGREES),
                instantaneous_freq_tracker.animate.increment_value(f_dot * part2_runtime)
            ]
        )

        ### PART 3 - Pause to show the final scene ###
        self.play(
            Rotate(ellipsoid, angle=total_rotation_angle * (part3_runtime/total_runtime), axis=OUT, about_point=ORIGIN, run_time=part3_runtime, rate_func=linear),
            instantaneous_freq_tracker.animate.increment_value(f_dot * part3_runtime), run_time=part3_runtime, rate_func=linear
        )
